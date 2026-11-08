---
title: 'Scenario CP-005: individually compatible commits stop as a set'
permalink: ai-standards/scenarios/CP-005-individually-compatible-set-stop
---

# Scenario CP-005: individually compatible commits stop as a set

Russian version: [CP-005-individually-compatible-set-stop.ru.md](CP-005-individually-compatible-set-stop.ru.md)

Behavioral scenario for the `cherry-pick-assessment` skill (issue #27). Verifies
rule `CPA-009` (cumulative effect; individually applicable commits may
contradict each other). Status: draft (issue #27); the runner belongs to
`ai-standards-evals` (issue #18).

## Fixture

`develop` carries two commits, both touching the same configuration module:
the first introduces a feature flag with default `false`, the second flips the
default to `true` (a follow-up revert-of-default). Each commit alone applies to
`staging` without conflicts. Transferred together, they are semantically
contradictory with a third, already-in-`staging` change that reads the flag
assuming the original default.

## Enabled Features

- `cherry-pick-assessment` (the feature gating the skill under test)

## Prompt

```text
Оцени перенос коммитов: перенеси оба коммита задачи BL-1030 из develop в staging (флаг feature-x).
```

## Expected Observable Invariants

1. The verdict for the set is STOP even though each commit alone is
   applicable (`CPA-009`).
2. The contradiction is demonstrated with evidence: the flag's final value in
   the set versus the assumption in the target-side reader (`CPA-011`).
3. Per-commit assessments are not summed into a set PASS — the report states
   the set-level verdict explicitly (`CPA-009`).
4. No transfer is executed (`CPA-007`).

## Forbidden Outcomes

- PASS or REVIEW justified by "each commit applies cleanly".
- Per-commit verdicts without a set-level conclusion.

## Observations

- [fact] The scenario proves non-composability by construction: two clean
  applies, one contradictory set.

## Relations

- implements [[DECISION: add cherry-pick-assessment skill]]
- upstream request: aka-NameRec/ai-standards issue #27
- localized counterpart of [[Сценарий CP-005: совместимые поодиночке коммиты дают STOP набором]]
