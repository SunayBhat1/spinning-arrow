# PHASES — state machine

The single place where current state is tracked. [SPEC.md](../SPEC.md) is the contract and does
not change as work progresses; this file does. Update it at every phase close, and at any gate
that returns a decision.

**Current phase: 1 — pilot probe in progress.**
**Blocking on:** implementation and execution of the six-model pilot, then Sunay’s Gate 1
go/no-go decision.

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
**Status:** in progress
**Open:** The six-model panel was re-verified live. OpenRouter currently requires reasoning for
`openai/gpt-oss-120b` and `google/gemini-3.5-flash-lite`; Sunay authorized a narrowly scoped,
explicitly recorded exception for these two *Phase 1 pilot* entries only. All other pilot requests
remain reasoning-disabled or explicitly omit an unsupported `reasoning` parameter, and this does
not change the Phase 2+ main-battery policy. The first 8-token exception-model attempt was stopped
after 461 checkpointed calls because reasoning consumed the final-answer allowance; the clean retry
uses recorded 64- and 512-token exception-model ceilings and records usage even when content is empty.

## Phase 2 — Full battery and scoring

**Planned:** ~300-item bank, scoring + fragility + CIs, GGB replication check on 3 models.
**Gate 2 deliverable:** `reports/02_scoring.md`
**Status:** not started

## Phase 3 — Revealed preference

**Planned:** ~30 paired behavioral scenarios; stated-vs-revealed gap.
**Gate 3a:** `reports/03a_scenarios.md` (drafts, before any large run — needs Sunay's edits)
**Gate 3b:** `reports/03b_gap.md`
**Status:** not started

## Phase 4 — Site

**Planned:** Astro static site, themed SVG plots, methodology page, GitHub Pages deploy.
**Gate 4 deliverable:** deployed preview URL + `reports/04_site.md`. Domain decided here.
**Status:** not started

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
