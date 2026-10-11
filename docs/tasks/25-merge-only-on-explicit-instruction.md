---
title: 'Task 25: merge-only-on-explicit-instruction'
permalink: ai-standards/tasks/25-merge-only-on-explicit-instruction
---

# Task 25: merge-only-on-explicit-instruction

## Status

Completed on the feature branch
`feature/25-merge-only-on-explicit-instruction`; landed into `main` and
released as 2.8.1 on the user's explicit order (the approved plan mandated
the landing and the release).

## Scope

- Corrected the `autonomous-task-run` landing order (issue #25): the run ends
  at the final commit on the working branch — knowledge captured, checks
  green; merging into the target branch, and deleting the merged branch,
  happens only on the human's explicit instruction, by the project standard.
  Push discipline (step 10) unchanged.
- Reworded procedure step 9, the Completion Report, and Non-goals in all
  three adapter forms of the skill template.
- Traced the correction: `ATR-006` (completion state) and `ATR-007` (landing
  order) reworded in `rule_map.toml`; scenario `ATR-001` (EN/RU) pins that a
  merge happens only because the prompt orders it, with a new forbidden
  outcome for unordered merges and pushes.
- Knowledge capture: decision record
  `docs/decisions/2026-10-11-merge-only-on-explicit-instruction.md` (EN/RU,
  superseding the landing clause of the adoption decision), addendum in the
  authoring worksheet, this task record, CHANGELOG entry.
- Released as 2.8.1 (patch per the user's decision).

## Verification

- `uv run pytest` (153 passed, including the updated skill-invariants test)
- `uv run mypy scripts/`: clean
- `uv run ai-sync render --project-root .` idempotent
- `uv run ai-sync doctor --project-root .`: zero errors, no new warnings

## Related Artifacts

- [../decisions/2026-10-11-merge-only-on-explicit-instruction.md](../decisions/2026-10-11-merge-only-on-explicit-instruction.md)
- [../artifacts/2026-10-11-autonomous-task-run-authoring.md](../artifacts/2026-10-11-autonomous-task-run-authoring.md)
- Upstream request: aka-NameRec/ai-standards issue #25

## Observations

- [decision] The landing-and-release step of this very task was executed under
  the corrected rule: the approved plan was the human's explicit instruction
  to land and publish.
- [fact] The skill released in 2.8.0 carried the flawed landing clause; the
  correction ships as 2.8.1.

## Relations

- implements [[DECISION: merge-only-on-explicit-instruction]]
- relates_to [[Worksheet: autonomous-task-run skill authoring and task spec]]
- localized counterpart of [[Задача 25: merge только по явной инструкции]]
