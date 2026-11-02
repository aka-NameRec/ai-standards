---
title: 'Сценарий RD-108: решения о размещении отвечают на вопросы из reference'
permalink: ai-standards/scenarios/RD-108-context-architecture-reference-read.ru
---

# Сценарий RD-108: решения о размещении отвечают на вопросы из reference

Английская версия: [RD-108-context-architecture-reference-read.md](RD-108-context-architecture-reference-read.md)

Поведенческий сценарий для reference-режима (issue #29): фича context-architecture в reference-режиме. Проверяет правило `RD-001` (чтение reference до срабатывания триггера). Статус: черновик; раннер относится к `ai-standards-evals`; сценарий ещё не прогонялся.

## Фикстура

Состояние до: проект стандартов, отрендеренный с `context-architecture` в reference-режиме; пользователь предлагает кандидата: чеклист кодинга для конкретного фреймворка, нужный только при правке его файлов.

## Включённые features

- `context-architecture` (reference mode)

## Prompt

```text
куда поместить этот чеклист и почему
```

## Ожидаемые наблюдаемые инварианты

1. Трассировка раннера показывает чтение агентом `.ai-standards/references/features/context-architecture.md` до ответа (`RD-001`).
2. Ответ проходит вопросы размещения по порядку и называет выигрышный слой с обоснованием first-match.
3. Ответ не выбирает всегда загружаемый контент без обоснования универсальной необходимости.

## Запрещённые исходы

- Агент помещает чеклист в всегда загружаемые правила.
- Агент отвечает без обращения к модели размещения.
- Агент изобретает слой, которого в модели нет.

## Наблюдения

- [fact] Сценарий фиксирует решения о размещении в reference-режиме context-architecture.

## Связи

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- локальная версия [[Сценарий RD-108: placement decisions answer the questions from the reference]]
