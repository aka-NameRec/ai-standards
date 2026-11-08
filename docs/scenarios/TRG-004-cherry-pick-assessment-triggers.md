---
title: 'Activation trigger set TRG-004: cherry-pick-assessment'
permalink: ai-standards/scenarios/TRG-004-cherry-pick-assessment-triggers
---

# Activation trigger set TRG-004: cherry-pick-assessment

Russian version: [TRG-004-cherry-pick-assessment-triggers.ru.md](TRG-004-cherry-pick-assessment-triggers.ru.md)

Activation trigger set for the `cherry-pick-assessment` skill. Verifies
`SE-003` (the description carries concrete trigger phrases) against the
skill's own activation phrases. Status: draft (issue #27); the runner belongs
to `ai-standards-evals` (issue #18).

## Enabled Features

- `cherry-pick-assessment` (the feature gating the skill)

## Positive Cases

| prompt | expected should_trigger |
|---|---|
| оцени перенос коммитов из develop в staging | true |
| проверь cherry-pick до выполнения | true |
| assess cherry-pick safety for task BL-1234 | true |
| check which commits to cherry-pick from the task branch | true |
| перенесём ли задачу BL-1050 в staging, ничего не сломаем? | true |

## Negative Cases

| prompt | expected should_trigger |
|---|---|
| сделай ревью диффа в merge request | false — regular code review, not a pre-transfer assessment |
| выполни cherry-pick коммитов на staging | false — execution, explicitly excluded |
| утверди релиз на staging | false — release approval, not an assessment |
| cherry-pick уже выполнен, проверь ветку после переноса | false — post-transfer verification, not a pre-transfer assessment |

## Boundary Cases

| prompt | expected should_trigger |
|---|---|
| оцени перенос, а выполнять будет человек | true — assessment with explicit human execution is exactly the skill |
| какие коммиты нужны для переноса задачи BL-1050? | true — selector resolution is the skill's input phase |

## Observations

- [fact] Execution requests and post-transfer checks stay negative: the skill
  is read-only and pre-transfer only.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Activation trigger set TRG-003: autonomous-task-run]]
- upstream request: aka-NameRec/ai-standards issue #27
- localized counterpart of [[Набор триггер-кейсов TRG-004: cherry-pick-assessment]]
