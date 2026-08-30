from __future__ import annotations

from pathlib import Path

from spinning_arrow.items import item_set_hash, load_items
from spinning_arrow.phase2 import _load_config, _phase2_items
from spinning_arrow.render import render_item

ROOT = Path(__file__).parents[1]


def test_phase2_bank_is_complete_and_uses_its_item_level_scoring_contract() -> None:
    items = _phase2_items(ROOT)

    assert len(items) == 315
    assert {item.instrument for item in items} == {
        "attention_checks",
        "ethics_phase2",
        "ipip_neo_120",
        "mfq2_phase2",
        "ous_ggb",
    }
    assert sum(item.score_type == "reference_agreement" for item in items) == 120
    assert sum(item.score_type == "attention" for item in items) == 15
    assert all(item.answer_key for item in items if item.score_type != "value")


def test_phase2_reverse_keying_and_item_options_are_loaded() -> None:
    items = _phase2_items(ROOT)
    reverse_keyed = next(item for item in items if item.id == "ipip_neo_120_008")
    ethics = next(item for item in items if item.instrument == "ethics_phase2")

    assert [option.value for option in reverse_keyed.options] == [5, 4, 3, 2, 1]
    assert [option.id for option in ethics.options] == ["A", "B"]
    assert ethics.answer_key in {"A", "B"}


def test_phase2_all_instruments_render_under_every_experimental_condition() -> None:
    items = _phase2_items(ROOT)

    for item in items:
        for framing in ("first_person", "third_person"):
            for condition in ("bare", "evaluator"):
                rendered = render_item(item, framing=framing, condition=condition, permutation=4)
                assert rendered.messages[-1]["role"] == "user"
                assert "Reply with only the option letter." in rendered.messages[-1]["content"]
                assert len(rendered.option_order) == len(item.options)


def test_phase2_panel_has_exact_required_call_count_and_d5_configuration() -> None:
    config = _load_config(ROOT / "panels" / "phase2.yaml")

    assert len(config.models) == 9
    call_count = (
        len(_phase2_items(ROOT))
        * len(config.conditions)
        * len(config.framings)
        * config.permutations
    )
    assert call_count == 6300
    assert config.budget_usd == 25
    assert config.maximum_forecast_usd == 20
    assert {model.id for model in config.models} == {
        "anthropic/claude-sonnet-5",
        "deepseek/deepseek-v4-pro-0813",
        "google/gemini-2.5-flash-lite",
        "meta-llama/llama-3.3-70b-instruct",
        "mistralai/mistral-medium-3.1",
        "openai/gpt-5.4-mini",
        "qwen/qwen3.8-27b",
        "x-ai/grok-4.20",
        "z-ai/glm-5.2",
    }


def test_phase1_item_hash_remains_reproducible() -> None:
    items = load_items(
        [ROOT / "instruments" / "mfq2.yaml", ROOT / "instruments" / "ethics_sample.yaml"]
    )

    assert item_set_hash(items) == (
        "sha256:8069cad2776162b453dd564985d8e8843dd2fb9766b7b63edbf942f857adca84"
    )
