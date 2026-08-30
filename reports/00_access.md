# Gate 0 — access and scaffold

**Status: open — not ready for review until the real smoke call is run.**

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
9 passed
```

The tests replay `tests/fixtures/openrouter_completion.json`; they never make network requests.
They cover usage-cost accounting, transient retry behavior, pre-request spend-cap enforcement,
missing-cost failure, response and manifest round trips, canonical-choice validation, the
suppressed-score form, and end-to-end smoke artifact creation.

## Real smoke-call status

No real API request has been made. This workspace has neither a Git repository with a committed
revision nor a local `.env` key. The guard was verified with:

```text
make smoke
Smoke call did not run: A committed Git revision is required before the smoke call so its manifest is reproducible.
```

It stopped before reading the API key or opening the network connection. No response or manifest
was written, so there is no cost to reconcile yet.

## Sunay’s remaining Gate 0 actions

1. Create and push the public `spinning-arrow` GitHub repository, then make a commit containing
   this scaffold. The smoke manifest intentionally refuses an uncommitted revision.
2. Create the dedicated OpenRouter key, set its hard $30 spend limit, and place it in a local,
   uncommitted `.env` as `OPENROUTER_API_KEY=...`.
3. Run `make smoke` from a committed checkout.
4. Review the resulting gzipped response record and manifest, then reconcile its `cost_usd` with
   the OpenRouter dashboard. They must agree before Gate 0 passes.

Do not begin Phase 1 until this gate is reviewed and explicitly closed.
