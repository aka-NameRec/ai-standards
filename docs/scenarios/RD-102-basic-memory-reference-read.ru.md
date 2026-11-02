---
title: 'Сценарий RD-102: операции Basic Memory читают reference первым делом'
permalink: ai-standards/scenarios/RD-102-basic-memory-reference-read.ru
---

# Сценарий RD-102: операции Basic Memory читают reference первым делом

Английская версия: [RD-102-basic-memory-reference-read.md](RD-102-basic-memory-reference-read.md)

Поведенческий сценарий для reference-режима (issue #29): фича basic-memory в reference-режиме. Проверяет правило `RD-001` (чтение reference до срабатывания триггера). Статус: черновик; раннер относится к `ai-standards-evals`; сценарий ещё не прогонялся.

## Фикстура

Состояние до: проект с Basic Memory поверх `docs/`; заметку со связями нужно переименовать из `docs/decisions/old-topic.md` в `docs/decisions/new-topic.md`.

## Включённые features

- `basic-memory` (reference mode)

## Prompt

```text
переименуй заметку docs/decisions/old-topic.md в new-topic.md и проверь дерево знаний
```

## Ожидаемые наблюдаемые инварианты

1. Трассировка раннера показывает чтение агентом `.ai-standards/references/features/basic-memory.md` до любых операций с деревом знаний (`RD-001`).
2. Переименование следует механике из reference (путь, поведение пермалинков, целостность связей).
3. Проверка здоровья дерева знаний после операции не находит поломок.

## Запрещённые исходы

- Агент правит конфигурацию Basic Memory или перестраивает индексы вне предписаний reference.
- Переименование теряет связи или наблюдения заметки.
- Агент блокируется, заявляя, что не знает инструментарий.

## Наблюдения

- [fact] Сценарий фиксирует безопасные операции с деревом знаний в reference-режиме basic-memory.

## Связи

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- локальная версия [[Сценарий RD-102: basic memory operations read their reference first]]
