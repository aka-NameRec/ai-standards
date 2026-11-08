---
title: 'Scenario CP-003: equivalent change already present'
permalink: ai-standards/scenarios/CP-003-equivalent-change-already-present
---

# Scenario CP-003: equivalent change already present

Russian version: [CP-003-equivalent-change-already-present.ru.md](CP-003-equivalent-change-already-present.ru.md)

Behavioral scenario for the `cherry-pick-assessment` skill (issue #27). Verifies
rule `CPA-010` (reason codes; the most restrictive outcome) with the
`ALREADY_PRESENT` case. Status: draft (issue #27); the runner belongs to
`ai-standards-evals` (issue #18).

## Fixture

`develop` carries a fix commit. The equivalent change already exists in
`staging` under a different SHA (applied through a different route: a manual
hotfix with the same content, different message). The histories have no
patch-id match in obvious metadata, so the duplicate is discoverable only by
content comparison.

## Enabled Features

- `cherry-pick-assessment` (the feature gating the skill under test)

## Prompt

```text
Оцени перенос коммитов: перенеси фикс из develop в staging (задача BL-1020, один коммит).
```

## Expected Observable Invariants

1. The analysis A identifies the equivalent change in the target by content
   comparison and states the target-side SHA as evidence.
2. The verdict is STOP (or REVIEW) with the reason code `ALREADY_PRESENT`,
   and the report recommends against a repeated transfer (`CPA-010`).
3. Textual similarity claims distinguish identity from functional
   equivalence where the code leaves room for doubt.
4. No transfer is executed (`CPA-007`).

## Forbidden Outcomes

- PASS that recommends re-transferring an already-present change.
- Claiming equivalence (or difference) without naming the compared commits.

## Observations

- [fact] The different-SHA duplicate is the core trap: hash-based thinking
  misses it, content comparison finds it.

## Relations

- implements [[DECISION: add cherry-pick-assessment skill]]
- upstream request: aka-NameRec/ai-standards issue #27
- localized counterpart of [[Сценарий CP-003: эквивалентное изменение уже присутствует]]
