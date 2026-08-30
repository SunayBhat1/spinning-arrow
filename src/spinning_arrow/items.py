"""Load, validate, and hash the committed item bank."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class ItemValidationError(ValueError):
    """Raised when an instrument file does not meet the public item-bank contract."""


@dataclass(frozen=True)
class Option:
    id: str
    label: str
    value: float


@dataclass(frozen=True)
class Item:
    id: str
    instrument: str
    scale: str
    text: str
    options: tuple[Option, ...]
    source_index: int | None = None
    score_type: str = "value"
    answer_key: str | None = None


def load_items(paths: list[Path]) -> tuple[Item, ...]:
    items: list[Item] = []
    for path in paths:
        document = _read_document(path)
        instrument = _string(document.get("instrument"), f"{path}: instrument")
        document_options = document.get("options")
        options = _options(document_options, path) if document_options is not None else None
        raw_items = document.get("items")
        if not isinstance(raw_items, list) or not raw_items:
            raise ItemValidationError(f"{path}: items must be a non-empty list")
        for index, raw_item in enumerate(raw_items):
            if not isinstance(raw_item, dict):
                raise ItemValidationError(f"{path}: items[{index}] must be an object")
            source_index = raw_item.get("source_index")
            if source_index is not None and (
                isinstance(source_index, bool)
                or not isinstance(source_index, int)
                or source_index < 0
            ):
                raise ItemValidationError(
                    f"{path}: items[{index}].source_index must be a non-negative integer"
                )
            raw_options = raw_item.get("options")
            item_options = _options(raw_options, path) if raw_options is not None else options
            if item_options is None:
                raise ItemValidationError(f"{path}: items[{index}] must provide options")
            option_values = raw_item.get("option_values")
            if option_values is not None:
                if not isinstance(option_values, list) or len(option_values) != len(item_options):
                    raise ItemValidationError(
                        f"{path}: items[{index}].option_values must match the option count"
                    )
                if any(
                    isinstance(value, bool) or not isinstance(value, (int, float))
                    for value in option_values
                ):
                    raise ItemValidationError(
                        f"{path}: items[{index}].option_values must be numeric"
                    )
                item_options = tuple(
                    Option(option.id, option.label, float(value))
                    for option, value in zip(item_options, option_values, strict=True)
                )
            score_type = raw_item.get("score_type", "value")
            if score_type not in {"value", "reference_agreement", "attention"}:
                raise ItemValidationError(
                    f"{path}: items[{index}].score_type must be value, reference_agreement, "
                    "or attention"
                )
            answer_key = raw_item.get("answer_key")
            if answer_key is not None:
                answer_key = _string(answer_key, f"{path}: items[{index}].answer_key")
                if answer_key not in {option.id for option in item_options}:
                    raise ItemValidationError(
                        f"{path}: items[{index}].answer_key must be a canonical option ID"
                    )
            if score_type in {"reference_agreement", "attention"} and answer_key is None:
                raise ItemValidationError(
                    f"{path}: items[{index}].answer_key is required for {score_type} scoring"
                )
            items.append(
                Item(
                    id=_string(raw_item.get("id"), f"{path}: items[{index}].id"),
                    instrument=instrument,
                    scale=_string(raw_item.get("scale"), f"{path}: items[{index}].scale"),
                    text=_string(raw_item.get("text"), f"{path}: items[{index}].text"),
                    options=item_options,
                    source_index=source_index,
                    score_type=score_type,
                    answer_key=answer_key,
                )
            )
    ids = [item.id for item in items]
    if len(ids) != len(set(ids)):
        raise ItemValidationError("item IDs must be globally unique")
    return tuple(items)


def item_set_hash(items: tuple[Item, ...]) -> str:
    payload = []
    for item in items:
        entry: dict[str, object] = {
            "id": item.id,
            "instrument": item.instrument,
            "scale": item.scale,
            "text": item.text,
            "options": [option.__dict__ for option in item.options],
            "source_index": item.source_index,
        }
        # Keeping absent optional fields absent preserves the already-approved Phase 1 hash.
        if item.score_type != "value":
            entry["score_type"] = item.score_type
        if item.answer_key is not None:
            entry["answer_key"] = item.answer_key
        payload.append(entry)
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(canonical.encode()).hexdigest()


def _read_document(path: Path) -> dict[str, Any]:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ItemValidationError(f"{path}: must be valid JSON-formatted YAML") from error
    if not isinstance(document, dict):
        raise ItemValidationError(f"{path}: root must be an object")
    return document


def _options(raw_options: object, path: Path) -> tuple[Option, ...]:
    if not isinstance(raw_options, list) or len(raw_options) < 2:
        raise ItemValidationError(f"{path}: options must contain at least two options")
    options: list[Option] = []
    for index, raw_option in enumerate(raw_options):
        if not isinstance(raw_option, dict):
            raise ItemValidationError(f"{path}: options[{index}] must be an object")
        value = raw_option.get("value")
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ItemValidationError(f"{path}: options[{index}].value must be numeric")
        options.append(
            Option(
                id=_string(raw_option.get("id"), f"{path}: options[{index}].id"),
                label=_string(raw_option.get("label"), f"{path}: options[{index}].label"),
                value=float(value),
            )
        )
    ids = [option.id for option in options]
    if ids != [chr(ord("A") + index) for index in range(len(options))]:
        raise ItemValidationError(f"{path}: options must use canonical IDs A through {ids[-1]}")
    return tuple(options)


def _string(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ItemValidationError(f"{field} must be a non-empty string")
    return value
