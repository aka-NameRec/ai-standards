---
title: 'Migration plan: context architecture classification (issue #17)'
permalink: ai-standards/artifacts/2026-09-21-context-architecture-migration-plan
---

# Migration plan: context architecture classification (issue #17)

Status: complete (2026-09-21, branch `rules-change/17-rule-engineering`).
Phase 4 of the change plan
`docs/artifacts/2026-09-19-rule-engineering-change-plan.md`: the formal
placement model ships as the `context-architecture` feature, the current
self-hosted `AGENTS.md` is classified against it, and the migration plan is
recorded — **with no physical moves performed in this phase**.

## What Shipped

- Feature `context-architecture` (`process/context-architecture.md`):
  the seven-layer placement model, the ordered placement questions with the
  latest-loading tie-break, and the control-plane invariant with the
  reduction gate (`CA-001`–`CA-005` in `rule_map.toml`).
- Uniqueness note: the placement principle inside the Rule Engineering flow
  (`RE-006`) and this feature's rules are principle and instrument, not
  duplicates — `RE-006` records the in-flow step, `CA-002`–`CA-003` are the
  formal questions that step consults. Precedence: the questions decide.

## Classification Of The Self-Hosted AGENTS.md

Measured at 63,530 bytes / 37 sections before this feature renders (the
feature adds one section). Dispositions use the placement model:

| Group | Sections | Layer today | Disposition |
|---|---|---|---|
| Core invariants (Engineering Workflow, Completion Discipline, DRY, Git Workflow, Architecture & Layering, Error Handling, Language & Communication) | 8 | always-loaded | keep — universal invariants, the control plane by definition |
| Routing, gates, governance (Retrieval Routing, Autonomy Boundaries, Session Hygiene, Agent Usage Hygiene, Design-First + Planning, Reasoning Hygiene, Module Contract Discovery Gate) | 7 | always-loaded | keep — routing rules and mandatory gates are control-plane content; prose compression only, as M2/M3 below |
| Knowledge-layer policy (Basic Memory Usage, Project Memory, Chroma Usage) | 3 | always-loaded | keep — policy for operating retrieval layers is routing; mechanics already live in skills/adapters |
| Engineering-artifact policy (Structured Artifacts, Change Plans, Module Contracts, Decision Records, Canonical Documentation policies, Optional Maps, Rejected Formalism, Knowledge Capture) | 8 | always-loaded | keep — durable policy; long enumerations are M3 compression candidates |
| Review workflow (Code Review) | 1 | always-loaded | **M1 — prime relocation candidate**; a conditional task-specific procedure with a natural-language trigger |
| Initiative features (Rule Engineering, Context Architecture) | 2 | always-loaded | keep — process invariants |
| Stack (Python Stack) | 1 | always-loaded | keep — project-level conditioning (the project chose the stack); not per-task knowledge |
| Self-hosted overrides (Documentation Language Policy, Documentation Scope, Workflow, Issue Tracker Language, Release Workflow) | 5 | always-loaded | keep — by definition project knowledge, but the rendered file is this repository's delivery vehicle for its own rules |

## Migration Plan (executed in Phase 8, not now)

Each move is gated: baseline vs candidate behavior comparison on the recorded
scenarios (`docs/scenarios/CR-001`–`CR-003` plus later additions), executed by
`ai-standards-evals` (issue #18). A move without a passing comparison is
rejected.

- **M1 — Code Review procedural body → skill reference.** Always-loaded keeps
  the reporting invariants (evidence, no-padding, marker semantics, shape
  pointer); the pass-by-pass procedure moves into the
  `standard-code-review` skill's reference. Prerequisite: Phase 7 activation
  evals show the skill triggers reliably on bare review requests across at
  least two harnesses.
- **M2 — Module Contract Discovery Gate details → skill reference.** The gate
  itself (mandatory at edit time) stays always-loaded as a routing rule; the
  coverage criteria and reporting detail move to a reference loaded when the
  gate fires. Prerequisite: same eval gate.
- **M3 — Prose compression pass** over the longest always-loaded sections
  (report shape enumerations, artifact-policy enumerations): same content,
  fewer tokens; gated by the same comparisons.

## Non-Goals

- No fragment moves, deletions, or renderer changes in Phase 4.
- No downstream-project changes: adopters are unaffected until they enable the
  feature and run their own classification.

## Verification

- `uv run pytest` (including the new feature render/fragment tests and the
  rule-map policy tests for `CA-*`)
- `uv run ai-sync render --project-root .` idempotent; `ai-sync doctor`
  zero errors
- The classification above is re-derivable: section list via `rg -n '^## ' AGENTS.md`
