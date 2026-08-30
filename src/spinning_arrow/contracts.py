"""Validated, JSON-serialisable data contracts for runs and scores.

The files written by this project are the public artifact. These models deliberately use only
the standard library so a response record can be validated and recovered without an SDK.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from math import isfinite
from typing import Any


class ContractValidationError(ValueError):
    """Raised when persisted data violates a Spinning Arrow contract."""


class Outcome(StrEnum):
    ANSWERED = "answered"
    REFUSED = "refused"
    HEDGED = "hedged"
    UNPARSEABLE = "unparseable"
    ERROR = "error"


def _required_string(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractValidationError(f"{field} must be a non-empty string")
    return value


def _nonnegative_int(value: object, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ContractValidationError(f"{field} must be a non-negative integer")
    return value


def _number(value: object, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not isfinite(value):
        raise ContractValidationError(f"{field} must be a finite number")
    return float(value)


def _nonnegative_number(value: object, field: str) -> float:
    numeric = _number(value, field)
    if numeric < 0:
        raise ContractValidationError(f"{field} must be a non-negative number")
    return numeric


def _rate(value: object, field: str) -> float:
    numeric = _nonnegative_number(value, field)
    if numeric > 1:
        raise ContractValidationError(f"{field} must be between 0 and 1")
    return numeric


def _timestamp(value: object, field: str) -> str:
    value = _required_string(value, field)
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ContractValidationError(f"{field} must be an ISO-8601 timestamp") from error
    if parsed.tzinfo is None:
        raise ContractValidationError(f"{field} must include a timezone")
    return value


def _sha256(value: object, field: str) -> str:
    value = _required_string(value, field)
    prefix, separator, digest = value.partition(":")
    if prefix != "sha256" or not separator or len(digest) != 64:
        raise ContractValidationError(f"{field} must be formatted as sha256:<64 hex characters>")
    try:
        int(digest, 16)
    except ValueError as error:
        raise ContractValidationError(f"{field} contains a non-hex digest") from error
    return value


def _json_messages(value: object) -> tuple[dict[str, str], ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ContractValidationError("messages must be a list of role/content objects")
    messages: list[dict[str, str]] = []
    for index, message in enumerate(value):
        if not isinstance(message, Mapping):
            raise ContractValidationError(f"messages[{index}] must be an object")
        role = _required_string(message.get("role"), f"messages[{index}].role")
        content = _required_string(message.get("content"), f"messages[{index}].content")
        messages.append({"role": role, "content": content})
    if not messages:
        raise ContractValidationError("messages must not be empty")
    return tuple(messages)


@dataclass(frozen=True)
class ParsedResponse:
    """The canonical answer option extracted from a raw model response."""

    choice: str | None
    valid: bool

    def __post_init__(self) -> None:
        if self.choice is not None:
            _required_string(self.choice, "parsed.choice")
        if not isinstance(self.valid, bool):
            raise ContractValidationError("parsed.valid must be a boolean")
        if self.valid != (self.choice is not None):
            raise ContractValidationError(
                "parsed.valid must be true exactly when parsed.choice is set"
            )

    def to_dict(self) -> dict[str, object]:
        return {"choice": self.choice, "valid": self.valid}

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> ParsedResponse:
        return cls(choice=data.get("choice"), valid=data.get("valid"))  # type: ignore[arg-type]


@dataclass(frozen=True)
class TokenUsage:
    """Token accounting as persisted in a response record."""

    input_tokens: int
    output_tokens: int
    reasoning_tokens: int

    def __post_init__(self) -> None:
        _nonnegative_int(self.input_tokens, "tokens.in")
        _nonnegative_int(self.output_tokens, "tokens.out")
        _nonnegative_int(self.reasoning_tokens, "tokens.reasoning")

    def to_dict(self) -> dict[str, int]:
        return {
            "in": self.input_tokens,
            "out": self.output_tokens,
            "reasoning": self.reasoning_tokens,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> TokenUsage:
        return cls(
            input_tokens=data.get("in"),  # type: ignore[arg-type]
            output_tokens=data.get("out"),  # type: ignore[arg-type]
            reasoning_tokens=data.get("reasoning", 0),  # type: ignore[arg-type]
        )


@dataclass(frozen=True)
class ResponseRecord:
    """One persisted OpenRouter call, including the raw model response and its cost."""

    run_id: str
    ts: str
    model_id: str
    provider_served: str | None
    instrument: str
    item_id: str
    condition: str
    framing: str
    permutation: int
    option_order: tuple[str, ...]
    prompt_hash: str
    messages: tuple[dict[str, str], ...]
    raw_response: str | None
    parsed: ParsedResponse
    outcome: Outcome
    tokens: TokenUsage
    cost_usd: float
    latency_ms: int
    error: str | None

    def __post_init__(self) -> None:
        for field in ("run_id", "model_id", "instrument", "item_id", "condition", "framing"):
            _required_string(getattr(self, field), field)
        _timestamp(self.ts, "ts")
        if self.provider_served is not None:
            _required_string(self.provider_served, "provider_served")
        _nonnegative_int(self.permutation, "permutation")
        if not self.option_order:
            raise ContractValidationError("option_order must not be empty")
        if len(set(self.option_order)) != len(self.option_order):
            raise ContractValidationError("option_order must contain each canonical option once")
        for choice in self.option_order:
            _required_string(choice, "option_order entry")
        _sha256(self.prompt_hash, "prompt_hash")
        _json_messages(self.messages)
        if self.raw_response is not None and not isinstance(self.raw_response, str):
            raise ContractValidationError("raw_response must be a string or null")
        if not isinstance(self.outcome, Outcome):
            raise ContractValidationError("outcome must be a recognized outcome")
        if self.parsed.valid and self.parsed.choice not in self.option_order:
            raise ContractValidationError(
                "parsed.choice must be canonical and appear in option_order"
            )
        if self.outcome is Outcome.ANSWERED and not self.parsed.valid:
            raise ContractValidationError("answered records require a valid parsed choice")
        if self.outcome is not Outcome.ANSWERED and self.parsed.valid:
            raise ContractValidationError("only answered records may contain a valid parsed choice")
        _nonnegative_number(self.cost_usd, "cost_usd")
        _nonnegative_int(self.latency_ms, "latency_ms")
        if self.error is not None:
            _required_string(self.error, "error")
        if self.outcome is Outcome.ERROR and self.error is None:
            raise ContractValidationError("error records require an error message")

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "ts": self.ts,
            "model_id": self.model_id,
            "provider_served": self.provider_served,
            "instrument": self.instrument,
            "item_id": self.item_id,
            "condition": self.condition,
            "framing": self.framing,
            "permutation": self.permutation,
            "option_order": list(self.option_order),
            "prompt_hash": self.prompt_hash,
            "messages": list(self.messages),
            "raw_response": self.raw_response,
            "parsed": self.parsed.to_dict(),
            "outcome": self.outcome.value,
            "tokens": self.tokens.to_dict(),
            "cost_usd": self.cost_usd,
            "latency_ms": self.latency_ms,
            "error": self.error,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> ResponseRecord:
        parsed = data.get("parsed")
        tokens = data.get("tokens")
        if not isinstance(parsed, Mapping) or not isinstance(tokens, Mapping):
            raise ContractValidationError("parsed and tokens must be objects")
        option_order = data.get("option_order")
        if not isinstance(option_order, Sequence) or isinstance(option_order, (str, bytes)):
            raise ContractValidationError("option_order must be a list")
        return cls(
            run_id=data.get("run_id"),  # type: ignore[arg-type]
            ts=data.get("ts"),  # type: ignore[arg-type]
            model_id=data.get("model_id"),  # type: ignore[arg-type]
            provider_served=data.get("provider_served"),  # type: ignore[arg-type]
            instrument=data.get("instrument"),  # type: ignore[arg-type]
            item_id=data.get("item_id"),  # type: ignore[arg-type]
            condition=data.get("condition"),  # type: ignore[arg-type]
            framing=data.get("framing"),  # type: ignore[arg-type]
            permutation=data.get("permutation"),  # type: ignore[arg-type]
            option_order=tuple(option_order),  # type: ignore[arg-type]
            prompt_hash=data.get("prompt_hash"),  # type: ignore[arg-type]
            messages=_json_messages(data.get("messages")),
            raw_response=data.get("raw_response"),  # type: ignore[arg-type]
            parsed=ParsedResponse.from_dict(parsed),
            outcome=Outcome(data.get("outcome")),
            tokens=TokenUsage.from_dict(tokens),
            cost_usd=data.get("cost_usd"),  # type: ignore[arg-type]
            latency_ms=data.get("latency_ms"),  # type: ignore[arg-type]
            error=data.get("error"),  # type: ignore[arg-type]
        )


@dataclass(frozen=True)
class ScoreRecord:
    """A single scale score, including rates and the fragility-sized confidence interval."""

    run_id: str
    model_id: str
    condition: str
    scale: str
    score: float | None
    scale_min: float
    scale_max: float
    n_items: int
    n_observations: int
    n_valid: int
    refusal_rate: float
    hedge_rate: float
    fragility: float | None
    ci_low: float | None
    ci_high: float | None
    computed_at: str
    suppression_reason: str | None = None

    def __post_init__(self) -> None:
        for field in ("run_id", "model_id", "condition", "scale"):
            _required_string(getattr(self, field), field)
        scale_min = _number(self.scale_min, "scale_min")
        scale_max = _number(self.scale_max, "scale_max")
        if scale_max <= scale_min:
            raise ContractValidationError("scale_max must be greater than scale_min")
        _nonnegative_int(self.n_items, "n_items")
        _nonnegative_int(self.n_observations, "n_observations")
        _nonnegative_int(self.n_valid, "n_valid")
        if self.n_valid > self.n_observations:
            raise ContractValidationError("n_valid cannot exceed n_observations")
        _rate(self.refusal_rate, "refusal_rate")
        _rate(self.hedge_rate, "hedge_rate")
        _timestamp(self.computed_at, "computed_at")
        fields = (self.score, self.fragility, self.ci_low, self.ci_high)
        if self.score is None:
            if self.suppression_reason is None:
                raise ContractValidationError("suppressed scores require suppression_reason")
            if any(value is not None for value in fields[1:]):
                raise ContractValidationError(
                    "suppressed scores cannot have fragility or confidence bounds"
                )
        else:
            score = _number(self.score, "score")
            if not scale_min <= score <= scale_max:
                raise ContractValidationError("score must be in the native scale range")
            if self.suppression_reason is not None:
                raise ContractValidationError("published scores cannot have suppression_reason")
            if self.fragility is None or self.ci_low is None or self.ci_high is None:
                raise ContractValidationError(
                    "published scores require fragility and confidence bounds"
                )
            _nonnegative_number(self.fragility, "fragility")
            ci_low = _number(self.ci_low, "ci_low")
            ci_high = _number(self.ci_high, "ci_high")
            if ci_low > ci_high:
                raise ContractValidationError("ci_low cannot exceed ci_high")

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "model_id": self.model_id,
            "condition": self.condition,
            "scale": self.scale,
            "score": self.score,
            "scale_min": self.scale_min,
            "scale_max": self.scale_max,
            "n_items": self.n_items,
            "n_observations": self.n_observations,
            "n_valid": self.n_valid,
            "refusal_rate": self.refusal_rate,
            "hedge_rate": self.hedge_rate,
            "fragility": self.fragility,
            "ci_low": self.ci_low,
            "ci_high": self.ci_high,
            "computed_at": self.computed_at,
            "suppression_reason": self.suppression_reason,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> ScoreRecord:
        return cls(
            run_id=data.get("run_id"),  # type: ignore[arg-type]
            model_id=data.get("model_id"),  # type: ignore[arg-type]
            condition=data.get("condition"),  # type: ignore[arg-type]
            scale=data.get("scale"),  # type: ignore[arg-type]
            score=data.get("score"),  # type: ignore[arg-type]
            scale_min=data.get("scale_min"),  # type: ignore[arg-type]
            scale_max=data.get("scale_max"),  # type: ignore[arg-type]
            n_items=data.get("n_items"),  # type: ignore[arg-type]
            n_observations=data.get("n_observations"),  # type: ignore[arg-type]
            n_valid=data.get("n_valid"),  # type: ignore[arg-type]
            refusal_rate=data.get("refusal_rate"),  # type: ignore[arg-type]
            hedge_rate=data.get("hedge_rate"),  # type: ignore[arg-type]
            fragility=data.get("fragility"),  # type: ignore[arg-type]
            ci_low=data.get("ci_low"),  # type: ignore[arg-type]
            ci_high=data.get("ci_high"),  # type: ignore[arg-type]
            computed_at=data.get("computed_at"),  # type: ignore[arg-type]
            suppression_reason=data.get("suppression_reason"),  # type: ignore[arg-type]
        )


@dataclass(frozen=True)
class RunManifest:
    """The reproducibility record for an API run (D15)."""

    run_id: str
    item_set_hash: str
    prompt_template_hashes: Mapping[str, str]
    panel_hash: str
    model_ids: tuple[str, ...]
    sampling_params: Mapping[str, Any]
    parameter_omissions: Mapping[str, tuple[str, ...]]
    git_commit: str
    started_at: str
    ended_at: str
    total_cost_usd: float
    per_model_cost_usd: Mapping[str, float]
    outcome_counts: Mapping[str, int]

    def __post_init__(self) -> None:
        _required_string(self.run_id, "run_id")
        _sha256(self.item_set_hash, "item_set_hash")
        _sha256(self.panel_hash, "panel_hash")
        _required_string(self.git_commit, "git_commit")
        _timestamp(self.started_at, "started_at")
        _timestamp(self.ended_at, "ended_at")
        if not self.model_ids:
            raise ContractValidationError("model_ids must not be empty")
        for model_id in self.model_ids:
            _required_string(model_id, "model_ids entry")
        if set(self.per_model_cost_usd) != set(self.model_ids):
            raise ContractValidationError(
                "per_model_cost_usd must have exactly one entry per model"
            )
        for name, digest in self.prompt_template_hashes.items():
            _required_string(name, "prompt template name")
            _sha256(digest, "prompt template hash")
        if not self.prompt_template_hashes:
            raise ContractValidationError("prompt_template_hashes must not be empty")
        for model_id, omissions in self.parameter_omissions.items():
            if model_id not in self.model_ids:
                raise ContractValidationError(
                    "parameter omissions must refer to a model in model_ids"
                )
            if not isinstance(omissions, tuple):
                raise ContractValidationError("parameter omissions must be tuples")
            for omission in omissions:
                _required_string(omission, "parameter omission")
        _nonnegative_number(self.total_cost_usd, "total_cost_usd")
        costs: list[float] = []
        for model_id, cost in self.per_model_cost_usd.items():
            _required_string(model_id, "per-model cost model id")
            costs.append(_nonnegative_number(cost, "per-model cost"))
        if abs(sum(costs) - _nonnegative_number(self.total_cost_usd, "total_cost_usd")) > 1e-9:
            raise ContractValidationError("per-model costs must sum to total_cost_usd")
        for outcome, count in self.outcome_counts.items():
            Outcome(outcome)
            _nonnegative_int(count, f"outcome_counts[{outcome}]")

    def to_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "item_set_hash": self.item_set_hash,
            "prompt_template_hashes": dict(self.prompt_template_hashes),
            "panel_hash": self.panel_hash,
            "model_ids": list(self.model_ids),
            "sampling_params": dict(self.sampling_params),
            "parameter_omissions": {
                model_id: list(omissions)
                for model_id, omissions in self.parameter_omissions.items()
            },
            "git_commit": self.git_commit,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "total_cost_usd": self.total_cost_usd,
            "per_model_cost_usd": dict(self.per_model_cost_usd),
            "outcome_counts": dict(self.outcome_counts),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, object]) -> RunManifest:
        hashes = data.get("prompt_template_hashes")
        costs = data.get("per_model_cost_usd")
        counts = data.get("outcome_counts")
        omissions = data.get("parameter_omissions", {})
        model_ids = data.get("model_ids")
        params = data.get("sampling_params")
        maps = (hashes, costs, counts, omissions, params)
        if not all(isinstance(value, Mapping) for value in maps):
            raise ContractValidationError("manifest maps must be objects")
        if not isinstance(model_ids, Sequence) or isinstance(model_ids, (str, bytes)):
            raise ContractValidationError("model_ids must be a list")
        typed_omissions: dict[str, tuple[str, ...]] = {}
        for model_id, values in omissions.items():
            is_sequence = isinstance(values, Sequence) and not isinstance(values, (str, bytes))
            if not isinstance(model_id, str) or not is_sequence:
                raise ContractValidationError("parameter omissions must map models to lists")
            typed_omissions[model_id] = tuple(values)  # type: ignore[arg-type]
        return cls(
            run_id=data.get("run_id"),  # type: ignore[arg-type]
            item_set_hash=data.get("item_set_hash"),  # type: ignore[arg-type]
            prompt_template_hashes=hashes,  # type: ignore[arg-type]
            panel_hash=data.get("panel_hash"),  # type: ignore[arg-type]
            model_ids=tuple(model_ids),  # type: ignore[arg-type]
            sampling_params=params,  # type: ignore[arg-type]
            parameter_omissions=typed_omissions,
            git_commit=data.get("git_commit"),  # type: ignore[arg-type]
            started_at=data.get("started_at"),  # type: ignore[arg-type]
            ended_at=data.get("ended_at"),  # type: ignore[arg-type]
            total_cost_usd=data.get("total_cost_usd"),  # type: ignore[arg-type]
            per_model_cost_usd=costs,  # type: ignore[arg-type]
            outcome_counts=counts,  # type: ignore[arg-type]
        )
