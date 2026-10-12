---
title: 'Task 26: verified user feedback on 2.8.1'
permalink: ai-standards/tasks/26-verified-user-feedback-2-8-1
---

# Task 26: verified user feedback on 2.8.1

## Status

Completed: the feedback is archived, all six findings verified against
`main` at `50ab280`, and the results filed as Russian-language issue #26
(https://github.com/aka-NameRec/ai-standards/issues/26).

## Scope

- Archived the incoming user feedback verbatim as
  [../archive/2026-10-12-ai-standards-2.8.1-defects.md](../archive/2026-10-12-ai-standards-2.8.1-defects.md).
  Source context: a devcats project updated from 2.5.0 to 2.8.1 with agents
  `claude` and `cursor`; features `code-review`, `autonomy-boundaries`,
  `knowledge-capture`, `basic-memory` enabled, `project-memory` disabled.
- Verified all six findings; none was rejected:
  1. `standard-code-review.procedure.md` deploys only for `kilo`
     (`AGENT_TEMPLATES` in `scripts/ai_sync.py`); the `codex` copy references
     a missing `references/procedure.md`, `claude`/`cursor` copies point at
     the slimmed `AGENTS.md` — the safe-to-fix list, the review-then-fix
     order, the realistic-data-volumes rule, and the Correctness
     boundary-reading line exist only in the procedure since `34baa19` (M1,
     2.6.0).
  2. `autonomous-task-run` step 6 (standing commit-flow approval) contradicts
     the `capture-knowledge` "Never" clause on step 7; the precedence clause
     lives only in the adoption decision and the skill text.
  3. Step 7 requires knowledge capture regardless of the `knowledge-capture`
     and `project-memory` features; the `docs/tasks/` location is hard-coded
     with no manifest key.
  4. Step 1 fixes the branch shape instead of deferring to project rules, as
     steps 6 and 9 do for commits and merges.
  5. `fragments/tools/basic-memory.md` still blanket-exempts `docs/local/**`
     from canonical-note rules, contrary to the narrowed 2.8.0 state (issue
     #23), and its Note Shape cross-reference "see Project Memory" dangles
     when `project-memory` is off.
  6. `update-ai-standards` Upgrade step 5 deploys templates (including new
     skills bound to enabled features) silently, before the step-6
     announcement and step-7 confirmation; no per-template manifest opt-out
     exists.

## Verification

- Introduction claims: `meta.toml` release `2.8.1`/`2026-10-11`; tag
  `2.8.1-2026-10-11` exists; post-tag commits (`45daf97`, `ca08731`,
  `50ab280`) touch only `CHANGELOG.md` and decision/task documents.
- Every finding checked in repository source (templates, fragments,
  `scripts/ai_sync.py`, `registry.toml`, `CHANGELOG.md`, decision records),
  not from the diff; `aa7ac33` (2026-09-01) confirmed as the last touch of
  the `claude`/`cursor` code-review templates.
- No behavioral runs were executed for the affected skills; the eval suite
  (`ai-standards-evals`) is not exercised by this task.

## Related Artifacts

- [../archive/2026-10-12-ai-standards-2.8.1-defects.md](../archive/2026-10-12-ai-standards-2.8.1-defects.md)
- Upstream request: aka-NameRec/ai-standards issue #26

## Observations

- [fact] All six findings of the feedback were confirmed by source reading;
  the report carries no rejections or downgrades.
- [fact] The verification covered rule texts and the deployment table only;
  no behavioral scenario from `ai-standards-evals` was run against the
  affected skills.

## Relations

- relates_to [[DECISION: adopt-autonomous-task-run-skill]]
- relates_to [[DECISION: local-memory-date-prefix-naming]]
- localized counterpart of [[Задача 26: верифицированный отзыв пользователя о 2.8.1]]
