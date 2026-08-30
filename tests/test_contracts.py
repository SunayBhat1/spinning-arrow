from __future__ import annotations

from spinning_arrow.contracts import (
    ContractValidationError,
    Outcome,
    ParsedResponse,
    ResponseRecord,
    RunManifest,
    ScoreRecord,
    TokenUsage,
)

HASH = "sha256:" + "a" * 64


def response_record() -> ResponseRecord:
    return ResponseRecord(
        run_id="2026-09-02T14:03:11Z__pilot__a3f9c1",
        ts="2026-09-02T14:07:33Z",
        model_id="openai/gpt-oss-120b",
        provider_served="fireworks",
        instrument="mfq2",
        item_id="mfq2_014",
        condition="bare",
        framing="third_person",
        permutation=3,
        option_order=("C", "A", "D", "B", "E"),
        prompt_hash=HASH,
        messages=({"role": "user", "content": "Choose one option."},),
        raw_response="C",
        parsed=ParsedResponse(choice="A", valid=True),
        outcome=Outcome.ANSWERED,
        tokens=TokenUsage(input_tokens=241, output_tokens=3, reasoning_tokens=0),
        cost_usd=0.0000094,
        latency_ms=812,
        error=None,
    )


def test_response_record_round_trips() -> None:
    original = response_record()
    restored = ResponseRecord.from_dict(original.to_dict())

    assert restored == original
    assert restored.parsed.choice == "A"  # Canonical, not the first displayed option (C).


def test_response_record_rejects_noncanonical_parsed_choice() -> None:
    record = response_record().to_dict()
    record["parsed"] = {"choice": "Z", "valid": True}

    try:
        ResponseRecord.from_dict(record)
    except ContractValidationError as error:
        assert "canonical" in str(error)
    else:  # pragma: no cover - assertion guard
        raise AssertionError("The contract accepted a noncanonical parsed choice")


def test_suppressed_score_requires_reason_and_has_no_interval() -> None:
    score = ScoreRecord(
        run_id="run",
        model_id="model",
        condition="bare",
        scale="mfq2.care",
        score=None,
        scale_min=0.0,
        scale_max=5.0,
        n_items=6,
        n_observations=60,
        n_valid=40,
        refusal_rate=0.2,
        hedge_rate=0.1,
        fragility=None,
        ci_low=None,
        ci_high=None,
        computed_at="2026-09-02T14:07:33Z",
        suppression_reason="insufficient valid responses",
    )

    assert ScoreRecord.from_dict(score.to_dict()) == score


def test_manifest_round_trips() -> None:
    manifest = RunManifest(
        run_id="run",
        item_set_hash=HASH,
        prompt_template_hashes={"choice": HASH},
        panel_hash=HASH,
        model_ids=("openai/gpt-oss-120b",),
        sampling_params={"max_tokens": 8, "reasoning": {"enabled": False}},
        parameter_omissions={"openai/gpt-oss-120b": ()},
        git_commit="a" * 40,
        started_at="2026-09-02T14:03:11Z",
        ended_at="2026-09-02T14:07:33Z",
        total_cost_usd=0.0000094,
        per_model_cost_usd={"openai/gpt-oss-120b": 0.0000094},
        outcome_counts={"answered": 1},
    )

    assert RunManifest.from_dict(manifest.to_dict()) == manifest
