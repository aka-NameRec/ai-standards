---
title: 'Activation trigger set TRG-001: standard-code-review'
permalink: ai-standards/scenarios/TRG-001-standard-code-review-triggers
---

# Activation trigger set TRG-001: standard-code-review

Russian version: [TRG-001-standard-code-review-triggers.ru.md](TRG-001-standard-code-review-triggers.ru.md)

Activation trigger set for the `standard-code-review` skill. Verifies rule
`RVW-029` (the skill's activation phrases select it over the bare default
workflow) and `SE-008` (activation correctness). Status: Phase 7 draft; the
runner belongs to `ai-standards-evals` (issue #18).

## Enabled Features

- `code-review` (the skill gates on this feature and deploys alongside the always-loaded workflow)

## Positive Cases

| prompt | expected should_trigger |
|---|---|
| standard code review | true |
| «стандартный code review» | true |
| «сделай ревью по стандарту» | true |
| run the standard code review on this diff | true |

## Negative Cases

| prompt | expected should_trigger |
|---|---|
| code review | false — the bare default workflow, not the skill |
| review this file | false — default workflow |
| «проверь этот файл» | false — default workflow |
| упрости этот код | false — the review-lenses cleanup mode, not the standard review |
| write tests for this function | false — no review at all |

## Boundary Cases

| prompt | expected should_trigger |
|---|---|
| code review по стандарту проекта | true — the standard is named |
| review this, use the standard report format | true — the standard report format is requested |
| code review, but skip the standard stuff | false — explicit opt-out; default workflow |

## Observations

- [fact] The bare "code review" phrase belongs to the always-loaded workflow; the skill must not steal it.
- [fact] Boundary cases turn on explicit naming of the standard or its explicit rejection.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Dogfooding: Rule Engineering on the code-review feature (issue #17)]]
- localized counterpart of [[Набор триггер-кейсов TRG-001: standard-code-review]]
