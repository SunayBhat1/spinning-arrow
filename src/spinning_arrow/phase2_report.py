"""Score a complete Phase 2 run and render durable Markdown, data, and HTML artifacts."""

# ruff: noqa: E501 -- report prose, HTML, and tables are intentionally literal.

from __future__ import annotations

import argparse
import base64
import csv
import html
import io
import json
import os
import random
import statistics
import tempfile
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass, replace
from decimal import Decimal
from pathlib import Path

import matplotlib

_MPL_CONFIG = Path(tempfile.gettempdir()) / "spinning-arrow-matplotlib"
_MPL_CONFIG.mkdir(exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_MPL_CONFIG))
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402 -- backend/cache configuration must precede pyplot.

from spinning_arrow.contracts import Outcome, ResponseRecord, RunManifest  # noqa: E402
from spinning_arrow.items import Item, load_items  # noqa: E402
from spinning_arrow.phase2 import PHASE2_ITEM_FILENAMES  # noqa: E402
from spinning_arrow.report import _load_manifest, _load_records  # noqa: E402

EXPECTED_CALLS_PER_MODEL = 6300
BOOTSTRAP_REPLICATES = 2000
SUPPRESSION_THRESHOLD = 0.70
IPIP_REFERENCE = {
    "source": "IPIP Chinese IPIP-120 norms (n=131 convenience sample)",
    "url": "https://ipip.ori.org/ChineseIPIP-120norms.htm",
    "n": 131,
    "means": {
        "ipip.neuroticism": 71.77 / 24,
        "ipip.extraversion": 73.56 / 24,
        "ipip.openness": 84.61 / 24,
        "ipip.agreeableness": 83.90 / 24,
        "ipip.conscientiousness": 80.26 / 24,
    },
    "sds": {
        "ipip.neuroticism": 15.50 / 24,
        "ipip.extraversion": 12.36 / 24,
        "ipip.openness": 11.03 / 24,
        "ipip.agreeableness": 10.82 / 24,
        "ipip.conscientiousness": 15.78 / 24,
    },
}


@dataclass(frozen=True)
class CellScore:
    model_id: str
    instrument: str
    scale: str
    item_id: str
    condition: str
    framing: str
    score_type: str
    expected_n: int
    valid_n: int
    coverage: float
    score: float | None
    raw_value_mean: float | None
    score_observations: tuple[float, ...]
    correct_n: int | None
    raw_fragility: float | None
    fragility: float | None
    refusal_n: int
    error_n: int


@dataclass(frozen=True)
class ScaleScore:
    model_id: str
    instrument: str
    scale: str
    condition: str
    framing: str
    score_type: str
    eligible_items: int
    suppressed_items: int
    total_items: int
    score: float | None
    ci_low: float | None
    ci_high: float | None
    mean_raw_fragility: float | None
    mean_fragility: float | None
    mean_coverage: float
    refusal_rate: float
    error_rate: float


@dataclass(frozen=True)
class EffectScore:
    model_id: str
    instrument: str
    scale: str
    effect: str
    pairs: int
    difference: float | None
    ci_low: float | None
    ci_high: float | None


@dataclass(frozen=True)
class Phase2Report:
    markdown_path: Path
    html_path: Path
    data_directory: Path
    run_id: str


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Score and render a complete Phase 2 battery.")
    parser.add_argument("run_id")
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args(argv)
    try:
        artifact = generate_phase2_report(Path(args.project_root), args.run_id)
    except (OSError, ValueError) as error:
        print(f"Phase 2 report was not generated: {error}")
        return 2
    print(f"Phase 2 Markdown report: {artifact.markdown_path}")
    print(f"Phase 2 HTML report: {artifact.html_path}")
    print(f"Phase 2 derived data: {artifact.data_directory}")
    return 0


def generate_phase2_report(project_root: Path, run_id: str) -> Phase2Report:
    root = project_root.resolve()
    manifest = _load_manifest(root / "data" / "manifests" / f"{run_id}.json")
    if manifest.run_id != run_id:
        raise ValueError("manifest run ID does not match the requested run ID")
    records = _load_records(root / "data" / "raw" / run_id, run_id)
    items = load_items([root / "instruments" / filename for filename in PHASE2_ITEM_FILENAMES])
    _validate_complete_run(manifest, records, items)
    item_lookup = {item.id: item for item in items}
    cells = _cell_scores(records, item_lookup)
    scales = [*_scale_scores(cells), *_ipip_domain_scores(cells)]
    effects = _effect_scores(cells)
    overview = _model_overview(records, cells, item_lookup, manifest)
    data_directory = root / "data" / "derived" / run_id
    data_directory.mkdir(parents=True, exist_ok=False)
    _write_csv(data_directory / "cell_scores.csv", [asdict(cell) for cell in cells])
    _write_csv(data_directory / "scale_scores.csv", [asdict(score) for score in scales])
    _write_csv(data_directory / "effects.csv", [asdict(effect) for effect in effects])
    _write_csv(data_directory / "model_overview.csv", overview)
    summary = {
        "run_id": run_id,
        "records": len(records),
        "models": list(manifest.model_ids),
        "total_cost_usd": manifest.total_cost_usd,
        "suppression_threshold": SUPPRESSION_THRESHOLD,
        "bootstrap_replicates": BOOTSTRAP_REPLICATES,
        "ipip_reference": IPIP_REFERENCE,
        "outcome_counts": manifest.outcome_counts,
    }
    _write_json(data_directory / "summary.json", summary)
    markdown = _markdown_report(manifest, records, overview, scales, effects, data_directory, root)
    markdown_path = root / "reports" / "02_scoring.md"
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(markdown, encoding="utf-8")
    html_path = root / "reports" / "02_scoring.html"
    html_path.write_text(
        _html_report(manifest, records, overview, scales, effects, data_directory, root), encoding="utf-8"
    )
    return Phase2Report(markdown_path, html_path, data_directory, run_id)


def _validate_complete_run(
    manifest: RunManifest, records: Sequence[ResponseRecord], items: Sequence[Item]
) -> None:
    expected_models = set(manifest.model_ids)
    if len(manifest.model_ids) != 21:
        raise ValueError("Phase 2 launch manifest must list exactly 21 models")
    if len(items) != 315:
        raise ValueError("Phase 2 report requires 315 fixed items")
    by_model = Counter(record.model_id for record in records)
    if set(by_model) != expected_models:
        raise ValueError("raw data model IDs do not match the manifest")
    incomplete = {
        model: count for model, count in by_model.items() if count != EXPECTED_CALLS_PER_MODEL
    }
    if incomplete:
        detail = ", ".join(f"{model}={count}" for model, count in sorted(incomplete.items()))
        raise ValueError(f"Phase 2 is incomplete; expected 6300 records per model: {detail}")
    if len(records) != EXPECTED_CALLS_PER_MODEL * len(manifest.model_ids):
        raise ValueError("raw record count is inconsistent with the Phase 2 panel")
    if any(record.tokens.reasoning_tokens for record in records):
        raise ValueError("main-battery raw records contain billed reasoning tokens")
    actual_cost = sum((Decimal(str(record.cost_usd)) for record in records), start=Decimal("0"))
    if abs(actual_cost - Decimal(str(manifest.total_cost_usd))) > Decimal("0.00000001"):
        raise ValueError("manifest total cost does not reconcile to raw records")


def _cell_scores(
    records: Iterable[ResponseRecord], item_lookup: Mapping[str, Item]
) -> list[CellScore]:
    grouped: dict[tuple[str, str, str, str], list[ResponseRecord]] = defaultdict(list)
    for record in records:
        grouped[(record.model_id, record.item_id, record.condition, record.framing)].append(record)
    cells: list[CellScore] = []
    for key, group in sorted(grouped.items()):
        model_id, item_id, condition, framing = key
        item = item_lookup[item_id]
        valid = [record for record in group if record.outcome is Outcome.ANSWERED]
        values = [_value(item, record) for record in valid]
        expected_n = len(group)
        valid_n = len(valid)
        coverage = valid_n / expected_n if expected_n else 0.0
        raw_value_mean = _mean(values)
        correct_n = (
            sum(record.parsed.choice == item.answer_key for record in valid)
            if item.answer_key is not None
            else None
        )
        score_observations = (
            tuple(values)
            if item.score_type == "value"
            else tuple(float(record.parsed.choice == item.answer_key) for record in valid)
        )
        if coverage >= SUPPRESSION_THRESHOLD and valid_n:
            score = _mean(score_observations)
        else:
            score = None
        cells.append(
            CellScore(
                model_id=model_id,
                instrument=item.instrument,
                scale=item.scale,
                item_id=item_id,
                condition=condition,
                framing=framing,
                score_type=item.score_type,
                expected_n=expected_n,
                valid_n=valid_n,
                coverage=coverage,
                score=score,
                raw_value_mean=raw_value_mean,
                score_observations=score_observations,
                correct_n=correct_n,
                raw_fragility=None,
                fragility=None,
                refusal_n=sum(record.outcome is Outcome.REFUSED for record in group),
                error_n=sum(record.outcome is Outcome.ERROR for record in group),
            )
        )
    by_item_condition: dict[tuple[str, str, str], list[CellScore]] = defaultdict(list)
    for cell in cells:
        by_item_condition[(cell.model_id, cell.item_id, cell.condition)].append(cell)
    fragilities: dict[tuple[str, str, str], tuple[float | None, float | None]] = {}
    for key, group in by_item_condition.items():
        item = item_lookup[key[1]]
        observations = [value for cell in group for value in cell.score_observations]
        scale_range = (
            max(option.value for option in item.options) - min(option.value for option in item.options)
            if item.score_type == "value"
            else 1.0
        )
        raw_fragility = statistics.pstdev(observations) if len(observations) >= 2 else None
        normalized = raw_fragility / scale_range if raw_fragility is not None and scale_range else None
        fragilities[key] = raw_fragility, normalized
    return [
        replace(
            cell,
            raw_fragility=fragilities[(cell.model_id, cell.item_id, cell.condition)][0],
            fragility=fragilities[(cell.model_id, cell.item_id, cell.condition)][1],
        )
        for cell in cells
    ]


def _scale_scores(cells: Iterable[CellScore]) -> list[ScaleScore]:
    grouped: dict[tuple[str, str, str, str, str, str], list[CellScore]] = defaultdict(list)
    for cell in cells:
        grouped[
            (
                cell.model_id,
                cell.instrument,
                cell.scale,
                cell.condition,
                cell.framing,
                cell.score_type,
            )
        ].append(cell)
    scores: list[ScaleScore] = []
    for key, group in sorted(grouped.items()):
        model_id, instrument, scale, condition, framing, score_type = key
        eligible = [cell for cell in group if cell.score is not None]
        values = [cell.score for cell in eligible if cell.score is not None]
        ci_low, ci_high = _bootstrap_ci_cells(eligible, _seed_for(key))
        all_records = sum(cell.expected_n for cell in group)
        scores.append(
            ScaleScore(
                model_id=model_id,
                instrument=instrument,
                scale=scale,
                condition=condition,
                framing=framing,
                score_type=score_type,
                eligible_items=len(eligible),
                suppressed_items=len(group) - len(eligible),
                total_items=len(group),
                score=_mean(values),
                ci_low=ci_low,
                ci_high=ci_high,
                mean_raw_fragility=_mean(
                    cell.raw_fragility for cell in eligible if cell.raw_fragility is not None
                ),
                mean_fragility=_mean(
                    cell.fragility for cell in eligible if cell.fragility is not None
                ),
                mean_coverage=_mean(cell.coverage for cell in group) or 0.0,
                refusal_rate=(sum(cell.refusal_n for cell in group) / all_records if all_records else 0.0),
                error_rate=(sum(cell.error_n for cell in group) / all_records if all_records else 0.0),
            )
        )
    return scores


def _ipip_domain_scores(cells: Iterable[CellScore]) -> list[ScaleScore]:
    """Roll the 30 four-item IPIP facets into the five 24-item domain means."""

    grouped: dict[tuple[str, str, str, str], list[CellScore]] = defaultdict(list)
    for cell in cells:
        if cell.instrument != "ipip_neo_120":
            continue
        parts = cell.scale.split(".")
        if len(parts) != 3:
            raise ValueError(f"unexpected IPIP scale identifier: {cell.scale}")
        grouped[(cell.model_id, parts[1], cell.condition, cell.framing)].append(cell)
    domains: list[ScaleScore] = []
    for (model_id, domain, condition, framing), group in sorted(grouped.items()):
        eligible = [cell for cell in group if cell.score is not None]
        values = [cell.score for cell in eligible if cell.score is not None]
        ci_low, ci_high = _bootstrap_ci_cells(
            eligible, _seed_for((model_id, domain, condition, framing))
        )
        all_records = sum(cell.expected_n for cell in group)
        domains.append(
            ScaleScore(
                model_id=model_id,
                instrument="ipip_neo_120",
                scale=f"ipip.{domain}",
                condition=condition,
                framing=framing,
                score_type="value",
                eligible_items=len(eligible),
                suppressed_items=len(group) - len(eligible),
                total_items=len(group),
                score=_mean(values),
                ci_low=ci_low,
                ci_high=ci_high,
                mean_raw_fragility=_mean(
                    cell.raw_fragility for cell in eligible if cell.raw_fragility is not None
                ),
                mean_fragility=_mean(
                    cell.fragility for cell in eligible if cell.fragility is not None
                ),
                mean_coverage=_mean(cell.coverage for cell in group) or 0.0,
                refusal_rate=(sum(cell.refusal_n for cell in group) / all_records if all_records else 0.0),
                error_rate=(sum(cell.error_n for cell in group) / all_records if all_records else 0.0),
            )
        )
    return domains


def _effect_scores(cells: Iterable[CellScore]) -> list[EffectScore]:
    index = {
        (cell.model_id, cell.item_id, cell.condition, cell.framing): cell
        for cell in cells
        if cell.score is not None
    }
    grouped: dict[tuple[str, str, str], dict[str, list[float]]] = defaultdict(
        lambda: {"evaluator_minus_bare": [], "first_minus_third": []}
    )
    for cell in index.values():
        group_key = (cell.model_id, cell.instrument, cell.scale)
        if cell.condition == "evaluator":
            other = index.get((cell.model_id, cell.item_id, "bare", cell.framing))
            if other is not None:
                assert cell.score is not None and other.score is not None
                grouped[group_key]["evaluator_minus_bare"].append(cell.score - other.score)
        if cell.framing == "first_person":
            other = index.get((cell.model_id, cell.item_id, cell.condition, "third_person"))
            if other is not None:
                assert cell.score is not None and other.score is not None
                grouped[group_key]["first_minus_third"].append(cell.score - other.score)
    effects: list[EffectScore] = []
    for (model_id, instrument, scale), by_effect in sorted(grouped.items()):
        for effect, values in by_effect.items():
            ci_low, ci_high = _bootstrap_ci(values, _seed_for((model_id, scale, effect)))
            effects.append(
                EffectScore(
                    model_id=model_id,
                    instrument=instrument,
                    scale=scale,
                    effect=effect,
                    pairs=len(values),
                    difference=_mean(values),
                    ci_low=ci_low,
                    ci_high=ci_high,
                )
            )
    return effects


def _model_overview(
    records: Iterable[ResponseRecord],
    cells: Iterable[CellScore],
    item_lookup: Mapping[str, Item],
    manifest: RunManifest,
) -> list[dict[str, object]]:
    by_model: dict[str, list[ResponseRecord]] = defaultdict(list)
    for record in records:
        by_model[record.model_id].append(record)
    by_model_cells: dict[str, list[CellScore]] = defaultdict(list)
    for cell in cells:
        by_model_cells[cell.model_id].append(cell)
    overview: list[dict[str, object]] = []
    for model_id in manifest.model_ids:
        group = by_model[model_id]
        attention = [record for record in group if item_lookup[record.item_id].score_type == "attention"]
        attention_correct = sum(
            record.outcome is Outcome.ANSWERED
            and record.parsed.choice == item_lookup[record.item_id].answer_key
            for record in attention
        )
        overview.append(
            {
                "model_id": model_id,
                "records": len(group),
                "answered": sum(record.outcome is Outcome.ANSWERED for record in group),
                "parse_rate": sum(record.outcome is Outcome.ANSWERED for record in group) / len(group),
                "refusal_rate": sum(record.outcome is Outcome.REFUSED for record in group) / len(group),
                "hedged_rate": sum(record.outcome is Outcome.HEDGED for record in group) / len(group),
                "unparseable_rate": sum(
                    record.outcome is Outcome.UNPARSEABLE for record in group
                )
                / len(group),
                "error_rate": sum(record.outcome is Outcome.ERROR for record in group) / len(group),
                "attention_accuracy": attention_correct / len(attention),
                "mean_raw_fragility": _mean(
                    cell.raw_fragility
                    for cell in by_model_cells[model_id]
                    if cell.raw_fragility is not None
                ),
                "mean_fragility": _mean(
                    cell.fragility
                    for cell in by_model_cells[model_id]
                    if cell.fragility is not None
                ),
                "suppressed_cells": sum(
                    cell.score is None for cell in by_model_cells[model_id]
                ),
                "cost_usd": sum(record.cost_usd for record in group),
                "mean_latency_ms": _mean(record.latency_ms for record in group),
            }
        )
    return overview


def _markdown_report(
    manifest: RunManifest,
    records: Sequence[ResponseRecord],
    overview: Sequence[Mapping[str, object]],
    scales: Sequence[ScaleScore],
    effects: Sequence[EffectScore],
    data_directory: Path,
    root: Path,
) -> str:
    quality_rows = [
        "| Model | Parse | Attention | Refusal | Hedge | Unparseable | Error | Mean fragility | Suppressed cells | Cost |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in overview:
        quality_rows.append(
            "| {model_id} | {parse_rate:.1%} | {attention_accuracy:.1%} | "
            "{refusal_rate:.1%} | {hedged_rate:.1%} | {unparseable_rate:.1%} | {error_rate:.1%} | "
            "{fragility} | {suppressed_cells} | ${cost:.4f} |".format(
                model_id=row["model_id"],
                parse_rate=float(row["parse_rate"]),
                attention_accuracy=float(row["attention_accuracy"]),
                refusal_rate=float(row["refusal_rate"]),
                hedged_rate=float(row["hedged_rate"]),
                unparseable_rate=float(row["unparseable_rate"]),
                error_rate=float(row["error_rate"]),
                fragility=_decimal_or_dash(row["mean_fragility"]),
                suppressed_cells=row["suppressed_cells"],
                cost=float(row["cost_usd"]),
            )
        )
    ggb_rows = _selected_scale_table(scales, "ous_ggb", condition="bare", framing="first_person")
    ethics_rows = _selected_scale_table(
        scales, "ethics_phase2", condition="bare", framing="first_person"
    )
    effect_rows = _effect_table(effects)
    fragility_rows = _fragility_table(scales)
    outcome_rows = _outcome_by_instrument_table(records, manifest.model_ids)
    suppression_rows = _suppression_table(scales)
    ggb_check = _ggb_replication_note(scales, manifest.model_ids)
    raw_path = f"data/raw/{manifest.run_id}/"
    manifest_path = f"data/manifests/{manifest.run_id}.json"
    derived_path = data_directory.relative_to(root)
    return "\n".join(
        [
            "# Phase 2 main-battery report",
            "",
            f"**Run:** `{manifest.run_id}`  ",
            f"**Window:** {manifest.started_at} to {manifest.ended_at}  ",
            f"**Commit:** `{manifest.git_commit}`  ",
            f"**Raw data:** `{raw_path}`  ",
            f"**Manifest:** `{manifest_path}`  ",
            f"**Derived data:** `{derived_path}/`  ",
            "",
            "## Decision-ready result",
            "",
            "Phase 2 is complete and mechanically reproducible. Gate 2 remains pending user review; "
            "this report does not advance the project to Phase 3. Each score averages valid option "
            "permutations within an item/condition/framing cell. Cells below 70% valid coverage are "
            "suppressed; scale intervals use 2,000 deterministic item-and-permutation bootstraps.",
            "",
            "## Run integrity and response quality",
            "",
            f"**Records:** {len(records):,} (6,300 per model)  ",
            f"**OpenRouter-recorded cost:** ${manifest.total_cost_usd:.6f}  ",
            "**Reasoning tokens in main battery:** 0 (hard requirement)",
            "",
            *quality_rows,
            "",
            "### Outcome classes by instrument",
            "",
            *outcome_rows,
            "",
            "## Fragility (bare, first-person)",
            "",
            "Fragility is the within-item SD across both framings and five option permutations, "
            "then averaged over eligible items. Raw and range-normalized values are both shown.",
            "",
            *fragility_rows,
            "",
            "## Suppression list",
            "",
            "Any listed score has at least one item/condition/framing cell below 70% valid coverage "
            "and is excluded from that aggregate. Unlisted aggregates had no suppressed item cells.",
            "",
            *suppression_rows,
            "",
            "## GGB validation (bare, first-person)",
            "",
            "Higher impartial-beneficence agreement and lower instrumental-harm agreement are the "
            "pre-specified directional sanity check. Values are 1–5 agreement means with 95% bootstrap "
            "intervals; they are descriptive model outputs, not evidence of moral competence.",
            "",
            ggb_check,
            "",
            *ggb_rows,
            "",
            "## ETHICS reference agreement (bare, first-person)",
            "",
            "Each cell is exact agreement with the public ETHICS test label. The score is not a broad "
            "ethical-validity claim and should be interpreted alongside the raw prompts and framing effects.",
            "",
            *ethics_rows,
            "",
            "## Design sensitivity",
            "",
            "Effects are paired at item level after the coverage rule. `evaluator − bare` holds framing "
            "constant; `first − third` holds condition constant. Positive values mean the named first term "
            "was higher on the item’s native score scale.",
            "",
            *effect_rows,
            "",
            "## Big Five comparison caveat",
            "",
            "The HTML artifact compares bare first-person IPIP means with the only readily published "
            "IPIP-120 external norm table used here: a Chinese convenience sample (n=131). It is an "
            "illustrative reference, not a representative human population benchmark and not a basis for "
            "ranking models as people. Source: "
            "https://ipip.ori.org/ChineseIPIP-120norms.htm.",
            "",
            "## Artifacts",
            "",
            "- `reports/02_scoring.html` — self-contained visual dashboard with embedded plots.",
            "- `data/derived/<run-id>/cell_scores.csv` — score/coverage/fragility for every analytical cell.",
            "- `data/derived/<run-id>/scale_scores.csv` and `effects.csv` — publication-facing aggregates.",
            "- `data/derived/<run-id>/summary.json` — run-level machine-readable summary.",
            "",
            "Gate 2 remains a Sunay decision.",
            "",
        ]
    )


def _html_report(
    manifest: RunManifest,
    records: Sequence[ResponseRecord],
    overview: Sequence[Mapping[str, object]],
    scales: Sequence[ScaleScore],
    effects: Sequence[EffectScore],
    data_directory: Path,
    root: Path,
) -> str:
    images = {
        "quality": _quality_plot(overview),
        "bigfive": _bigfive_plot(scales, manifest.model_ids),
        "ggb": _ggb_ethics_plot(scales, manifest.model_ids),
        "effects": _effects_plot(effects, manifest.model_ids),
    }
    overview_table = _html_table(
        [
            "Model",
            "Parse",
            "Attention",
            "Refusal",
            "Hedge",
            "Unparseable",
            "Error",
            "Fragility",
            "Suppressed",
            "Cost",
        ],
        [
            [
                row["model_id"],
                _percent(row["parse_rate"]),
                _percent(row["attention_accuracy"]),
                _percent(row["refusal_rate"]),
                _percent(row["hedged_rate"]),
                _percent(row["unparseable_rate"]),
                _percent(row["error_rate"]),
                _decimal_or_dash(row["mean_fragility"]),
                str(row["suppressed_cells"]),
                f"${float(row['cost_usd']):.4f}",
            ]
            for row in overview
        ],
    )
    ggb_table = _html_scale_table(scales, "ous_ggb")
    ethics_table = _html_scale_table(scales, "ethics_phase2")
    effects_table = _html_effect_table(effects)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Spinning Arrow — Phase 2 report</title>
<style>
:root {{ color-scheme: light; --ink:#172033; --muted:#536075; --line:#d9dfeb; --panel:#fff; --wash:#f5f7fb; --accent:#4b5fc0; --good:#18794e; }}
* {{ box-sizing:border-box; }} body {{ margin:0; font:15px/1.55 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; color:var(--ink); background:var(--wash); }}
main {{ max-width:1440px; margin:auto; padding:34px 26px 54px; }}
h1 {{ letter-spacing:-.035em; font-size:34px; line-height:1.1; margin:0 0 8px; }} h2 {{ font-size:21px; margin:34px 0 12px; }} h3 {{ font-size:16px; margin:0 0 8px; }}
.subtitle,.muted {{ color:var(--muted); }} .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(210px,1fr)); gap:13px; margin:22px 0; }}
.card,.section {{ background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:18px; box-shadow:0 1px 1px #17203308; }} .metric {{ font-size:26px; font-weight:750; letter-spacing:-.03em; }}
.notice {{ border-left:4px solid var(--accent); background:#eef1ff; padding:14px 16px; border-radius:0 8px 8px 0; }} .good {{ color:var(--good); }}
.plot {{ background:var(--panel); border:1px solid var(--line); border-radius:12px; padding:10px; margin:16px 0 24px; }} .plot img {{ display:block; width:100%; height:auto; }}
.table-wrap {{ overflow:auto; background:var(--panel); border:1px solid var(--line); border-radius:12px; }} table {{ border-collapse:collapse; width:100%; min-width:850px; font-size:13px; }} th {{ background:#f1f4f9; text-align:left; }} th,td {{ padding:8px 10px; border-bottom:1px solid var(--line); white-space:nowrap; }} tr:last-child td {{ border-bottom:0; }}
details {{ background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:12px 16px; margin:12px 0; }} summary {{ cursor:pointer; font-weight:650; }} a {{ color:#354aac; }} code {{ font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:.92em; }}
@media (max-width:650px) {{ main {{ padding:22px 14px 36px; }} h1 {{ font-size:28px; }} }}
</style>
</head>
<body><main>
  <p class="muted">SPINNING ARROW / PHASE 2 / COMPLETE RUN</p>
  <h1>Cross-model survey robustness report</h1>
  <p class="subtitle">Run <code>{html.escape(manifest.run_id)}</code> · {html.escape(manifest.started_at)} to {html.escape(manifest.ended_at)} · commit <code>{html.escape(manifest.git_commit[:12])}</code></p>
  <div class="notice"><strong>Gate 2 is still pending review.</strong> The run is complete and auditable; this artifact does not advance the project to Phase 3.</div>
  <div class="grid">
    <div class="card"><h3>Calls</h3><div class="metric">{len(records):,}</div><span class="muted">6,300 per model</span></div>
    <div class="card"><h3>Recorded cost</h3><div class="metric">${manifest.total_cost_usd:.2f}</div><span class="muted">OpenRouter usage.cost reconciliation</span></div>
    <div class="card"><h3>Main-path reasoning</h3><div class="metric good">0</div><span class="muted">billed reasoning tokens</span></div>
    <div class="card"><h3>Scoring rule</h3><div class="metric">≥70%</div><span class="muted">valid permutation coverage</span></div>
  </div>
  <h2>Response quality</h2><p class="muted">Attention accuracy treats malformed, refused, and incorrect responses as failures. Fragility uses both framings and option permutations, normalized by each item’s response range.</p>
  <div class="plot"><img alt="Response quality across models" src="{images['quality']}"></div>
  {overview_table}
  <h2>Big Five: descriptive first-person comparison</h2><p class="muted">Bare first-person IPIP means. The reference row is an illustrative Chinese IPIP-120 convenience sample (n=131), not a representative human benchmark.</p>
  <div class="plot"><img alt="Big Five heatmap" src="{images['bigfive']}"></div>
  <h2>Moral task outputs</h2><p class="muted">GGB values are 1–5 agreement means; ETHICS values are exact agreement with published labels. Both panels use bare, first-person responses.</p>
  <div class="plot"><img alt="GGB and ETHICS heatmaps" src="{images['ggb']}"></div>
  <h3>GGB validation table</h3>{ggb_table}
  <h3>ETHICS reference agreement table</h3>{ethics_table}
  <h2>Condition and framing sensitivity</h2><p class="muted">Paired item-level differences; intervals use 2,000 deterministic bootstrap replicates. Positive values are in the direction named on the chart.</p>
  <div class="plot"><img alt="Design sensitivity chart" src="{images['effects']}"></div>
  {effects_table}
  <details><summary>Methods and provenance</summary>
    <p>Scores first average valid permutations for each model × item × condition × framing cell. A cell with less than 70% valid answers is suppressed. Scale scores average eligible item cells, and their 95% intervals resample eligible items and their valid response permutations 2,000 times with a deterministic seed. Raw records retain prompt hashes, displayed option order, responses, parsed canonical answer, provider, usage, cost, and latency.</p>
    <p>Fixed bank: 120 IPIP-NEO items, 36 MFQ-2, 24 GGB, 120 ETHICS, and 15 explicit attention checks. See <code>instruments/LICENSES.md</code> and <code>instruments/PHASE2_SOURCES.json</code>. External IPIP reference: <a href="https://ipip.ori.org/ChineseIPIP-120norms.htm">IPIP Chinese IPIP-120 norms</a>.</p>
    <p>Derived tables: <code>{html.escape(str(data_directory.relative_to(root)))}/</code>. Raw: <code>data/raw/{html.escape(manifest.run_id)}/</code>. Manifest: <code>data/manifests/{html.escape(manifest.run_id)}.json</code>.</p>
  </details>
</main></body></html>"""


def _quality_plot(overview: Sequence[Mapping[str, object]]) -> str:
    labels = [_short_model(str(row["model_id"])) for row in overview]
    parse = [float(row["parse_rate"]) * 100 for row in overview]
    attention = [float(row["attention_accuracy"]) * 100 for row in overview]
    figure, axis = plt.subplots(figsize=(11.5, 5.1))
    position = list(range(len(labels)))
    axis.barh([value + 0.18 for value in position], parse, height=0.34, label="Clean parse", color="#4b5fc0")
    axis.barh([value - 0.18 for value in position], attention, height=0.34, label="Attention accuracy", color="#29a36a")
    axis.set(yticks=position, yticklabels=labels, xlim=(0, 101), xlabel="Percent", title="Response quality")
    axis.axvline(95, color="#9aa5b7", linestyle="--", linewidth=1)
    axis.legend(loc="lower right", ncols=2)
    figure.tight_layout()
    return _figure_data_uri(figure)


def _bigfive_plot(scales: Sequence[ScaleScore], models: Sequence[str]) -> str:
    columns = [
        "ipip.neuroticism",
        "ipip.extraversion",
        "ipip.openness",
        "ipip.agreeableness",
        "ipip.conscientiousness",
    ]
    lookup = _scale_lookup(scales, condition="bare", framing="first_person")
    rows = list(models) + ["human reference"]
    matrix = [
        [
            lookup.get((model, scale)).score if lookup.get((model, scale)) else float("nan")
            for scale in columns
        ]
        for model in models
    ]
    matrix.append([IPIP_REFERENCE["means"][scale] for scale in columns])
    figure, axis = plt.subplots(figsize=(10.8, 6.4))
    image = axis.imshow(matrix, cmap="YlGnBu", vmin=1, vmax=5, aspect="auto")
    axis.set(
        xticks=range(len(columns)),
        xticklabels=[column.split(".")[-1].title() for column in columns],
        yticks=range(len(rows)),
        yticklabels=[_short_model(row) for row in rows[:-1]] + ["Human ref.*"],
        title="IPIP-NEO-120 bare first-person mean (1–5)",
    )
    for row, values in enumerate(matrix):
        for column, value in enumerate(values):
            if value == value:
                axis.text(column, row, f"{value:.2f}", ha="center", va="center", fontsize=8)
    figure.colorbar(image, ax=axis, label="Mean item score")
    axis.text(
        0,
        -0.17,
        "* Illustrative Chinese convenience-sample norm (n=131), not a representative population benchmark.",
        transform=axis.transAxes,
        fontsize=8,
        color="#536075",
    )
    figure.tight_layout()
    return _figure_data_uri(figure)


def _ggb_ethics_plot(scales: Sequence[ScaleScore], models: Sequence[str]) -> str:
    lookup = _scale_lookup(scales, condition="bare", framing="first_person")
    ggb_columns = ["ggb.impartial_beneficence", "ggb.instrumental_harm"]
    ethics_columns = [
        "ethics.commonsense",
        "ethics.deontology",
        "ethics.justice",
        "ethics.virtue",
        "ethics.utilitarianism",
    ]
    figure, axes = plt.subplots(1, 2, figsize=(14.5, 6.4), gridspec_kw={"width_ratios": [2, 5]})
    for axis, columns, title, minimum, maximum in (
        (axes[0], ggb_columns, "GGB agreement (1–5)", 1, 5),
        (axes[1], ethics_columns, "ETHICS reference agreement", 0, 1),
    ):
        matrix = [
            [
                lookup.get((model, scale)).score if lookup.get((model, scale)) else float("nan")
                for scale in columns
            ]
            for model in models
        ]
        image = axis.imshow(matrix, cmap="YlGnBu", vmin=minimum, vmax=maximum, aspect="auto")
        axis.set(
            xticks=range(len(columns)),
            xticklabels=[column.split(".")[-1].replace("_", " ").title() for column in columns],
            yticks=range(len(models)),
            yticklabels=[_short_model(model) for model in models],
            title=title,
        )
        axis.tick_params(axis="x", labelrotation=30)
        for row, values in enumerate(matrix):
            for column, value in enumerate(values):
                if value == value:
                    axis.text(
                        column,
                        row,
                        f"{value:.2f}",
                        ha="center",
                        va="center",
                        fontsize=8,
                    )
        figure.colorbar(image, ax=axis, fraction=0.046, pad=0.04)
    figure.suptitle("Bare first-person moral-task outputs", fontsize=15, y=1.02)
    figure.tight_layout()
    return _figure_data_uri(figure)


def _effects_plot(effects: Sequence[EffectScore], models: Sequence[str]) -> str:
    selected = [effect for effect in effects if effect.instrument in {"mfq2_phase2", "ous_ggb"}]
    by_model: dict[str, list[EffectScore]] = defaultdict(list)
    for effect in selected:
        by_model[effect.model_id].append(effect)
    figure, axis = plt.subplots(figsize=(11.5, 5.8))
    labels = [_short_model(model) for model in models]
    positions = list(range(len(models)))
    for offset, effect_name, color, marker in (
        (-0.16, "evaluator_minus_bare", "#4b5fc0", "o"),
        (0.16, "first_minus_third", "#d47b2a", "s"),
    ):
        xs: list[float] = []
        ys: list[float] = []
        errors: list[tuple[float, float]] = []
        for position, model in zip(positions, models, strict=True):
            candidates = [
                effect
                for effect in by_model.get(model, [])
                if effect.effect == effect_name and effect.difference is not None
            ]
            if not candidates:
                continue
            value = _mean(effect.difference for effect in candidates if effect.difference is not None)
            assert value is not None
            lower = _mean(effect.ci_low for effect in candidates if effect.ci_low is not None)
            upper = _mean(effect.ci_high for effect in candidates if effect.ci_high is not None)
            xs.append(position + offset)
            ys.append(value)
            errors.append((value - (lower or value), (upper or value) - value))
        if xs:
            axis.errorbar(
                xs,
                ys,
                yerr=[[error[0] for error in errors], [error[1] for error in errors]],
                fmt=marker,
                color=color,
                capsize=3,
                label=effect_name.replace("_", " "),
            )
    axis.axhline(0, color="#8994a8", linewidth=1)
    axis.set(
        xticks=positions,
        xticklabels=labels,
        ylabel="Mean paired score difference",
        title="Average condition and framing sensitivity across MFQ-2 + GGB scales",
    )
    axis.tick_params(axis="x", rotation=22)
    axis.legend()
    figure.tight_layout()
    return _figure_data_uri(figure)


def _scale_lookup(
    scales: Iterable[ScaleScore], *, condition: str, framing: str
) -> dict[tuple[str, str], ScaleScore]:
    return {
        (score.model_id, score.scale): score
        for score in scales
        if score.condition == condition and score.framing == framing
    }


def _selected_scale_table(
    scales: Sequence[ScaleScore], instrument: str, *, condition: str, framing: str
) -> list[str]:
    selected = [
        score
        for score in scales
        if score.instrument == instrument and score.condition == condition and score.framing == framing
    ]
    labels = sorted({score.scale.split(".")[-1].replace("_", " ") for score in selected})
    lines = [
        "| Model | " + " | ".join(label.title() for label in labels) + " |",
        "|---|" + "---:|" * len(labels),
    ]
    for model in sorted({score.model_id for score in selected}):
        lookup = {score.scale.split(".")[-1].replace("_", " "): score for score in selected if score.model_id == model}
        values = []
        for label in labels:
            score = lookup[label]
            values.append(_score_with_ci(score))
        lines.append(f"| {model} | " + " | ".join(values) + " |")
    return lines


def _fragility_table(scales: Sequence[ScaleScore]) -> list[str]:
    selected = [
        score
        for score in scales
        if score.condition == "bare"
        and score.framing == "first_person"
        and not (score.instrument == "ipip_neo_120" and score.scale.count(".") == 2)
    ]
    grouped: dict[tuple[str, str], list[ScaleScore]] = defaultdict(list)
    for score in selected:
        grouped[(score.model_id, score.instrument)].append(score)
    lines = [
        "| Model | Instrument | Raw fragility | Normalized fragility | Suppressed / total items |",
        "|---|---|---:|---:|---:|",
    ]
    for (model_id, instrument), group in sorted(grouped.items()):
        lines.append(
            f"| {model_id} | {instrument} | "
            f"{_decimal_or_dash(_mean(score.mean_raw_fragility for score in group))} | "
            f"{_decimal_or_dash(_mean(score.mean_fragility for score in group))} | "
            f"{sum(score.suppressed_items for score in group)} / "
            f"{sum(score.total_items for score in group)} |"
        )
    return lines


def _suppression_table(scales: Sequence[ScaleScore]) -> list[str]:
    suppressed = [score for score in scales if score.suppressed_items]
    if not suppressed:
        return ["No score aggregates had suppressed item cells."]
    lines = [
        "| Model | Instrument | Scale | Condition | Framing | Suppressed / total | Mean coverage |",
        "|---|---|---|---|---|---:|---:|",
    ]
    for score in suppressed:
        lines.append(
            f"| {score.model_id} | {score.instrument} | {score.scale} | {score.condition} | "
            f"{score.framing} | {score.suppressed_items} / {score.total_items} | "
            f"{score.mean_coverage:.1%} |"
        )
    return lines


def _outcome_by_instrument_table(
    records: Sequence[ResponseRecord], models: Sequence[str]
) -> list[str]:
    grouped: dict[tuple[str, str], list[ResponseRecord]] = defaultdict(list)
    for record in records:
        grouped[(record.model_id, record.instrument)].append(record)
    lines = [
        "| Model | Instrument | Calls | Parse | Refusal | Hedge | Unparseable | Error |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for model in models:
        for instrument in sorted({key[1] for key in grouped if key[0] == model}):
            group = grouped[(model, instrument)]
            total = len(group)
            lines.append(
                f"| {model} | {instrument} | {total} | "
                f"{sum(record.outcome is Outcome.ANSWERED for record in group) / total:.1%} | "
                f"{sum(record.outcome is Outcome.REFUSED for record in group) / total:.1%} | "
                f"{sum(record.outcome is Outcome.HEDGED for record in group) / total:.1%} | "
                f"{sum(record.outcome is Outcome.UNPARSEABLE for record in group) / total:.1%} | "
                f"{sum(record.outcome is Outcome.ERROR for record in group) / total:.1%} |"
            )
    return lines


def _ggb_replication_note(scales: Sequence[ScaleScore], models: Sequence[str]) -> str:
    lookup = _scale_lookup(scales, condition="bare", framing="first_person")
    reproduced: list[str] = []
    nonconforming: list[str] = []
    for model in models:
        ib = lookup.get((model, "ggb.impartial_beneficence"))
        ih = lookup.get((model, "ggb.instrumental_harm"))
        if ib is None or ih is None or ib.score is None or ih.score is None:
            nonconforming.append(f"{model} (suppressed)")
        elif ib.score > 3 and ih.score < 3:
            reproduced.append(model)
        else:
            nonconforming.append(model)
    return (
        "Directional flag uses the neutral midpoint: impartial beneficence > 3 and instrumental "
        "harm < 3. Reproduced: "
        f"{', '.join(reproduced) if reproduced else 'none'}. "
        f"Not reproduced / suppressed: {', '.join(nonconforming) if nonconforming else 'none'}."
    )


def _effect_table(effects: Sequence[EffectScore]) -> list[str]:
    ranked = sorted(
        (effect for effect in effects if effect.difference is not None),
        key=lambda effect: abs(effect.difference or 0),
        reverse=True,
    )[:25]
    lines = [
        "| Model | Scale | Effect | Pairs | Difference [95% CI] |",
        "|---|---|---|---:|---:|",
    ]
    for effect in ranked:
        lines.append(
            f"| {effect.model_id} | {effect.scale} | {effect.effect} | {effect.pairs} | "
            f"{_effect_with_ci(effect)} |"
        )
    return lines


def _html_scale_table(scales: Sequence[ScaleScore], instrument: str) -> str:
    selected = [
        score
        for score in scales
        if score.instrument == instrument
        and score.condition == "bare"
        and score.framing == "first_person"
    ]
    labels = sorted({score.scale.split(".")[-1].replace("_", " ") for score in selected})
    rows: list[list[str]] = []
    for model in sorted({score.model_id for score in selected}):
        lookup = {score.scale.split(".")[-1].replace("_", " "): score for score in selected if score.model_id == model}
        rows.append([model, *[_score_with_ci(lookup[label]) for label in labels]])
    return _html_table(["Model", *[label.title() for label in labels]], rows)


def _html_effect_table(effects: Sequence[EffectScore]) -> str:
    ranked = sorted(
        (effect for effect in effects if effect.difference is not None),
        key=lambda effect: abs(effect.difference or 0),
        reverse=True,
    )[:25]
    return _html_table(
        ["Model", "Scale", "Effect", "Pairs", "Difference [95% CI]"],
        [
            [
                effect.model_id,
                effect.scale,
                effect.effect,
                str(effect.pairs),
                _effect_with_ci(effect),
            ]
            for effect in ranked
        ],
    )


def _html_table(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    head = "".join(f"<th>{html.escape(header)}</th>" for header in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{html.escape(cell)}</td>" for cell in row) + "</tr>" for row in rows
    )
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def _write_csv(path: Path, rows: Sequence[Mapping[str, object]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty derived table {path.name}")
    keys = list(rows[0])
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)


def _write_json(path: Path, document: Mapping[str, object]) -> None:
    path.write_text(json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _value(item: Item, record: ResponseRecord) -> float:
    choice = record.parsed.choice
    assert choice is not None
    return next(option.value for option in item.options if option.id == choice)


def _bootstrap_ci(values: Sequence[float], seed: int) -> tuple[float | None, float | None]:
    if not values:
        return None, None
    if len(values) == 1:
        return values[0], values[0]
    generator = random.Random(seed)
    n = len(values)
    means = sorted(
        sum(generator.choice(values) for _ in range(n)) / n for _ in range(BOOTSTRAP_REPLICATES)
    )
    return _quantile(means, 0.025), _quantile(means, 0.975)


def _bootstrap_ci_cells(cells: Sequence[CellScore], seed: int) -> tuple[float | None, float | None]:
    """Resample item cells and their valid option-permutation observations."""

    if not cells:
        return None, None
    if len(cells) == 1 and len(cells[0].score_observations) == 1:
        value = cells[0].score_observations[0]
        return value, value
    generator = random.Random(seed)
    n = len(cells)
    means: list[float] = []
    for _ in range(BOOTSTRAP_REPLICATES):
        resampled_items = [generator.choice(cells) for _ in range(n)]
        item_means = [
            sum(
                generator.choice(cell.score_observations)
                for _ in range(len(cell.score_observations))
            )
            / len(cell.score_observations)
            for cell in resampled_items
        ]
        means.append(sum(item_means) / n)
    means.sort()
    return _quantile(means, 0.025), _quantile(means, 0.975)


def _quantile(values: Sequence[float], probability: float) -> float:
    if not values:
        raise ValueError("cannot calculate a quantile of no values")
    index = round((len(values) - 1) * probability)
    return values[index]


def _seed_for(value: object) -> int:
    return sum((index + 1) * ord(character) for index, character in enumerate(str(value)))


def _mean(values: Iterable[float | None]) -> float | None:
    populated = [value for value in values if value is not None]
    return statistics.mean(populated) if populated else None


def _figure_data_uri(figure: plt.Figure) -> str:
    output = io.BytesIO()
    figure.savefig(output, format="png", dpi=170, bbox_inches="tight", facecolor="white")
    plt.close(figure)
    return "data:image/png;base64," + base64.b64encode(output.getvalue()).decode("ascii")


def _short_model(model: str) -> str:
    replacements = {
        "openai/gpt-5.4-mini": "GPT-5.4 mini",
        "openai/gpt-5.6-luna": "GPT-5.6 Luna",
        "google/gemini-2.5-flash-lite": "Gemini 2.5 Flash-Lite",
        "google/gemini-2.5-flash": "Gemini 2.5 Flash",
        "anthropic/claude-sonnet-5": "Claude Sonnet 5",
        "x-ai/grok-4.20": "Grok 4.20",
        "meta-llama/llama-3.1-70b-instruct": "Llama 3.1 70B",
        "meta-llama/llama-3.1-8b-instruct": "Llama 3.1 8B",
        "mistralai/mistral-medium-3.1": "Mistral Medium 3.1",
        "mistralai/mistral-small-3.2-24b-instruct": "Mistral Small 3.2",
        "qwen/qwen3.8-27b": "Qwen 3.8 27B",
        "openai/gpt-4o-mini-2024-07-18": "GPT-4o mini",
        "deepseek/deepseek-v4-pro-0813": "DeepSeek V4 Pro",
        "deepseek/deepseek-v4-flash-0731": "DeepSeek V4 Flash",
        "z-ai/glm-5.2": "GLM-5.2",
        "z-ai/glm-4.5-air": "GLM-4.5 Air",
        "google/gemma-3-27b-it": "Gemma 3 27B",
        "nvidia/nemotron-3.5-lightning": "Nemotron 3.5 Lightning",
        "amazon/nova-lite-v1": "Nova Lite 1.0",
        "microsoft/phi-4": "Phi-4",
        "openai/gpt-4.1-mini": "GPT-4.1 mini",
    }
    return replacements.get(model, model)


def _percent(value: object) -> str:
    return f"{float(value):.1%}"


def _decimal_or_dash(value: object) -> str:
    return "—" if value is None else f"{float(value):.3f}"


def _score_with_ci(score: ScaleScore) -> str:
    if score.score is None:
        return "suppressed"
    return f"{score.score:.3f} [{score.ci_low:.3f}, {score.ci_high:.3f}]"


def _effect_with_ci(effect: EffectScore) -> str:
    if effect.difference is None:
        return "—"
    return f"{effect.difference:+.3f} [{effect.ci_low:+.3f}, {effect.ci_high:+.3f}]"
