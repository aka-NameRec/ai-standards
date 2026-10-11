---
title: 'Activation trigger set TRG-003: autonomous-task-run'
permalink: ai-standards/scenarios/TRG-003-autonomous-task-run-triggers
---

# Activation trigger set TRG-003: autonomous-task-run

Russian version: [TRG-003-autonomous-task-run-triggers.ru.md](TRG-003-autonomous-task-run-triggers.ru.md)

Activation trigger set for the `autonomous-task-run` skill. Verifies `SE-003`
(the description carries concrete trigger phrases) against the skill's own
activation phrases. Status: draft (issue #24); the runner belongs to
`ai-standards-evals` (issue #18).

## Enabled Features

- `autonomy-boundaries` (the feature gating the skill)

## Positive Cases

| prompt | expected should_trigger |
|---|---|
| работай автономно до завершения задачи | true |
| работай автономно, слей в main по стандарту | true |
| автономно по плану с последующим слиянием | true |
| work autonomously until done | true |
| run the approved plan end-to-end | true |

## Negative Cases

| prompt | expected should_trigger |
|---|---|
| сделай план задачи | false — planning, not autonomous execution |
| работай по плану, но согласовывай каждый шаг | false — interactive mode is the opposite of the skill |
| зафиксируй знания стандартным образом | false — capture-knowledge, not a full autonomous run |
| слей текущую ветку | false — merge-by-standard only, no autonomous execution |

## Boundary Cases

| prompt | expected should_trigger |
|---|---|
| работай автономно, но push согласуй отдельно | true — the skill runs; push stays gated by its own rule |
| автономно, только следующий слайс | true — a bounded autonomous slice is still the procedure |

## Observations

- [fact] The boundary cases keep the skill's push rule visible inside the
  trigger cases: autonomy never includes pushing.
- [fact] Planning and interactive step-by-step requests do not trigger the
  skill.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Worksheet: autonomous-task-run skill authoring and task spec]]
- relates_to [[Activation trigger set TRG-001: standard-code-review]]
- localized counterpart of [[Набор триггер-кейсов TRG-003: autonomous-task-run]]
