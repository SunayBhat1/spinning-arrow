"""Generate the Phase 1 pilot Gate report from committed raw records."""

# ruff: noqa: E501 -- Markdown table rows and report prose are intentionally literal.

from __future__ import annotations

import argparse
import gzip
import json
import statistics
from collections import Counter, defaultdict
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path

from spinning_arrow.contracts import Outcome, ResponseRecord, RunManifest
from spinning_arrow.items import Item, load_items

PILOT_CALLS_PER_MODEL = 400


@dataclass(frozen=True)
class PilotReport:
    path: Path
    run_id: str


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate the Phase 1 pilot report.")
    parser.add_argument("run_id")
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args(argv)
    try:
        artifact = generate_pilot_report(Path(args.project_root), args.run_id)
    except (OSError, ValueError) as error:
        print(f"Pilot report was not generated: {error}")
        return 2
    print(f"Pilot report: {artifact.path}")
    return 0


def generate_pilot_report(project_root: Path, run_id: str) -> PilotReport:
    root = project_root.resolve()
    manifest = _load_manifest(root / "data" / "manifests" / f"{run_id}.json")
    if manifest.run_id != run_id:
        raise ValueError("manifest run ID does not match the requested run ID")
    records = _load_records(root / "data" / "raw" / run_id, run_id)
    by_model = _group_records(records, lambda record: record.model_id)
    missing = {
        model_id: PILOT_CALLS_PER_MODEL - len(by_model.get(model_id, []))
        for model_id in manifest.model_ids
        if len(by_model.get(model_id, [])) != PILOT_CALLS_PER_MODEL
    }
    if missing:
        detail = ", ".join(f"{model}: {delta:+d}" for model, delta in missing.items())
        raise ValueError(f"pilot is incomplete; calls relative to {PILOT_CALLS_PER_MODEL}: {detail}")
    unexpected_models = set(by_model).difference(manifest.model_ids)
    if unexpected_models:
        raise ValueError(f"raw data contains models absent from manifest: {sorted(unexpected_models)}")
    if len(records) != len(manifest.model_ids) * PILOT_CALLS_PER_MODEL:
        raise ValueError("pilot raw record count is inconsistent with its manifest panel")
    items = load_items(
        [root / "instruments" / "mfq2.yaml", root / "instruments" / "ethics_sample.yaml"]
    )
    item_lookup = {item.id: item for item in items}
    panel = _load_panel(root / "panels" / "pilot.yaml")
    report = _render_report(manifest, records, item_lookup, panel)
    path = root / "reports" / "01_pilot.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report, encoding="utf-8")
    return PilotReport(path=path, run_id=run_id)


def _load_manifest(path: Path) -> RunManifest:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"could not read manifest {path}") from error
    if not isinstance(document, Mapping):
        raise ValueError("manifest must be a JSON object")
    return RunManifest.from_dict(document)


def _load_records(directory: Path, run_id: str) -> list[ResponseRecord]:
    paths = sorted(directory.glob("*.jsonl.gz"))
    if not paths:
        raise ValueError(f"no raw JSONL gzip files found for {run_id}")
    records: list[ResponseRecord] = []
    for path in paths:
        try:
            with gzip.open(path, "rt", encoding="utf-8") as handle:
                for line_number, line in enumerate(handle, start=1):
                    document = json.loads(line)
                    if not isinstance(document, Mapping):
                        raise ValueError(f"{path}:{line_number} is not a JSON object")
                    record = ResponseRecord.from_dict(document)
                    if record.run_id != run_id:
                        raise ValueError(f"{path}:{line_number} belongs to a different run")
                    records.append(record)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError(f"could not read raw records at {path}") from error
    return records


def _load_panel(path: Path) -> Mapping[str, object]:
    try:
        panel = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"could not read panel {path}") from error
    if not isinstance(panel, Mapping):
        raise ValueError("pilot panel must be a JSON object")
    return panel


def _render_report(
    manifest: RunManifest,
    records: list[ResponseRecord],
    item_lookup: Mapping[str, Item],
    panel: Mapping[str, object],
) -> str:
    models = list(manifest.model_ids)
    lines = [
        "# Phase 1 pilot report",
        "",
        f"**Run:** `{manifest.run_id}`  ",
        f"**Window:** {manifest.started_at} to {manifest.ended_at}  ",
        f"**Raw data:** `data/raw/{manifest.run_id}/`  ",
        f"**Manifest:** `data/manifests/{manifest.run_id}.json`  ",
        f"**Records:** {len(records)} (400 per model)",
        "",
        "The two documented mandatory-reasoning exceptions are pilot-only. Their reasoning tokens "
        "are retained in raw records and their results do not alter the Phase 2+ main-battery rule.",
        "",
        "## 1. Parse rate",
        "",
        "Clean parse rate is `answered / all calls`; it counts neither refusals nor malformed output as "
        "a usable response. The pre-specified scaling threshold is approximately 95%.",
        "",
        "| Model | Answered | Refused | Hedged | Unparseable | Error | Clean parse rate |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    by_model = _group_records(records, lambda record: record.model_id)
    for model in models:
        counts = Counter(record.outcome.value for record in by_model[model])
        total = len(by_model[model])
        answered = counts[Outcome.ANSWERED.value]
        refused = counts[Outcome.REFUSED.value]
        hedged = counts[Outcome.HEDGED.value]
        unparseable = counts[Outcome.UNPARSEABLE.value]
        error = counts[Outcome.ERROR.value]
        rate = _percent(answered, total)
        lines.append(
            f"| {model} | {answered} | {refused} | {hedged} | {unparseable} | {error} | {rate} |"
        )

    lines.extend(_refusal_section(records, models))
    lines.extend(_position_bias_section(records, models, item_lookup))
    lines.extend(_framing_section(records, models, item_lookup))
    lines.extend(_fragility_section(records, models, item_lookup))
    lines.extend(_cost_section(records, models, panel, manifest))
    lines.extend(_latency_section(records, models))
    lines.extend(_recommendation(records, models, item_lookup))
    return "\n".join(lines) + "\n"


def _refusal_section(records: list[ResponseRecord], models: list[str]) -> list[str]:
    lines = [
        "",
        "## 2. Refusal rate by model and instrument",
        "",
        "| Model | MFQ-2 refusals | ETHICS refusals | Overall refusals |",
        "|---|---:|---:|---:|",
    ]
    for model in models:
        model_records = [record for record in records if record.model_id == model]
        cells = []
        for instrument in ("mfq2", "ethics_deontology"):
            group = [record for record in model_records if record.instrument == instrument]
            cells.append(_percent(_count(group, Outcome.REFUSED), len(group)))
        lines.append(
            f"| {model} | {cells[0]} | {cells[1]} | "
            f"{_percent(_count(model_records, Outcome.REFUSED), len(model_records))} |"
        )
    return lines


def _position_bias_section(
    records: list[ResponseRecord], models: list[str], item_lookup: Mapping[str, Item]
) -> list[str]:
    lines = [
        "",
        "## 3. Position-bias magnitude",
        "",
        "For each instrument, this is the range of mean selected *canonical option values* conditional "
        "on the displayed response letter. A value near zero indicates the display slot did not move "
        "answers; values are not compared across the two instruments' different scales.",
        "",
        "| Model | Instrument | Valid n | A mean | B mean | C mean | D mean | E mean | Slot range |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for model in models:
        for instrument in ("mfq2", "ethics_deontology"):
            groups: dict[str, list[float]] = {letter: [] for letter in "ABCDE"}
            for record in records:
                if (
                    record.model_id != model
                    or record.instrument != instrument
                    or record.outcome is not Outcome.ANSWERED
                ):
                    continue
                item = item_lookup[record.item_id]
                canonical = record.parsed.choice
                assert canonical is not None
                displayed = record.option_order[ord(canonical) - ord("A")]
                value = item.options[ord(canonical) - ord("A")].value
                groups[displayed].append(value)
            means = {letter: _mean(values) for letter, values in groups.items()}
            available = [value for value in means.values() if value is not None]
            span = max(available) - min(available) if available else None
            cells = " | ".join(_number(means[letter]) for letter in "ABCDE")
            lines.append(
                f"| {model} | {instrument} | {sum(len(values) for values in groups.values())} | "
                f"{cells} | {_number(span)} |"
            )
    return lines


def _framing_section(
    records: list[ResponseRecord], models: list[str], item_lookup: Mapping[str, Item]
) -> list[str]:
    lines = [
        "",
        "## 4. Framing sensitivity",
        "",
        "Pairs hold model, item, condition, and option permutation constant. The reported difference is "
        "`first-person mean − third-person mean` in the instrument's response-value units.",
        "",
        "| Model | Instrument | Complete pairs | First-person mean | Third-person mean | Difference |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for model in models:
        for instrument in ("mfq2", "ethics_deontology"):
            paired: dict[tuple[str, str, int], dict[str, float]] = defaultdict(dict)
            for record in records:
                if (
                    record.model_id != model
                    or record.instrument != instrument
                    or record.outcome is not Outcome.ANSWERED
                ):
                    continue
                canonical = record.parsed.choice
                assert canonical is not None
                value = item_lookup[record.item_id].options[ord(canonical) - ord("A")].value
                paired[(record.item_id, record.condition, record.permutation)][record.framing] = value
            first = [values["first_person"] for values in paired.values() if len(values) == 2]
            third = [values["third_person"] for values in paired.values() if len(values) == 2]
            first_mean = _mean(first)
            third_mean = _mean(third)
            difference = None if first_mean is None or third_mean is None else first_mean - third_mean
            lines.append(
                f"| {model} | {instrument} | {len(first)} | {_number(first_mean)} | "
                f"{_number(third_mean)} | {_number(difference)} |"
            )
    return lines


def _fragility_section(
    records: list[ResponseRecord], models: list[str], item_lookup: Mapping[str, Item]
) -> list[str]:
    lines = [
        "",
        "## 5. Fragility signal",
        "",
        "For each model/instrument/item/framing cell, compute the population SD of selected response "
        "values across its five option permutations, then average those SDs. This is a descriptive "
        "pre-scoring fragility proxy, not an uncertainty interval.",
        "",
        "| Model | Instrument | Cells with 2+ valid permutations | Mean within-cell SD | Max within-cell SD |",
        "|---|---|---:|---:|---:|",
    ]
    for model in models:
        for instrument in ("mfq2", "ethics_deontology"):
            values: dict[tuple[str, str, str, str], list[float]] = defaultdict(list)
            for record in records:
                if (
                    record.model_id != model
                    or record.instrument != instrument
                    or record.outcome is not Outcome.ANSWERED
                ):
                    continue
                canonical = record.parsed.choice
                assert canonical is not None
                value = item_lookup[record.item_id].options[ord(canonical) - ord("A")].value
                key = (record.model_id, record.item_id, record.condition, record.framing)
                values[key].append(value)
            deviations = [statistics.pstdev(group) for group in values.values() if len(group) >= 2]
            lines.append(
                f"| {model} | {instrument} | {len(deviations)} | {_number(_mean(deviations))} | "
                f"{_number(max(deviations) if deviations else None)} |"
            )
    return lines


def _cost_section(
    records: list[ResponseRecord],
    models: list[str],
    panel: Mapping[str, object],
    manifest: RunManifest,
) -> list[str]:
    lines = [
        "",
        "## 6. Cost reconciliation",
        "",
        "Forecast is a conservative, pre-run ceiling calculation: 180 input tokens plus each model's "
        "recorded `max_tokens`, priced at the frozen per-million rates for 400 calls. Actual is the "
        "sum of OpenRouter `usage.cost` values in the raw records and must be reconciled with the "
        "OpenRouter dashboard before approving Gate 1.",
        "",
        "| Model | Forecast (USD) | Actual (USD) | Actual / forecast |",
        "|---|---:|---:|---:|",
    ]
    model_entries = _panel_models(panel)
    forecast_total = Decimal("0")
    actual_total = Decimal("0")
    for model in models:
        entry = model_entries[model]
        forecast = _forecast_cost(entry)
        actual = sum(Decimal(str(record.cost_usd)) for record in records if record.model_id == model)
        forecast_total += forecast
        actual_total += actual
        ratio = None if forecast == 0 else actual / forecast
        lines.append(
            f"| {model} | ${forecast:.6f} | ${actual:.6f} | {_number(float(ratio), digits=3)} |"
        )
    total_ratio = None if forecast_total == 0 else actual_total / forecast_total
    lines.append(
        f"| **Total** | **${forecast_total:.6f}** | **${actual_total:.6f}** | "
        f"**{_number(float(total_ratio), digits=3)}** |"
    )
    if actual_total != Decimal(str(manifest.total_cost_usd)):
        raise ValueError("manifest total cost does not reconcile to its raw records")
    return lines


def _latency_section(records: list[ResponseRecord], models: list[str]) -> list[str]:
    lines = [
        "",
        "## 7. Latency, error, and rate-limit observations",
        "",
        "Latency includes each completed client call. Error rates include transport, accounting, and "
        "contentless-completion errors; provider retryable HTTP statuses are retried up to three times.",
        "",
        "| Model | Mean latency (ms) | P95 latency (ms) | Error rate | 429/rate-limit errors |",
        "|---|---:|---:|---:|---:|",
    ]
    for model in models:
        model_records = [record for record in records if record.model_id == model]
        latencies = [record.latency_ms for record in model_records]
        rate_limited = sum(
            "HTTP 429" in (record.error or "") or "rate limit" in (record.error or "").lower()
            for record in model_records
        )
        lines.append(
            f"| {model} | {_number(_mean(latencies), digits=0)} | {_percentile(latencies, 0.95)} | "
            f"{_percent(_count(model_records, Outcome.ERROR), len(model_records))} | {rate_limited} |"
        )
    return lines


def _recommendation(
    records: list[ResponseRecord], models: list[str], item_lookup: Mapping[str, Item]
) -> list[str]:
    parse_rates = {
        model: _count([record for record in records if record.model_id == model], Outcome.ANSWERED)
        / PILOT_CALLS_PER_MODEL
        for model in models
    }
    failing = [model for model, rate in parse_rates.items() if rate < 0.95]
    unexpected = _count(records, Outcome.ERROR)
    if failing:
        recommendation = (
            "Do not scale this panel to Phase 2 unchanged. Repair or replace the low-parse models, "
            "then rerun this pilot before choosing the main battery."
        )
    else:
        recommendation = (
            "The pilot clears the parse-rate threshold. Review the position, framing, and fragility "
            "magnitudes above before selecting the Phase 2 scoring design."
        )
    surprises = []
    if failing:
        surprises.append("below-95% parse: " + ", ".join(failing))
    if unexpected:
        surprises.append(f"{unexpected} explicit error records")
    if not surprises:
        surprises.append("no parse or transport anomaly crossed the pre-specified trigger")
    return [
        "",
        "## Recommendation and surprises",
        "",
        recommendation,
        "",
        "**Surprises to review:** " + "; ".join(surprises) + ".",
        "",
        "Gate 1 remains a Sunay decision. This report deliberately does not advance the project to "
        "Phase 2 on its own.",
    ]


def _panel_models(panel: Mapping[str, object]) -> dict[str, Mapping[str, object]]:
    raw_models = panel.get("models")
    if not isinstance(raw_models, list):
        raise ValueError("pilot panel has no models list")
    models: dict[str, Mapping[str, object]] = {}
    for entry in raw_models:
        if not isinstance(entry, Mapping) or not isinstance(entry.get("id"), str):
            raise ValueError("pilot panel has an invalid model entry")
        models[entry["id"]] = entry
    return models


def _forecast_cost(entry: Mapping[str, object]) -> Decimal:
    pricing = entry.get("pricing_per_million_tokens")
    max_tokens = entry.get("max_tokens", 8)
    if (
        not isinstance(pricing, Mapping)
        or isinstance(max_tokens, bool)
        or not isinstance(max_tokens, int)
    ):
        raise ValueError("pilot panel lacks valid pricing or max_tokens")
    try:
        input_price = Decimal(str(pricing["input_usd"]))
        output_price = Decimal(str(pricing["output_usd"]))
    except (KeyError, ArithmeticError) as error:
        raise ValueError("pilot panel has invalid per-million pricing") from error
    return Decimal(PILOT_CALLS_PER_MODEL) * (
        Decimal(180) * input_price + Decimal(max_tokens) * output_price
    ) / Decimal(1_000_000)


def _group_records(
    records: Iterable[ResponseRecord], key: Callable[[ResponseRecord], str]
) -> dict[str, list[ResponseRecord]]:
    groups: dict[str, list[ResponseRecord]] = defaultdict(list)
    for record in records:
        groups[key(record)].append(record)
    return groups


def _count(records: Iterable[ResponseRecord], outcome: Outcome) -> int:
    return sum(record.outcome is outcome for record in records)


def _mean(values: Iterable[float | int]) -> float | None:
    values = list(values)
    return statistics.mean(values) if values else None


def _percent(numerator: int, denominator: int) -> str:
    return "—" if denominator == 0 else f"{numerator / denominator:.1%}"


def _number(value: float | None, *, digits: int = 2) -> str:
    return "—" if value is None else f"{value:.{digits}f}"


def _percentile(values: list[int], quantile: float) -> str:
    if not values:
        return "—"
    ordered = sorted(values)
    index = round((len(ordered) - 1) * quantile)
    return str(ordered[index])


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
