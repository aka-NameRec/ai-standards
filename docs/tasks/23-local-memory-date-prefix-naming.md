---
title: 'Task 23: local-memory date-prefix naming'
permalink: ai-standards/tasks/23-local-memory-date-prefix-naming
---

# Task 23: local-memory date-prefix naming

## Status

Completed on the feature branch
`feature/23-local-memory-date-prefix`, merged into `main`.

## Scope

- Adopted one naming standard for the local memory area
  (`YYYY-MM-DD-<topic>.md`, the notation of canonical dated artifacts) in the
  `project-memory` fragment; the target function is the promotion path — a
  local note keeps its file name when promoted into canonical documentation.
- Narrowed the two clauses that exempted the local area from dated naming:
  `project-memory` Note Shape And Durable Lessons and `basic-memory` Note
  Shape.
- Added rule `PM-001` to `rule_map.toml` and the behavioral scenario contract
  `docs/scenarios/PM-001-local-note-date-prefix.md` (EN/RU).
- Added the `ai-sync doctor` report-only check `local-note-without-date-prefix`
  (WARNING, never auto-fixed per the ai-sync module contract) with tests.
- Renamed the self-hosted non-conforming `docs/local/**` notes opportunistically.
- Prepared the repository release metadata for version `2.8.0`.

## Verification

- `uv run pytest` (unit and structural tests, including the new
  `local-note-without-date-prefix` doctor tests)
- `uv run mypy scripts/`
- `uv run ai-sync render --project-root .` leaves a clean worktree
- `uv run ai-sync doctor --project-root .` reports zero errors

## Related Artifacts

- [../decisions/2026-10-11-local-memory-date-prefix-naming.md](../decisions/2026-10-11-local-memory-date-prefix-naming.md)
- [../scenarios/PM-001-local-note-date-prefix.md](../scenarios/PM-001-local-note-date-prefix.md)
- Upstream request: aka-NameRec/ai-standards issue #23

## Observations

- [decision] The naming rule's target function is the promotion path: a local
  note named in the canonical notation moves into canonical documentation
  under the same file name.
- [fact] The candidate rule from issue #23 conflicted with two standing
  clauses that exempted local memory from dated naming; both were narrowed in
  the same change set.

## Relations

- implements [[DECISION: local-memory-date-prefix-naming]]
- relates_to [[Scenario PM-001: local note naming on create]]
- relates_to [[Module Contract: scripts/ai_sync.py]]
- localized counterpart of [[Задача 23: дата-префикс именования локальной памяти]]
