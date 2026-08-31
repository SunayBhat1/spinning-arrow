"""Run the guarded, reproducible Phase 2 battery."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from collections.abc import Iterator, Mapping, Sequence
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from spinning_arrow.client import (
    OPENROUTER_CHAT_URL,
    CompletionResult,
    OpenRouterClient,
    OpenRouterClientError,
    ReasoningTokenError,
    RunBudget,
    SpendCapExceeded,
    UsageAccountingError,
)
from spinning_arrow.contracts import (
    Outcome,
    ParsedResponse,
    ResponseRecord,
    RunManifest,
    TokenUsage,
)
from spinning_arrow.items import Item, item_set_hash, load_items
from spinning_arrow.parse import parse_response
from spinning_arrow.render import render_item
from spinning_arrow.run import (
    _append_jsonl_gzip,
    _file_stem,
    _git_commit,
    _hash_file,
    _hash_messages,
    _run_id,
    _utc_now,
    _write_json,
)
from spinning_arrow.smoke import _load_dotenv

MODEL_CATALOG_URL = "https://openrouter.ai/api/v1/models"
PHASE2_ITEM_FILENAMES = (
    "ipip_neo_120.yaml",
    "mfq2_phase2.yaml",
    "ous_ggb.yaml",
    "ethics_phase2.yaml",
    "attention_checks.yaml",
)


class Phase2PreflightError(RuntimeError):
    """Raised before full-battery traffic when an eligibility guard fails."""


class Phase2Aborted(RuntimeError):
    """Raised after a live-run stop condition has been durably recorded."""


@dataclass(frozen=True)
class Phase2Model:
    id: str
    max_call_cost_usd: Decimal
    max_tokens: int
    parameter_omissions: tuple[str, ...]


@dataclass(frozen=True)
class Phase2Config:
    budget_usd: Decimal
    maximum_forecast_usd: Decimal
    forecast_input_tokens: int
    conditions: tuple[str, ...]
    framings: tuple[str, ...]
    permutations: int
    max_tokens: int
    temperature: float
    models: tuple[Phase2Model, ...]


@dataclass(frozen=True)
class Phase2Artifacts:
    run_id: str
    raw_directory: Path
    manifest_path: Path
    cost_usd: Decimal


@dataclass(frozen=True)
class _TaskResult:
    record: ResponseRecord
    stop_reason: str | None


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Spinning Arrow's Phase 2 main battery.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--env-file", default=".env")
    parser.add_argument("--workers", type=int, default=12)
    args = parser.parse_args(argv)
    _load_dotenv(Path(args.env_file))
    try:
        artifacts = run_phase2(Path(args.project_root), workers=args.workers)
    except (
        OpenRouterClientError,
        Phase2PreflightError,
        Phase2Aborted,
        RuntimeError,
        ValueError,
    ) as error:
        print(f"Phase 2 did not complete: {error}", file=sys.stderr)
        return 2
    print(f"Phase 2 run ID: {artifacts.run_id}")
    print(f"Raw response directory: {artifacts.raw_directory}")
    print(f"Manifest: {artifacts.manifest_path}")
    print(f"Recorded cost: ${artifacts.cost_usd:.8f}")
    return 0


def run_phase2(project_root: Path, *, workers: int = 12) -> Phase2Artifacts:
    if workers < 1:
        raise ValueError("workers must be at least one")
    root = project_root.resolve()
    commit = _git_commit(root)
    config = _load_config(root / "panels" / "phase2.yaml")
    items = _phase2_items(root)
    if len(items) != 315:
        raise RuntimeError(f"Phase 2 requires exactly 315 items; found {len(items)}")
    expected_per_model = (
        len(items) * len(config.conditions) * len(config.framings) * config.permutations
    )
    if expected_per_model != 6300:
        raise RuntimeError(
            f"Phase 2 requires 6,300 calls per model; calculated {expected_per_model}"
        )
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    preflight = _run_preflight(root, api_key, config, items, expected_per_model)
    started_at = _utc_now()
    run_id = _run_id(started_at, "phase2", item_set_hash(items))
    raw_directory = root / "data" / "raw" / run_id
    raw_directory.mkdir(parents=True, exist_ok=False)
    budget = RunBudget(config.budget_usd)
    client = OpenRouterClient(api_key, budget)
    tasks = _iter_tasks(config.models, items, config)
    total_tasks = expected_per_model * len(config.models)
    records, stop_reason = _execute_tasks(
        client, run_id, config, tasks, total_tasks, raw_directory, workers
    )
    records.sort(key=_record_sort_key)
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
                "expected_records": total_tasks,
                "persisted_records": len(records),
                "recorded_cost_usd": float(budget.spent_usd),
                "stop_reason": stop_reason,
            },
        )
        raise Phase2Aborted(
            f"{stop_reason}. Persisted {len(records)}/{total_tasks} records and wrote "
            f"{incomplete_path}."
        )
    by_model: dict[str, list[ResponseRecord]] = defaultdict(list)
    for record in records:
        by_model[record.model_id].append(record)
    per_model_cost = {
        model.id: sum((record.cost_usd for record in by_model[model.id]), start=0.0)
        for model in config.models
    }
    manifest = RunManifest(
        run_id=run_id,
        item_set_hash=item_set_hash(items),
        prompt_template_hashes={
            "choice": _hash_file(root / "prompts" / "item_templates" / "choice.jinja"),
            "evaluator": _hash_file(root / "prompts" / "conditions" / "evaluator.txt"),
            "phase2_render": _hash_file(root / "src" / "spinning_arrow" / "render.py"),
        },
        panel_hash=_hash_file(root / "panels" / "phase2.yaml"),
        model_ids=tuple(model.id for model in config.models),
        sampling_params={
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
            "reasoning": {"enabled": False},
            "preflight": str(preflight.relative_to(root)),
            "source_manifest": _hash_file(root / "instruments" / "PHASE2_SOURCES.json"),
        },
        parameter_omissions={model.id: model.parameter_omissions for model in config.models},
        git_commit=commit,
        started_at=started_at,
        ended_at=ended_at,
        total_cost_usd=sum(per_model_cost.values()),
        per_model_cost_usd=per_model_cost,
        outcome_counts=dict(Counter(record.outcome.value for record in records)),
    )
    manifest_path = root / "data" / "manifests" / f"{run_id}.json"
    _write_json(manifest_path, manifest.to_dict())
    return Phase2Artifacts(run_id, raw_directory, manifest_path, budget.spent_usd)


def _phase2_items(root: Path) -> tuple[Item, ...]:
    return load_items([root / "instruments" / filename for filename in PHASE2_ITEM_FILENAMES])


def _iter_tasks(
    models: Sequence[Phase2Model], items: Sequence[Item], config: Phase2Config
) -> Iterator[tuple[Phase2Model, Item, str, str, int]]:
    for model in models:
        for item in items:
            for condition in config.conditions:
                for framing in config.framings:
                    for permutation in range(config.permutations):
                        yield model, item, condition, framing, permutation


def _execute_tasks(
    client: OpenRouterClient,
    run_id: str,
    config: Phase2Config,
    tasks: Iterator[tuple[Phase2Model, Item, str, str, int]],
    total_tasks: int,
    raw_directory: Path,
    workers: int,
    progress_label: str = "Phase 2",
) -> tuple[list[ResponseRecord], str | None]:
    records: list[ResponseRecord] = []
    stop_reason: str | None = None
    submitted = 0
    completed = 0
    in_flight: set[Future[_TaskResult]] = set()

    def submit_one(executor: ThreadPoolExecutor) -> bool:
        nonlocal submitted
        try:
            model, item, condition, framing, permutation = next(tasks)
        except StopIteration:
            return False
        in_flight.add(
            executor.submit(
                _run_one, client, run_id, model, item, condition, framing, permutation, config
            )
        )
        submitted += 1
        return True

    with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="phase2") as executor:
        while len(in_flight) < workers and submit_one(executor):
            pass
        while in_flight:
            done, in_flight = wait(in_flight, return_when=FIRST_COMPLETED)
            for future in done:
                result = future.result()
                records.append(result.record)
                _append_jsonl_gzip(
                    raw_directory / f"{_file_stem(result.record.model_id)}.jsonl.gz", result.record
                )
                completed += 1
                if result.stop_reason is not None and stop_reason is None:
                    stop_reason = result.stop_reason
                if completed % 250 == 0 or completed == total_tasks:
                    print(
                        f"{progress_label} progress: {completed}/{total_tasks} calls persisted; "
                        f"spent=${client.budget.spent_usd}",
                        file=sys.stderr,
                        flush=True,
                    )
            while stop_reason is None and len(in_flight) < workers and submit_one(executor):
                pass
    return records, stop_reason


def _run_one(
    client: OpenRouterClient,
    run_id: str,
    model: Phase2Model,
    item: Item,
    condition: str,
    framing: str,
    permutation: int,
    config: Phase2Config,
) -> _TaskResult:
    rendered = render_item(item, framing=framing, condition=condition, permutation=permutation)
    parameters: dict[str, Any] = {}
    if "temperature" not in model.parameter_omissions:
        parameters["temperature"] = config.temperature
    if "reasoning" not in model.parameter_omissions:
        parameters["reasoning"] = {"enabled": False}
    try:
        completion = client.chat_completion(
            model_id=model.id,
            messages=rendered.messages,
            maximum_cost_usd=model.max_call_cost_usd,
            max_tokens=model.max_tokens,
            parameters=parameters,
            omit_reasoning="reasoning" in model.parameter_omissions,
        )
    except ReasoningTokenError as error:
        return _TaskResult(
            _completion_error_record(
                run_id, model, item, condition, framing, permutation, rendered.option_order,
                rendered.messages, error.completion, str(error)
            ),
            str(error),
        )
    except (SpendCapExceeded, UsageAccountingError) as error:
        return _TaskResult(
            _error_record(
                run_id, model, item, condition, framing, permutation, rendered.option_order,
                rendered.messages, str(error)
            ),
            str(error),
        )
    except Exception as error:
        return _TaskResult(
            _error_record(
                run_id, model, item, condition, framing, permutation, rendered.option_order,
                rendered.messages, str(error)
            ),
            None,
        )
    if completion.text is None:
        return _TaskResult(
            _completion_error_record(
                run_id, model, item, condition, framing, permutation, rendered.option_order,
                rendered.messages, completion, "OpenRouter returned a choice without text content"
            ),
            None,
        )
    parsed = parse_response(completion.text, rendered.option_order)
    return _TaskResult(
        ResponseRecord(
            run_id=run_id,
            ts=_utc_now(),
            model_id=model.id,
            provider_served=completion.provider_served,
            instrument=item.instrument,
            item_id=item.id,
            condition=condition,
            framing=framing,
            permutation=permutation,
            option_order=rendered.option_order,
            prompt_hash=_hash_messages(rendered.messages),
            messages=rendered.messages,
            raw_response=completion.text,
            parsed=parsed.parsed,
            outcome=parsed.outcome,
            tokens=TokenUsage(
                completion.input_tokens, completion.output_tokens, completion.reasoning_tokens
            ),
            cost_usd=float(completion.cost_usd),
            latency_ms=completion.latency_ms,
            error=None,
        ),
        None,
    )


def _error_record(
    run_id: str,
    model: Phase2Model,
    item: Item,
    condition: str,
    framing: str,
    permutation: int,
    option_order: tuple[str, ...],
    messages: tuple[dict[str, str], ...],
    error: str,
) -> ResponseRecord:
    return ResponseRecord(
        run_id=run_id,
        ts=_utc_now(),
        model_id=model.id,
        provider_served=None,
        instrument=item.instrument,
        item_id=item.id,
        condition=condition,
        framing=framing,
        permutation=permutation,
        option_order=option_order,
        prompt_hash=_hash_messages(messages),
        messages=messages,
        raw_response=None,
        parsed=ParsedResponse(None, False),
        outcome=Outcome.ERROR,
        tokens=TokenUsage(0, 0, 0),
        cost_usd=0.0,
        latency_ms=0,
        error=error,
    )


def _completion_error_record(
    run_id: str,
    model: Phase2Model,
    item: Item,
    condition: str,
    framing: str,
    permutation: int,
    option_order: tuple[str, ...],
    messages: tuple[dict[str, str], ...],
    completion: CompletionResult,
    error: str,
) -> ResponseRecord:
    record = _error_record(
        run_id, model, item, condition, framing, permutation, option_order, messages, error
    )
    return ResponseRecord(
        **{
            **record.__dict__,
            "provider_served": completion.provider_served,
            "tokens": TokenUsage(
                completion.input_tokens, completion.output_tokens, completion.reasoning_tokens
            ),
            "cost_usd": float(completion.cost_usd),
            "latency_ms": completion.latency_ms,
        }
    )


def _load_config(path: Path) -> Phase2Config:
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"could not read Phase 2 panel {path}") from error
    raw_models = document.get("models")
    sampling = document.get("sampling")
    if not isinstance(raw_models, list) or len(raw_models) != 21:
        raise ValueError("Phase 2 launch panel must list exactly 21 models")
    if not isinstance(sampling, Mapping):
        raise ValueError("Phase 2 panel must include sampling settings")
    models: list[Phase2Model] = []
    for raw in raw_models:
        if not isinstance(raw, Mapping):
            raise ValueError("each Phase 2 model entry must be an object")
        omissions = raw.get("parameter_omissions", [])
        if not isinstance(omissions, list) or not all(
            isinstance(value, str) for value in omissions
        ):
            raise ValueError("parameter_omissions must be a list of strings")
        max_tokens = raw.get("max_tokens", sampling.get("max_tokens"))
        if isinstance(max_tokens, bool) or not isinstance(max_tokens, int) or max_tokens < 1:
            raise ValueError("model max_tokens must be a positive integer")
        model_id = raw.get("id")
        if not isinstance(model_id, str) or not model_id:
            raise ValueError("model id must be a non-empty string")
        models.append(
            Phase2Model(
                id=model_id,
                max_call_cost_usd=Decimal(str(raw.get("max_call_cost_usd"))),
                max_tokens=max_tokens,
                parameter_omissions=tuple(omissions),
            )
        )
    conditions = tuple(document.get("conditions", []))
    framings = tuple(document.get("framings", []))
    if conditions != ("bare", "evaluator") or set(framings) != {"first_person", "third_person"}:
        raise ValueError("Phase 2 requires bare/evaluator and first/third-person conditions")
    return Phase2Config(
        budget_usd=Decimal(str(document.get("budget_usd"))),
        maximum_forecast_usd=Decimal(str(document.get("maximum_forecast_usd"))),
        forecast_input_tokens=int(document.get("forecast_input_tokens")),
        conditions=conditions,
        framings=framings,
        permutations=int(document.get("permutations")),
        max_tokens=int(sampling.get("max_tokens")),
        temperature=float(sampling.get("temperature")),
        models=tuple(models),
    )


def _run_preflight(
    root: Path,
    api_key: str,
    config: Phase2Config,
    items: Sequence[Item],
    calls_per_model: int,
) -> Path:
    catalog = _fetch_catalog(api_key)
    selected: list[dict[str, object]] = []
    forecast_total = Decimal("0")
    by_id = {entry.get("id"): entry for entry in catalog if isinstance(entry.get("id"), str)}
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
            raise Phase2PreflightError(f"{model.id} has no auditable pricing in the live catalog")
        try:
            prompt_price = Decimal(str(pricing["prompt"]))
            completion_price = Decimal(str(pricing["completion"]))
        except Exception as error:
            raise Phase2PreflightError(f"{model.id} has unusable live pricing") from error
        if prompt_price < 0 or completion_price < 0:
            raise Phase2PreflightError(f"{model.id} has negative live pricing")
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
                "supported_parameters": entry.get("supported_parameters"),
                "pricing_per_token_usd": {
                    "prompt": str(prompt_price),
                    "completion": str(completion_price),
                },
                "forecast_usd": str(forecast),
            }
        )
    if forecast_total > config.maximum_forecast_usd or forecast_total > config.budget_usd:
        raise Phase2PreflightError(
            f"live forecast ${forecast_total:.4f} breaches the approved Phase 2 forecast/cap guard"
        )
    probe_budget = RunBudget(Decimal("0.50"))
    probe_client = OpenRouterClient(api_key, probe_budget, endpoint=OPENROUTER_CHAT_URL)
    probe_item = items[0]
    rendered = render_item(probe_item, framing="third_person", condition="bare", permutation=0)
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
        parsed = parse_response(result.text or "", rendered.option_order)
        if result.reasoning_tokens:
            raise Phase2PreflightError(
                f"live probe for {model.id} reported reasoning tokens under disabled reasoning"
            )
        if parsed.outcome is not Outcome.ANSWERED:
            raise Phase2PreflightError(
                f"live probe for {model.id} was not parseable as a response letter: {result.text!r}"
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
    path = root / "data" / "preflight" / f"{stamp}__phase2.json"
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


def _fetch_catalog(api_key: str) -> list[Mapping[str, object]]:
    if not api_key.strip():
        raise Phase2PreflightError("OPENROUTER_API_KEY is required; no catalog request was sent")
    request = Request(
        MODEL_CATALOG_URL,
        headers={"Authorization": f"Bearer {api_key}", "Accept": "application/json"},
        method="GET",
    )
    try:
        with urlopen(request, timeout=30) as response:  # noqa: S310 -- fixed HTTPS endpoint
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise Phase2PreflightError(
            f"could not fetch the OpenRouter model catalog: {error}"
        ) from error
    data = payload.get("data") if isinstance(payload, Mapping) else None
    if not isinstance(data, list):
        raise Phase2PreflightError("OpenRouter model catalog had no data array")
    entries = [entry for entry in data if isinstance(entry, Mapping)]
    if len(entries) != len(data):
        raise Phase2PreflightError("OpenRouter model catalog contains a malformed entry")
    return entries


def _record_sort_key(record: ResponseRecord) -> tuple[str, str, str, int, str]:
    return (record.model_id, record.item_id, record.framing, record.permutation, record.condition)
