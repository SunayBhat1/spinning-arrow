"""Classify model output and map displayed answer letters back to canonical options."""

from __future__ import annotations

import re
from dataclasses import dataclass

from spinning_arrow.contracts import Outcome, ParsedResponse

_ANSWER = re.compile(r"^\s*(?:answer\s*[:\-]?\s*)?\(?([A-E])\)?[.!]?\s*$", re.IGNORECASE)
_REFUSAL = re.compile(r"\b(i (?:can'?t|cannot|won'?t)|unable to|i must refuse)\b", re.IGNORECASE)
_HEDGE = re.compile(
    r"\b(it depends|not enough (?:information|context)|cannot determine|uncertain)\b", re.IGNORECASE
)


@dataclass(frozen=True)
class ParseResult:
    parsed: ParsedResponse
    outcome: Outcome
    displayed_choice: str | None


def parse_response(raw_response: str, option_order: tuple[str, ...]) -> ParseResult:
    match = _ANSWER.match(raw_response)
    if match:
        displayed = match.group(1).upper()
        if displayed in option_order:
            canonical = chr(ord("A") + option_order.index(displayed))
            return ParseResult(ParsedResponse(canonical, True), Outcome.ANSWERED, displayed)
    if _REFUSAL.search(raw_response):
        return ParseResult(ParsedResponse(None, False), Outcome.REFUSED, None)
    if _HEDGE.search(raw_response):
        return ParseResult(ParsedResponse(None, False), Outcome.HEDGED, None)
    return ParseResult(ParsedResponse(None, False), Outcome.UNPARSEABLE, None)
