---
title: 'Task 26: implement issue 26'
permalink: ai-standards/tasks/26-implement-issue-26
---

# Task 26: implement issue 26

## Status

Implemented on the branch `rules-change/26-implement-issue-26` under the
`autonomous-task-run` procedure (user instruction 2026-10-12: implement
autonomously). The run ends at the final commit on the working branch;
merging into `main` — which additionally requires the `ai-standards-evals`
comparison per the merge-gate rule — and pushing wait for the human's
explicit instruction.

## Scope

All six accepted directions from
[../decisions/2026-10-12-implement-issue-26.md](../decisions/2026-10-12-implement-issue-26.md):

- **D1** — `standard-code-review.procedure.md` moved to the shared infra
  template `templates/standard-code-review-procedure.reference.md`, deployed
  as `.ai-standards/references/standard-code-review-procedure.md` (gated on
  `code-review`); the kilo-private deployment entry removed and its
  destination added to `RETIRED_TEMPLATE_DESTINATIONS`; all four
  `standard-code-review` variants and both fragment pointers now reference
  the shared path; regression test pins that every deployed copy references
  an existing file (`scripts/ai_sync.py`, `tests/test_ai_sync.py`).
- **D2** — the autonomous-run exception added to `core/git-workflow` and to
  the `capture-knowledge` "Never" clause in all three adapters; pushing
  stays without exceptions.
- **D3/D4** — `autonomous-task-run` entry gate item 4, step 1, step 7, and
  the completion condition reworded in all three adapters: capture follows
  the project's enabled features with skips reported, the branch shape
  defers to project rules with the shared default; `[knowledge_capture]
  tasks_tree` documented in `templates/project_manifest.toml`; the
  `knowledge-capture` fragment and `capture-knowledge` adapters reference
  the configurable task-records directory; `rule_map.toml` updated
  (`ATR-001`, `ATR-006`, `ATR-007` reworded, `ATR-008` added) with invariant
  tests pinning the new clauses.
- **D5** — `fragments/tools/basic-memory.md` exempts only canonical-note
  body requirements and drops the dangling "see Project Memory"
  cross-reference.
- **D6** — `ai-sync sync-templates` gained `--plan` (plan computing refactored
  into `_plan_agent_template`/`plan_project_templates`/`_plan_retired_templates`);
  the `update-ai-standards` upgrade step 5 in all three adapters runs the
  preflight and requires confirmation for new skill/workflow files;
  `docs/standards-update-usage.md`/`.ru.md` updated; three plan-mode tests
  added (creates without writing, up-to-date after apply, retired reported
  without removal).
- CHANGELOG `[Unreleased]` carries the Fixed/Changed entries.

Commits: `477ce5f` (decision record), `3a179d8` (D1), `d85412c` (D2),
`fe72cdb` (D3/D4), `e616c48` (D5), `9f2815b` (D6), plus this record.

## Verification

- `uv run pytest`: 157 passed.
- `uv run mypy scripts/`: clean.
- `uv run ai-sync render --project-root .`: idempotent.
- `uv run ai-sync doctor --project-root .`: zero errors (pre-existing
  warnings unchanged).
- Live smoke of the plan mode: `--plan` on a fixture project lists
  `Planned create` lines without writing; apply creates them; a second
  `--plan` reports everything up to date.
- Known pre-existing lint debt, untouched by this task: `ruff check .`
  reports 6 errors in `templates/ai-infrastructure/scripts/code_index.py`
  and 1 `E501` in `tests/test_ai_sync.py`; both fail identically on the
  base commit.
- Not run (landing prerequisite, not part of this slice): the
  `ai-standards-evals` comparison required by the merge-gate rule for
  branches touching `fragments/**`/`templates/**`.

## Related Artifacts

- [../decisions/2026-10-12-implement-issue-26.md](../decisions/2026-10-12-implement-issue-26.md)
- [26-verified-user-feedback-2-8-1.md](26-verified-user-feedback-2-8-1.md)
- Upstream request: aka-NameRec/ai-standards issue #26

## Observations

- [fact] The implementation changed only rule texts, deployment tables, and
  the sync script; no eval scenario contracts were rewritten, and the eval
  comparison remains the open landing prerequisite.
- [fact] The plan mode reuses the apply path's content computation, so
  planning and applying cannot diverge.

## Relations

- implements [[DECISION: implement issue 26]]
- relates_to [[Task 26: verified user feedback on 2.8.1]]
- localized counterpart of [[Задача 26: реализация issue 26]]
