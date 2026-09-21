---
title: 'Набор триггер-кейсов TRG-002: skill-engineering'
permalink: ai-standards/scenarios/TRG-002-skill-engineering-triggers.ru
---

# Набор триггер-кейсов TRG-002: skill-engineering

Английская версия: [TRG-002-skill-engineering-triggers.md](TRG-002-skill-engineering-triggers.md)

Набор триггер-кейсов для навыка `skill-engineering`. Проверяет правило
`SE-003` (description несёт триггер-фразы) и `SE-008` (корректность
активации). Статус: черновик фазы 7; runner относится к `ai-standards-evals`
(issue #18).

## Включённые features

- `skill-engineering` (навык гейтится на этот feature)

## Позитивные кейсы

| prompt | expected should_trigger |
|---|---|
| создай skill для миграции конфигов | true |
| create a skill that formats our changelogs | true |
| «оформи навык по стандарту» | true |
| refactor the capture-knowledge skill | true — правка существующего навыка в объёме |

## Негативные кейсы

| prompt | expected should_trigger |
|---|---|
| добавь правило про тесты в AGENTS.md | false — нормативное правило идёт через Rule Engineering, не навыком |
| write a python script to migrate the data | false — слой script/tool, навык не нужен |
| задокументируй этот модуль | false — документация, не навык |
| создай команду /release для бенчей | false — механика адаптера, не переносимое содержимое навыка |

## Пограничные кейсы

| prompt | expected should_trigger |
|---|---|
| стоит ли нам делать skill для отчётов по ревью? | true — консультация по обоснованию и есть вопрос этого домена |
| добавь секцию в standard-code-review про производительность | true — правка тела навыка в объёме |
| создай плейбук миграции в docs/ | false — документ, не навык с активацией |

## Наблюдения

- [fact] Негативный набор охраняет границы слоёв: правила, скрипты, адаптеры и документы — не навыки.
- [fact] Правка тела существующего навыка в объёме; создание только адаптерной механики — нет.

## Связи

- implements [[РЕШЕНИЕ: принять инициативу Rule Engineering]]
- relates_to [[Dogfooding: skill-engineering создан через Rule Engineering (issue #17)]]
- localized counterpart of [[Activation trigger set TRG-002: skill-engineering]]
