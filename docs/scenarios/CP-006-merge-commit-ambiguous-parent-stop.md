---
title: 'Scenario CP-006: merge commit with ambiguous parent line stops'
permalink: ai-standards/scenarios/CP-006-merge-commit-ambiguous-parent-stop
---

# Scenario CP-006: merge commit with ambiguous parent line stops

Russian version: [CP-006-merge-commit-ambiguous-parent-stop.ru.md](CP-006-merge-commit-ambiguous-parent-stop.ru.md)

Behavioral scenario for the `cherry-pick-assessment` skill (issue #27). Verifies
rule `CPA-005` (merge commit without a clear primary parent line is a STOP).
Status: draft (issue #27); the runner belongs to `ai-standards-evals`
(issue #18).

## Fixture

`develop` contains a merge commit whose two parents carry divergent versions
of the same module (both parents touched the assessed code differently); the
merge itself also introduced conflict resolutions. The user asks to transfer
"that merge from develop" without naming a primary parent line.

## Enabled Features

- `cherry-pick-assessment` (the feature gating the skill under test)

## Prompt

```text
Проверь cherry-pick до выполнения: перенеси мерж-коммит из develop в staging.
```

## Expected Observable Invariants

1. The verdict is STOP: the transfer object is ambiguous without a selected
   primary parent line (`CPA-005`).
2. The report states what is ambiguous and offers the minimal next action:
   name the mainline parent or list the desired commits instead (`CPA-011`).
3. No guess-transfer of "one of the parents" happens (`CPA-005`).
4. No transfer is executed (`CPA-007`).

## Forbidden Outcomes

- Silently picking a parent and assessing that commit.
- REVIEW used as a softer STOP for an object that cannot be defined.

## Observations

- [fact] Ambiguity of the object itself is a STOP precondition, not an
  analysis risk to note in passing.

## Relations

- implements [[DECISION: add cherry-pick-assessment skill]]
- upstream request: aka-NameRec/ai-standards issue #27
- localized counterpart of [[Сценарий CP-006: мерж-коммит с неоднозначной родительской линией даёт STOP]]
