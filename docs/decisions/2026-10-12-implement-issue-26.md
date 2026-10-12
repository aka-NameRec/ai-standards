---
title: 'DECISION: implement issue 26'
permalink: ai-standards/decisions/2026-10-12-implement-issue-26
---

# DECISION: implement issue 26

Russian localized version: [2026-10-12-implement-issue-26.ru.md](2026-10-12-implement-issue-26.ru.md)

## Status

Accepted

## Date

2026-10-12

## Context

Issue #26 (verified user feedback on 2.8.1, archived as
`docs/archive/2026-10-12-ai-standards-2.8.1-defects.md`, task record
`docs/tasks/26-verified-user-feedback-2-8-1.md`) confirms six defects: the
code-review pass procedure deploys only for kilo; the `autonomous-task-run`
commit clause contradicts `capture-knowledge`; the autonomous knowledge-capture
step ignores project features and hard-codes `docs/tasks/`; the autonomous
branch shape is fixed in the skill instead of the project's rules; the
`basic-memory` fragment still blanket-exempts `docs/local/**` from
canonical-note rules and carries a dangling section cross-reference; and
`update-ai-standards` deploys new skills bound to already-enabled features
silently, before its announcement step. The user accepted the six-direction
proposal (D1–D6) on 2026-10-12.

## Decision

1. **D1 — shared procedure reference.** Move the pass procedure to a new
   infra template deployed as `.ai-standards/references/standard-code-review-procedure.md`,
   gated on the `code-review` feature (the M4/M5 pattern). All four
   `standard-code-review` variants reference the shared path; the kilo skill's
   private `references/procedure.md` is dropped; the fragment pointers are
   updated. Acceptance: after `ai-sync sync-templates` in a project with
   `tooling.agents = ["codex", "claude", "cursor", "kilo"]`, every deployed
   `standard-code-review` copy references an existing file, and the
   "Safe to fix without asking" list resolves for each agent.
2. **D2 — commit-approval reconciliation.** The standing-approval precedence
   (adoption decision point 3) is surfaced at both rule sites: the
   `capture-knowledge` "Never" clause gains the autonomous-run exception
   (commits under the run's standing approval; pushing stays always explicit),
   and `core/git-workflow` gains the explicit exception line. Acceptance: the
   two texts name the exception, and no wording weakens the push rule.
3. **D3 — feature-conditional knowledge capture.** `autonomous-task-run`
   step 7 and the completion condition require only the parts the project's
   enabled features define; skipped parts are recorded in the completion
   report; the entry gate requires knowing the enabled capture targets. The
   task-records directory becomes project-configurable via
   `[knowledge_capture] tasks_tree` (default `tasks`), documented in the
   manifest template and referenced by the fragment and the skill (the
   `[project_memory] local_tree` pattern); ai-sync does not consume the key
   yet. Acceptance: a project without `knowledge-capture`/`project-memory`
   gets an executable step 7 whose skips are reported, and the manifest
   template documents the key.
4. **D4 — branch naming defers to project rules.** Step 1 defers to the
   project's branch rules with `<purpose>/<task_id>-<slug>` as the shared
   default shape, mirroring step 6's commit wording. Acceptance: the skill
   no longer mandates the shape unconditionally.
5. **D5 — narrowed local-memory exemption.** The `basic-memory` genre bullet
   exempts only canonical-note body requirements (`## Observations`,
   `## Relations`, frontmatter shape) — the date-prefix naming applies — and
   the dangling "see Project Memory" cross-reference is dropped. Acceptance:
   the fragment no longer contradicts the narrowed 2.8.0 state and renders
   no reference to a section a `basic-memory`-only project lacks.
6. **D6 — confirmed deployment of new skills on upgrade.** `ai-sync
   sync-templates` gains a plan mode (`--plan`) listing the files it would
   create, update, or remove without writing; the upgrade procedure runs the
   plan first and requires the user's confirmation before applying when the
   plan creates skill or workflow files for already-enabled features; text
   refreshes of existing deployments stay silent. Acceptance: the plan mode
   is covered by tests, and the upgrade skill text requires confirmation
   before applying a plan that creates new skill files.

Rule-text and template changes follow the merge-gate rule: the branch merges
into `main` only with an attached `ai-standards-evals` comparison. Version
bumping stays a human-decided release step (`docs/decisions/2026-10-12-release-versioning-human-decided.md`).

## Why

- D1 reuses the established progressive-disclosure deployment path instead of
  per-adapter copies: one source, one deployed path every agent already reads
  (`.ai-standards/references/`), and the failure mode of 2.6.0 cannot recur
  for a new adapter.
- D2 removes a normative conflict instead of annotating one side of it; Rule
  Engineering requires conflicts to carry explicit precedence where the rules
  live.
- D3 and D4 make the autonomous procedure configurable by the same mechanisms
  the standards already have (manifest keys, project rules) instead of
  hard-coding project policy in a portable skill.
- D5 restores the invariant the 2.8.0 decision intended and removes a
  cross-reference that renders dangle-prone text.
- D6 fixes the ordering problem (deploy happens before announce) with a
  deterministic preflight instead of adding manifest surface.

## Alternatives Considered

### D1: per-adapter procedure copies inside each skill directory

Rejected: four sources of truth for one procedure; the 2.6.0 defect showed
adapter parity is not maintained by hand.

### D1: move the procedure back into `AGENTS.md`

Rejected: contradicts the control-plane invariant and reverses the accepted
M1 relocation.

### D2: change only `capture-knowledge`

Rejected: `core/git-workflow` would still hide the exception from every agent
that runs autonomously without the skill text at hand.

### D3: refuse to start a run when `knowledge-capture` is off

Rejected: capture remains possible ad hoc; blocking the run trades a missing
optional feature for a blocked task.

### D6: per-template manifest opt-out key

Deferred: it adds configuration surface without removing the surprise; the
ordering fix addresses the reported behavior. Revisit if confirmed-noise
skills accumulate.

## Consequences

### Benefits

- One procedure source for all four agents; the 2.6.0 regression class
  (dangling skill references) is structurally closed.
- No normative conflict between the autonomous run and the capture/git rules.
- Autonomous runs stay executable in projects with partial feature sets.
- Upgrades can no longer silently deploy behavior-changing skills.

### Trade-offs

- `ai-sync` grows a plan mode and the upgrade skill grows a confirmation
  step: slightly more ceremony on every upgrade.
- The `[knowledge_capture] tasks_tree` key is agent-level until ai-sync
  consumes it; doctor does not validate the relocated directory yet.
- The eval gate is a landing prerequisite, so the fix cycle carries the usual
  comparison cost.

## Observations

- [decision] The code-review pass procedure becomes a shared
  `.ai-standards/references/` deployment gated on `code-review`, referenced
  by all four `standard-code-review` variants.
- [decision] The autonomous-run standing approval covers commits, never
  pushes, and is stated in `core/git-workflow`, `capture-knowledge`, and the
  `autonomous-task-run` skill consistently.
- [decision] Autonomous knowledge capture and branch naming defer to what the
  project enables and declares, with the shared defaults documented in the
  skill texts.
- [fact] Issue #26 confirmed all six reported defects; none was rejected
  during verification.

## Relations

- relates_to [[Task 26: verified user feedback on 2.8.1]]
- relates_to [[DECISION: adopt-autonomous-task-run-skill]]
- relates_to [[DECISION: local-memory-date-prefix-naming]]
- relates_to [[DECISION: release-versioning-human-decided]]
- localized counterpart of [[РЕШЕНИЕ: реализация issue 26]]
