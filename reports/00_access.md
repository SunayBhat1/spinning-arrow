# Gate 0 — access and scaffold

**Status: ready for Sunay’s Gate 0 review.**

## What is ready

- A Python 3.12+ `uv` project is scaffolded with Ruff and pytest.
- `ResponseRecord`, `ScoreRecord`, and `RunManifest` are validated and JSON-serialisable. The
  response contract enforces canonical (rather than displayed-position) answer options; the score
  contract can represent the specified suppression rule; and the manifest records hashes, model
  IDs, sampling parameters, parameter omissions, costs, outcomes, and a Git revision.
- The OpenRouter chat-completions client uses only the specified endpoint. It retries transient
  failures with exponential backoff, requests router metadata, records the `usage.cost` returned by
  OpenRouter, and refuses responses without auditable cost data.
- Each call reserves a caller-provided maximum charge before sending. A request that would exceed
  the run cap is never sent; an upstream charge that exceeds its reservation stops the run
  immediately. Main-path calls force `reasoning: {"enabled": false}` and fail if the returned usage
  reports reasoning tokens.
- `make smoke` performs exactly one unscored `openai/gpt-oss-120b` format check. On success it
  writes `data/raw/<run_id>/smoke.jsonl.gz` and `data/manifests/<run_id>.json`; both artifacts are
  created only after contract validation.

## Verification performed

```text
make lint
All checks passed!

make test
11 passed
```

The tests replay `tests/fixtures/openrouter_completion.json`; they never make network requests.
They cover usage-cost accounting, transient retry behavior, pre-request spend-cap enforcement,
missing-cost failure, response and manifest round trips, canonical-choice validation, the
suppressed-score form, and end-to-end smoke artifact creation.

## Real smoke-call result

`make smoke` completed successfully on `20260830T054017Z__smoke__ab0291` and wrote both required
artifacts:

- [`data/raw/20260830T054017Z__smoke__ab0291/smoke.jsonl.gz`](../data/raw/20260830T054017Z__smoke__ab0291/smoke.jsonl.gz)
- [`data/manifests/20260830T054017Z__smoke__ab0291.json`](../data/manifests/20260830T054017Z__smoke__ab0291.json)

The raw record validates as an `answered` response with canonical choice `C`, routed to
`SiliconFlow`. It records 85 input tokens, 16 output tokens, 15 reasoning tokens, 1,347 ms
latency, and **$0.00001145** in OpenRouter `usage.cost`. The manifest links it to code revision
`e4e1f608e090dc8b8e726301fffd6928bee32bae` and the exact prompt, panel, and item-set hashes.

### Required, documented smoke-only exception

The first disabled-reasoning attempt was rejected before a completion with HTTP 400:
`Reasoning is mandatory for this endpoint and cannot be disabled.` OpenRouter's public model
metadata currently marks `openai/gpt-oss-120b` as mandatory reasoning with high/medium/low effort
only. The smoke check is unscored and not part of the main battery, so its second (successful)
attempt used `reasoning: {"effort": "low", "exclude": true}`. This exception appears directly in
the manifest; its reasoning tokens are recorded and charged. It does **not** change D5: Phase 1+
main-battery requests still default to `reasoning: {"enabled": false}` and require an explicit
documented exception to do otherwise.

## Sunay’s remaining Gate 0 actions

1. Confirm OpenRouter's dashboard lists the same **$0.00001145** charge for the smoke call.
2. Review the linked gzipped response record, manifest, and smoke-only reasoning exception.
3. Explicitly approve or return a decision on Gate 0. Do not begin Phase 1 until that happens.

Do not begin Phase 1 until this gate is reviewed and explicitly closed.
