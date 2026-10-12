# Narrative-richness stability pilot

Status: **stopped**. Actual spend this run: **$0.000237**. Cumulative pilot ledger: **$0.000237**; uncertain reservations: **$0.000000**.

0 valid decisions. 6 independent samples per item × model × richness × perturbation. Temperature 0.7; output cap 300 tokens; reasoning disabled; response caching disabled. Provider pinned, no fallback.

This is a methods pilot, not a moral scoreboard or a public claim. Richer context changes information and narrative framing, not only length. Literary recall, option construction and correlated samples remain confounds. Author agreement is not success; confidence is not calibration.

## Matched five-story comparison (R2-eligible only)

| Model | R0 flip | R1 flip | R2 flip | R0 repeat agreement | R1 | R2 |
|---|---:|---:|---:|---:|---:|---:|
| openai/gpt-4o-mini | — | — | — | — | — | — |
| openai/gpt-4.1-mini | — | — | — | — | — | — |
| google/gemini-2.5-flash-lite | — | — | — | — | — | — |
| anthropic/claude-haiku-4.5 | — | — | — | — | — | — |

Flip rate compares unique p1–p3 modes with the unique p0 mode; tied or incomplete cells are excluded and denominators shown. Repeat agreement is the fraction of pairs within an identical prompt cell choosing the same semantic option. Larger is more repeatable. It is less tie-sensitive than modal flips.

## All item × model × condition results

| Item | Model | Arm | Modal choice/share | Flip | Entropy (bits) | Confidence | Author match |
|---|---|---|---|---|---:|---:|---|

## Separate author-knowledge probes

These are self-reports, not proof of training contamination. Descriptions require human checking against the saved author-path annotations. Jekyll has no exact author option; Postmaster's later actions overlap B/C.


## Limitations

Only eight stories and five full-text stories, a single summary and paraphrase per item, a single option shuffle, no name masking, and no real agent actions. Temperature is not behaviorally equivalent across providers. Repeated responses are not independent new dilemmas. Richness can stabilize a choice by supplying facts or by encouraging imitation; this design cannot distinguish those explanations. Do not extrapolate to general moral reliability.
