---
title: 'Change plan: Rule Engineering initiative (issue #17)'
permalink: ai-standards/artifacts/2026-09-19-rule-engineering-change-plan
---

# Change plan: Rule Engineering initiative (issue #17)

Status: in progress. Branch `rules-change/17-rule-engineering`.
Source proposal: `docs/archive/20260917-000618-proposal-rule-engineering-skill-engineering-context-architecture-evals.md`.
Accepted decision: `docs/decisions/2026-09-19-adopt-rule-engineering-initiative.md`.
Baseline: `docs/artifacts/2026-09-19-rule-engineering-baseline.md`.

## Goal

Shift `ai-standards` from accumulating instructions to managing their lifecycle
and context: one Rule Engineering process for every normative rule regardless
of source, a formal context placement model, a single Skill Engineering domain,
and behavior-level verification — with executable eval infrastructure kept
separate in the `ai-standards-evals` specification (issue #18).

## Scope

Phased; this branch delivers Phase 0 and Phase 1 only:

- Phase 0 (this branch): baseline artifact (repository measures, current
  review behavior, candidate scenarios).
- Phase 1 (this branch): new feature `rule-engineering` — fragment
  `process/rule-engineering.md`, registry entry with `feature_meta` `2.5.0`,
  usage guides (both languages), render test. The README `Import External
  Rules` flow is restated as a special case of Rule Engineering. Existing
  rules are not mass-rewritten.
- Phase 2 (later): rule traceability — stable rule IDs in source/eval metadata
  only, `rule ↔ source ↔ expected behavior ↔ scenarios` support.
- Phase 3 (later): Rule Engineering dogfooding on `standard-code-review`.
- Phase 4 (later): `context-architecture` feature with the formal placement
  model; classification of current `AGENTS.md` content; migration plan without
  physical moves.
- Phase 5 (later): scenario format contract under `docs/scenarios/`; runner
  implementation belongs to #18.
- Phase 6 (later): `skill-engineering` domain; `skill-authoring` created
  through Rule Engineering (mandatory dogfooding).
- Phase 7 (later): skill activation/effect eval scenario sets.
- Phase 8 (later): `AGENTS.md` minification, each move gated by regression evals.
- Phase 9 (later): cross-agent compatibility matrix.

## Out Of Scope

- Everything assigned to issue #18: scenario runner, harness adapters,
  baseline/candidate execution, cross-agent execution.
- Physical migration of `AGENTS.md` content (Phase 8) and mass rewriting of
  existing rules (explicitly excluded from Phase 1).
- Splitting `skill-engineering` into separate skills without usage/eval data.

## Touched Modules (Phases 0–1, this branch)

- `fragments/process/rule-engineering.md` (new)
- `registry.toml` (feature entry, `feature_meta` `2.5.0`)
- `docs/rule-engineering-usage.md` + `.ru.md` (new)
- `docs/artifacts/2026-09-19-rule-engineering-baseline.md` + `.ru.md` (new)
- `docs/decisions/2026-09-19-adopt-rule-engineering-initiative.md` + `.ru.md` (new)
- `ai.project.toml` (self-hosting: enable the feature)
- `AGENTS.md` (re-rendered)
- `tests/test_ai_sync.py` (render + fragment tests)
- `README.md` / `README.ru.md` (feature groups, `Import External Rules` reframe, usage section)
- `CHANGELOG.md` (Unreleased entry)

## Intended Structure

The fragment carries the always-required normative core: when the flow
applies, the nine rule quality properties, the interpretation surface
concept, the engineering flow, and context placement principles. Detailed
checklists and worked examples stay in the usage guides so the rendered
section stays compact.

## Risks

- Fragment growth against context economy — mitigation: fragment stays near
  4 KB; detail lives in usage docs.
- Duplication with the README import flow — mitigation: the import section
  routes through Rule Engineering instead of restating methodology.
- Version pin: `feature_meta` points at `2.5.0`, which must match the version
  the next release actually receives (adjusted at `bump-version` if needed).

## Invariants

- Existing rules keep their behavior; no mass rewrite in Phase 1.
- Shared policy stays vendor-neutral; no harness-specific mechanics in shared rules.
- The `ai-sync` module contract is preserved: no renderer changes; the new
  feature is pure content over existing inputs.
- `AGENTS.md` growth from this change is limited to the new section and is
  justified by it.

## Verification

- `uv run pytest` (including the new render/fragment tests)
- `uv run mypy scripts/`
- `uv run ai-sync render --project-root .` idempotency (clean worktree after re-render)
- `uv run ai-sync doctor --project-root .` reports zero errors
- Baseline numbers remain reproducible (byte/line counts re-measurable)

## Outcome

Filled after implementation if the plan meaningfully guided the work:
Phase 0 and Phase 1 delivered on this branch — baseline recorded; feature
`rule-engineering` shipped (fragment, registry `2.5.0`, usage guides en/ru,
self-hosting enabled, render/fragment tests, README/CHANGELOG alignment, import
flow restated as a Rule Engineering special case). Phases 2–9 remain open with
their own artifacts to come.
