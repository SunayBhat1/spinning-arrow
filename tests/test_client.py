from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path
from urllib.request import Request

import pytest

from spinning_arrow.client import (
    HTTPResponse,
    OpenRouterClient,
    RunBudget,
    SpendCapExceeded,
    UsageAccountingError,
)

FIXTURES = Path(__file__).parent / "fixtures"


def _fixture() -> bytes:
    return (FIXTURES / "openrouter_completion.json").read_bytes()


def test_cost_accounting_uses_openrouter_usage_cost() -> None:
    requests: list[Request] = []

    def transport(request: Request, _: float) -> HTTPResponse:
        requests.append(request)
        return HTTPResponse(status=200, body=_fixture(), headers={})

    budget = RunBudget("0.01")
    client = OpenRouterClient("test-key", budget, transport=transport)
    result = client.chat_completion(
        model_id="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": "Reply C"}],
        maximum_cost_usd="0.001",
    )

    payload = json.loads(requests[0].data.decode("utf-8"))
    assert payload["reasoning"] == {"enabled": False}
    assert result.cost_usd == Decimal("0.00000123")
    assert budget.spent_usd == Decimal("0.00000123")


def test_retry_reuses_one_budget_reservation() -> None:
    calls = 0
    sleeps: list[float] = []

    def transport(_: Request, __: float) -> HTTPResponse:
        nonlocal calls
        calls += 1
        if calls == 1:
            return HTTPResponse(status=429, body=b'{"error":{"message":"slow down"}}', headers={})
        return HTTPResponse(status=200, body=_fixture(), headers={})

    client = OpenRouterClient(
        "test-key", RunBudget("0.01"), transport=transport, sleep=sleeps.append
    )
    client.chat_completion(
        model_id="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": "Reply C"}],
        maximum_cost_usd="0.001",
    )

    assert calls == 2
    assert sleeps == [0.5]


def test_spend_cap_blocks_before_network_call() -> None:
    def transport(_: Request, __: float) -> HTTPResponse:  # pragma: no cover - must not be reached
        raise AssertionError("network request should have been blocked")

    client = OpenRouterClient("test-key", RunBudget("0.0001"), transport=transport)

    with pytest.raises(SpendCapExceeded):
        client.chat_completion(
            model_id="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": "Reply C"}],
            maximum_cost_usd="0.001",
        )


def test_missing_cost_is_a_hard_accounting_error() -> None:
    payload = json.loads(_fixture())
    del payload["usage"]["cost"]

    def transport(_: Request, __: float) -> HTTPResponse:
        return HTTPResponse(status=200, body=json.dumps(payload).encode("utf-8"), headers={})

    client = OpenRouterClient("test-key", RunBudget("0.01"), transport=transport)
    with pytest.raises(UsageAccountingError):
        client.chat_completion(
            model_id="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": "Reply C"}],
            maximum_cost_usd="0.001",
        )


def test_reasoning_requires_an_explicit_documented_exception() -> None:
    client = OpenRouterClient("test-key", RunBudget("0.01"), transport=lambda *_: None)  # type: ignore[arg-type]

    with pytest.raises(ValueError, match="documented non-main-battery exception"):
        client.chat_completion(
            model_id="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": "Reply C"}],
            maximum_cost_usd="0.001",
            parameters={"reasoning": {"effort": "low", "exclude": True}},
        )


def test_documented_reasoning_exception_is_sent_and_accounted() -> None:
    requests: list[Request] = []

    def transport(request: Request, _: float) -> HTTPResponse:
        requests.append(request)
        payload = json.loads(_fixture())
        payload["usage"]["completion_tokens_details"]["reasoning_tokens"] = 2
        return HTTPResponse(status=200, body=json.dumps(payload).encode("utf-8"), headers={})

    client = OpenRouterClient("test-key", RunBudget("0.01"), transport=transport)
    result = client.chat_completion(
        model_id="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": "Reply C"}],
        maximum_cost_usd="0.001",
        parameters={"reasoning": {"effort": "low", "exclude": True}},
        reasoning_exception="Phase 0 smoke only",
    )

    payload = json.loads(requests[0].data.decode("utf-8"))
    assert payload["reasoning"] == {"effort": "low", "exclude": True}
    assert result.reasoning_tokens == 2


def test_reasoning_can_be_explicitly_omitted_for_an_unsupported_model() -> None:
    requests: list[Request] = []

    def transport(request: Request, _: float) -> HTTPResponse:
        requests.append(request)
        return HTTPResponse(status=200, body=_fixture(), headers={})

    client = OpenRouterClient("test-key", RunBudget("0.01"), transport=transport)
    client.chat_completion(
        model_id="meta-llama/llama-3.3-70b-instruct",
        messages=[{"role": "user", "content": "Reply C"}],
        maximum_cost_usd="0.001",
        omit_reasoning=True,
    )

    payload = json.loads(requests[0].data.decode("utf-8"))
    assert "reasoning" not in payload
