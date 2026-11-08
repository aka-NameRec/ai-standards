---
title: 'DECISION: add cherry-pick-assessment skill'
permalink: ai-standards/decisions/2026-11-08-add-cherry-pick-assessment-skill
---

# DECISION: add cherry-pick-assessment skill

Russian localized version: [2026-11-08-add-cherry-pick-assessment-skill.ru.md](2026-11-08-add-cherry-pick-assessment-skill.ru.md)

## Status

- Proposed (issue #27, stage 1; behavioral execution belongs to
  `ai-standards-evals` per issue #18)

## Date

- 2026-11-08

## Context

During a long `staging` stabilization period, the business requests selective
transfer of commit groups from `develop`. Git conflicts and a successful build
do not prove dependency completeness or semantic compatibility: mandatory
companion commits, cross-service contract changes, migrations, and consumer
reactions can be missed. Listing source SHAs by hand is error-prone — typos,
rebase-stale hashes, forgotten fix/revert companions, wrong order — and the
assessment skill itself must analyze history (already-transferred equivalents,
partial carries, rollbacks), so it can resolve "what to transfer" into a
concrete ordered SHA list itself. A separate read-only skill
`cherry-pick-assessment` gives a checkable pre-transfer verdict with
controlled stopping; it does not approve a release and does not shift analysis
to QA/QC/AF.

## Decision

1. **A standalone read-only skill** `cherry-pick-assessment` assesses one
   specific candidate set against one specific target branch state, before
   any transfer. Verdicts: PASS / REVIEW / STOP with the most restrictive
   outcome winning (STOP > REVIEW > PASS).
2. **Input is selector-based, resolved, and confirmed.** The user states what
   to transfer — task ids, a merge request, a source branch, a commit range,
   explicit SHAs, or a mix — and names the source repository and the target
   branch. The skill resolves the selectors into an ordered SHA list from Git
   data, includes provable companion commits (fixes, revert pairs sharing the
   task id) in the candidate set, presents the resolved list (SHA, subject,
   order, target HEAD) and proceeds only after the user confirms it.
3. **Selection discipline.** A selector that resolves ambiguously (task id
   matching unrelated commits, ambiguous merge-base, merge commit without a
   clear primary parent line) and is not clarified by the user is a STOP. A
   selector may only widen, never silently shrink, the candidate set.
4. **Validity binding.** The verdict is valid only for the confirmed SHA
   list, its order, and the target HEAD it was computed against. Any change
   to those invalidates it (re-resolution + re-assessment); a fresh
   resolution never reuses a stale verdict.
5. **Boundaries.** The analysis never mutates the real branches: no recorded
   cherry-pick, conflict resolution committed to the target, merge, push,
   rebase, or reset; trial application only in a safe isolated throwaway
   tree; no production approval.
6. **Execution split.** Performing the transfer stays outside this skill and
   remains a possible future skill.

## Why

- Selector-based input removes the hand-listed-SHA failure class and reuses
  what the assessment already must do (history analysis) to define the
  object; the confirmation step keeps the strict validity binding without
  making the human enumerate hashes.
- Reusable pre-transfer assessment makes missed dependencies visible,
  separates the developers' technical verdict from the release owner's risk
  decision, and produces a repeatable report for GitLab.
- No findings is not proof of safety; PASS means admission to a controlled
  transfer, not to a release.

## Alternatives Considered

- Automatic cherry-pick + successful build: does not prove semantic
  compatibility.
- Always full regression: expensive, and does not name the missed dependency.
- Numeric risk scoring: false precision without calibration.
- Folding into normal code review: different triggers and completion
  criteria; a separate procedure is cleaner.
- Human-enumerated SHAs as the only input (the original issue draft):
  error-prone, duplicates work the skill performs anyway, and contradicts the
  companion-completeness goal.

## Consequences

### Benefits

- Checkable grounds for transfer or stop; repeatable report tied to exact
  SHAs and the target HEAD.
- One resolution step removes the typo/stale-hash/forgotten-companion class
  before analysis starts.

### Costs Or Tradeoffs

- One extra confirmation round per assessment; selector resolution reads
  history and several services; REVIEW cases need support; check scenarios
  must be maintained.

## Affected Modules

- `templates/` (skill in three adapter forms), `registry.toml` (new feature,
  reference-capable), `scripts/ai_sync.py` (deployment registration),
  `fragments/process/cherry-pick-assessment.md` (+ authored pointer block),
  self-hosted `ai.project.toml` (`reference_features`), `rule_map.toml`
  (`CPA-*`), `docs/scenarios/` (`CP-*`, `TRG-004`), activation docs.

## Placement (context architecture)

The always-loaded surface follows the reference disclosure mode (decision
2026-11-02, issue #29): the self-hosted manifest and downstream manifests put
`cherry-pick-assessment` into `reference_features`, so `AGENTS.md` renders a
~300-byte pointer block naming the deployed reference file, and the full
invariants deploy as `.ai-standards/features/cherry-pick-assessment.md` via
`sync-templates` for every agent that can read a file — no dependence on
per-agent skill activation. The full procedure lives in the skill (four
adapter forms); the fragment remains the single source of truth for both the
pointer and the deployed reference copy. Pointer growth is capped: further
detail goes into the skill, never into `AGENTS.md`.

## Invariants And Constraints

- Clean Git application does not prove correct behavior; per-commit
  assessments do not compose into a PASS for the set.
- The resolved set is presented to the user before analysis; silent
  shrinking or widening is forbidden.
- Hypotheses are never presented as facts; unverified consumers are not
  treated as checked.
- PASS admits to a controlled transfer only; STOP and REVIEW are never
  downgraded to finish a task.
- The user's working tree and remote systems are never modified.

## Verification

- Structural pytest: frontmatter, normative blocks, deployment registration
  for all four agents gated on the new feature.
- `tests/test_rule_map.py`: `CPA-*` sections exist, scenario references
  resolve, `.ru.md` pairs present.
- Behavioral contracts `CP-001`…`CP-010` and trigger set `TRG-004` under
  `docs/scenarios/`; execution in `ai-standards-evals` (issue #18), including
  with-skill versus without-skill comparison and fabricated-evidence checks.

## Related Artifacts

- upstream request: aka-NameRec/ai-standards issue #27
- Worksheet: [[Worksheet: cherry-pick-assessment skill authoring and task
  spec]]
- [[DECISION: adopt the Rule Engineering initiative]], issue #18 (evals),
  issue #29 (reference disclosure mode)

## Observations

- [decision] Input becomes two-phase: selector resolution by the skill, then
  user confirmation of the resolved list — keeping the strict SHA binding
  without hand-enumerated hashes.
- [decision] Always-loaded placement follows the reference disclosure mode:
  pointer block in `AGENTS.md`, full fragment deployed under
  `.ai-standards/references/features/`; the inline full-fragment render would
  have left the self-hosted `AGENTS.md` within 160 bytes of the Codex
  32 768-byte truncation budget.
- [fact] `registry.toml` features require a non-empty fragment list and
  skill deployment is feature-gated in `scripts/ai_sync.py` (`AGENT_TEMPLATES`).

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- localized counterpart of [[РЕШЕНИЕ: добавить skill cherry-pick-assessment]]
