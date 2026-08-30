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


def load_items(paths: list[Path]) -> tuple[Item, ...]:
    items: list[Item] = []
    for path in paths:
        document = _read_document(path)
        instrument = _string(document.get("instrument"), f"{path}: instrument")
        options = _options(document.get("options"), path)
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
            items.append(
                Item(
                    id=_string(raw_item.get("id"), f"{path}: items[{index}].id"),
                    instrument=instrument,
                    scale=_string(raw_item.get("scale"), f"{path}: items[{index}].scale"),
                    text=_string(raw_item.get("text"), f"{path}: items[{index}].text"),
                    options=options,
                    source_index=source_index,
                )
            )
    ids = [item.id for item in items]
    if len(ids) != len(set(ids)):
        raise ItemValidationError("item IDs must be globally unique")
    return tuple(items)


def item_set_hash(items: tuple[Item, ...]) -> str:
    payload = [
        {
            "id": item.id,
            "instrument": item.instrument,
            "scale": item.scale,
            "text": item.text,
            "options": [option.__dict__ for option in item.options],
            "source_index": item.source_index,
        }
        for item in items
    ]
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
