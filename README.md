# Spinning Arrow

Spinning Arrow is a free, open-source dashboard for measuring **what language models say under
precisely specified ethical-questionnaire conditions, and how much those answers depend on those
conditions**. It does not claim to measure a model's ethics or true values.

The name credits R\u00f6ttger et al., *Political Compass or Spinning Arrow? Towards More Meaningful
Evaluations for Values and Opinions in Large Language Models* (ACL 2024).

## Status

Phases 0 and 1 are approved, and the strict-D5 Phase 2 battery and scoring are complete. The
nine-model run made 56,700 calls at a recorded cost of `$5.378043`, with zero reasoning tokens.
Review the [visual dashboard](reports/02_scoring.html), [written scoring report](reports/02_scoring.md),
and [phase state](docs/PHASES.md). Gate 2 remains pending user review; Phase 3 has not started.

## Local setup

Spinning Arrow requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```sh
uv sync --group dev
make lint
make test
```

To make the one Phase 0 API smoke call, copy `.env.example` to `.env`, put the dedicated
`OPENROUTER_API_KEY` there, and first set its hard $30 spend limit in OpenRouter. Then run:

```sh
make smoke
```

The command refuses to run without a committed Git revision, an API key, and an explicit spend
cap. A successful call writes a gzipped JSONL response under `data/raw/<run_id>/` and a matching
manifest under `data/manifests/`. It never prints the key.

The smoke call is unscored and is not a main-battery request. As of 2026-08-29,
`openai/gpt-oss-120b` requires reasoning on OpenRouter, so this one format check uses low-effort
reasoning and records that exception in its manifest. Main-battery calls continue to require
`reasoning: {"enabled": false}`.

The Phase 1 pilot can be reproduced with `make pilot`; it enforces its recorded `$2` cap and
writes raw records as each call completes. Generate its Gate 1 report with
`RUN_ID=<run_id> make pilot-report`.

The completed Phase 2 main battery can be reproduced with `make phase2`; it performs a live
preflight, enforces its run guards, and records every response as it completes. Generate the
scoring report with:

```sh
RUN_ID=20260830T155412Z__phase2__8fbf10 make phase2-report
```

## Reproducibility and licenses

Every eventual run is designed to commit its prompts, raw responses, usage and cost, and manifest.
Code is licensed under Apache-2.0 ([LICENSE](LICENSE)); instruments, data, reports, and prose use
CC BY 4.0 ([LICENSE-DATA](LICENSE-DATA)). Third-party notices live in [NOTICE](NOTICE).

See [SPEC.md](SPEC.md) for the project contract and [docs/PHASES.md](docs/PHASES.md) for the
current gate.
