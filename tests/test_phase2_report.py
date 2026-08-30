from __future__ import annotations

from spinning_arrow.contracts import Outcome, ParsedResponse, ResponseRecord, TokenUsage
from spinning_arrow.items import Item, Option
from spinning_arrow.phase2_report import (
    SUPPRESSION_THRESHOLD,
    _bootstrap_ci,
    _cell_scores,
    _ipip_domain_scores,
)


def _record(permutation: int, outcome: Outcome, choice: str | None) -> ResponseRecord:
    return ResponseRecord(
        run_id="run",
        ts="2026-08-30T00:00:00Z",
        model_id="model/test",
        provider_served="provider",
        instrument="instrument",
        item_id="item",
        condition="bare",
        framing="first_person",
        permutation=permutation,
        option_order=("A", "B"),
        prompt_hash="sha256:" + "0" * 64,
        messages=({"role": "user", "content": "Prompt"},),
        raw_response=choice,
        parsed=ParsedResponse(choice, choice is not None),
        outcome=outcome,
        tokens=TokenUsage(1, 1, 0),
        cost_usd=0.000001,
        latency_ms=1,
        error="failure" if outcome is Outcome.ERROR else None,
    )


def test_cell_scoring_suppresses_under_seventy_percent_coverage() -> None:
    item = Item(
        id="item",
        instrument="instrument",
        scale="instrument.scale",
        text="text",
        options=(Option("A", "No", 0), Option("B", "Yes", 1)),
        score_type="reference_agreement",
        answer_key="B",
    )
    records = [
        _record(0, Outcome.ANSWERED, "B"),
        _record(1, Outcome.ANSWERED, "A"),
        _record(2, Outcome.ANSWERED, "B"),
        _record(3, Outcome.ERROR, None),
        _record(4, Outcome.ERROR, None),
    ]

    cell = _cell_scores(records, {"item": item})[0]

    assert cell.coverage == 0.6
    assert cell.coverage < SUPPRESSION_THRESHOLD
    assert cell.score is None
    assert cell.correct_n == 2


def test_bootstrap_interval_is_deterministic() -> None:
    first = _bootstrap_ci([1.0, 2.0, 3.0, 4.0], 42)
    second = _bootstrap_ci([1.0, 2.0, 3.0, 4.0], 42)

    assert first == second
    assert first[0] is not None and first[1] is not None
    assert first[0] <= 2.5 <= first[1]


def test_ipip_domain_scores_roll_up_facet_cells() -> None:
    item = Item(
        id="item",
        instrument="ipip_neo_120",
        scale="ipip.openness.imagination",
        text="text",
        options=(Option("A", "Low", 1), Option("B", "High", 5)),
    )
    records = [_record(index, Outcome.ANSWERED, "B") for index in range(5)]
    cells = _cell_scores(records, {"item": item})

    domain = _ipip_domain_scores(cells)[0]

    assert domain.scale == "ipip.openness"
    assert domain.score == 5
    assert domain.total_items == 1
