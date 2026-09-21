---
title: 'DECISION: rule traceability map design'
type: decision
permalink: ai-standards/decisions/2026-09-19-rule-traceability-design
---

# DECISION: rule traceability map design

## Status

- Accepted

## Date

- 2026-09-19

## Context

Phase 2 of the adopted Rule Engineering initiative (decision record
`docs/decisions/2026-09-19-adopt-rule-engineering-initiative.md`) requires a
stable link `rule ↔ source ↔ expected behavior ↔ eval scenarios` for rules
that evals reference, with IDs kept out of rendered `AGENTS.md` and usable by
tooling only. Constraints verified in the repository: the renderer strips
leading frontmatter from fragments (`scripts/ai_sync.py`, `_load_fragment`),
so fragment frontmatter never leaks into the render — but frontmatter is
per-file and cannot address an individual rule inside a fragment; `docs/` is
the Basic Memory knowledge tree where non-Markdown files draw
`non-note-data-file-inside-knowledge-tree` doctor warnings; `registry.toml` is
the feature/stack catalog per the `ai-sync` module contract.

## Decision

Rule traceability lives in a dedicated root-level `rule_map.toml`:

- one table per rule keyed by a stable ID (`<PREFIX>-<NNN>`, e.g. `RE-001`);
  an ID is never reused for a different rule, and retiring a rule keeps its ID
  reserved;
- each entry binds the ID to `fragment` (path under `fragments/`), `section`
  (a heading inside that fragment anchoring the normative text), `behavior`
  (a one-line statement of the expected observable behavior), and `scenarios`
  (eval scenario IDs from the `ai-standards-evals` specification, issue #18;
  empty until Phase 3+ produces scenarios);
- policy tests in `tests/test_rule_map.py` are the map's deterministic
  validation: well-formed unique IDs, existing fragments and sections,
  well-formed behaviors and scenario references, and no rule ID in the
  rendered `AGENTS.md`;
- seeded with `RE-001`–`RE-006` covering the `rule-engineering` feature
  fragment.

## Why

- A single tooling metadata home at the configuration layer (beside
  `registry.toml`, outside the knowledge tree) keeps IDs usable by eval
  tooling while structurally unable to reach rendered output.
- Section-heading anchors give stable, human-checkable locations without
  inline markers in prose.
- The policy tests make the map itself verifiable — the same
  observable-behavior requirement the standard imposes on rules.

## Alternatives Considered

- Frontmatter on fragment files: per-file only — cannot identify individual
  rules; also reserved by design for knowledge-base indexer stamping.
- IDs inline in rendered prose: would leak IDs into every enabling project's
  context, against the Phase 2 requirement.
- A section inside `registry.toml`: mixes the feature/stack catalog named by
  the `ai-sync` module contract with per-rule metadata.

## Consequences

- Benefits: every eval-bearing rule gets a stable, test-verified anchor;
  scenario work in Phase 3+ and in `ai-standards-evals` (#18) can reference
  concrete IDs; the question "which tests cover this rule?" becomes answerable
  from the map.
- Costs or tradeoffs: each new eval-bearing rule must be added to the map;
  renaming a heading requires a map update (caught by tests); the
  `ai-standards-evals` runner must agree on scenario ID format (deferred to
  #18).

## Affected Modules

- `rule_map.toml` (new, repository root)
- `tests/test_rule_map.py` (new policy tests)
- `fragments/process/rule-engineering.md` (referenced, unchanged)

## Invariants And Constraints

- Rule IDs never render into `AGENTS.md` (enforced by a policy test).
- An ID is never reused for a different rule.
- The map stays at the configuration layer, outside the `docs/` knowledge tree.
- Scenario execution semantics remain with `ai-standards-evals` (issue #18);
  the map only reserves references.

## Verification

- `uv run pytest tests/test_rule_map.py` (five policy tests)
- `uv run ai-sync render --project-root .` stays idempotent
- `uv run ruff check` / `uv run mypy scripts/` clean

## Related Artifacts

- Parent decision: `docs/decisions/2026-09-19-adopt-rule-engineering-initiative.md`
- Change plan: `docs/artifacts/2026-09-19-rule-engineering-change-plan.md` (Phase 2)
- Issue #18 (`ai-standards-evals` specification) — scenario ID consumer
