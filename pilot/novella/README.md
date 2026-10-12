# Novella-context stability smoke test

This directory contains a deliberately small, budget-capped methods pilot: does adding literary context make a model's *forced decision* less sensitive to simple prompt perturbations? It is **not** a moral scoreboard, a measure of literary understanding, or evidence of a model's real-world values or deployment suitability.

The protocol source is [`docs/NOVELLA_PILOT_PROTOCOL.md`](../../docs/NOVELLA_PILOT_PROTOCOL.md). This smoke test uses four US-public-domain works from its item bank:

- *The Strange Case of Dr. Jekyll and Mr. Hyde* — Robert Louis Stevenson
- *Bartleby, the Scrivener* — Herman Melville
- *Ethan Frome* — Edith Wharton
- *The Metamorphosis* — Franz Kafka

It intentionally excludes *Animal Farm* and *Of Mice and Men*, which the protocol identifies as rights-gated for a US-hosted evaluation.

## Design

For every item, `run_pilot.py` fetches a UTF-8 Project Gutenberg text, removes the Project Gutenberg wrapper, and makes a mechanical cut at the exact anchor recorded in [`items.json`](items.json). The cache stores only `*.up_to_stop.txt`, never the post-stop text. Its sidecar metadata includes the exact anchor and the exclusive character offset. Inspect this before trusting an item.

Three matched context arms end with the same decision frame from `items.json`:

- **R0 — vignette:** 80–120 word neutral setup in [`prompts/vignettes`](prompts/vignettes/)
- **R1 — synopsis:** roughly 600–800 word retelling through the stopping point in [`prompts/synopses`](prompts/synopses/)
- **R2 — full text:** the actual pre-stop text; if it is over 25k tokens, the runner retains its opening 3k and final 20k tokens and records that omission in the run manifest.

Each R0/R1/R2 cell gets `n` independent samples at temperature 0.7 under p0 canonical, p1 fixed-seed option order, p2 saved decision-question paraphrase, and p3 numeric labels. p4 is a separate, no-story-text author-recall check (one call per item/model to contain cost). Responses must validate as strict JSON:

```json
{"choice":"A","confidence":0.73,"reason":"60 words or fewer"}
```

The runner retries a parse failure once and records both attempts. It does not persist keys: requests saved in `raw.jsonl` omit Authorization headers, and API keys are read only from environment variables.

## Cost guard and rerunning

The supported direct-API models are `gpt-4o-mini` and `gpt-4.1-mini`. An `OPENAI_API_KEY` is required for either. A missing key does **not** trigger a fallback provider: the corresponding model is skipped and the run records that fact. `ANTHROPIC_API_KEY` is intentionally not used by this smoke-test runner yet; no Anthropic model is selected by default.

Run the required preflight first. It uses `tiktoken`, prints a model × item × condition table, and makes no API calls:

```sh
UV_CACHE_DIR=/private/tmp/spinning-arrow-uv-cache \
  uv run --no-project --with-requirements pilot/novella/requirements.txt \
  pilot/novella/run_pilot.py --dry-run
```

If its maximum-output estimate is over $4, the runner first drops R2 for the longest item, then reduces `n` from 3 to 2. It refuses a plan above the $5 hard cap. A normal run asks for confirmation after showing the final plan:

```sh
UV_CACHE_DIR=/private/tmp/spinning-arrow-uv-cache \
  OPENAI_API_KEY="..." \
  uv run --no-project --with-requirements pilot/novella/requirements.txt \
  pilot/novella/run_pilot.py
```

Use `--yes` only after reviewing the printed plan. Other useful controls are `--models gpt-4o-mini`, `--items ethan_frome,metamorphosis`, and `--n 2`.

Actual spend is calculated from response usage tokens and the pinned per-token price schedule in `run_pilot.py`. Before each call, a conservative maximum-output estimate is checked against the $5 cap; the runner also stops if actual accumulated cost crosses it.

## Outputs and interpretation

Each execution creates `runs/<UTC timestamp>/` with:

- `preflight.md` — the exact planned cost table
- `manifest.json` — model IDs, cut points, source hashes, context truncation, and protocol settings
- `raw.jsonl` — every key-free request/response attempt
- `results.json` and `results.csv` — parse-validated samples and per-cell metrics
- `summary.md` — flip rates, entropy, confidence, descriptive canon matches, and p4 contamination results
- `provider_skips.json` and `run_status.json` — missing-key and spending status

For each item × model × richness condition, the summary reports the modal option across p0–p3, its share, the fraction of p1/p2/p3 modal choices that differ from p0, entropy within each `n`-sample perturbation cell, and mean confidence. An author-path match is **descriptive only**, never a success metric. Famous narratives and non-linear narration can still create recall contamination even with a valid mechanical cut; p4 and the raw responses should be reviewed before any interpretation.

This is a smoke test. A result where R2 has fewer flips would be a directional observation, not support for a general claim that richer context stabilizes moral decision-making.
