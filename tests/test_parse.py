from __future__ import annotations

import itertools
import json
from pathlib import Path

from spinning_arrow.parse import parse_response

FIXTURES = Path(__file__).parent / "fixtures"


def test_option_mapping_canonicalizes_every_permutation() -> None:
    canonical = ("A", "B", "C", "D", "E")
    for option_order in itertools.permutations(canonical):
        for index, expected_choice in enumerate(canonical):
            displayed_choice = option_order[index]
            result = parse_response(displayed_choice, option_order)

            assert result.outcome.value == "answered"
            assert result.parsed.choice == expected_choice


def test_parse_outcomes_match_golden_fixtures() -> None:
    fixtures = json.loads((FIXTURES / "parse_outcomes.json").read_text(encoding="utf-8"))
    option_order = ("C", "A", "D", "B", "E")

    for fixture in fixtures:
        result = parse_response(fixture["raw_response"], option_order)

        assert result.outcome.value == fixture["outcome"]
        assert result.parsed.choice == fixture["canonical_choice"]
