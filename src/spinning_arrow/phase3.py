"""Run the guarded Phase 3 stated-versus-scenario battery."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any

from spinning_arrow.client import (
    OPENROUTER_CHAT_URL,
    OpenRouterClient,
    OpenRouterClientError,
    RunBudget,
)
from spinning_arrow.contracts import Outcome, RunManifest
from spinning_arrow.items import Item, item_set_hash, load_items
from spinning_arrow.parse import parse_response
from spinning_arrow.phase2 import (
    MODEL_CATALOG_URL,
    Phase2Aborted,
    Phase2Config,
    Phase2Model,
    Phase2PreflightError,
    _execute_tasks,
    _fetch_catalog,
    _iter_tasks,
    _run_id,
)
from spinning_arrow.render import render_item
from spinning_arrow.report import _load_records
from spinning_arrow.run import _git_commit, _hash_file, _utc_now, _write_json
from spinning_arrow.smoke import _load_dotenv

PHASE3_ITEM_FILENAME = "phase3_scenarios.yaml"


@dataclass(frozen=True)
class Phase3Config:
    runtime: Phase2Config
    baseline_run_id: str


@dataclass(frozen=True)
class Phase3Artifacts:
    run_id: str
    raw_directory: Path
    manifest_path: Path
    cost_usd: Decimal


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Spinning Arrow's guarded Phase 3 battery.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--env-file", default=".env")
    parser.add_argument("--workers", type=int, default=12)
    parser.add_argument(
        "--resume-run-id",
        help="resume an interrupted Phase 3 run after validating its durable raw records",
    )
    args = parser.parse_args(argv)
    _load_dotenv(Path(args.env_file))
    try:
        artifacts = run_phase3(
            Path(args.project_root), workers=args.workers, resume_run_id=args.resume_run_id
        )
    except (
        OpenRouterClientError,
        Phase2PreflightError,
        Phase2Aborted,
        RuntimeError,
        ValueError,
    ) as error:
        print(f"Phase 3 did not complete: {error}", file=sys.stderr)
        return 2
    print(f"Phase 3 run ID: {artifacts.run_id}")
    print(f"Raw response directory: {artifacts.raw_directory}")
    print(f"Manifest: {artifacts.manifest_path}")
    print(f"Recorded cost: ${artifacts.cost_usd:.8f}")
    return 0


def run_phase3(
    project_root: Path, *, workers: int = 12, resume_run_id: str | None = None
) -> Phase3Artifacts:
    if workers < 1:
        raise ValueError("workers must be at least one")
    root = project_root.resolve()
    commit = _git_commit(root)
    config = _load_config(root / "panels" / "phase3.yaml")
    items = _phase3_items(root)
    if len(items) != 30:
        raise RuntimeError(f"Phase 3 requires exactly 30 scenarios; found {len(items)}")
    expected_per_model = (
        len(items)
        * len(config.runtime.conditions)
        * len(config.runtime.framings)
        * config.runtime.permutations
    )
    if expected_per_model != 360:
        raise RuntimeError(f"Phase 3 requires 360 calls per model; calculated {expected_per_model}")
    preflight = _run_preflight(
        root, os.environ.get("OPENROUTER_API_KEY", ""), config.runtime, items, expected_per_model
    )
    started_at = _utc_now()
    run_id = resume_run_id or _run_id(started_at, "phase3", item_set_hash(items))
    raw_directory = root / "data" / "raw" / run_id
    existing_records = _load_resumable_records(raw_directory, run_id, config.runtime, items)
    if resume_run_id is None:
        raw_directory.mkdir(parents=True, exist_ok=False)
    budget = RunBudget(config.runtime.budget_usd)
    _seed_budget_from_existing_records(budget, existing_records)
    client = OpenRouterClient(os.environ.get("OPENROUTER_API_KEY", ""), budget)
    existing_keys = {_task_key(record) for record in existing_records}
    tasks = (
        task
        for task in _iter_tasks(config.runtime.models, items, config.runtime)
        if _task_key_from_task(task) not in existing_keys
    )
    records, stop_reason = _execute_tasks(
        client,
        run_id,
        config.runtime,
        tasks,
        expected_per_model * len(config.runtime.models) - len(existing_records),
        raw_directory,
        workers,
        progress_label="Phase 3",
    )
    records = [*existing_records, *records]
    records.sort(
        key=lambda record: (record.model_id, record.item_id, record.framing, record.permutation)
    )
    ended_at = _utc_now()
    if stop_reason is not None:
        incomplete_path = root / "data" / "manifests" / f"{run_id}.incomplete.json"
        _write_json(
            incomplete_path,
            {
                "status": "incomplete",
                "run_id": run_id,
                "started_at": started_at,
                "ended_at": ended_at,
                "git_commit": commit,
                "preflight": str(preflight.relative_to(root)),
                "expected_records": expected_per_model * len(config.runtime.models),
                "persisted_records": len(records),
                "recorded_cost_usd": float(budget.spent_usd),
                "stop_reason": stop_reason,
            },
        )
        raise Phase2Aborted(
            f"{stop_reason}. Persisted {len(records)} records and wrote {incomplete_path}."
        )
    by_model: dict[str, list[Any]] = defaultdict(list)
    for record in records:
        by_model[record.model_id].append(record)
    per_model_cost = {
        model.id: sum((record.cost_usd for record in by_model[model.id]), start=0.0)
        for model in config.runtime.models
    }
    manifest = RunManifest(
        run_id=run_id,
        item_set_hash=item_set_hash(items),
        prompt_template_hashes={
            "choice": _hash_file(root / "prompts" / "item_templates" / "choice.jinja"),
            "phase3_render": _hash_file(root / "src" / "spinning_arrow" / "render.py"),
            "scenario_contract": _hash_file(root / "instruments" / "phase3_contract.json"),
        },
        panel_hash=_hash_file(root / "panels" / "phase3.yaml"),
        model_ids=tuple(model.id for model in config.runtime.models),
        sampling_params={
            "temperature": config.runtime.temperature,
            "max_tokens": config.runtime.max_tokens,
            "reasoning": {"enabled": False},
            "preflight": str(preflight.relative_to(root)),
            "baseline_run_id": config.baseline_run_id,
            "resumed_existing_records": len(existing_records),
        },
        parameter_omissions={
            model.id: model.parameter_omissions for model in config.runtime.models
        },
        git_commit=commit,
        started_at=started_at,
        ended_at=ended_at,
        total_cost_usd=sum(per_model_cost.values()),
        per_model_cost_usd=per_model_cost,
        outcome_counts=dict(Counter(record.outcome.value for record in records)),
    )
    manifest_path = root / "data" / "manifests" / f"{run_id}.json"
    _write_json(manifest_path, manifest.to_dict())
    return Phase3Artifacts(run_id, raw_directory, manifest_path, budget.spent_usd)


def _phase3_items(root: Path) -> tuple[Item, ...]:
    return load_items([root / "instruments" / PHASE3_ITEM_FILENAME])


def _load_resumable_records(
    raw_directory: Path,
    run_id: str,
    config: Phase2Config,
    items: Sequence[Item],
) -> list[Any]:
    if not raw_directory.exists():
        return []
    if not raw_directory.is_dir():
        raise ValueError(f"Phase 3 raw path is not a directory: {raw_directory}")
    records = _load_records(raw_directory, run_id)
    valid_keys = {
        (model.id, item.id, condition, framing, permutation)
        for model in config.models
        for item in items
        for condition in config.conditions
        for framing in config.framings
        for permutation in range(config.permutations)
    }
    keys = [_task_key(record) for record in records]
    if len(keys) != len(set(keys)):
        raise ValueError("interrupted Phase 3 raw data contains duplicate task records")
    if not set(keys).issubset(valid_keys):
        raise ValueError("interrupted Phase 3 raw data does not match the active panel")
    if any(record.tokens.reasoning_tokens for record in records):
        raise ValueError("interrupted Phase 3 raw data contains billed reasoning tokens")
    return records


def _task_key(record: Any) -> tuple[str, str, str, str, int]:
    return (
        record.model_id,
        record.item_id,
        record.condition,
        record.framing,
        record.permutation,
    )


def _task_key_from_task(
    task: tuple[Phase2Model, Item, str, str, int],
) -> tuple[str, str, str, str, int]:
    model, item, condition, framing, permutation = task
    return model.id, item.id, condition, framing, permutation


def _seed_budget_from_existing_records(budget: RunBudget, records: Sequence[Any]) -> None:
    """Carry prior durable spend into a resumed run's same hard-cap accounting."""

    prior_spend = sum((Decimal(str(record.cost_usd)) for record in records), start=Decimal("0"))
    if prior_spend:
        reservation = budget.reserve(prior_spend)
        budget.settle(reservation, prior_spend)


def _load_config(path: Path) -> Phase3Config:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"could not read Phase 3 panel {path}") from error
    if not isinstance(document, Mapping) or document.get("panel") != "phase3":
        raise ValueError("Phase 3 panel must be a phase3 object")
    sampling = document.get("sampling")
    raw_models = document.get("models")
    if (
        not isinstance(sampling, Mapping)
        or not isinstance(raw_models, list)
        or len(raw_models) != 3
    ):
        raise ValueError("Phase 3 panel must define sampling and exactly three models")
    models: list[Phase2Model] = []
    for raw in raw_models:
        if not isinstance(raw, Mapping) or not isinstance(raw.get("id"), str):
            raise ValueError("each Phase 3 model must have an id")
        omissions = raw.get("parameter_omissions", [])
        if not isinstance(omissions, list) or not all(
            isinstance(value, str) for value in omissions
        ):
            raise ValueError("Phase 3 parameter_omissions must be strings")
        models.append(
            Phase2Model(
                id=raw["id"],
                max_call_cost_usd=Decimal(str(raw.get("max_call_cost_usd"))),
                max_tokens=int(raw.get("max_tokens", sampling.get("max_tokens"))),
                parameter_omissions=tuple(omissions),
            )
        )
    conditions = tuple(document.get("conditions", []))
    framings = tuple(document.get("surface_forms", []))
    if (
        conditions != ("bare",)
        or set(framings) != {"direct", "advice"}
        or int(document.get("permutations", 0)) != 6
    ):
        raise ValueError("Phase 3 requires bare, direct/advice, and six permutations")
    baseline = document.get("baseline_run_id")
    if not isinstance(baseline, str) or not baseline:
        raise ValueError("Phase 3 panel requires baseline_run_id")
    return Phase3Config(
        runtime=Phase2Config(
            budget_usd=Decimal(str(document.get("budget_usd"))),
            maximum_forecast_usd=Decimal(str(document.get("maximum_forecast_usd"))),
            forecast_input_tokens=int(document.get("forecast_input_tokens")),
            conditions=conditions,
            framings=framings,
            permutations=6,
            max_tokens=int(sampling.get("max_tokens")),
            temperature=float(sampling.get("temperature")),
            models=tuple(models),
        ),
        baseline_run_id=baseline,
    )


def _run_preflight(
    root: Path, api_key: str, config: Phase2Config, items: Sequence[Item], calls_per_model: int
) -> Path:
    catalog = _fetch_catalog(api_key)
    by_id = {entry.get("id"): entry for entry in catalog if isinstance(entry.get("id"), str)}
    selected: list[dict[str, object]] = []
    forecast_total = Decimal("0")
    for model in config.models:
        entry = by_id.get(model.id)
        if not isinstance(entry, Mapping):
            raise Phase2PreflightError(f"OpenRouter catalog no longer lists {model.id}")
        reasoning = entry.get("reasoning")
        if isinstance(reasoning, Mapping) and reasoning.get("mandatory") is True:
            raise Phase2PreflightError(
                f"{model.id} now requires reasoning and is ineligible under D5"
            )
        pricing = entry.get("pricing")
        if not isinstance(pricing, Mapping):
            raise Phase2PreflightError(f"{model.id} has no auditable pricing")
        try:
            prompt_price = Decimal(str(pricing["prompt"]))
            completion_price = Decimal(str(pricing["completion"]))
        except Exception as error:
            raise Phase2PreflightError(f"{model.id} has unusable pricing") from error
        forecast = Decimal(calls_per_model) * (
            Decimal(config.forecast_input_tokens) * prompt_price
            + Decimal(model.max_tokens) * completion_price
        )
        forecast_total += forecast
        selected.append(
            {
                "id": model.id,
                "name": entry.get("name"),
                "reasoning": reasoning,
                "pricing_per_token_usd": {
                    "prompt": str(prompt_price),
                    "completion": str(completion_price),
                },
                "forecast_usd": str(forecast),
            }
        )
    if forecast_total > config.maximum_forecast_usd or forecast_total > config.budget_usd:
        raise Phase2PreflightError(
            f"live forecast ${forecast_total:.4f} breaches the approved Phase 3 forecast/cap guard"
        )
    probe_budget = RunBudget(Decimal("0.10"))
    probe_client = OpenRouterClient(api_key, probe_budget, endpoint=OPENROUTER_CHAT_URL)
    rendered = render_item(items[0], framing="direct", condition="bare", permutation=0)
    probes: list[dict[str, object]] = []
    for model in config.models:
        parameters: dict[str, Any] = {}
        if "temperature" not in model.parameter_omissions:
            parameters["temperature"] = config.temperature
        if "reasoning" not in model.parameter_omissions:
            parameters["reasoning"] = {"enabled": False}
        try:
            result = probe_client.chat_completion(
                model_id=model.id,
                messages=rendered.messages,
                maximum_cost_usd=model.max_call_cost_usd,
                max_tokens=model.max_tokens,
                parameters=parameters,
                omit_reasoning="reasoning" in model.parameter_omissions,
            )
        except Exception as error:
            raise Phase2PreflightError(f"live probe failed for {model.id}: {error}") from error
        if result.reasoning_tokens:
            raise Phase2PreflightError(
                f"live probe for {model.id} reported reasoning tokens under disabled reasoning"
            )
        parsed = parse_response(result.text or "", rendered.option_order)
        if parsed.outcome is not Outcome.ANSWERED:
            raise Phase2PreflightError(
                f"live probe for {model.id} was not parseable: {result.text!r}"
            )
        probes.append(
            {
                "model_id": model.id,
                "provider_served": result.provider_served,
                "raw_response": result.text,
                "outcome": parsed.outcome.value,
                "tokens": {
                    "in": result.input_tokens,
                    "out": result.output_tokens,
                    "reasoning": result.reasoning_tokens,
                },
                "cost_usd": str(result.cost_usd),
                "latency_ms": result.latency_ms,
            }
        )
    stamp = _utc_now().replace("-", "").replace(":", "").replace("+00:00", "Z")
    path = root / "data" / "preflight" / f"{stamp}__phase3.json"
    _write_json(
        path,
        {
            "checked_at": _utc_now(),
            "catalog_url": MODEL_CATALOG_URL,
            "calls_per_model": calls_per_model,
            "forecast_input_tokens": config.forecast_input_tokens,
            "forecast_total_usd": str(forecast_total),
            "approved_forecast_limit_usd": str(config.maximum_forecast_usd),
            "run_cap_usd": str(config.budget_usd),
            "models": selected,
            "probes": probes,
            "probe_total_cost_usd": str(probe_budget.spent_usd),
        },
    )
    return path
