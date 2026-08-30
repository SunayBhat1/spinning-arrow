# Spinning Arrow

Spinning Arrow is a free, open-source dashboard for measuring **what language models say under
precisely specified ethical-questionnaire conditions, and how much those answers depend on those
conditions**. It does not claim to measure a model's ethics or true values.

The name credits R\u00f6ttger et al., *Political Compass or Spinning Arrow? Towards More Meaningful
Evaluations for Values and Opinions in Large Language Models* (ACL 2024).

## Status

Phase 0 is being prepared. The repository currently provides the OpenRouter client, data
contracts, and a narrowly scoped smoke call. No questionnaire scores are produced yet.

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

## Reproducibility and licenses

Every eventual run is designed to commit its prompts, raw responses, usage and cost, and manifest.
Code is licensed under Apache-2.0 ([LICENSE](LICENSE)); instruments, data, reports, and prose use
CC BY 4.0 ([LICENSE-DATA](LICENSE-DATA)). Third-party notices live in [NOTICE](NOTICE).

See [SPEC.md](SPEC.md) for the project contract and [docs/PHASES.md](docs/PHASES.md) for the
current gate.
