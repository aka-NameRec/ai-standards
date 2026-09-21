---
title: 'Activation trigger set TRG-002: skill-engineering'
permalink: ai-standards/scenarios/TRG-002-skill-engineering-triggers
---

# Activation trigger set TRG-002: skill-engineering

Russian version: [TRG-002-skill-engineering-triggers.ru.md](TRG-002-skill-engineering-triggers.ru.md)

Activation trigger set for the `skill-engineering` skill. Verifies rule
`SE-003` (the description carries the trigger phrases) and `SE-008`
(activation correctness). Status: Phase 7 draft; the runner belongs to
`ai-standards-evals` (issue #18).

## Enabled Features

- `skill-engineering` (the skill gates on this feature)

## Positive Cases

| prompt | expected should_trigger |
|---|---|
| создай skill для миграции конфигов | true |
| create a skill that formats our changelogs | true |
| «оформи навык по стандарту» | true |
| refactor the capture-knowledge skill | true — editing an existing skill is in scope |

## Negative Cases

| prompt | expected should_trigger |
|---|---|
| добавь правило про тесты в AGENTS.md | false — a normative rule goes through Rule Engineering, not a skill |
| write a python script to migrate the data | false — the script/tool layer, no skill needed |
| задокументируй этот модуль | false — documentation, no skill |
| создай команду /release для бенчей | false — adapter mechanics, not portable skill content |

## Boundary Cases

| prompt | expected should_trigger |
|---|---|
| стоит ли нам делать skill для отчётов по ревью? | true — the justification consult is exactly this domain's question |
| добавь секцию в standard-code-review про производительность | true — editing a skill's body is in scope |
| создай плейбук миграции в docs/ | false — a document, not an activation-gated skill |

## Observations

- [fact] The negative set guards the layer boundaries: rules, scripts, adapters, and documents are not skills.
- [fact] Editing an existing skill's body is in scope; creating adapter-only mechanics is not.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Dogfooding: skill-engineering authored through Rule Engineering (issue #17)]]
- localized counterpart of [[Набор триггер-кейсов TRG-002: skill-engineering]]
