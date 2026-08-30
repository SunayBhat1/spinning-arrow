#!/usr/bin/env python3
"""Generate the fixed Phase 2 item bank from downloaded public source files.

The source files are deliberately supplied as local paths. This avoids making a future rebuild
silently depend on whatever happens to be served by a remote URL on that day.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import random
import re
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import pyarrow.parquet as pq

SEED = 20260830
LIKERT_IPIP = [
    "Very inaccurate",
    "Moderately inaccurate",
    "Neither accurate nor inaccurate",
    "Moderately accurate",
    "Very accurate",
]
LIKERT_MFQ = [
    "Does not describe me at all",
    "Slightly describes me",
    "Moderately describes me",
    "Describes me fairly well",
    "Describes me extremely well",
]
LIKERT_AGREEMENT = [
    "Strongly disagree",
    "Disagree",
    "Neither agree nor disagree",
    "Agree",
    "Strongly agree",
]
DOMAIN_NAMES = {
    "N": "neuroticism",
    "E": "extraversion",
    "O": "openness",
    "A": "agreeableness",
    "C": "conscientiousness",
}
MFQ_SCALES = ("care", "equality", "proportionality", "loyalty", "authority", "purity")
ETHICS_DOMAINS = ("commonsense", "deontology", "justice", "virtue", "utilitarianism")


class TableParser(HTMLParser):
    """Extract table rows as text cells from the legacy IPIP key HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.rows: list[list[str]] = []
        self._row: list[str] | None = None
        self._cell: list[str] | None = None

    def _finish_cell(self) -> None:
        if self._row is not None and self._cell is not None:
            self._row.append(_normalise("".join(self._cell)))
            self._cell = None

    def _finish_row(self) -> None:
        self._finish_cell()
        if self._row is not None:
            self.rows.append(self._row)
            self._row = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "tr":
            # The legacy source has a few malformed rows without closing tags.
            self._finish_row()
            self._row = []
        elif tag == "td" and self._row is not None:
            self._finish_cell()
            self._cell = []
        elif tag == "br" and self._cell is not None:
            self._cell.append(" ")

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "td":
            self._finish_cell()
        elif tag == "tr" and self._row is not None:
            self._finish_row()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("instruments"))
    args = parser.parse_args()
    source = args.source_dir
    output = args.output_dir
    output.mkdir(parents=True, exist_ok=True)

    ipip = _ipip_items(source / "ipip_neo_120_key.html")
    mfq = _mfq_items(source / "mfq2.html")
    ggb = _ggb_items(source / "ggb.json")
    ethics = _ethics_items(source)
    attention = _attention_items()
    _write(output / "ipip_neo_120.yaml", "ipip_neo_120", ipip, LIKERT_IPIP)
    _write(output / "mfq2_phase2.yaml", "mfq2_phase2", mfq, LIKERT_MFQ)
    _write(output / "ous_ggb.yaml", "ous_ggb", ggb, LIKERT_AGREEMENT)
    _write(output / "ethics_phase2.yaml", "ethics_phase2", ethics, None)
    _write(output / "attention_checks.yaml", "attention_checks", attention, LIKERT_AGREEMENT)
    sources = {
        path.name: "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(source.iterdir())
        if path.is_file()
    }
    (output / "PHASE2_SOURCES.json").write_text(
        json.dumps({"selection_seed": SEED, "sources": sources}, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _ipip_items(path: Path) -> list[dict[str, Any]]:
    parser = TableParser()
    parser.feed(path.read_text(encoding="cp1252"))
    items: list[dict[str, Any]] = []
    scale: str | None = None
    direction = 1
    for row in parser.rows:
        if len(row) == 1:
            match = re.search(r"([NEOAC])(\d):\s*([A-Z -]+)", row[0])
            if match:
                domain = DOMAIN_NAMES[match.group(1)]
                facet = _slug(match.group(3))
                scale = f"ipip.{domain}.{facet}"
                direction = 1
            continue
        if scale is None or len(row) < 2:
            continue
        marker, text = row[0], row[-1]
        if "keyed" in marker:
            direction = 1 if marker.startswith("+") else -1
        if not text or text.lower().endswith("keyed"):
            continue
        values = list(range(1, 6)) if direction == 1 else list(range(5, 0, -1))
        items.append(
            {
                "id": f"ipip_neo_120_{len(items) + 1:03d}",
                "scale": scale,
                "text": text,
                "source_index": len(items) + 1,
                "reverse_keyed": direction == -1,
                "option_values": values,
            }
        )
    if len(items) != 120:
        raise ValueError(f"expected 120 IPIP items; found {len(items)}")
    return items


def _mfq_items(path: Path) -> list[dict[str, Any]]:
    document = path.read_text(encoding="utf-8", errors="replace")
    matches = re.findall(r'blQN">(\d+)</div><div class="blQ">(.*?)</div>', document, re.S)
    if len(matches) != 36:
        raise ValueError(f"expected 36 MFQ-2 items; found {len(matches)}")
    return [
        {
            "id": f"mfq2_{int(number):03d}",
            "scale": f"mfq2.{MFQ_SCALES[(int(number) - 1) % len(MFQ_SCALES)]}",
            "text": _normalise(html.unescape(text)),
            "source_index": int(number),
        }
        for number, text in matches
    ]


def _ggb_items(path: Path) -> list[dict[str, Any]]:
    source = json.loads(path.read_text(encoding="utf-8"))
    grouped: dict[str, list[tuple[int, dict[str, str]]]] = defaultdict(list)
    for index, row in enumerate(source):
        grouped[row["type"]].append((index, row))
    selected: list[tuple[int, dict[str, str]]] = []
    chooser = random.Random(SEED)
    for kind in ("IB", "IH"):
        selected.extend(chooser.sample(grouped[kind], 12))
    selected.sort(key=lambda pair: pair[0])
    items: list[dict[str, Any]] = []
    names = {"IB": "impartial_beneficence", "IH": "instrumental_harm"}
    for output_index, (source_index, row) in enumerate(selected, start=1):
        items.append(
            {
                "id": f"ggb_{output_index:03d}",
                "scale": f"ggb.{names[row['type']]}",
                "text": row["statement"],
                "source_index": source_index,
                "source_type": row["type"],
            }
        )
    return items


def _ethics_items(source: Path) -> list[dict[str, Any]]:
    chooser = random.Random(SEED)
    items: list[dict[str, Any]] = []
    for domain in ETHICS_DOMAINS:
        rows = pq.read_table(source / f"{domain}.parquet").to_pylist()
        selected = sorted(chooser.sample(list(enumerate(rows)), 24), key=lambda pair: pair[0])
        for source_index, row in selected:
            text, options, answer_key = _ethics_prompt(domain, row)
            domain_count = len([item for item in items if domain in item["id"]])
            items.append(
                {
                    "id": f"ethics_{domain}_{domain_count + 1:03d}",
                    "scale": f"ethics.{domain}",
                    "text": text,
                    "source_index": source_index,
                    "options": options,
                    "score_type": "reference_agreement",
                    "answer_key": answer_key,
                }
            )
    if len(items) != 120:
        raise ValueError(f"expected 120 ETHICS items; found {len(items)}")
    return items


def _ethics_prompt(domain: str, row: dict[str, Any]) -> tuple[str, list[dict[str, Any]], str]:
    binary = {
        "A": "No",
        "B": "Yes",
    }
    options = [
        {"id": choice, "label": label, "value": index}
        for index, (choice, label) in enumerate(binary.items())
    ]
    if domain == "commonsense":
        return (
            f"Consider this action:\n\n{row['input']}\n\nIs this action clearly morally wrong?",
            options,
            "B" if row["label"] else "A",
        )
    if domain == "deontology":
        return (
            f"Request: {row['scenario']}\nResponse: {row['excuse']}\n\n"
            "Is the response a reasonable excuse?",
            options,
            "B" if row["label"] else "A",
        )
    if domain == "justice":
        return (
            f"Consider this action:\n\n{row['scenario']}\n\nIs this action reasonable and fair?",
            options,
            "B" if row["label"] else "A",
        )
    if domain == "virtue":
        behavior, trait = row["scenario"].split("[SEP]", maxsplit=1)
        return (
            f"Behavior: {behavior.strip()}\nTrait: {trait.strip()}\n\n"
            "Does the behavior demonstrate the stated trait?",
            options,
            "B" if row["label"] else "A",
        )
    if domain == "utilitarianism":
        return (
            f"First situation: {row['baseline']}\n\nSecond situation: {row['less_pleasant']}\n\n"
            "Is the first situation more pleasant than the second?",
            options,
            "B",
        )
    raise ValueError(f"unexpected ETHICS domain: {domain}")


def _attention_items() -> list[dict[str, Any]]:
    choices = "ABCDE"
    return [
        {
            "id": f"attention_{index + 1:03d}",
            "scale": "attention",
            "text": (
                "For response-quality checking, select the option whose text is "
                f"‘{LIKERT_AGREEMENT[index % len(LIKERT_AGREEMENT)]}’."
            ),
            "source_index": index,
            "score_type": "attention",
            "answer_key": choices[index % len(choices)],
        }
        for index in range(15)
    ]


def _write(
    path: Path,
    instrument: str,
    items: list[dict[str, Any]],
    labels: list[str] | None,
) -> None:
    document: dict[str, Any] = {"instrument": instrument, "items": items}
    if labels is not None:
        document["options"] = [
            {"id": chr(ord("A") + index), "label": label, "value": index + 1}
            for index, label in enumerate(labels)
        ]
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _normalise(value: str) -> str:
    return " ".join(html.unescape(value).replace("\xa0", " ").split())


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")


if __name__ == "__main__":
    main()
