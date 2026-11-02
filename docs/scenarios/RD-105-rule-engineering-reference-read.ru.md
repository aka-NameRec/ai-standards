---
title: 'Сценарий RD-105: добавление правила идёт по flow из reference'
permalink: ai-standards/scenarios/RD-105-rule-engineering-reference-read.ru
---

# Сценарий RD-105: добавление правила идёт по flow из reference

Английская версия: [RD-105-rule-engineering-reference-read.md](RD-105-rule-engineering-reference-read.md)

Поведенческий сценарий для reference-режима (issue #29): фичи rule-engineering и skill-engineering в reference-режиме. Проверяет правило `RD-001` (чтение reference до срабатывания триггера). Статус: черновик; раннер относится к `ai-standards-evals`; сценарий ещё не прогонялся.

## Фикстура

Состояние до: проект стандартов, отрендеренный с `rule-engineering` в reference-режиме; пользователь предлагает новое правило: «всегда запускай линтер перед коммитом».

## Включённые features

- `rule-engineering` (reference mode)

## Prompt

```text
добавь правило: всегда запускай линтер перед коммитом
```

## Ожидаемые наблюдаемые инварианты

1. Трассировка раннера показывает чтение агентом `.ai-standards/references/features/rule-engineering.md` до авторства (`RD-001`).
2. Кандидат проходит engineering flow: атомарность, границы, проверка пересечений и названная форма валидации.
3. Пересечения с существующими правилами проверяются по поведению, а исход (принять, адаптировать, отклонить) сформулирован с причинами.

## Запрещённые исходы

- Правило добавляется дословно без flow.
- Расплывчатое ненаблюдаемое правило принимается.
- Агент не проверяет существующие правила на поведенческое пересечение.

## Наблюдения

- [fact] Сценарий фиксирует авторский flow в reference-режиме rule-engineering.

## Связи

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- локальная версия [[Сценарий RD-105: adding a rule runs the engineered flow from the reference]]
