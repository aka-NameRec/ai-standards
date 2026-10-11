---
title: 'Task 24: autonomous-task-run skill'
permalink: ai-standards/tasks/24-autonomous-task-run-skill
---

# Task 24: autonomous-task-run skill

## Status

Completed on the feature branch
`feature/24-autonomous-task-run-skill`, merged into `main`.

## Scope

- Adopted the `autonomous-task-run` skill (issue #24): entry gate with a
  verifiable task spec and a pre-flight slice check, slice-end conformance
  checks, requirements immutability (no add/change/reinterpret), stop
  conditions with a detailed stop report, commit/push rules, knowledge
  capture, merge by standard.
- Authored the skill templates in all four adapter forms and registered the
  deployment gated on the `autonomy-boundaries` feature.
- Added one pointer line to the `autonomy-boundaries` fragment.
- Traced the rules as `ATR-001`–`ATR-007` in `rule_map.toml`; scenario
  contracts `ATR-001`, `ATR-002` (behavior) and `TRG-003` (trigger set) in
  `docs/scenarios/` (EN/RU); execution belongs to `ai-standards-evals`.
- Knowledge capture: decision record, authoring worksheet/task spec artifact,
  local-memory progress note (all EN/RU where canonical), CHANGELOG entry.
- Prepared the repository release metadata for version `2.9.0`; the bump was
  subsequently reverted — the version increases only when a release is cut,
  and the release moment is a human decision.

## Verification

- `uv run pytest` (including the new deployment-registry and skill-invariants
  tests, rule-map and scenario policy tests)
- `uv run mypy scripts/`
- `uv run ai-sync sync-templates --project-root .` deploys the skill adapters
- `uv run ai-sync render --project-root .` leaves a clean worktree
- `uv run ai-sync doctor --project-root .` reports zero errors

## Related Artifacts

- [../decisions/2026-10-11-adopt-autonomous-task-run-skill.md](../decisions/2026-10-11-adopt-autonomous-task-run-skill.md)
- [../artifacts/2026-10-11-autonomous-task-run-authoring.md](../artifacts/2026-10-11-autonomous-task-run-authoring.md)
- [../scenarios/ATR-001-slice-loop-conformance.md](../scenarios/ATR-001-slice-loop-conformance.md)
- Upstream request: aka-NameRec/ai-standards issue #24

## Observations

- [decision] The run itself executed through the new skill's procedure
  (dogfooding): task spec before start, slices with targeted verification,
  knowledge capture before merge.
- [fact] Scenario execution for `ATR-001`/`ATR-002`/`TRG-003` remains with
  `ai-standards-evals` and was not run in this task.

## Relations

- implements [[DECISION: adopt-autonomous-task-run-skill]]
- relates_to [[Worksheet: autonomous-task-run skill authoring and task spec]]
- localized counterpart of [[Задача 24: навык autonomous-task-run]]
