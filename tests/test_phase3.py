from __future__ import annotations

from pathlib import Path

from spinning_arrow.phase3 import _load_config, _phase3_items
from spinning_arrow.phase3_report import _prediction
from spinning_arrow.render import render_item

ROOT = Path(__file__).parents[1]


def test_phase3_panel_and_scenario_bank_have_the_approved_call_shape() -> None:
    config = _load_config(ROOT / "panels" / "phase3.yaml")
    items = _phase3_items(ROOT)

    assert len(items) == 30
    assert len(config.runtime.models) == 3
    assert (
        len(items)
        * len(config.runtime.models)
        * len(config.runtime.framings)
        * config.runtime.permutations
        == 1080
    )
    assert config.runtime.budget_usd == 2
    assert config.runtime.maximum_forecast_usd == 1


def test_phase3_surfaces_render_and_all_six_orders_are_available() -> None:
    item = _phase3_items(ROOT)[0]
    orders = set()
    for framing in ("direct", "advice"):
        for permutation in range(6):
            rendered = render_item(item, framing=framing, condition="bare", permutation=permutation)
            orders.add(rendered.option_order)
            assert "Reply with only the option letter." in rendered.messages[-1]["content"]
    assert len(orders) == 6


def test_directional_prediction_requires_every_anchor_to_clear_neutral() -> None:
    pairing = {
        "mode": "directional",
        "anchors": [
            {"scale": "a", "direction": "higher"},
            {"scale": "b", "direction": "lower"},
        ],
    }
    baseline = {
        ("model", "a"): {"score": 4.0, "ci_low": 3.2, "ci_high": 4.8},
        ("model", "b"): {"score": 2.0, "ci_low": 1.2, "ci_high": 2.8},
    }
    assert _prediction("model", pairing, baseline, 3.0)["expected_direction"] == "higher"
    baseline[("model", "b")] = {"score": 3.0, "ci_low": 2.8, "ci_high": 3.2}
    assert _prediction("model", pairing, baseline, 3.0)["eligible"] is False
