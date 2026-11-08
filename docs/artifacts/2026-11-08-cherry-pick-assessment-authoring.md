---
title: 'Worksheet: cherry-pick-assessment skill authoring and task spec'
permalink: ai-standards/artifacts/2026-11-08-cherry-pick-assessment-authoring
---

# Worksheet: cherry-pick-assessment skill authoring and task spec

Russian localized version: [2026-11-08-cherry-pick-assessment-authoring.ru.md](2026-11-08-cherry-pick-assessment-authoring.ru.md)

Rule Engineering authoring worksheet (SE-002) and task spec for issue #27,
stage 1. Written before implementation starts; the requirements are the
constant of the run.

## Goal

Ship the `cherry-pick-assessment` skill as a standards-deployed template: a
read-only pre-transfer assessment procedure that resolves user-stated
selectors into a confirmed ordered SHA set and produces a PASS / REVIEW /
STOP verdict with evidence, unknowns, and a concrete next action.

## Non-goals

- No executor skill: no recorded cherry-pick, conflict resolution committed
  to the target, merge, push, rebase, or reset.
- No release approval and no QA/QC/AF regulation changes.
- No eval-runner implementation (execution belongs to `ai-standards-evals`,
  issue #18).
- No numeric risk scoring.

## Requirements (the constant of this run)

| ID | Requirement | Acceptance criterion |
|---|---|---|
| REQ-1 | Skill template exists in all four adapter forms (SKILL.md for codex/kilo, `.cursor.mdc`, `.claude.md`), frontmatter `name`/`description` carrying RU and EN positive and negative trigger phrases | Files exist under `templates/cherry-pick-assessment/`; deployed copies appear after `sync-templates` |
| REQ-2 | Deployment registered for codex, cursor, claude, kilo, gated on the new `cherry-pick-assessment` feature; the feature resolves to the new fragment and is reference-capable | Registry entries in `scripts/ai_sync.py`, `registry.toml` (`features` + `[reference_disclosure].features`); new registry tests pass `uv run pytest` |
| REQ-3 | Skill body carries the issue #27 invariants: purpose and boundaries; selector input and two-phase resolution (resolve → present → user confirmation); target-state fixing (merge-base, target HEAD); read-only allowed actions with isolated trial application; forbidden actions; analyses A–F (identity/history, completeness/dependencies, compatibility, applicability, testability, cumulative effect); verdict rules with STOP > REVIEW > PASS precedence; FACT/HYPOTHESIS/UNKNOWN evidence discipline; invalidation on SHA-set/order/target-HEAD change; mandatory report shape | Structural pytest asserts key phrases of every normative block in the SKILL.md template |
| REQ-4 | Rules traced as `CPA-001`–`CPA-012` in `rule_map.toml`, atomic, bound to skill-source sections; prefix comment updated | `tests/test_rule_map.py` passes |
| REQ-5 | Scenario contracts `CP-001`…`CP-010` (behavior) and `TRG-004` (trigger set), each EN + RU, wired into rule references | Policy scenario tests pass; every referenced id resolves |
| REQ-6 | New `process/cherry-pick-assessment` fragment holds the invariants; the self-hosted manifest places the feature into `reference_features`, so `AGENTS.md` renders an authored ~300-byte pointer block and the full fragment deploys as `.ai-standards/references/features/cherry-pick-assessment.md` for every agent that reads files; pointer growth is capped — further detail goes into the skill | Fragment + `fragments/process/cherry-pick-assessment.pointer.md` exist; self-hosted `AGENTS.md` contains the pointer line and stays well under the 32 768-byte Codex budget after render |
| REQ-7 | Knowledge capture in the same change set: decision record (+.ru), task record (+.ru), this artifact (+.ru), local-memory progress note (date-prefixed) | Files exist; `ai-sync doctor` reports no new warnings |
| REQ-8 | Full verification: `pytest` green, `mypy scripts/` clean, `render` idempotent, `doctor` zero errors | Commands run on the final state with results recorded in the completion report |
| REQ-9 | Merge into `main` only on the human's explicit instruction; no push | Merge happens by the merge-by-standard flow after review; branch carries the final commit; no push without approval |

## Worksheet (Rule Engineering verdicts)

| Candidate guidance | Verdict | Note |
|---|---|---|
| Selector-based input: task ids, merge request, source branch, range, explicit SHAs, mixes | accepted | Removes the hand-listed-SHA failure class; each selector has a deterministic Git-resolution mechanism or a named external source |
| Two-phase input: skill resolves selectors, presents the resolved list, user confirms before analysis | accepted | Keeps the strict SHA/order/target-HEAD validity binding (issue #27 clause 5) without hand-enumerated hashes; the confirmation is observable |
| Companion-completeness: fix/revert commits sharing the task id join the candidate set; the set may only widen | accepted | Operationalizes issue #27 analysis B; silent truncation is the observable anti-pattern (scenario CP-009) |
| Always-loaded placement via the reference disclosure mode (pointer block + deployed reference file, decision 2026-11-02) | adapted | The first draft rendered the full fragment inline into `AGENTS.md` (+1 270 bytes, 160 bytes from the Codex truncation budget); pointer mode keeps the always-loaded delta at ~345 bytes and stays deterministic across agents |
| Ambiguous resolution without user clarification → STOP | accepted | Extends issue #27 clause 2 ("состав нельзя установить — STOP") to selectors; no best-guess interpretation |
| Merge commits require a primary parent line, else STOP | accepted | Direct continuation of scenario CP-06 |
| Explicit SHAs verified (exist in source history, subject echoed) | accepted | Typed-SHA protection without forbidding the expert path |
| Analyses A–F with confirmed/probable/unverified dependency classes | accepted | Verbatim from issue #27; each analysis names observable outputs |
| Verdict precedence STOP > REVIEW > PASS and reason codes (e.g. `ALREADY_PRESENT`) | accepted | From issue #27 clause 11; precedence is observable |
| FACT / HYPOTHESIS / UNKNOWN marking; performed/recommended/unavailable/not-found test classes | accepted | From issue #27 clauses 12 and 9; judged from the report text |
| Validity binding and invalidation on any change of set, order, or target HEAD | accepted | Issue #27 clause 5 and scenario CP-008 |
| Read-only guarantees; isolated trial application in a throwaway tree | accepted | From issue #27 clauses 3–4 and the autonomy boundaries' sensitive-areas rules |
| Numeric risk scoring | rejected | Issue #27 alternatives: false precision without calibration |
| Folding the procedure into standard code review | rejected | Different triggers and completion criteria; issue #27 names a standalone procedure |

Uniqueness: no existing rule or skill demands the same observable behavior —
`standard-code-review` reviews a diff against a review checklist;
`cherry-pick-assessment` judges transfer completeness and semantic
compatibility of a commit set against a target state, before the transfer
exists. Overlap with `autonomy-boundaries` is complementary: the fragment
states invariants, the skill is the procedure that satisfies them.

Validation forms: behavioral scenarios (CP-001…CP-010), trigger set
(TRG-004), structural pytest (REQ-3), and the with-skill versus without-skill
ablation in `ai-standards-evals`.

## Slices

| Slice | Content | Verification |
|---|---|---|
| S1 | Discovery: template registry shape, adapter forms, worksheet precedent, issue #27 re-read | Done pre-branch; no code change |
| S2 | Decision record (EN/RU) + this worksheet (EN/RU) + skill templates (3 files) + fragment + registry/feature wiring + registry and structural tests | Targeted pytest on new tests |
| S3 | `rule_map.toml` CPA rules + scenario contracts CP-001…CP-010, TRG-004 (EN/RU) | `uv run pytest tests/test_rule_map.py` |
| S4 | Task record (EN/RU), local-memory progress note, CHANGELOG `[Unreleased]` entry | `doctor` — no new warnings |
| S5 | Full verification suite, deployment smoke on a demo manifest, issue #27 comment | REQ-8 command suite |

## Scenario Map (issue #27 CP-01…CP-08 → contract files)

| Issue code | Contract file | Note |
|---|---|---|
| CP-01 | `CP-001-independent-commit-pass.md` | PASS with evidence |
| CP-02 | `CP-002-missing-mandatory-interface-change-stop.md` | STOP with the exact dependency |
| CP-03 | `CP-003-equivalent-change-already-present.md` | STOP / `ALREADY_PRESENT` |
| CP-04 | `CP-004-kafka-event-consumer-unavailable-review.md` | REVIEW with knowledge boundaries |
| CP-05 | `CP-005-individually-compatible-set-stop.md` | STOP on the cumulative set |
| CP-06 | `CP-006-merge-commit-ambiguous-parent-stop.md` | STOP |
| CP-07 | `CP-007-missing-integration-check-review.md` | REVIEW, no safety claims |
| CP-08 | `CP-008-invalidation-on-target-or-set-change.md` | Prior verdict void |
| — | `CP-009-selector-companion-completeness.md` | New: selector resolves with a companion commit; the full set is presented |
| — | `CP-010-ambiguous-selector-stop.md` | New: ambiguous selector without clarification → STOP |

Trigger set `TRG-004` covers positive («оцени перенос коммитов», «проверь
cherry-pick до выполнения», "assess cherry-pick safety"), negative (regular
code review, executing the transfer, release approval), and boundary cases
(a selector plus a clarifying answer; an assessment request with the transfer
already executed).

## Observations

- [decision] The input model is the only material deviation from the issue
  draft: selectors resolved by the skill plus mandatory confirmation replace
  hand-enumerated SHAs; every other issue clause carries over.
- [decision] The always-loaded placement follows the reference disclosure
  mode (decision 2026-11-02): pointer block in `AGENTS.md`, full fragment
  deployed as `.ai-standards/references/features/cherry-pick-assessment.md`;
  the first draft's inline fragment render would have left the self-hosted
  `AGENTS.md` 160 bytes under the Codex truncation budget.
- [fact] Scenario IDs follow the repo pattern `[A-Z]{2,5}-\d{3}`
  (`tests/test_rule_map.py`), so the issue's CP-01…CP-08 map to CP-001…CP-010.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- implements [[DECISION: add cherry-pick-assessment skill]]
- relates_to [[Spec: ai-standards-evals repository (issue #18)]]
- relates_to [[Worksheet: autonomous-task-run skill authoring and task spec]]
- upstream request: aka-NameRec/ai-standards issue #27
- localized counterpart of [[Рабочий лист: авторинг skill cherry-pick-assessment и task spec]]
