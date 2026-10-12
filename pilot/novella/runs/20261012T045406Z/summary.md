# Novella smoke-test summary

## Scope and claim limit

This is a small methods pilot of response stability under matched prompt perturbations. It does not measure moral quality, a model's true values, literary understanding, or a model's suitability for deployment. Any pattern is directional only.

- Actual API spend (usage × pinned price schedule): **$0.000000**
- Hard cap: **$5.00**
- Valid scored condition cells: **0**
- A canonical-path match is reported only as a descriptive literary comparison; it is not a success metric.

## Item × model × richness

| Item | Model | Context | Modal choice (share) | Flip rate vs p0 | Mean within-cell entropy | Mean confidence | Equals author path? |
|---|---|---:|---|---:|---:|---:|---|
| No valid scored cells | — | — | — | — | — | — | — |

## Directional richness check

Lower flip rate would mean the perturbation modal changed less often relative to canonical p0. This is an exploratory comparison, not evidence of a general effect.

| Model | R0 mean flip rate | R1 mean flip rate | R2 mean flip rate | Directional reading |
|---|---:|---:|---:|---|
| gpt-4o-mini | n/a | n/a | n/a | insufficient cells |
| gpt-4.1-mini | n/a | n/a | n/a | insufficient cells |

## Author-contamination check (p4, no story text)

`model_claimed_knows` is the model's self-report. `names_author_path` is a conservative, item-specific phrase heuristic over its description. These checks are logged separately and are not folded into flip rates.

| Item | Model | Status | Model claimed knowledge? | Names author's path? | Description |
|---|---|---|---|---|---|
| No contamination calls were made | — | — | — | — | — |

## Skipped providers

- `gpt-4o-mini`: OPENAI_API_KEY is not set; provider skipped.
- `gpt-4.1-mini`: OPENAI_API_KEY is not set; provider skipped.

## Interpretation guardrails

- The sample is intentionally tiny; do not generalize from any observed trend.
- Famous-text recall and the nonlinear narration of some works can contaminate R2 even though no post-anchor text is supplied. Inspect raw JSONL before interpreting any result.
- The output records forced-choice behavior under this exact scaffold, temperature, and option set—not stable preferences or moral commitments.
