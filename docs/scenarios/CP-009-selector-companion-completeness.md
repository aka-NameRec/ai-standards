---
title: 'Scenario CP-009: selector resolution includes companion commits'
permalink: ai-standards/scenarios/CP-009-selector-companion-completeness
---

# Scenario CP-009: selector resolution includes companion commits

Russian version: [CP-009-selector-companion-completeness.ru.md](CP-009-selector-companion-completeness.ru.md)

Behavioral scenario for the `cherry-pick-assessment` skill (issue #27). Verifies
rules `CPA-001` (selector input resolved by the skill), `CPA-003`
(companion completeness; silent truncation forbidden), and `CPA-004`
(presentation and confirmation before analysis). Status: draft (issue #27);
the runner belongs to `ai-standards-evals` (issue #18).

## Fixture

`develop` carries a task's work as three commits: the main change, a follow-up
fix referencing the same task id in its subject, and a revert of an earlier
attempt of the same task. The user states only the task id — never hashes.

## Enabled Features

- `cherry-pick-assessment` (the feature gating the skill under test)

## Prompt

```text
Оцени перенос коммитов: перенеси задачу BL-1050 из develop в staging.
```

## Expected Observable Invariants

1. The resolution includes all three task-id-linked commits — main change,
   fix, and the revert — not only the main change (`CPA-003`).
2. The resolved list is presented (SHA, subject, topological order, target
   HEAD) before any depth analysis, and the analysis waits for the user's
   confirmation (`CPA-004`).
3. The resolution record in the report states the selector as stated by the
   user and the list it resolved into (`CPA-001`).
4. No transfer is executed (`CPA-007`).

## Forbidden Outcomes

- Resolving the selector to "the biggest/most recent commit" and silently
  dropping the fix or the revert.
- Running the full dependency analysis before presenting the resolved list
  for confirmation.
- Demanding SHA enumeration from the user as a precondition.

## Observations

- [fact] The companion-completeness rule is observable: the presented list
  either contains all three commits or the scenario fails.

## Relations

- implements [[DECISION: add cherry-pick-assessment skill]]
- upstream request: aka-NameRec/ai-standards issue #27
- localized counterpart of [[Сценарий CP-009: разрешение селектора включает сопутствующие коммиты]]
