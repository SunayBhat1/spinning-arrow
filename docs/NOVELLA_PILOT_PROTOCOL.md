# Novella pilot protocol (v0 exploratory)

**Status:** pre-registered exploratory pilot  
**Relation to main:** not a phase gate; does not replace owner control-reset on claim/axes/v0.2  
**Budget discipline:** $20–25 lean replication envelope

---

## Purpose

Test whether richer narrative grounding increases response **stability** under perturbation, not whether it reveals "true values." The Spinning Arrow claim remains conditional: measured direction + measured stability under published conditions. This pilot asks whether literary context buys invariance, not whether novels reveal ethics.

---

## Design (factorial)

Cross **scenario richness** × **perturbations**.

### Richness levels

1. **Short Likert item** — axis-matched, questionnaire style (e.g. MFQ-2 statement)
2. **Short open-ended** — same moral tension, free-text response (~100 tokens)
3. **Grounded 1–2k token dilemma** — original vignette with character + stakes, no famous book
4. **Longer literary excerpt** — obscure PD or original; mechanical cut before the decision point

If using owner shortlist books, cut before the canonical action. Obscure excerpts or original literary vignettes are also permitted.

### Perturbations (orthogonal)

Applied within each richness level:

- **Paraphrase** — 2–3 matched rewrites of the same moral tension
- **Option order** — when forced-choice options exist
- **Forced vs free response** — choice set vs open completion
- **Point of view** — advisor vs actor (or character vs narrator; select one operationalization and freeze it)

Each perturbation tests stability independently; cross-perturbation interactions (e.g. order×POV) are optional if budget permits.

---

## Corpus: owner's ten novella candidates

| # | Title | Dilemma (one line) | PD status (US / life+70) |
|---|---|---|---|
| 1 | Animal Farm | betrayal of ideals / complicity | **Rights-gated** — still under US copyright through ~2040 (Orwell 1945); may be PD in some life+70 jurisdictions (Orwell d.1950 → 2021) but **do not treat as freely usable for US-hosted evals without rights review** |
| 2 | The Metamorphosis | family duty vs individual survival | PD (Kafka 1915) |
| 3 | Of Mice and Men | mercy killing vs loyalty | **Rights-gated** — still under US copyright through ~2032 (Steinbeck 1937) |
| 4 | The Strange Case of Dr. Jekyll and Mr. Hyde | responsibility for one's darker self | PD (Stevenson 1886) |
| 5 | Heart of Darkness | complicity in atrocity | PD (Conrad 1899) |
| 6 | The Turn of the Screw | protection vs truth | PD (James 1898) |
| 7 | Bartleby the Scrivener | employer duty vs worker autonomy | PD (Melville 1853) |
| 8 | The Death of Ivan Ilyich | authenticity vs social conformity | PD (Tolstoy 1886) |
| 9 | The Yellow Wallpaper | medical authority vs patient's self-knowledge | PD (Gilman 1892) |
| 10 | Ethan Frome | duty vs desire | PD (Wharton 1911) |

**Pilot selection:** use **5–10** from this shortlist. Prefer the clear-PD set first (titles 2, 4–10). Treat *Animal Farm* and *Of Mice and Men* as optional and rights-gated; do not include them without explicit clearance.

---

## Item construction rules

### Mechanical cut point

Stop the excerpt **before** the canonical decision or action. The model must choose, not recall the ending. Mark the cut point with a timestamp/page reference and document it in the run manifest.

### Name-swap normalization script

Replace character names with neutral labels (e.g. "Person A," "the worker," "the doctor") or swap to obscure names. This reduces plot-memory shortcuts. Document the character mapping in the item metadata. Apply consistently within each book; do not randomize per call.

### Optional summarization pass

If long excerpts exceed token budget, use a **fixed summarizer prompt** that compresses to a target token band (e.g. 800–1200). If summarization is used:

- Freeze the summarizer model/prompt and document it
- Treat summary vs full-text as a factor or a separate arm, **not** silent preprocessing
- Report which items were summarized and which were not

### Forced-choice options

When a richness level requires forced options (Likert or grounded dilemma with choices):

- Provide **five plausible action packages**
- No hidden "ask a manager" escape
- Balanced length and valence (match OWNER_BRIEFING / SPEC ladder rules if they exist; otherwise match mean token count and sentiment polarity)

---

## Metrics (pre-registered)

### Primary: flip rate under perturbation

For each richness level, measure **flip rate** under each perturbation type:

- Paraphrase flip: same moral tension, reworded → different answer
- Option-order flip: same content, permuted options → different answer
- Forced/free flip: forced choice vs open response → incompatible direction
- POV flip: advisor vs actor → different answer

Compute flip rate as `(changed responses) / (valid pairs)`. Report per richness level and per model.

### Secondary: cross-model agreement

Pairwise choice agreement (Cohen's κ or raw proportion) on the same item×condition. Higher agreement suggests the item elicits a clearer signal; lower agreement suggests idiosyncratic interpretation.

### Non-metrics

**Do not treat mean direction shift under narrative as success.** Narrative may move means without buying invariance. The question is stability, not revealed preference.

---

## Models

Small set spanning sizes: suggest **4–6 OpenRouter models**:

- **1–2 frontier** (e.g. `anthropic/claude-sonnet-5`, `openai/gpt-5.4-mini`)
- **2 mid-range** (e.g. `mistralai/mistral-medium-3.1`, `meta-llama/llama-3.3-70b-instruct`)
- **1–2 small/light** (e.g. `qwen/qwen3.8-27b`, `google/gemini-2.5-flash-lite`)

Pin model IDs. Reasoning **off** unless a named arm requires it. Hard spend discipline: preflight every batch, stop at cap.

---

## Budget envelope

Fit under **$20–25 lean replication** from OWNER_BRIEFING.

### Rough call-count × cost sketch

Assume:

- **N books** = 5–8 from clear-PD set
- **K richness levels** that use API = 3 (Likert, grounded dilemma, literary excerpt; skip open-ended or run locally if free-text)
- **P perturbations** = 4 factors × 2–3 conditions each ≈ 10–12 conditions per item
- **M models** = 4–6

**Upper bound:** 8 books × 3 richness × 12 conditions × 6 models = **1,728 calls**

At an average cost of **$0.012/call** (frontier ~$0.02, mid ~$0.01, light ~$0.002 weighted), total ≈ **$20.74**.

### What to cut first if over budget

1. Drop **order×POV cross-perturbations** (run order and POV as separate arms, not factorial)
2. Reduce books from 8 → 5 (saves ~40% of calls)
3. Drop the **Likert arm** (already covered in main battery; literary arms are the novel contribution)
4. Reduce models from 6 → 4 (drop one frontier and one light)

Do not silently exceed cap. Stop the run, report partial results, and propose cuts.

---

## Exclusion rules

### Parse failures / refusals

Excluded from flip-rate denominators but **reported separately**. High refusal rate on a literary excerpt is itself a signal (e.g. contamination guard, content-policy trigger).

### Contaminated recall

If a model **quotes the canonical ending** or **names the original climax action** unprompted, flag the response as contaminated. Exclude from stability primary analysis; report contamination rate separately as a validity check.

Operational test: regex match on known character names + known outcome phrases (e.g. "Boxer was sent to the knacker" for *Animal Farm*, "Gregor died" for *Metamorphosis*). Document the contamination filters in the scoring contract.

### Duplicate cells, spend-cap hits, empty completions

- Duplicate cells (same model/item/condition called twice) → retain first, discard rest
- Spend-cap hit before completion → report partial results and stopped-cell count
- Empty completions (usage recorded, no content) → exclude from scoring, report as API anomaly

---

## Claims this pilot can support

### Can support

- Whether **flip rates differ by richness** under matched perturbations
- **Exploratory cost** of literary arms (tokens, API expense, contamination rate)
- **Contamination rates** on famous PD texts (how often models recall the ending)
- Whether forced-choice vs open-response formats show different stability profiles

### Cannot support

- "Models have more stable **true values** in rich context" (stability ≠ ground truth)
- Literary interpretation = revealed ethics (narrative frames may induce consistency without revealing preference)
- Leaderboard or safety benchmark (exploratory, small item set, no claims about capability or harm)
- Agentic claims (single-turn responses only)
- That PD books are a **validated instrument** (this pilot *tests* whether they might be useful, not whether they are)

---

## Relation to main Spinning Arrow

**Exploratory; not a phase gate.** Does not replace owner control-reset on claim/axes/v0.2. Main battery continues with short, validated instruments (MFQ-2, ETHICS, IPIP-NEO-120, phase 3 scenarios). This pilot explores whether richer narrative buys stability **before** committing to literary scoring in a versioned protocol.

Keep claims **local and conditional** per SPEC §0. If literary excerpts reduce flip rates, report it as "under these conditions, these models, these books." Do not generalize to "LLMs are more stable in narrative" or "novels reveal values."

If the pilot shows promising stability gains and acceptable contamination, propose a follow-on arm with:

- Expanded book set (15–20 clear-PD works)
- Frozen summarization + name-swap pipeline
- Pre-registered flip-rate threshold for "useful stability"
- Independent item review before fielding

That follow-on is **not authorized by this protocol**. This is a spend-disciplined probe to see if the method is worth pursuing.

---

## Success criteria (protocol adherence)

- [ ] Item bank constructed per mechanical-cut + name-swap + forced-option rules
- [ ] Preflight cost forecast under $25 with documented cuts if over
- [ ] Run stopped at hard cap if forecast was wrong
- [ ] Contamination filters applied and contamination rate reported
- [ ] Flip rates computed per richness×perturbation, not silently aggregated
- [ ] No claims about "true values" or "validated instrument" in any output
- [ ] Raw responses committed to `data/raw/` as gzipped JSONL
- [ ] Run manifest includes model IDs, cut points, name mappings, summarizer config (if used)

Pilot report path (proposed): `reports/0X_novella_pilot.md` — numbered after current exploratory run sequence, pending owner assignment.
