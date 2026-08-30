"""Small OpenRouter chat-completions client with durable cost controls."""

from __future__ import annotations

import json
import logging
import threading
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

OPENROUTER_CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"


class OpenRouterClientError(RuntimeError):
    """Base class for expected client failures that should stop a run cleanly."""


class MissingConfigurationError(OpenRouterClientError):
    """Raised before network access when the API key is not configured."""


class OpenRouterHTTPError(OpenRouterClientError):
    """A non-success HTTP response from OpenRouter."""

    def __init__(self, status: int, message: str) -> None:
        super().__init__(f"OpenRouter returned HTTP {status}: {message}")
        self.status = status
        self.message = message


class UsageAccountingError(OpenRouterClientError):
    """Raised when OpenRouter does not provide auditable cost information."""


class ReasoningTokenError(OpenRouterClientError):
    """Raised if main-battery traffic is billed for reasoning tokens."""


class SpendCapExceeded(OpenRouterClientError):
    """Raised when reserving a request would exceed the configured run cap."""


@dataclass(frozen=True)
class HTTPResponse:
    status: int
    body: bytes
    headers: Mapping[str, str]


@dataclass(frozen=True)
class CompletionResult:
    """OpenRouter response data needed by the raw-response contract."""

    raw: Mapping[str, Any]
    text: str
    provider_served: str | None
    input_tokens: int
    output_tokens: int
    reasoning_tokens: int
    cost_usd: Decimal
    latency_ms: int


class RunBudget:
    """Reserve an upper bound before each request and settle it from OpenRouter's usage.cost."""

    def __init__(self, cap_usd: Decimal | str | float) -> None:
        self._cap_usd = _decimal(cap_usd, "cap_usd")
        if self._cap_usd <= 0:
            raise ValueError("cap_usd must be greater than zero")
        self._spent_usd = Decimal("0")
        self._reserved_usd = Decimal("0")
        self._lock = threading.Lock()

    @property
    def cap_usd(self) -> Decimal:
        return self._cap_usd

    @property
    def spent_usd(self) -> Decimal:
        with self._lock:
            return self._spent_usd

    @property
    def available_usd(self) -> Decimal:
        with self._lock:
            return self._cap_usd - self._spent_usd - self._reserved_usd

    def reserve(self, maximum_cost_usd: Decimal | str | float) -> Decimal:
        reservation = _decimal(maximum_cost_usd, "maximum_cost_usd")
        if reservation <= 0:
            raise ValueError("maximum_cost_usd must be greater than zero")
        with self._lock:
            if self._spent_usd + self._reserved_usd + reservation > self._cap_usd:
                raise SpendCapExceeded(
                    "Run spend cap would be exceeded before sending this request: "
                    f"spent=${self._spent_usd}, reserved=${self._reserved_usd}, "
                    f"next_max=${reservation}, cap=${self._cap_usd}."
                )
            self._reserved_usd += reservation
        return reservation

    def settle(self, reservation: Decimal, actual_cost_usd: Decimal | str | float) -> None:
        actual = _decimal(actual_cost_usd, "actual_cost_usd")
        if actual < 0:
            raise ValueError("actual_cost_usd cannot be negative")
        with self._lock:
            if reservation > self._reserved_usd:
                raise RuntimeError("budget reservation was already released")
            self._reserved_usd -= reservation
            self._spent_usd += actual
            if self._spent_usd > self._cap_usd:
                raise SpendCapExceeded(
                    "OpenRouter reported a cost greater than the reserved maximum; the run is "
                    f"stopped after this call. spent=${self._spent_usd}, cap=${self._cap_usd}."
                )

    def release(self, reservation: Decimal) -> None:
        with self._lock:
            if reservation > self._reserved_usd:
                raise RuntimeError("budget reservation was already released")
            self._reserved_usd -= reservation


Transport = Callable[[Request, float], HTTPResponse]


class OpenRouterClient:
    """Thin, testable wrapper around OpenRouter's OpenAI-compatible chat endpoint."""

    def __init__(
        self,
        api_key: str,
        budget: RunBudget,
        *,
        endpoint: str = OPENROUTER_CHAT_URL,
        timeout_seconds: float = 60,
        max_attempts: int = 3,
        transport: Transport | None = None,
        sleep: Callable[[float], None] = time.sleep,
        logger: logging.Logger | None = None,
    ) -> None:
        if not api_key.strip():
            raise MissingConfigurationError("OPENROUTER_API_KEY is required; no request was sent")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least one")
        self._api_key = api_key
        self.budget = budget
        self._endpoint = endpoint
        self._timeout_seconds = timeout_seconds
        self._max_attempts = max_attempts
        self._transport = transport or _default_transport
        self._sleep = sleep
        self._logger = logger or logging.getLogger("spinning_arrow.client")

    def chat_completion(
        self,
        *,
        model_id: str,
        messages: Sequence[Mapping[str, str]],
        maximum_cost_usd: Decimal | str | float,
        max_tokens: int = 8,
        parameters: Mapping[str, Any] | None = None,
        reasoning_exception: str | None = None,
        omit_reasoning: bool = False,
    ) -> CompletionResult:
        """Send one non-streaming completion and settle the pre-reserved maximum cost.

        The caller supplies a conservative upper-bound cost. This is intentional: the client can
        stop a run *before* a request that would breach its cap, rather than merely notice an
        overage afterward.
        """

        if not model_id.strip():
            raise ValueError("model_id must be non-empty")
        if max_tokens < 1:
            raise ValueError("max_tokens must be at least one")
        normalized_messages = _normalise_messages(messages)
        request_parameters = dict(parameters or {})
        requested_reasoning = request_parameters.pop("reasoning", None)
        if omit_reasoning:
            if requested_reasoning is not None:
                raise ValueError("omit_reasoning cannot be combined with a reasoning parameter")
        else:
            reasoning = {"enabled": False} if requested_reasoning is None else requested_reasoning
            if not isinstance(reasoning, Mapping):
                raise ValueError("reasoning must be an object")
            reasoning = dict(reasoning)
            if reasoning != {"enabled": False} and not reasoning_exception:
                raise ValueError(
                    "reasoning-enabled requests require a documented non-main-battery exception"
                )
            request_parameters["reasoning"] = reasoning
        payload = {
            "model": model_id,
            "messages": normalized_messages,
            "max_tokens": max_tokens,
            **request_parameters,
        }
        reservation = self.budget.reserve(maximum_cost_usd)
        started = time.perf_counter()
        settled = False
        try:
            response = self._request_with_retries(payload, model_id)
            latency_ms = round((time.perf_counter() - started) * 1000)
            result = _completion_result(response, latency_ms)
            settled = True
            self.budget.settle(reservation, result.cost_usd)
            if result.reasoning_tokens and not reasoning_exception:
                raise ReasoningTokenError(
                    f"{model_id} returned {result.reasoning_tokens} reasoning tokens "
                    "in the main path"
                )
            self._log(
                "completion_succeeded",
                model_id=model_id,
                cost_usd=str(result.cost_usd),
                input_tokens=result.input_tokens,
                output_tokens=result.output_tokens,
                reasoning_tokens=result.reasoning_tokens,
                latency_ms=result.latency_ms,
                run_spend_usd=str(self.budget.spent_usd),
            )
            return result
        except Exception:
            if not settled:
                self.budget.release(reservation)
            raise

    def _request_with_retries(self, payload: Mapping[str, Any], model_id: str) -> Mapping[str, Any]:
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "spinning-arrow/0.1.0",
            "X-OpenRouter-Metadata": "enabled",
        }
        retryable: Exception | None = None
        for attempt in range(1, self._max_attempts + 1):
            request = Request(self._endpoint, data=body, headers=headers, method="POST")
            try:
                response = self._transport(request, self._timeout_seconds)
                parsed = _decode_json(response.body)
                if 200 <= response.status < 300:
                    if not isinstance(parsed, Mapping):
                        raise OpenRouterClientError(
                            "OpenRouter success response was not a JSON object"
                        )
                    return parsed
                error = OpenRouterHTTPError(response.status, _error_message(parsed))
                if response.status not in {408, 409, 429, 500, 502, 503, 504}:
                    raise error
                retryable = error
            except URLError as error:
                retryable = OpenRouterClientError(f"OpenRouter network error: {error.reason}")
            if attempt == self._max_attempts:
                assert retryable is not None
                raise retryable
            delay_seconds = 0.5 * (2 ** (attempt - 1))
            self._log(
                "completion_retrying",
                model_id=model_id,
                attempt=attempt,
                max_attempts=self._max_attempts,
                delay_seconds=delay_seconds,
                error=str(retryable),
            )
            self._sleep(delay_seconds)
        raise AssertionError("retry loop exited unexpectedly")

    def _log(self, event: str, **fields: Any) -> None:
        self._logger.info(json.dumps({"event": event, **fields}, sort_keys=True))


def _decimal(value: Decimal | str | float, field: str) -> Decimal:
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as error:
        raise ValueError(f"{field} must be a decimal value") from error
    if not result.is_finite():
        raise ValueError(f"{field} must be finite")
    return result


def _default_transport(request: Request, timeout_seconds: float) -> HTTPResponse:
    try:
        with urlopen(request, timeout=timeout_seconds) as response:  # noqa: S310 -- fixed HTTPS endpoint
            return HTTPResponse(
                status=response.status,
                body=response.read(),
                headers=dict(response.headers.items()),
            )
    except HTTPError as error:
        return HTTPResponse(
            status=error.code,
            body=error.read(),
            headers=dict(error.headers.items()),
        )


def _normalise_messages(messages: Sequence[Mapping[str, str]]) -> list[dict[str, str]]:
    if not messages:
        raise ValueError("messages must not be empty")
    normalized: list[dict[str, str]] = []
    for index, message in enumerate(messages):
        role = message.get("role")
        content = message.get("content")
        is_valid = isinstance(role, str) and role.strip() and isinstance(content, str) and content
        if not is_valid:
            raise ValueError(f"messages[{index}] must have non-empty string role and content")
        normalized.append({"role": role, "content": content})
    return normalized


def _decode_json(body: bytes) -> Any:
    try:
        return json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise OpenRouterClientError("OpenRouter returned malformed JSON") from error


def _error_message(payload: Any) -> str:
    if isinstance(payload, Mapping):
        error = payload.get("error")
        if isinstance(error, Mapping) and isinstance(error.get("message"), str):
            return error["message"]
        if isinstance(payload.get("message"), str):
            return payload["message"]
    return "no error message supplied"


def _completion_result(payload: Mapping[str, Any], latency_ms: int) -> CompletionResult:
    usage = payload.get("usage")
    if not isinstance(usage, Mapping):
        raise UsageAccountingError("OpenRouter response has no usage block; cost cannot be audited")
    cost = usage.get("cost")
    if cost is None:
        raise UsageAccountingError("OpenRouter usage block has no cost; cost cannot be audited")
    try:
        cost_usd = _decimal(cost, "usage.cost")
    except ValueError as error:
        raise UsageAccountingError("OpenRouter usage.cost was not numeric") from error
    if cost_usd < 0:
        raise UsageAccountingError("OpenRouter usage.cost cannot be negative")
    input_tokens = _usage_int(usage, "prompt_tokens")
    output_tokens = _usage_int(usage, "completion_tokens")
    reasoning_tokens = _reasoning_tokens(usage)
    choices = payload.get("choices")
    if not isinstance(choices, Sequence) or isinstance(choices, (str, bytes)) or not choices:
        raise OpenRouterClientError("OpenRouter response has no choices")
    first_choice = choices[0]
    if not isinstance(first_choice, Mapping):
        raise OpenRouterClientError("OpenRouter first choice was not an object")
    message = first_choice.get("message")
    if not isinstance(message, Mapping):
        raise OpenRouterClientError("OpenRouter first choice has no message")
    text = _content_text(message.get("content"))
    return CompletionResult(
        raw=payload,
        text=text,
        provider_served=_provider_served(payload),
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        reasoning_tokens=reasoning_tokens,
        cost_usd=cost_usd,
        latency_ms=latency_ms,
    )


def _usage_int(usage: Mapping[str, Any], field: str) -> int:
    value = usage.get(field, 0)
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise UsageAccountingError(f"OpenRouter usage.{field} was not a non-negative integer")
    return value


def _reasoning_tokens(usage: Mapping[str, Any]) -> int:
    direct = usage.get("reasoning_tokens")
    details = usage.get("completion_tokens_details")
    detailed = details.get("reasoning_tokens") if isinstance(details, Mapping) else None
    values = [value for value in (direct, detailed) if value is not None]
    if not values:
        return 0
    if any(isinstance(value, bool) or not isinstance(value, int) or value < 0 for value in values):
        raise UsageAccountingError("OpenRouter reasoning token count was invalid")
    return max(values)


def _content_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, Sequence) and not isinstance(content, (str, bytes)):
        parts: list[str] = []
        for part in content:
            if isinstance(part, Mapping) and isinstance(part.get("text"), str):
                parts.append(part["text"])
        if parts:
            return "".join(parts)
    raise OpenRouterClientError("OpenRouter returned a choice without text content")


def _provider_served(payload: Mapping[str, Any]) -> str | None:
    provider = payload.get("provider")
    if isinstance(provider, str) and provider:
        return provider
    metadata = payload.get("openrouter_metadata")
    if isinstance(metadata, Mapping):
        for key in ("provider_name", "provider"):
            value = metadata.get(key)
            if isinstance(value, str) and value:
                return value
    return None
