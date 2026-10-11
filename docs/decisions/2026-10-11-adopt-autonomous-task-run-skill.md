---
title: 'DECISION: adopt-autonomous-task-run-skill'
permalink: ai-standards/decisions/2026-10-11-adopt-autonomous-task-run-skill
---

# DECISION: adopt-autonomous-task-run-skill

Russian localized version: [2026-10-11-adopt-autonomous-task-run-skill.ru.md](2026-10-11-adopt-autonomous-task-run-skill.ru.md)

## Status

Accepted

## Date

2026-10-11

## Context

Issue #24 captured a recurring practice from tasks #22–#23: the user approves
a plan and instructs the agent to work autonomously until done, merge into
`main` by the standard, capture knowledge first, and commit without
per-commit approval. The invariants live in `autonomy-boundaries` and
`session-hygiene`, but the procedure — entry gate, slice loop, conformance
checks against requirements, landing order — was assembled from chat each
time. During the issue discussion the user fixed five additional normative
points: a verifiable task spec (an ADR where the project uses that form) with
per-requirement acceptance criteria; a slice-level plan verified before
start; a slice-end conformance check against the requirements; requirements
as the absolute constant of the run (no add, change, or reinterpretation);
and a stop with a detailed report on any unresolvable contradiction or
blocker.

## Decision

1. Adopt the `autonomous-task-run` skill, gated on the `autonomy-boundaries`
   feature, deployed for codex, cursor, claude, and kilo.
2. The skill's entry gate, procedure, stop conditions, completion report, and
   non-goals follow the issue #24 candidate as verified through Rule
   Engineering; the authoring worksheet with per-clause verdicts is
   `docs/artifacts/2026-10-11-autonomous-task-run-authoring.md`.
3. Two wording adaptations were accepted: the requirements artifact is named
   "task spec (an ADR where the project uses that form)" for portability, and
   the commit rule is paired with a precedence clause — the instruction to
   run autonomously is the standing approval of the commit flow, which keeps
   the skill co-satisfiable with the shared commit-approval rule.
4. Normative content is traced as `ATR-001`–`ATR-007` in `rule_map.toml`,
   with behavioral scenario contracts `ATR-001`, `ATR-002` and trigger set
   `TRG-003` in `docs/scenarios/` (execution belongs to `ai-standards-evals`,
   issue #18).
5. The `autonomy-boundaries` fragment gains one pointer line to the deployed
   skill; its normative content is otherwise unchanged.

## Why

- The skill layer loads the procedure exactly when the trigger phrase appears,
  instead of keeping always-loaded procedural detail (Context Architecture).
- The five user points close the two failure modes the #22–#23 runs actually
  risked: requirements drift during a long run, and silent requirement
  rewording to force convergence.
- Report-only verification is impossible for a procedure; the scenario
  contracts give the procedure its behavioral validation form.

## Alternatives Considered

### Encode the procedure in the always-loaded autonomy-boundaries fragment

Rejected: task-specific operational detail violates the control-plane
invariant (CA-004); the fragment keeps the invariants, the skill keeps the
steps.

### Keep assembling the run from chat each time

Rejected: the #23 run needed the user to restate the full contract (commits
without approval, merge to main, knowledge capture first) — exactly the
repetition a skill exists to remove.

### Gate the skill on a new dedicated feature

Rejected: `autonomy-boundaries` already owns long-execution rules and is the
natural gate; a new feature would add surface without changing who loads it.

## Consequences

### Benefits

- One repeatable procedure for autonomous runs across projects and agents.
- Requirements immutability and slice conformance become named, evaluable
  rules (`ATR-002`–`ATR-004`).
- The commit-approval deviation is written down with its precedence instead
  of living in chat history.

### Trade-offs

- The skill duplicates the scenario-contract obligation: until
  `ai-standards-evals` executes ATR-001/ATR-002, validation is structural
  only.
- Adapter deployment adds four template files and registry entries to
  maintain per adapter syntax.

## Observations

- [decision] The `autonomous-task-run` skill ships gated on
  `autonomy-boundaries` with the entry gate, slice conformance loop,
  requirements immutability, stop conditions, and landing order from issue
  #24.
- [decision] Requirements of a task spec are the absolute constant of a run:
  no add, change, or reinterpretation; a fix needing either is a stop
  condition.
- [fact] Two wording adaptations were accepted for portability and
  precedence: "task spec (an ADR where the project uses that form)" and the
  standing-approval commit clause.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Worksheet: autonomous-task-run skill authoring and task spec]]
- relates_to [[Scenario ATR-001: slice loop with task-spec conformance]]
- relates_to [[Scenario ATR-002: stop on requirements change]]
