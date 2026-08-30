from __future__ import annotations

import gzip
import json
from decimal import Decimal
from pathlib import Path

from spinning_arrow.client import CompletionResult
from spinning_arrow.contracts import Outcome, ParsedResponse, ResponseRecord, TokenUsage
from spinning_arrow.items import load_items
from spinning_arrow.run import PilotConfig, PilotModel, _append_jsonl_gzip, _run_one


def _record() -> ResponseRecord:
    return ResponseRecord(
        run_id="run",
        ts="2026-08-30T00:00:00Z",
        model_id="test/model",
        provider_served="provider",
        instrument="mfq2",
        item_id="mfq2_001",
        condition="bare",
        framing="third_person",
        permutation=0,
        option_order=("C", "A", "D", "B", "E"),
        prompt_hash="sha256:" + "0" * 64,
        messages=({"role": "user", "content": "Prompt"},),
        raw_response="C",
        parsed=ParsedResponse("A", True),
        outcome=Outcome.ANSWERED,
        tokens=TokenUsage(3, 1, 0),
        cost_usd=0.000001,
        latency_ms=10,
        error=None,
    )


def test_append_jsonl_gzip_persists_each_completed_record(tmp_path: Path) -> None:
    path = tmp_path / "records.jsonl.gz"
    _append_jsonl_gzip(path, _record())
    _append_jsonl_gzip(path, _record())

    with gzip.open(path, "rt", encoding="utf-8") as handle:
        rows = [json.loads(line) for line in handle]

    assert len(rows) == 2
    assert rows[0]["model_id"] == "test/model"


def test_worker_records_unexpected_call_failures_as_errors() -> None:
    class FailingClient:
        def chat_completion(self, **_: object) -> object:
            raise ValueError("unexpected client failure")

    root = Path(__file__).parents[1]
    item = load_items([root / "instruments" / "mfq2.yaml"])[0]
    config = PilotConfig(
        budget_usd=1,
        conditions=("bare",),
        framings=("third_person",),
        permutations=1,
        max_tokens=8,
        temperature=0,
        models=(),
    )
    record = _run_one(
        FailingClient(),  # type: ignore[arg-type]
        "run",
        PilotModel("test/model", Decimal("0.01"), 8, (), None, None),
        item,
        "bare",
        "third_person",
        0,
        config,
    )

    assert record.outcome is Outcome.ERROR
    assert record.error == "unexpected client failure"


def test_worker_accounts_for_a_completion_without_text() -> None:
    class EmptyContentClient:
        def chat_completion(self, **_: object) -> CompletionResult:
            return CompletionResult(
                raw={},
                text=None,
                provider_served="provider",
                input_tokens=5,
                output_tokens=8,
                reasoning_tokens=3,
                cost_usd=Decimal("0.000123"),
                latency_ms=10,
            )

    root = Path(__file__).parents[1]
    item = load_items([root / "instruments" / "mfq2.yaml"])[0]
    config = PilotConfig(Decimal("1"), ("bare",), ("third_person",), 1, 8, 0, ())
    record = _run_one(
        EmptyContentClient(),  # type: ignore[arg-type]
        "run",
        PilotModel("test/model", Decimal("0.01"), 8, (), None, None),
        item,
        "bare",
        "third_person",
        0,
        config,
    )

    assert record.outcome is Outcome.ERROR
    assert record.cost_usd == 0.000123
    assert record.tokens.reasoning_tokens == 3
