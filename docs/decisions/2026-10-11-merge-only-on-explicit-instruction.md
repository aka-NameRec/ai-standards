---
title: 'DECISION: merge-only-on-explicit-instruction'
permalink: ai-standards/decisions/2026-10-11-merge-only-on-explicit-instruction
---

# DECISION: merge-only-on-explicit-instruction

Russian localized version: [2026-10-11-merge-only-on-explicit-instruction.ru.md](2026-10-11-merge-only-on-explicit-instruction.ru.md)

## Status

Accepted — supersedes the landing clause of
[[DECISION: adopt-autonomous-task-run-skill]]

## Date

2026-10-11

## Context

The `autonomous-task-run` skill shipped in 2.8.0 with procedure step 9 reading
"Merge the branch into the target by the project standard", alongside step 10
forbidding push without explicit approval. The user caught this in the
post-release review (issue #25): step 10 is correct, step 9 is not. Far from
every developer holds merge rights to the main lines — `develop` and `main`
are commonly protected branches — so an autonomous run must never end with a
merge of its own accord. The work ends at the final commit; merging is a
human order, and so is pushing.

## Decision

1. An autonomous run ends at the final commit on the working branch: session
   knowledge captured, checks green. That is the completion state.
2. Merging the branch into the target — and deleting the merged branch —
   happens only on the human's explicit instruction, executed then by the
   project standard (for this ecosystem, the `merge-by-standard` flow).
3. Push keeps its standing rule: never without the user's explicit approval,
   including `main`.
4. The completion report names merge and push among the items awaiting the
   human's instruction, unless the instruction was already given in the run's
   mandate (for example, a prompt that explicitly orders the merge).

## Why

- Landing someone else's work into a protected line is a privilege, not an
  assumption: the skill must work for contributors without merge rights.
- It resolves the latent tension with the shared rule that commits, pushes,
  and pull requests happen only when explicitly requested; a step ordering an
  autonomous merge was the one remaining violation.
- The end state — final commit, captured knowledge, green checks — is fully
  reviewable and hands the human the landing decision with everything ready.

## Alternatives Considered

### Keep merge-by-default, gate only on protected branches

Rejected: the agent would need to predict branch protection and permissions,
which vary per repository and change over time; the human knows the rights
model, the agent does not.

### Allow autonomous merge but require a post-merge report

Rejected: the blast radius lands before the review; `autonomy-boundaries`
treats the main lines as sensitive areas, and undoing a merge is not a cheap,
predictable rollback.

### Leave it project-local (a cockpit rule)

Rejected: the flaw is in the portable skill text itself; every downstream
project would inherit the wrong default.

## Consequences

### Benefits

- The skill is usable by contributors without merge rights and safe on
  repositories with protected main lines.
- Landing decisions stay with the human, consistent with push discipline and
  the `merge-by-standard` trigger model.

### Trade-offs

- Runs that used to end "fully landed" now end one instruction short; the
  human issues the merge (and push) order explicitly.
- Scenario `ATR-001` had to pin that a merge may happen only because the
  prompt ordered it, adding one forbidden outcome to check.

## Observations

- [decision] An autonomous run completes at the final commit on the working
  branch — knowledge captured, checks green — never with a merge of its own
  accord.
- [decision] Merging into the target branch and deleting the merged branch
  are human-ordered steps executed by the project standard.
- [fact] Step 10 (push) was already correct; only the landing clause of the
  2.8.0 skill needed the correction.

## Relations

- supersedes [[DECISION: adopt-autonomous-task-run-skill]]
- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Worksheet: autonomous-task-run skill authoring and task spec]]
- relates_to [[Scenario ATR-001: slice loop with task-spec conformance]]
