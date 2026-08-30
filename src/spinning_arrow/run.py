"""Execute the Phase 1 pilot and persist every response as committed JSONL."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

from spinning_arrow.client import (
    OpenRouterClient,
    OpenRouterClientError,
    RunBudget,
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
from spinning_arrow.smoke import _load_dotenv


@dataclass(frozen=True)
class PilotModel:
    id: str
    max_call_cost_usd: Decimal
    max_tokens: int
    parameter_omissions: tuple[str, ...]
    reasoning: dict[str, Any] | None
    reasoning_exception: str | None


@dataclass(frozen=True)
class PilotConfig:
    budget_usd: Decimal
    conditions: tuple[str, ...]
    framings: tuple[str, ...]
    permutations: int
    max_tokens: int
    temperature: float
    models: tuple[PilotModel, ...]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Spinning Arrow's Phase 1 pilot.")
    parser.add_argument("--project-root", default=".")
    parser.add_argument("--env-file", default=".env")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args(argv)
    _load_dotenv(Path(args.env_file))
    try:
        artifacts = run_pilot(Path(args.project_root), workers=args.workers)
    except (OpenRouterClientError, RuntimeError, ValueError) as error:
        print(f"Pilot did not complete: {error}", file=sys.stderr)
        return 2
    print(f"Pilot run ID: {artifacts.run_id}")
    print(f"Raw response directory: {artifacts.raw_directory}")
    print(f"Manifest: {artifacts.manifest_path}")
    print(f"Recorded cost: ${artifacts.cost_usd:.8f}")
    return 0


@dataclass(frozen=True)
class PilotArtifacts:
    run_id: str
    raw_directory: Path
    manifest_path: Path
    cost_usd: Decimal


def run_pilot(project_root: Path, *, workers: int = 4) -> PilotArtifacts:
    if workers < 1:
        raise ValueError("workers must be at least one")
    root = project_root.resolve()
    commit = _git_commit(root)
    config = _load_config(root / "panels" / "pilot.yaml")
    items = load_items(
        [root / "instruments" / "mfq2.yaml", root / "instruments" / "ethics_sample.yaml"]
    )
    if len(items) != 40:
        raise RuntimeError(f"pilot requires exactly 40 items; found {len(items)}")
    calls_per_model = (
        len(items) * len(config.framings) * len(config.conditions) * config.permutations
    )
    if calls_per_model != 400:
        raise RuntimeError(f"pilot requires 400 calls per model; calculated {calls_per_model}")
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    budget = RunBudget(config.budget_usd)
    client = OpenRouterClient(api_key, budget)
    started_at = _utc_now()
    run_id = _run_id(started_at, "pilot", item_set_hash(items))
    tasks = [
        (model, item, condition, framing, permutation)
        for model in config.models
        for item in items
        for condition in config.conditions
        for framing in config.framings
        for permutation in range(config.permutations)
    ]
    raw_directory = root / "data" / "raw" / run_id
    raw_directory.mkdir(parents=True, exist_ok=True)
    records: list[ResponseRecord] = []
    with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="pilot") as executor:
        futures = [
            executor.submit(
                _run_one,
                client,
                run_id,
                model,
                item,
                condition,
                framing,
                permutation,
                config,
            )
            for model, item, condition, framing, permutation in tasks
        ]
        for completed, future in enumerate(as_completed(futures), start=1):
            record = future.result()
            records.append(record)
            _append_jsonl_gzip(raw_directory / f"{_file_stem(record.model_id)}.jsonl.gz", record)
            if completed % 100 == 0:
                print(
                    f"Pilot progress: {completed}/{len(tasks)} calls persisted",
                    file=sys.stderr,
                    flush=True,
                )
    records.sort(key=_record_sort_key)
    ended_at = _utc_now()
    by_model: dict[str, list[ResponseRecord]] = defaultdict(list)
    for record in records:
        by_model[record.model_id].append(record)
    per_model_cost = {
        model.id: sum(record.cost_usd for record in by_model[model.id]) for model in config.models
    }
    outcomes = Counter(record.outcome.value for record in records)
    manifest = RunManifest(
        run_id=run_id,
        item_set_hash=item_set_hash(items),
        prompt_template_hashes={
            "choice": _hash_file(root / "prompts" / "item_templates" / "choice.jinja"),
            "bare": _hash_text(""),
        },
        panel_hash=_hash_file(root / "panels" / "pilot.yaml"),
        model_ids=tuple(model.id for model in config.models),
        sampling_params={
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
            "model_max_tokens": {model.id: model.max_tokens for model in config.models},
            "reasoning": {"enabled": False},
            "exceptions": {
                model.id: {"reasoning": model.reasoning, "reason": model.reasoning_exception}
                for model in config.models
                if model.reasoning_exception
            },
        },
        parameter_omissions={model.id: model.parameter_omissions for model in config.models},
        git_commit=commit,
        started_at=started_at,
        ended_at=ended_at,
        total_cost_usd=sum(per_model_cost.values()),
        per_model_cost_usd=per_model_cost,
        outcome_counts=dict(outcomes),
    )
    manifest_path = root / "data" / "manifests" / f"{run_id}.json"
    _write_json(manifest_path, manifest.to_dict())
    return PilotArtifacts(run_id, raw_directory, manifest_path, budget.spent_usd)


def _run_one(
    client: OpenRouterClient,
    run_id: str,
    model: PilotModel,
    item: Item,
    condition: str,
    framing: str,
    permutation: int,
    config: PilotConfig,
) -> ResponseRecord:
    rendered = render_item(item, framing=framing, condition=condition, permutation=permutation)
    parameters: dict[str, Any] = {}
    if "temperature" not in model.parameter_omissions:
        parameters["temperature"] = config.temperature
    if model.reasoning is not None:
        parameters["reasoning"] = model.reasoning
    try:
        completion = client.chat_completion(
            model_id=model.id,
            messages=rendered.messages,
            maximum_cost_usd=model.max_call_cost_usd,
            max_tokens=model.max_tokens,
            parameters=parameters,
            reasoning_exception=model.reasoning_exception,
            omit_reasoning="reasoning" in model.parameter_omissions,
        )
    except Exception as error:
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
            option_order=rendered.option_order,
            prompt_hash=_hash_messages(rendered.messages),
            messages=rendered.messages,
            raw_response=None,
            parsed=ParsedResponse(None, False),
            outcome=Outcome.ERROR,
            tokens=TokenUsage(0, 0, 0),
            cost_usd=0.0,
            latency_ms=0,
            error=str(error),
        )
    if completion.text is None:
        return ResponseRecord(
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
            raw_response=None,
            parsed=ParsedResponse(None, False),
            outcome=Outcome.ERROR,
            tokens=TokenUsage(
                completion.input_tokens,
                completion.output_tokens,
                completion.reasoning_tokens,
            ),
            cost_usd=float(completion.cost_usd),
            latency_ms=completion.latency_ms,
            error="OpenRouter returned a choice without text content",
        )
    parsed = parse_response(completion.text, rendered.option_order)
    return ResponseRecord(
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
            completion.input_tokens,
            completion.output_tokens,
            completion.reasoning_tokens,
        ),
        cost_usd=float(completion.cost_usd),
        latency_ms=completion.latency_ms,
        error=None,
    )


def _load_config(path: Path) -> PilotConfig:
    document = json.loads(path.read_text(encoding="utf-8"))
    raw_models = document.get("models")
    if not isinstance(raw_models, list) or len(raw_models) != 6:
        raise ValueError("pilot panel must list exactly six models")
    sampling = document.get("sampling")
    if not isinstance(sampling, dict):
        raise ValueError("pilot panel must include sampling settings")
    models: list[PilotModel] = []
    for raw in raw_models:
        if not isinstance(raw, dict):
            raise ValueError("each model entry must be an object")
        omissions = raw.get("parameter_omissions", [])
        if not isinstance(omissions, list) or not all(
            isinstance(value, str) for value in omissions
        ):
            raise ValueError("parameter_omissions must be a list of strings")
        reasoning = raw.get("reasoning")
        if reasoning is not None and not isinstance(reasoning, dict):
            raise ValueError("reasoning must be an object")
        exception = raw.get("reasoning_exception")
        if exception is not None and not isinstance(exception, str):
            raise ValueError("reasoning_exception must be a string")
        max_tokens = raw.get("max_tokens", sampling.get("max_tokens"))
        if isinstance(max_tokens, bool) or not isinstance(max_tokens, int) or max_tokens < 1:
            raise ValueError("model max_tokens must be a positive integer")
        models.append(
            PilotModel(
                id=_required_string(raw.get("id"), "model id"),
                max_call_cost_usd=Decimal(str(raw.get("max_call_cost_usd"))),
                max_tokens=max_tokens,
                parameter_omissions=tuple(omissions),
                reasoning=reasoning,
                reasoning_exception=exception,
            )
        )
    return PilotConfig(
        budget_usd=Decimal(str(document.get("budget_usd"))),
        conditions=tuple(document.get("conditions", [])),
        framings=tuple(document.get("framings", [])),
        permutations=int(document.get("permutations")),
        max_tokens=int(sampling.get("max_tokens")),
        temperature=float(sampling.get("temperature")),
        models=tuple(models),
    )


def _required_string(value: object, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} must be a non-empty string")
    return value


def _record_sort_key(record: ResponseRecord) -> tuple[str, str, str, int, str]:
    return (record.model_id, record.item_id, record.framing, record.permutation, record.condition)


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _run_id(started_at: str, kind: str, item_hash: str) -> str:
    stamp = started_at.replace("-", "").replace(":", "").replace("+00:00", "Z")
    suffix = hashlib.sha256(f"{started_at}:{kind}:{item_hash}".encode()).hexdigest()[:6]
    return f"{stamp}__{kind}__{suffix}"


def _git_commit(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, check=False, text=True
    )
    commit = result.stdout.strip()
    if result.returncode != 0 or len(commit) != 40:
        raise RuntimeError("a committed Git revision is required before running the pilot")
    return commit


def _hash_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode()).hexdigest()


def _hash_messages(messages: Sequence[Mapping[str, str]]) -> str:
    payload = json.dumps(messages, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return _hash_text(payload)


def _hash_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _file_stem(model_id: str) -> str:
    return model_id.replace("/", "__").replace(":", "_")


def _append_jsonl_gzip(path: Path, record: ResponseRecord) -> None:
    """Append one independently recoverable gzip member as soon as a call completes."""

    with gzip.open(path, "at", encoding="utf-8") as handle:
        handle.write(json.dumps(record.to_dict(), ensure_ascii=False, sort_keys=True))
        handle.write("\n")


def _write_json(path: Path, document: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
