"""Phase 0's deliberately tiny real-call check.

This is not an evaluation and does not produce a score. It verifies that the public raw-response
and manifest contracts survive one OpenRouter chat-completions call end to end.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import logging
import os
import subprocess
import sys
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path

from spinning_arrow.client import (
    MissingConfigurationError,
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

SMOKE_MODEL = "openai/gpt-oss-120b"
SMOKE_PROMPT = "This is a response-format check. Reply with exactly the letter C and no other text."
SMOKE_REASONING = {"effort": "low", "exclude": True}
SMOKE_REASONING_EXCEPTION = (
    "Phase 0 smoke only: OpenRouter reports reasoning mandatory for openai/gpt-oss-120b; "
    "this unscored format check is not part of the main battery."
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = _argument_parser()
    args = parser.parse_args(argv)
    _load_dotenv(Path(args.env_file))
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    try:
        artifacts = run_smoke(
            project_root=Path(args.project_root),
            model_id=args.model,
            spend_cap_usd=Decimal(args.spend_cap_usd),
            maximum_call_cost_usd=Decimal(args.max_call_cost_usd),
        )
    except (MissingConfigurationError, OpenRouterClientError, ValueError, RuntimeError) as error:
        print(f"Smoke call did not run: {error}", file=sys.stderr)
        return 2
    print(f"Smoke response record: {artifacts.response_path}")
    print(f"Smoke manifest: {artifacts.manifest_path}")
    print(f"Recorded cost: ${artifacts.cost_usd:.8f}")
    return 0


def run_smoke(
    *,
    project_root: Path,
    model_id: str = SMOKE_MODEL,
    spend_cap_usd: Decimal = Decimal("0.01"),
    maximum_call_cost_usd: Decimal = Decimal("0.01"),
    client: OpenRouterClient | None = None,
    git_commit: str | None = None,
) -> SmokeArtifacts:
    """Run a single format check and write only validated public artifacts."""

    project_root = project_root.resolve()
    commit = git_commit or _git_commit(project_root)
    started = _utc_now()
    run_id = _run_id(started, model_id)
    messages = ({"role": "user", "content": SMOKE_PROMPT},)
    if client is None:
        api_key = os.environ.get("OPENROUTER_API_KEY", "")
        client = OpenRouterClient(api_key, RunBudget(spend_cap_usd))
    completion = client.chat_completion(
        model_id=model_id,
        messages=messages,
        maximum_cost_usd=maximum_call_cost_usd,
        max_tokens=8,
        parameters={"reasoning": SMOKE_REASONING},
        reasoning_exception=SMOKE_REASONING_EXCEPTION,
    )
    parsed = _parse_smoke_response(completion.text)
    outcome = Outcome.ANSWERED if parsed.valid else Outcome.UNPARSEABLE
    response_record = ResponseRecord(
        run_id=run_id,
        ts=_utc_now(),
        model_id=model_id,
        provider_served=completion.provider_served,
        instrument="phase0_smoke",
        item_id="smoke_001",
        condition="bare",
        framing="direct_instruction",
        permutation=0,
        option_order=("A", "B", "C"),
        prompt_hash=_hash_json(messages),
        messages=messages,
        raw_response=completion.text,
        parsed=parsed,
        outcome=outcome,
        tokens=TokenUsage(
            input_tokens=completion.input_tokens,
            output_tokens=completion.output_tokens,
            reasoning_tokens=completion.reasoning_tokens,
        ),
        cost_usd=float(completion.cost_usd),
        latency_ms=completion.latency_ms,
        error=None,
    )
    manifest = RunManifest(
        run_id=run_id,
        item_set_hash=_hash_json({"instrument": "phase0_smoke", "item_id": "smoke_001"}),
        prompt_template_hashes={"phase0_smoke": _hash_text(SMOKE_PROMPT)},
        panel_hash=_hash_file(project_root / "panels" / "smoke.yaml"),
        model_ids=(model_id,),
        sampling_params={
            "temperature": 0,
            "max_tokens": 8,
            "reasoning": SMOKE_REASONING,
            "main_battery": False,
            "reasoning_exception": SMOKE_REASONING_EXCEPTION,
        },
        parameter_omissions={model_id: ()},
        git_commit=commit,
        started_at=started,
        ended_at=_utc_now(),
        total_cost_usd=float(completion.cost_usd),
        per_model_cost_usd={model_id: float(completion.cost_usd)},
        outcome_counts={outcome.value: 1},
    )
    response_path = project_root / "data" / "raw" / run_id / "smoke.jsonl.gz"
    manifest_path = project_root / "data" / "manifests" / f"{run_id}.json"
    _write_jsonl_gzip(response_path, [response_record.to_dict()])
    _write_json(manifest_path, manifest.to_dict())
    return SmokeArtifacts(
        response_path=response_path,
        manifest_path=manifest_path,
        cost_usd=completion.cost_usd,
    )


class SmokeArtifacts:
    def __init__(self, *, response_path: Path, manifest_path: Path, cost_usd: Decimal) -> None:
        self.response_path = response_path
        self.manifest_path = manifest_path
        self.cost_usd = cost_usd


def _argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Make Spinning Arrow's one Phase 0 API smoke call."
    )
    parser.add_argument("smoke", nargs="?", help=argparse.SUPPRESS)
    parser.add_argument(
        "--project-root", default=".", help="Repository root (default: current directory)."
    )
    parser.add_argument(
        "--env-file", default=".env", help="Local dotenv file to read without printing."
    )
    parser.add_argument("--model", default=SMOKE_MODEL)
    parser.add_argument("--spend-cap-usd", default="0.01")
    parser.add_argument("--max-call-cost-usd", default="0.01")
    return parser


def _load_dotenv(path: Path) -> None:
    """Load simple KEY=VALUE lines without overriding explicitly exported environment values."""

    if not path.is_file():
        return
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        key, separator, value = stripped.partition("=")
        if not separator or not key or not key.replace("_", "").isalnum():
            raise ValueError(f"{path}:{line_number} is not a valid dotenv assignment")
        value = value.strip().strip("\"'")
        os.environ.setdefault(key, value)


def _git_commit(project_root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=project_root,
        capture_output=True,
        check=False,
        text=True,
    )
    commit = result.stdout.strip()
    if result.returncode != 0 or len(commit) != 40:
        raise RuntimeError(
            "A committed Git revision is required before the smoke call "
            "so its manifest is reproducible."
        )
    return commit


def _parse_smoke_response(raw_response: str) -> ParsedResponse:
    normalized = raw_response.strip().upper()
    if normalized == "C":
        return ParsedResponse(choice="C", valid=True)
    return ParsedResponse(None, False)


def _run_id(started_at: str, model_id: str) -> str:
    stamp = started_at.replace("-", "").replace(":", "").replace("+00:00", "Z")
    suffix = hashlib.sha256(f"{started_at}:{model_id}".encode()).hexdigest()[:6]
    return f"{stamp}__smoke__{suffix}"


def _utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def _hash_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def _hash_json(value: object) -> str:
    canonical = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return _hash_text(canonical)


def _hash_file(path: Path) -> str:
    if not path.is_file():
        raise RuntimeError(f"Required panel file is missing: {path}")
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _write_jsonl_gzip(path: Path, records: Sequence[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with gzip.open(temporary, "wt", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True))
            handle.write("\n")
    temporary.replace(path)


def _write_json(path: Path, document: Mapping[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    rendered = json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    temporary.write_text(rendered, encoding="utf-8")
    temporary.replace(path)


if __name__ == "__main__":  # pragma: no cover - console-script entry point
    raise SystemExit(main())
