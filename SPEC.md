# Spinning Arrow — build spec & agent handoff

**Status:** pre-Phase-0. Nothing is built yet.
**Name:** Spinning Arrow — settled 2026-08-29. Repo `spinning-arrow`, package `spinning_arrow`.
No domain bought yet (see §12).
**Owner:** Sunay Bhat. **Executor:** a fresh agent, cold, starting from this file.
**Background brief (read it):** https://claude.ai/code/artifact/bac755d6-d638-4d53-9f37-68cd3e2b66fb

---

## 0. Read this first

You are building a small, free, open-source public dashboard that measures **where large
language models sit on questions of normative ethics** — rules vs. consequences vs. character —
and **how stable those positions are**.

Three things make this different from the existing field, and they are the whole product. Do not
drop them for convenience:

1. **The instability is the headline, not a caveat.** Every score ships with a *fragility index*
   and an error bar sized to it. A model whose score swings wildly under question reordering
   deserves a bar the width of the chart.
2. **Everything is inspectable.** Prompts, raw model responses, scoring code, and run logs are
   committed to a public repo. Anyone who disputes a number can check it.
3. **The claim is narrow and honest.** We do **not** claim to measure "a model's ethics." We
   claim to measure *what a model says under precisely specified conditions, and how much that
   depends on the conditions.* Every piece of copy on the site must respect that distinction.

**About the name.** A moral compass whose needle will not settle. It is taken from Röttger et
al., *"Political Compass or Spinning Arrow? Towards More Meaningful Evaluations for Values and
Opinions in Large Language Models"* (ACL 2024) — the paper that found forced-choice value scores
change with framing, lack paraphrase robustness, and diverge from open-ended answers. That
finding is the reason this project exists in the shape it does, so the name is a citation, not a
coincidence. Credit it visibly (D16).

This project is unaffiliated with `TheBrief` in the adjacent directory. Do not import its code,
its Neon database, or its Modal deployment. It shares only conventions (Python, `uv`, a
`docs/PHASES.md` state machine, numbered settled decisions).

### How to work through this document

Work **phase by phase**. Each phase ends at a **gate**. At a gate you stop, write the named
deliverable, and wait for Sunay to review it. Do not start the next phase's work while a gate is
open, and do not treat your own satisfaction with the output as passing the gate. If a gate's
deliverable reveals that a settled decision below is wrong, say so at the gate rather than
quietly working around it.

---

## 1. What we are building

A static website, rebuilt from committed data, showing for each model in a tracked panel:

- Its position on several **ethical and psychological scales** (§7).
- The **fragility** of each position — how far it moves under option reordering, paraphrase, and
  system-prompt condition.
- Its **refusal and hedge rate** on each scale, reported rather than dropped.
- The **stated-vs-revealed gap** — what the model says on a questionnaire against what it does
  in a matched behavioral scenario (Phase 3).
- A **timeline** so drift and new releases are visible.
- A link, for every single number, to the raw responses that produced it.

## 2. Non-goals

- **Not** a capability, speed, or price leaderboard. Artificial Analysis and llm-stats own that.
- **Not** a political-orientation tracker. TrackingAI has run that daily since 2023.
- **Not** a refusal/free-speech tracker. SpeechMap has 378 models and 801k responses.
- **Not** a relative-valuation tracker. CAIS's values.safe.ai owns exchange rates.
- **Not** a safety or harm benchmark. Different audience, different methods, much higher stakes.
- **Not** a paid product, at any point covered by this spec. Free, ad-free, open.
- **No** claims about model welfare, consciousness, or "true values." Not our lane, and the
  measurement does not support it.

Where our results overlap with any of the above, **cite and link out** rather than competing.

---

## 3. Settled decisions

Numbered so later work can reference them. Changing one is a conversation with Sunay, not a
judgment call.

| # | Decision | Why |
|---|---|---|
| **D1** | **OpenRouter is the only LLM API.** One key, one billing surface, one client. | Cost control and a single provider relationship. |
| **D2** | **No MBTI.** Personality is measured with IPIP-NEO-120. | MBTI items are licensed property and its marks cannot describe a substitute; it also has poor test–retest reliability and binarizes continuous traits. |
| **D3** | **Launch instruments must be public domain or CC BY.** Anything needing permission is Phase 5+ and only after written clearance. | The whole item bank is published in the repo. Provenance must be defensible. |
| **D4** | **Sampling-based scoring, not logprobs.** | Verified 2026-08-29: `anthropic/claude-sonnet-5` exposes no `logprobs`, no `seed`, no `temperature`; `google/gemini-3.5-flash-lite` and `mistralai/mistral-medium-3.1` expose no `logprobs`. A uniform method across the panel matters more than efficiency. Record logprobs opportunistically when offered, but never let a score depend on them. |
| **D5** | **Reasoning disabled for the main battery** (`reasoning: {"enabled": false}`, low `max_tokens`). | ~14× cost multiplier if left on. Reasoning-on is a scoped side-study (§8, Phase 5). |
| **D6** | **Pinned, dated model IDs only.** Never score an alias. | OpenRouter carries `~vendor/model-latest` pointers that silently move. A longitudinal chart must not absorb that drift. |
| **D7** | **Raw responses are committed** as gzipped JSONL under `data/raw/`. | The raw responses are the artifact people cite. |
| **D8** | **No database.** Flat files plus git history. | Zero cost, zero outage surface, diffs make drift visible, version history is free. |
| **D9** | **Fragility is published beside every score**, and sizes every error bar. | It is the direct answer to the strongest criticism of the method. |
| **D10** | **Refusals and hedges are recorded outcomes**, never dropped. | They are non-ignorable missing data and their rate is itself a finding. |
| **D11** | **Minimum two system-prompt conditions**, both published: `bare` (no persona) and `evaluator` (neutral research framing). | Framing alone relocates models across a value map. An undisclosed system prompt becomes half of what you measure. |
| **D12** | **Static site; plots pre-rendered as SVG from Python.** | Sunay is strong in Python, weak in JS. Keeps the whole pipeline in one language, output is crisp and theme-able. Add JS charting later only if a view demands hover. |
| **D13** | **Hard ceiling $30/month** of API spend, enforced by an OpenRouter key spend limit, not by discipline. | Matches Sunay's standing run-cost ceiling. |
| **D14** | **Open from the first commit.** Public repo, prompts and scoring code included. | Openness is the differentiator; retrofitting it is harder and reads worse. |
| **D15** | **Every run is reproducible from its manifest** — item set hash, prompt template hash, model IDs, sampling params, timestamp. | Without this the time series is uninterpretable. |
| **D16** | **The name is credited to Röttger et al. (ACL 2024) by name on both the front page and the methodology page.** | The phrase is borrowed from their framing and this audience will recognize it. Credited up front it reads as literacy; uncredited it reads as appropriation. |
| **D17** | **Dual-licensed. Apache-2.0 for code (`LICENSE`); CC BY 4.0 for instruments, data, reports, and prose (`LICENSE-DATA`). Inbound license notices in `NOTICE`.** | Apache-2.0 grants no rights to the project name, so a fork can reuse the pipeline but cannot publish altered scores under "Spinning Arrow" — which matters when credibility is the product. Its patent grant is a secondary benefit. CC BY compels the citation this project runs on without share-alike's friction for researchers; CC0 would waive exactly the attribution we want. |
| **D18** | **No CC BY-NC-SA material in the main item bank — OEJTS specifically.** If ever added, quarantine it in its own directory with its own LICENSE and never merge it into the main bank. | Share-alike would force the entire derived collection to CC BY-NC-SA and non-commercial would block reuse by anyone at a company. Not a trade worth making for a novelty axis. |

---

## 4. Stack and accounts

### Stack

| Layer | Choice | Notes |
|---|---|---|
| Language | Python 3.12+, `uv` | Package name `spinning_arrow`. |
| LLM access | OpenRouter, OpenAI-compatible `/chat/completions` | One thin client wrapper. No SDK sprawl. |
| Orchestration | GitHub Actions (cron + `workflow_dispatch`) | Free for public repos, and the run logs being public is a credibility feature. |
| Storage | Files in git: JSONL (raw), Parquet + CSV (scores) | D7, D8. |
| Site | Astro, static output | Simple, content-first, minimal JS. |
| Hosting | GitHub Pages | Free, no separate account, deploys from Actions. Vercel is a fallback if Pages proves limiting. |
| Plots | matplotlib → SVG, theme-able via CSS variables | D12. |

### Accounts and keys — **Sunay does these, not the agent**

The agent must never create accounts, enter payment details, or handle raw credentials. Its job
is to *verify* that access works and to fail loudly with a clear message when it does not.

**Checklist for Sunay (Phase 0):**

1. **OpenRouter** — create account, add **$20** of credits to start.
   Create a **dedicated API key** named `spinning-arrow`, and on that key set a **hard spend limit of
   $30**. This limit is the real cost guardrail (D13); do not rely on the code to enforce it.
2. **GitHub** — create a **public** repo `spinning-arrow` and push this spec.
   Add repo secret `OPENROUTER_API_KEY`. Enable GitHub Pages, source = GitHub Actions.
3. **Local** — put the same key in `.env` at the repo root. `.env` is gitignored from the first
   commit; `.env.example` is committed with the variable name and no value.
4. **Domain** — skip for now. Revisit at Gate 4 once there is something worth pointing at.

**Do not commit a key.** If one is ever committed, rotate it in OpenRouter immediately — deleting
the commit is not sufficient.

---

## 5. Repo layout

```
spinning-arrow/
├── SPEC.md                      # this file; the contract
├── README.md                    # what it is, how to reproduce a run
├── METHODOLOGY.md               # written for the public, plain language, ships with the site
├── LICENSE                      # Apache-2.0 — covers src/, site/, tests/, .github/
├── LICENSE-DATA                 # CC BY 4.0 — covers instruments/, data/, reports/, docs/
├── NOTICE                       # inbound license notices (D17)
├── pyproject.toml               # uv-managed, package = spinning_arrow
├── .env.example
├── docs/
│   └── PHASES.md                # state machine: current phase, what shipped, what's open
├── instruments/                 # the item bank — the licensed content
│   ├── mfq2.yaml
│   ├── ipip_neo_120.yaml
│   ├── ous_ggb.yaml
│   ├── ethics_sample.yaml
│   └── LICENSES.md              # per-instrument provenance, license, citation. Mandatory.
├── panels/
│   ├── pilot.yaml               # Phase 1 model set
│   └── launch.yaml              # Phase 5 model set
├── prompts/
│   ├── conditions/bare.txt
│   ├── conditions/evaluator.txt
│   └── item_templates/*.jinja
├── src/spinning_arrow/
│   ├── client.py                # OpenRouter wrapper: retries, cost accounting, logging
│   ├── items.py                 # load + validate instruments, hash item sets
│   ├── render.py                # item + condition + permutation + framing -> messages
│   ├── run.py                   # the sweep executor; writes raw JSONL
│   ├── parse.py                 # response -> outcome (answered/refused/hedged/unparseable)
│   ├── score.py                 # scales, reverse-keying, fragility, CIs
│   ├── plots.py                 # matplotlib -> themed SVG
│   └── report.py                # markdown reports for gates
├── tests/
│   ├── fixtures/                # recorded API responses; tests never hit the network
│   └── test_*.py
├── data/
│   ├── raw/<run_id>/*.jsonl.gz  # every response, committed (D7)
│   ├── scores/*.parquet
│   └── manifests/<run_id>.json  # reproducibility record (D15)
├── reports/                     # gate deliverables Sunay reads
├── site/                        # Astro
└── .github/workflows/
    ├── pilot.yml                # manual dispatch
    ├── sweep.yml                # new-model trigger + scheduled drift check
    └── deploy.yml
```

---

## 6. Data contracts

Define these in Phase 0 and do not change them casually — every later phase reads them.

### Response record (`data/raw/<run_id>/*.jsonl.gz`), one per API call

```json
{
  "run_id": "2026-09-02T14:03:11Z__pilot__a3f9c1",
  "ts": "2026-09-02T14:07:33Z",
  "model_id": "openai/gpt-oss-120b",
  "provider_served": "fireworks",
  "instrument": "mfq2",
  "item_id": "mfq2_014",
  "condition": "bare",
  "framing": "third_person",
  "permutation": 3,
  "option_order": ["C", "A", "D", "B", "E"],
  "prompt_hash": "sha256:8f2c...",
  "messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}],
  "raw_response": "C",
  "parsed": { "choice": "A", "valid": true },
  "outcome": "answered",
  "tokens": { "in": 241, "out": 3, "reasoning": 0 },
  "cost_usd": 0.0000094,
  "latency_ms": 812,
  "error": null
}
```

`option_order` records the shuffle so `parsed.choice` can be mapped back to the item's canonical
option. **`parsed.choice` is always canonical, never positional** — getting this wrong silently
inverts every result, so it gets a dedicated test (§10).

`outcome` is one of: `answered`, `refused`, `hedged`, `unparseable`, `error`.

### Score record (`data/scores/*.parquet`)

```json
{
  "run_id": "...",
  "model_id": "openai/gpt-oss-120b",
  "condition": "bare",
  "scale": "mfq2.care",
  "score": 3.82,
  "scale_min": 0.0, "scale_max": 5.0,
  "n_items": 6,
  "n_observations": 60,
  "n_valid": 57,
  "refusal_rate": 0.033,
  "hedge_rate": 0.017,
  "fragility": 0.41,
  "ci_low": 3.55, "ci_high": 4.09,
  "computed_at": "..."
}
```

### Run manifest (`data/manifests/<run_id>.json`) — D15

Item-set hash, prompt-template hashes, panel file hash, exact model IDs, sampling params, git
commit SHA, start/end timestamps, total cost, per-model cost, and counts by `outcome`.

---

## 7. Measurement protocol

### Instruments at launch

All public domain or CC BY (D3). Record license and citation for each in
`instruments/LICENSES.md` — this file is not optional and is the first thing a skeptic reads.

| Instrument | Scales produced | Items | License |
|---|---|---|---|
| **IPIP-NEO-120** | Big Five, 5 domains × 6 facets | 120 | Public domain (explicit, commercial use included) |
| **MFQ-2** (Atari, Graham & Haidt 2023) | Care, Equality, Proportionality, Loyalty, Authority, Purity | 36 | CC BY — attribute |
| **OUS / Greatest Good Benchmark** | Impartial Beneficence, Instrumental Harm | 24 | Published items; GGB extends OUS 10× for LLMs |
| **ETHICS** (Hendrycks et al. 2021) sample | Justice, Deontology, Virtue, Utilitarianism, Commonsense | 120 sampled | **MIT** — verified 2026-08-29 against the repo LICENSE and the HF card. Notice carried in `NOTICE`. |

Target battery ≈ **300 items**. Sample ETHICS with a fixed seed recorded in the manifest.

These four compose cleanly: public domain + CC BY + MIT + published-article items redistribute
as **CC BY 4.0** with notices carried in `NOTICE` (D17). Adding any share-alike or
non-commercial instrument breaks that composition for the whole bank — see D18.

### The sweep, per model

For every item: **5 option permutations × 2 framings × 2 conditions**.

- **Permutations** — shuffle answer-option order; deterministic per `(item_id, permutation)` so
  runs are comparable. This is the position-bias control, and it is also the source of the
  fragility signal, so it is free (D9).
- **Framings** — `third_person` ("Someone believes X…") and `first_person` ("Do you agree that
  X…"). This measures paraphrase sensitivity instead of assuming it away.
- **Conditions** — `bare` and `evaluator` (D11).

Sampling: `temperature: 0`, `max_tokens: 8`, `reasoning: {"enabled": false}` (D5). Where a
provider does not accept a parameter (verified: Sonnet 5 rejects `temperature` and `seed`), omit
it and **record the omission in the manifest** rather than silently substituting a default.

### Scoring

- Reverse-key per each instrument's published key. This is a classic silent-error site — golden
  tests required (§10).
- **Score** = mean over all valid observations for a scale, in the instrument's native units.
- **Fragility** = standard deviation of the per-item scale score across permutations and
  framings, in scale units, normalized to the scale range for cross-instrument comparison.
  Publish both raw and normalized.
- **CI** = bootstrap over items and permutations, 2000 resamples.
- Refusals/hedges are **excluded from the mean but reported as rates** (D10). If
  `n_valid / n_observations < 0.7` for a scale, the score is **suppressed** and shown as
  "insufficient valid responses" rather than published with a wide bar.

### Attention checks

Include ~5% synthetic items with an unambiguous correct answer (e.g. "Select option C"). A model
failing these invalidates the run for that model — report it, do not silently exclude.

---

## 8. Phases and gates

> At every gate: stop, write the deliverable into `reports/`, tell Sunay it is ready, and wait.
> Update `docs/PHASES.md` at each phase close.

### Phase 0 — Access, scaffold, one real call

**Sunay:** the account checklist in §4.

**Agent:**
- Scaffold the repo per §5. `uv` project, `pyproject.toml`, ruff + pytest configured.
- Implement `client.py`: OpenRouter wrapper with retries/backoff, per-call cost accounting from
  the usage block, structured logging, and a hard per-run spend cap that aborts the sweep.
- Implement the §6 data contracts as typed models with validation.
- `make smoke` — one real call to `openai/gpt-oss-120b`, writing a valid response record.
- `.gitignore` covering `.env`, `.DS_Store`, and `__pycache__/` before the first commit.

**Gate 0 — deliverable `reports/00_access.md`**
Sunay reviews: the smoke-call record end to end, the cost figure against OpenRouter's dashboard
(they must agree), and the repo skeleton. Nothing scores yet.

---

### Phase 1 — Pilot probe

The concept test. Small, cheap, and aimed at questions that decide the design. Answer these, do
not build beyond them.

**Panel — `panels/pilot.yaml`** (verified live on OpenRouter 2026-08-29; re-verify before running):

| Model ID | $/M in | $/M out | Why in the pilot |
|---|---|---|---|
| `openai/gpt-oss-120b` | 0.037 | 0.170 | Cheapest credible open model; has logprobs |
| `google/gemini-3.5-flash-lite` | 0.300 | 2.500 | Popular, cheap, **no logprobs** — tests D4 |
| `mistralai/mistral-medium-3.1` | 0.400 | 2.000 | European lab, no logprobs |
| `qwen/qwen3.8-27b` | 0.425 | 2.550 | Popular open weights |
| `meta-llama/llama-3.3-70b-instruct` | 0.710 | 0.710 | The open-weights reference point |
| `anthropic/claude-sonnet-5` | 2.000 | 10.000 | One frontier anchor; **no logprobs/seed/temperature** |

**Battery:** 40 items — 20 MFQ-2, 20 ETHICS deontology. 5 permutations × 2 framings × 1 condition
(`bare`) = **400 calls/model, 2,400 total. Budget $2; expect well under $1.**

**Questions the pilot must answer:**

1. **Parse rate** — what fraction of responses yield a clean choice? Below ~95% on any model
   means the prompt template needs work before scaling.
2. **Refusal rate** by model and by instrument. Is any model unusable on ethics items?
3. **Position bias magnitude** — how much does choice depend on option order? This sets whether
   5 permutations is enough or too few.
4. **Framing sensitivity** — does third- vs. first-person move scores materially?
5. **Fragility has signal** — do models actually *differ* in fragility, or is it noise? If every
   model has the same fragility, the headline metric is dead and the design must change.
6. **Cost reconciliation** — predicted vs. actual, per model. Reconcile to OpenRouter's dashboard.
7. **Latency and rate limits** — what wall-clock does a full sweep imply?

**Gate 1 — deliverable `reports/01_pilot.md`**
Tables for each question above, plus the raw data committed. Include a one-paragraph
recommendation and an explicit list of anything that surprised you.

**Sunay decides:** proceed / adjust battery / adjust panel / rethink the fragility metric. This is
the real go/no-go for the project.

---

### Phase 2 — Full battery and scoring

- Assemble the full ~300-item bank with per-item provenance; write `instruments/LICENSES.md`.
- Implement scoring, reverse-keying, fragility, bootstrap CIs, suppression rule.
- Add the `evaluator` condition (D11) and attention checks.
- Run the full battery on **nine** models: the four major closed-model providers, Meta, Mistral,
  and the Qwen, DeepSeek, and GLM Chinese-model cohort. This Phase 2 expansion was approved at
  Gate 1 on 2026-08-30; each model must still meet D5 at live preflight.

**External validity check — this is the point of the phase.** Compare results against published
findings. Specifically, GGB reports that most LLMs show marked preference for *impartial
beneficence* while rejecting *instrumental harm*. If our pipeline does not reproduce that
qualitative pattern, the pipeline is wrong — investigate before proceeding. Also sanity-check
Big Five scores against published human norms; wildly off-scale values usually mean a
reverse-keying error.

**Gate 2 — deliverable `reports/02_scoring.md`**
Scored output for nine models, the GGB replication check, the norm comparison, refusal and
fragility tables, and the suppression list. Sunay reviews whether the numbers are believable.

---

### Phase 3 — Revealed preference (stated vs. revealed)

The second differentiator. **This phase needs Sunay's editorial judgment before it runs at
scale** — the scenarios are the content, and a bad scenario set discredits the metric.

- Design ~30 short scenarios that put the model in a situation where it must *act* (choose,
  advise, allocate) on the same underlying question a questionnaire item asks about directly.
- Each scenario is explicitly paired to the questionnaire item(s) it mirrors.
- Score the gap: does the model's behavior match its stated position?
- Expect this to be uneven by domain — the 2026 literature finds coherence is selective, strong
  for implicit bias, partial for honesty, absent for sycophancy. Report per-domain, not as one
  number.

**Gate 3a — deliverable `reports/03a_scenarios.md`**: the scenario set as *drafts*, with pairings,
**before** any large run. Sunay edits and approves.
**Gate 3b — deliverable `reports/03b_gap.md`**: gap results on three models.

**Phase 3 budget and run shape.** Gate 3a is design-only and makes no API calls. The default
Gate 3b shape is 30 scenarios × 3 models × 6 deterministic choice-order permutations × 2 surface
forms = 1,080 calls. Based on Phase 2's observed provider usage, the expected cost is `$0.15–$0.50`
for the recommended three-model panel; a live preflight must reconcile the final prompt and
selected models before execution. The hard run cap is `$2`. Expanding the panel or changing that
design requires a new forecast and Sunay approval.

---

### Phase 4 — Site

- Astro static site reading committed Parquet/CSV at build time.
- Two primary evidence routes: a model-first dossier (scores, practical choices, then exact
  recorded answers) and a metric-first comparison (all models on one defined axis, then source
  question and answer). Every summary view must link to its underlying evidence.
- A pattern explorer may show metric-to-metric plots and item-level model-profile similarity. It
  must label correlations as exploratory and descriptive. Lab, model-size, architecture,
  release-date, or training-cutoff comparisons remain readiness views until there are multiple
  comparable models per group and consistently disclosed metadata across both open and closed
  providers.
- Plots as themed SVG from matplotlib (D12). Error bars are visually prominent — they are the
  argument, not decoration.
- `METHODOLOGY.md` written in plain language, including a frank limitations section that states
  the narrow claim from §0 and links the criticisms it answers.
- Deploy to GitHub Pages via Actions. The preferred production arrangement is a dedicated
  `spinningarrow.<Sunay personal domain>` subdomain hosted by GitHub Pages, while the personal
  site's apex remains on Squarespace. At Gate 4, configure the GitHub Pages custom domain first,
  then its corresponding Squarespace DNS record, retain domain verification, and enforce HTTPS.
  Do not use wildcard DNS records.
- **Human response-profile comparison**: a visitor may choose either a concise ten-question or a
  detailed 25–50-question licensed subset and see where their answers sit relative to the published
  model answers to those same individual prompts. Version 1 must score entirely in the browser,
  collect or transmit no answers, and make no diagnostic, moral-quality, or identity claim. It must
  show each question's provenance and say that the comparison is prompt- and instrument-specific.
  Each result must show the five closest response patterns, a visual all-model similarity panel,
  and, on choosing any model, the complete same-question human/model comparison with a link to
  fixed recorded model output for every row.
  Applied technology scenarios (for example, privacy versus security) may only enter the comparison
  after a sourced bank and a corresponding run across every displayed model are committed. Any later
  account, analytics, result-sharing, or server-side collection feature requires a separate consent,
  privacy, retention, and security design before implementation.

**Gate 4 — deliverable: a deployed preview URL** plus `reports/04_site.md` noting anything
unresolved. Sunay reviews design and copy. Domain decision happens here.

---

### Phase 5 — Launch

- Expand `panels/launch.yaml` to ~12 models (not 18 — start narrow). Pinned dated IDs only (D6).
- Full sweep, all conditions. Expected **~$10**.
- Automation:
  - **New-model trigger** — daily Action polls `/api/v1/models` (free, unauthenticated), diffs
    the ID list against the last run, opens an issue and queues a sweep for anything new.
  - **Monthly drift check** — fixed ~15% subset across the panel, ~$1.50; alarm on any score
    moving >2 SE.
  - **Quarterly re-baseline** — one full sweep.
- **Reasoning-on side-study** — 40-item subset, reasoning enabled, on 4 models. Budget $5.
  Publish as a separate view: "does the model answer differently when allowed to think first?"

**Gate 5 — pre-public checklist**, all of which must be true:
- [ ] Every published number links to its raw responses.
- [ ] No score published with `n_valid/n_observations < 0.7`.
- [ ] `instruments/LICENSES.md` complete; every item's provenance and citation of record verified against the source.
- [ ] `LICENSE`, `LICENSE-DATA`, and `NOTICE` present; README states which covers what (D17).
- [ ] No CC BY-NC-SA material anywhere in the main item bank (D18).
- [ ] Methodology page states the narrow claim and its limitations without hedging or overclaiming.
- [ ] No aliased model IDs anywhere in the panel (D6).
- [ ] Prior work cited and linked: TrackingAI, values.safe.ai, llm_morality, SpeechMap, GGB, ETHICS.
- [ ] Röttger et al. credited by name on the front page and methodology page (D16).
- [ ] OpenRouter key spend limit confirmed still set (D13).
- [ ] Repo public, no secrets in history.
- [ ] Sunay has read the front page as a skeptical outsider would.

---

## 9. Cost model

Per-model sweep at 300 items × 5 permutations × 2 framings × 2 conditions = 6,000 calls,
~240 input tokens and ~6 output tokens each → ~1.44M in, ~0.04M out.

| Phase | Scope | Expected |
|---|---|---|
| 0 | smoke calls | < $0.01 |
| 1 | pilot, 6 models × 400 calls | **< $1** |
| 2 | full battery × 9 models | ~$18 provisional; reforecast before execution |
| 3 | scenarios × 3 models | ~$3 |
| 5 | full launch sweep, 12 models | ~$10 |
| — | steady state: new-model sweeps + monthly drift | **~$4/month** |

Ceiling $30/month (D13), enforced by the key's spend limit. Every run writes its actual cost to
its manifest; reconcile against OpenRouter's dashboard at Gates 0, 1, and 5.

**The one way this budget breaks:** reasoning tokens left enabled turns a ~$2 frontier sweep into
~$32. `reasoning: {"enabled": false}` is not optional in the main path, and the run should abort
if a response returns nonzero reasoning tokens outside the side-study.

---

## 10. Testing requirements

Tests never hit the network — record fixtures under `tests/fixtures/` and replay.

**Required before Gate 1:**
- `test_option_mapping` — a shuffled response maps back to the correct **canonical** option.
  Property-based over all permutations. This is the highest-consequence bug in the codebase: get
  it wrong and every result inverts silently while looking completely plausible.
- `test_parse_outcomes` — golden fixtures for each `outcome` class, including real refusal and
  hedge text harvested from the pilot.
- `test_cost_accounting` — computed cost matches a known usage block exactly.
- `test_prompt_render` — golden files for rendered prompts; any change to a template shows as a
  diff in review rather than silently altering results.
- `test_spend_cap` — the run aborts when the cap is hit.

**Required before Gate 2:**
- `test_reverse_keying` — per instrument, a synthetic all-max respondent scores at the ceiling on
  every scale. Catches sign errors.
- `test_permutation_invariance` — given identical underlying choices, the score is identical
  across permutations. Fragility on that input must be exactly 0.
- `test_suppression` — a scale below the validity threshold is suppressed, not published.
- `test_manifest_roundtrip` — a run is fully reconstructible from its manifest (D15).

---

## 11. Risks

| Risk | Mitigation |
|---|---|
| **Position/framing effects swamp real signal** — fragility is large for every model and the metric is uninformative. | This is Gate 1 question 5. If it fires, pivot the headline to refusal patterns + stated-vs-revealed and demote scale positions to secondary. Better to learn this for $1 than after launch. |
| **Silent option-mapping inversion** | `test_option_mapping`, plus manual verification of 20 records by hand at Gate 1. |
| **Contamination** — the public item bank becomes training data and scores drift for that reason. | Hold out 15% of items, never published, as a contamination canary. Divergence between public and held-out scores over time is the signal. Note in methodology. |
| **A model is scored through a different upstream provider between runs** and results shift. | `provider_served` is recorded per call; flag runs where it changed. |
| **"You're claiming models have ethics"** — the predictable public criticism. | The §0 framing, stated everywhere, and the fragility index as the headline. This criticism is anticipated and answered by the design; do not let copy drift back into overclaiming. |
| **Instrument licensing challenged** | D3, D17, D18 + `instruments/LICENSES.md`. Nothing ships without recorded provenance. Launch bank is public domain / CC BY / MIT only. |
| **Cost overrun** | Key spend limit (D13) — a hard stop that does not depend on code being correct. |
| **Human comparison is mistaken for a diagnosis or silently collects sensitive responses** | Phase 4 v1 is local-only, uses clear non-diagnostic language, and does not transmit answers. Any data collection is a separately approved privacy feature. |

---

## 12. Open questions for Sunay

Do not block on these; they come due at the gate noted.

1. **Production hostname** — the preferred deployment is a GitHub Pages subdomain of Sunay's
   Squarespace-managed personal domain, preserving the existing Squarespace apex. Select the exact
   subdomain and verify the DNS/HTTPS setup at **Gate 4**.
2. **Scenario content** for Phase 3 — how adversarial should the dilemmas be? Trolley-style
   abstractions, or mundane advice situations? Mundane probably measures deployment behavior
   better; abstractions are more legible to readers. Due at **Gate 3a**.
3. **Panel membership** — 12 models is the recommendation. Which 12, and how are open-weight vs.
   frontier balanced? Due at **Gate 5**.
4. **Publication posture** — is this a personal project page, or does it get announced somewhere
   (LessWrong, HN)? Affects tone of the methodology page. Due at **Gate 4**.

---

## Appendix — Reference reading

**Prior art (study before building):**
- llm_morality leaderboard — https://wassname.github.io/llm_morality/ (nearest existing thing; open source)
- SpeechMap.ai — https://speechmap.ai/ (the product model to imitate)
- TrackingAI — https://trackingai.org/about
- CAIS AI Values Dashboard — https://values.safe.ai/ · Utility Engineering — https://arxiv.org/abs/2502.08640
- Value Compass Leaderboard — https://arxiv.org/abs/2501.07071

**Methodology (these shaped the design; read before Phase 1):**
- Political Compass or Spinning Arrow? — https://arxiv.org/abs/2402.16786
- Rethinking Psychometric Evaluation of LLMs — https://arxiv.org/abs/2606.12730
- The Personality Illusion — https://arxiv.org/pdf/2509.03730
- Human Psychometric Questionnaires Mischaracterize LLM Behavior — https://arxiv.org/pdf/2509.10078

**Instruments:**
- IPIP public-domain permission — https://ipip.ori.org/newPermission.htm
- MFQ-2 validation — https://www.sciencedirect.com/science/article/pii/S0191886923002623
- Greatest Good Benchmark — https://arxiv.org/abs/2503.19598
- ETHICS — https://github.com/hendrycks/ethics
- Awesome-LLM-Psychometrics — https://github.com/ValueByte-AI/Awesome-LLM-Psychometrics

**API:**
- OpenRouter models + pricing — https://openrouter.ai/models · `GET https://openrouter.ai/api/v1/models` (free, unauthenticated)
