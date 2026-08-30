# PHASES — state machine

The single place where current state is tracked. [SPEC.md](../SPEC.md) is the contract and does
not change as work progresses; this file does. Update it at every phase close, and at any gate
that returns a decision.

**Current phase: 0 — Gate 0 open.**
**Blocking on:** Sunay completing the account checklist in SPEC.md §4, creating/pushing the
public Git repository, and reviewing one real smoke-call record.

---

## Phase 0 — Access, scaffold, one real call

**Planned:** repo scaffold, OpenRouter client with cost accounting, data contracts, `make smoke`.
**Gate 0 deliverable:** `reports/00_access.md`
**Status:** scaffold and offline verification complete; real smoke call not yet run
**Shipped:** `pyproject.toml` + `uv.lock`; ruff and pytest; validated response, score, and manifest
contracts; OpenRouter client with retries, usage-cost accounting, structured logging, reasoning-token
guard, and a pre-request run spend-cap reservation; `make smoke`; tests and a recorded API fixture.
**Open:** No local Git repository/committed revision is present, and no `.env` OpenRouter key is
available to this workspace. `make smoke` correctly stops before network access. See
[`reports/00_access.md`](../reports/00_access.md).

## Phase 1 — Pilot probe

**Planned:** 6 cheap-but-popular models × 40 items; answer the seven design questions in SPEC §8.
**Gate 1 deliverable:** `reports/01_pilot.md` — the real go/no-go.
**Status:** not started

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
