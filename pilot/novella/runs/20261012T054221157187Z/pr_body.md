## Private methods pilot — not a moral scoreboard

Implements and runs the updated eight-story context-richness experiment. **Do not merge or use this as a public moral-ranking claim.** Targets `phase4-preview`; existing September pilot data and the production website are untouched.

### Completed design

- 60 normalized source frames; four raw batch files preserved verbatim; rights exclusions and unverified frames explicit.
- Eight selected stories from eight authors: Jekyll, Bartleby, The Minister's Black Veil, To Build a Fire, The Three Strangers, Enemies, God Sees the Truth, and The Postmaster.
- Five stories have vignette/synopsis/full pre-stop text. Three exceed the requested whole-story 8k-word R2 limit and have vignette/synopsis only.
- GPT-4o mini, GPT-4.1 mini, Gemini 2.5 Flash-Lite, Claude Haiku 4.5 via the existing OpenRouter key.
- Six samples × four prompt versions × 21 item/context combinations × four models = **2,016 decisions**, plus **32 author-recall probes**.
- Provider-enforced JSON, temperature 0.7, 300 output-token cap, reasoning requested off, pinned providers, no response caching or fallback.
- Exact source anchors/offsets/hashes, frozen reviewable summaries and paraphrases, raw requests/responses, ledger, metrics, and local HTML response explorer.

### Actual spend

Main run **$2.02150547**; failed preliminary format checks **$0.00277425**; **total $2.02427972 of the $5 authorization**. No outstanding reservations. The fixed balanced design is complete; no further calls were made to seek a preferred result.

### Initial summary — matched five-story panel

The table uses **schema-valid first-attempt choices**, including explanations longer than the requested 60 words. This is an explicitly labeled format-robust sensitivity analysis, added after observing length failures and before inspecting aggregate choice outcomes. Original strict-format results are retained separately.

| Model | Repeat agreement: short | Synopsis | Full text | Full − short | Modal flips: short → full |
|---|---:|---:|---:|---:|---|
| GPT-4o mini | 76.0% | 93.0% | 88.7% | +12.7 pp | 3/15 → 1/15 |
| GPT-4.1 mini | 81.0% | 87.3% | 77.0% | −4.0 pp | 4/12 → 4/12 |
| Gemini Flash-Lite | 92.3% | 90.0% | 94.0% | +1.7 pp | 3/15 → 1/15 |
| Claude Haiku 4.5 | 97.0% | 92.3% | 88.7% | −8.3 pp | 1/14 → 2/15 |

Repeat agreement compares pairs of responses to the same prompt. Flip rates compare unique perturbed modes with the unique canonical mode; ties are excluded and denominators shown. The average full-minus-short repeat-agreement change is **+0.5 pp**, not a general stabilizing result. GPT-4o mini improves and Haiku declines in both preassigned three-sample blocks. Five selected full-text stories cannot support general claims.

### Important caveats and repairs

- Richer context changes facts, narrative framing, and visible prior character commitments—not only token count. Eight of 20 matched story/model combinations change modal action from short to full text.
- **1,962/2,016** decision jobs passed the entire strict response rule after at most one retry. All 54 remaining failures were Haiku explanations over 60 words. All 2,016 first attempts still had schema-valid choices. No Haiku story is complete in all three strict-format arms, so its all-model comparison depends on the labeled sensitivity analysis.
- First-attempt recall review: 30/32 claim familiarity, 25/32 name the broad author action, five affirmative claims name a wrong action, two admit ignorance. Even some correct broad actions contain invented details. Coding-assistant review is not independent human adjudication.
- Fixed a validator bug that unnecessarily retried honest `knows=false`/empty-description recall answers. Historical raw responses, failures, and charges remain unchanged; recall analysis uses first attempts.
- Gemini reported two reasoning tokens on 50 responses despite requested disablement; usage is preserved.
- PG5200's copyrighted Wyllie translation of Metamorphosis was removed from the active cache. Animal Farm and Of Mice and Men remain excluded. Jekyll's amnesia/control assertions, Aksénov's certainty of guilt, and Postmaster's supposed successful transfer were corrected before collection.
- Some remaining option packages need editorial review, notably Enemies and Postmaster. Do that before scaling.

### Review artifacts

- [Plain-language interpretation](pilot/novella/runs/20261012T054221157187Z/interpretation.md)
- [Detailed assessment](pilot/novella/runs/20261012T054221157187Z/assessment.md)
- [Local HTML explorer](pilot/novella/runs/20261012T054221157187Z/review.html) — open locally; no deployment
- [Strict metrics](pilot/novella/runs/20261012T054221157187Z/results.csv)
- [First-attempt sensitivity metrics](pilot/novella/runs/20261012T054221157187Z/first_attempt_choice_valid/results.csv)
- [Recall coding and corrections](pilot/novella/runs/20261012T054221157187Z/recall_coding.json)
- [Selection and source notes](pilot/novella/items/smoke_selection.md)
- [Rerun instructions](pilot/novella/README.md)

### Verification

Nine offline regression tests pass. The completed-run integrity audit verifies unique request/response IDs, complete balanced first-attempt cells, frozen prompt hashes, source cuts, raw-file preservation, 60 unique bank records, eight authors, actual spend reconciled to the durable shared ledger, and zero unsettled charges. Plot images inspected locally. HTML produced offline; automatic browser preview was blocked by the browser's local-file policy.
