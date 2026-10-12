---
name: autonomous-task-run
description: Run an approved plan end-to-end autonomously — entry gate with a verifiable task spec and a slice-level plan, slice-by-slice conformance checks against immutable requirements, stop conditions, knowledge capture, merge by project standard. Use when the user asks to «работай автономно до завершения», «автономно по плану с последующим слиянием», "work autonomously until done", or "run the approved plan end-to-end".
---

# Autonomous Task Run

Execute an approved plan without per-step supervision, then land the result by
the project standard. Long autonomous execution stays an exception governed by
the project's autonomy rules; this procedure is how a run satisfies them.

## Entry Gate

Every condition is mandatory; without any one of them, do not start — request
exactly what is missing:

1. The plan is approved by the user and captured in an artifact.
2. A detailed, verifiable task spec formalizes the requirements (an ADR where
   the project uses that form). Every requirement carries an observable
   acceptance criterion — a command, a test, or a checkable rubric — so the
   outcome is verifiable without asking the requirement's author.
3. The plan is detailed into slices, and this was checked before starting:
   every slice is small, coherent, and has its own way of being verified. A
   plan that does not decompose into such slices is a reason to request a
   re-slice, not to start.
4. The repository, the task id, and the merge-target branch are known; the
   target project's `AGENTS.md` and working memory are loaded. The
   knowledge-capture targets the project enables are known.

## Procedure

1. Create a working branch by the project's branch rules, from the
   merge-target branch; the shared default shape is
   `<purpose>/<task_id>-<slug>`.
2. Execute the slices in order; verify every risky change with the most
   targeted check before moving on.
3. At the end of each slice, check the result against the task-spec
   requirements by their acceptance criteria, and record the conformance in
   the slice report — this is the guard against requirements drift.
4. Fix detected drift only while the fix literally serves the existing
   requirements. A "fix" that would require adding, changing, or
   reinterpreting a requirement is not a fix — it is a stop condition.
5. The task-spec requirements are the absolute constant of the run: never add
   to, change, or reinterpret them.
6. Commit without pausing for per-commit message approval: the instruction to
   run autonomously is the standing approval of the commit flow. Commit
   messages still follow the project's standard form.
7. Before merging, capture the session knowledge the standard way — the
   parts the project's enabled features define: the `capture-knowledge`
   skill when it is deployed, a local working-memory update when the
   project maintains one. Record every part the project does not enable
   in the completion report, with the reason.
8. Run the project's full verification (tests, lint, type checks, render or
   doctor where applicable).
9. End the run at the final commit on the working branch: knowledge captured,
   checks green. Merge the branch into the target only when the human
   explicitly orders it, then by the project standard; the same instruction
   governs deleting the merged branch.
10. Never push to any remote without the user's explicit approval — including
    the main branch.

## Stop Conditions

Stop and ask the user — with a detailed report, not a resume attempt — when:

- a task-spec requirement cannot be met the way it is written;
- fixing drift would require adding, changing, or reinterpreting a
  requirement;
- the work contradicts the agreed plan, scope, or the requirements contradict
  each other;
- slice verification stops converging: repeated fixes do not stabilize the
  result;
- any blocker prevents starting or finishing the next slice.

The stop report states the current state, what was tried, which requirement
(by its id in the task spec) is blocked, and the options for moving on.

## Completion Report

End the run with: what changed, each slice's conformance to the requirements,
which checks ran with results, and what remains (merge, push, downstream
tasks). The run is complete when the branch carries the final commit, every
slice conforms to its acceptance criteria, checks are green, knowledge is
captured to the extent the project's enabled features define, and the
report is posted in chat — merging and pushing wait for
the human's explicit instruction.

## Non-goals

No scope expansion; no changes to requirements; no merging and no push
without the human's instruction; no writes to canonical documentation beyond
the knowledge capture itself.
