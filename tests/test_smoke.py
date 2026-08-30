from __future__ import annotations

import gzip
import json
from decimal import Decimal
from pathlib import Path

from spinning_arrow.client import CompletionResult
from spinning_arrow.contracts import ResponseRecord, RunManifest
from spinning_arrow.smoke import run_smoke


class FakeClient:
    def chat_completion(self, **_: object) -> CompletionResult:
        return CompletionResult(
            raw={},
            text="C",
            provider_served="fireworks",
            input_tokens=17,
            output_tokens=1,
            reasoning_tokens=0,
            cost_usd=Decimal("0.00000123"),
            latency_ms=12,
        )


def test_smoke_writes_a_valid_response_and_manifest(tmp_path: Path) -> None:
    (tmp_path / "panels").mkdir()
    (tmp_path / "panels" / "smoke.yaml").write_text("models: []\n", encoding="utf-8")
    artifacts = run_smoke(
        project_root=tmp_path,
        client=FakeClient(),  # type: ignore[arg-type]
        git_commit="a" * 40,
    )

    with gzip.open(artifacts.response_path, "rt", encoding="utf-8") as handle:
        response = ResponseRecord.from_dict(json.loads(handle.readline()))
    manifest_json = artifacts.manifest_path.read_text(encoding="utf-8")
    manifest = RunManifest.from_dict(json.loads(manifest_json))

    assert response.parsed.choice == "C"
    assert response.cost_usd == 0.00000123
    assert manifest.run_id == response.run_id
    assert manifest.total_cost_usd == response.cost_usd
