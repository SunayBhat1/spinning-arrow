# Spinning Arrow

Spinning Arrow is a free, open-source dashboard for measuring **what language models say under
precisely specified ethical-questionnaire conditions, and how much those answers depend on those
conditions**. It does not claim to measure a model's ethics or true values.

The name credits R\u00f6ttger et al., *Political Compass or Spinning Arrow? Towards More Meaningful
Evaluations for Values and Opinions in Large Language Models* (ACL 2024).

## Status

Phases 0–2 are approved. The strict-D5 Phase 2 battery made 56,700 calls at a recorded cost of
`$5.378043`, with zero reasoning tokens; see the [visual dashboard](reports/02_scoring.html) and
[written scoring report](reports/02_scoring.md). Phase 3 is complete: its 1,080 controlled
scenario calls across Llama, Mistral, and Claude cost `$0.123587`, with zero reasoning tokens and
a 100% clean parse rate. See [the gap report](reports/03b_gap.md), [interactive visual](reports/03b_gap.html),
and [phase state](docs/PHASES.md).

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

Phase 3 has the same durable-run controls, including a live catalog preflight and a `$2` hard cap:

```sh
make phase3
RUN_ID=20260830T230045Z__phase3__74142b make phase3-report
```

## Reproducibility and licenses

Every eventual run is designed to commit its prompts, raw responses, usage and cost, and manifest.
Code is licensed under Apache-2.0 ([LICENSE](LICENSE)); instruments, data, reports, and prose use
CC BY 4.0 ([LICENSE-DATA](LICENSE-DATA)). Third-party notices live in [NOTICE](NOTICE).

See [SPEC.md](SPEC.md) for the project contract and [docs/PHASES.md](docs/PHASES.md) for the
current gate.
