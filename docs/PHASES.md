# PHASES — state machine

The single place where current state is tracked. [SPEC.md](../SPEC.md) is the contract and does
not change as work progresses; this file does. Update it at every phase close, and at any gate
that returns a decision.

**Current phase: 4 — site.**
**Blocking on:** Phase 4 design and deployment work has not begun.

---

## Phase 0 — Access, scaffold, one real call

**Planned:** repo scaffold, OpenRouter client with cost accounting, data contracts, `make smoke`.
**Gate 0 deliverable:** `reports/00_access.md`
**Status:** approved 2026-08-29
**Shipped:** `pyproject.toml` + `uv.lock`; ruff and pytest; validated response, score, and manifest
contracts; OpenRouter client with retries, usage-cost accounting, structured logging, reasoning-token
guard, and a pre-request run spend-cap reservation; `make smoke`; tests and a recorded API fixture.
**Open:** —

## Phase 1 — Pilot probe

**Planned:** 6 cheap-but-popular models × 40 items; answer the seven design questions in SPEC §8.
**Gate 1 deliverable:** `reports/01_pilot.md` — the real go/no-go.
**Status:** approved 2026-08-30
**Shipped:** The completed clean pilot is recorded in
`reports/01_pilot.md` at run `20260830T060547Z__pilot__3258fb` (2,400 calls; `$0.17570126`
from raw OpenRouter usage). `mistralai/mistral-medium-3.1`, `qwen/qwen3.8-27b`,
`meta-llama/llama-3.3-70b-instruct`, and `anthropic/claude-sonnet-5` achieved 98–100% clean
parse. The two pilot-only mandatory-reasoning exceptions did not: GPT-OSS was 65.2% and Gemini
was 68.5%. The six-model panel was re-verified live. OpenRouter currently requires reasoning for
`openai/gpt-oss-120b` and `google/gemini-3.5-flash-lite`; Sunay authorized a narrowly scoped,
explicitly recorded exception for these two *Phase 1 pilot* entries only. All other pilot requests
remain reasoning-disabled or explicitly omit an unsupported `reasoning` parameter, and this does
not change the Phase 2+ main-battery policy. The first 8-token exception-model attempt was stopped
after 461 checkpointed calls because reasoning consumed the final-answer allowance; the clean retry
uses recorded 64- and 512-token exception-model ceilings and records usage even when content is empty.
**Open:** —

## Phase 2 — Full battery and scoring

**Planned:** ~300-item bank, scoring + fragility + CIs, GGB replication check on a nine-model
coverage panel.
**Gate 2 deliverable:** `reports/02_scoring.md`
**Status:** approved 2026-08-30
**Panel selected and live-reverified 2026-08-30:**

| Coverage | Pinned OpenRouter ID | D5 handling |
|---|---|---|
| OpenAI | `openai/gpt-5.4-mini` | `reasoning: {"enabled": false}` |
| Google | `google/gemini-2.5-flash-lite` | `reasoning: {"enabled": false}` |
| Anthropic | `anthropic/claude-sonnet-5` | `reasoning: {"enabled": false}`; omit unsupported sampling fields |
| xAI | `x-ai/grok-4.20` | `reasoning: {"enabled": false}` |
| Meta | `meta-llama/llama-3.3-70b-instruct` | omit unsupported `reasoning` field |
| Mistral | `mistralai/mistral-medium-3.1` | omit unsupported `reasoning` field |
| Alibaba | `qwen/qwen3.8-27b` | `reasoning: {"enabled": false}` |
| DeepSeek | `deepseek/deepseek-v4-pro-0813` | `reasoning: {"enabled": false}` |
| Z.ai | `z-ai/glm-5.2` | `reasoning: {"enabled": false}` |

**Shipped:** Run `20260830T155412Z__phase2__8fbf10` completed all 56,700 planned calls (6,300 per
model) across the nine-model panel. The live preflight forecast was `$15.577002` against a `$20`
forecast guardrail and `$25` hard run cap; raw OpenRouter-recorded cost was `$5.37804276152`.
The main battery recorded zero reasoning tokens. The reproducible evidence bundle includes the
raw JSONL, run manifest, derived score tables, [written scoring report](../reports/02_scoring.md),
and self-contained [visual dashboard](../reports/02_scoring.html). Scores with under 70% valid
cell coverage are suppressed; 896 responses are retained as unparseable and 9 as refusals rather
than silently scored. GPT-OSS, Gemini 3.5 Flash Lite, GLM 5.3, and Grok 4.6 remain excluded
because their current mandatory-reasoning configuration cannot carry into the D5 main battery.
**Open:** —

## Phase 3 — Revealed preference

**Planned:** ~30 paired behavioral scenarios; stated-vs-revealed gap.
**Gate 3a:** `reports/03a_scenarios.md` (approved scenario slate)
**Gate 3b:** `reports/03b_gap.md`
**Status:** approved and complete 2026-08-30
**Shipped:** Gate 3a's approved 30 scenarios and their versioned scoring contract are committed in
`instruments/phase3_scenarios.yaml` and `instruments/phase3_contract.json`. Gate 3b run
`20260830T230045Z__phase3__74142b` completed its planned 1,080 calls (360 per model) across
Llama 3.3 70B Instruct, Mistral Medium 3.1, and Claude Sonnet 5. The live preflight forecast was
`$0.372485` against a `$1` forecast guard and `$2` hard cap; raw-record cost was `$0.12358666`.
All responses parsed as choices and all reported zero reasoning tokens. The durable evidence bundle
includes raw JSONL, a manifest, preflight, derived tables, [gap report](../reports/03b_gap.md), and
[visual report](../reports/03b_gap.html). The report intentionally excludes ethics-reference
agreement from directional concordance because reference accuracy is not an action-direction scale.
**Open:** —

## Phase 4 — Site

**Planned:** Astro static site, themed SVG plots, methodology page, GitHub Pages deploy.
**Gate 4 deliverable:** deployed preview URL + `reports/04_site.md`. Domain decided here.
**Status:** in progress — local preview ready for review
**Shipped:** The first mobile-first Astro preview is in `site/`. It reads committed Phase 2 and 3
evidence at build time, offers model and scale drill-downs, and exposes one fixed, documented raw
answer per model/question/condition rather than loading the entire raw archive on a phone. The
browser-only human profile form now offers a ten-question quick route and a 33-question detailed
route; both compare only with each model's average answer to the same prompts, identify each
source, store and transmit no answers, and make no diagnostic or moral-quality claim. The visual
direction is deliberately minimal: warm paper, moss, clay, restrained metrics, and progressively
disclosed methodology. `.github/workflows/deploy-site.yml` is ready for a public GitHub Pages
project site after review; it is not yet deployed or connected to DNS.
**Open:** Sunay’s questionnaire/content and visual review; then enable GitHub Actions Pages,
deploy the preview, and add the `spinning-arrow.sunaybhat.me` domain and verification records in
Squarespace/GitHub. Privacy/security/technology scenarios remain a separately sourced and
evaluated follow-on, not an unsupported claim in the current form.

## Phase 5 — Launch

**Planned:** 12-model panel, full sweep, new-model trigger + drift automation, reasoning-on
side-study.
**Gate 5:** the pre-public checklist in SPEC §8.
**Status:** not started

---

## Decisions returned at gates

Record here what Sunay decided at each gate, with the date, so a cold session can see how the
design moved without re-reading every report.

- **2026-08-29 — name settled.** The project is **Spinning Arrow**, after Röttger et al.,
  *"Political Compass or Spinning Arrow?"* (ACL 2024). Repo `spinning-arrow`, package
  `spinning_arrow`. Attribution is required on the site (SPEC D16). Domain remains open, due at
  Gate 4.

- **2026-08-29 — licensing settled.** Dual-licensed: Apache-2.0 for code, CC BY 4.0 for data,
instruments, reports, and prose (SPEC D17). `LICENSE`, `LICENSE-DATA`, and `NOTICE` are in the
repo. ETHICS confirmed MIT. OEJTS excluded from the item bank on license grounds (D18).

- **2026-08-29 — Gate 0 approved.** The real `openai/gpt-oss-120b` smoke call produced a valid,
  committed raw record and manifest at a recorded cost of `$0.00001145`; Sunay confirmed the
  result and authorized Phase 1. The unscored smoke-only mandatory-reasoning exception remains
  documented in `reports/00_access.md`; Phase 1 battery calls remain reasoning-disabled.

- **2026-08-29 — Phase 1 reasoning exception approved.** OpenRouter's live metadata reports
  mandatory reasoning for `openai/gpt-oss-120b` and `google/gemini-3.5-flash-lite`. Sunay approved
  including both in the six-model pilot with the lowest supported reasoning effort, recording the
  configuration and any reasoning-token cost in every raw record and manifest. This is limited to
  the pilot and does not change D5 for the Phase 2+ main battery.

- **2026-08-30 — Gate 1 report ready.** The clean 2,400-call pilot completed at
  `20260830T060547Z__pilot__3258fb` with all raw records, a manifest, and
  `reports/01_pilot.md` committed. Actual raw-record cost was `$0.17570126`. Gate 1 remains
  pending Sunay’s decision; Phase 2 has not started.

- **2026-08-30 — Gate 1 approved.** Sunay closed Phase 1 after reviewing the pilot. Phase 2 may
  select only from the four strict-D5 candidates: Mistral Medium 3.1, Qwen 3.8 27B, Llama 3.3 70B
  Instruct, and Claude Sonnet 5. GPT-OSS 120B and Gemini 3.5 Flash Lite remain pilot-only
  mandatory-reasoning exceptions and are excluded from the main battery.

- **2026-08-30 — Phase 2 panel expanded.** Sunay selected a nine-model full-battery coverage
  panel: OpenAI, Google, Anthropic, xAI, Meta, Mistral, Qwen, DeepSeek, and Z.ai. This supersedes
  the original three-model Phase 2 scope. Live OpenRouter metadata confirms the recorded IDs can
  run with reasoning disabled (or omit an unsupported reasoning parameter); GLM 5.3 and the newest
  Gemini and Grok flagships are excluded because reasoning is mandatory.

- **2026-08-30 — Phase 2 collected; Gate 2 pending.** The strict-D5 main battery completed as
  run `20260830T155412Z__phase2__8fbf10`: 56,700 calls, 6,300 per model, `$5.37804276152` in raw
  OpenRouter-recorded cost, and zero reasoning tokens. The report and visual dashboard are ready
  for review; this records no Gate 2 decision and does not authorize Phase 3.

- **2026-08-30 — Gate 2 approved; Phase 3 started.** Sunay reviewed the Phase 2 battery and
  approved advancing to Gate 3a. Phase 3 begins with drafted, paired behavioural scenarios only;
  no model calls occur until Sunay edits and approves that scenario set. The default Gate 3b
  design is 1,080 calls on three models with an expected `$0.15–$0.50` cost and a `$2` hard cap.

- **2026-08-30 — Gate 3a approved; Phase 3 completed.** Sunay approved the scenario slate,
  six choice-order permutations, direct/advice surface controls, the Llama/Mistral/Claude contrast
  panel, and the conservative interval rule. The live preflight forecast `$0.37248480`; the full
  run `20260830T230045Z__phase3__74142b` completed 1,080 calls at `$0.12358666`, with 100% clean
  parsing and zero reasoning tokens. Gate 3b results are in `reports/03b_gap.md` and
  `reports/03b_gap.html`; Phase 4 may begin.

- **2026-08-30 — Gate 3b approved.** Sunay reviewed the completed Phase 3 evidence bundle and
  accepted the results. Phase 3 is formally closed; Phase 4 is authorized to begin when requested.

- **2026-08-30 — Phase 4 deployment and human-comparison direction.** The preferred live-site
  arrangement is a GitHub Pages subdomain beneath Sunay's Squarespace-managed personal domain.
  A future human response-profile comparison belongs to Phase 4 and must begin as local-only
  browser scoring with no answer collection, diagnostic claim, or user ranking.

- **2026-08-30 — Phase 4 questionnaire curation.** Sunay requested a fast and a deeper human
  response path, both using more nuanced sourced prompts and scenario cases. The site now uses a
  10-question quick path and a 33-question detailed path, with exact item-level comparison to all
  nine models. The completed bank contains no evaluated technology privacy/security dilemmas, so
  those are deferred until a public source and a corresponding full-panel run are approved.
