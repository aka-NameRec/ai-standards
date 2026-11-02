---
title: 'Сценарий RD-107: фиксация знаний следует reference с маршрутом фиксации'
permalink: ai-standards/scenarios/RD-107-knowledge-capture-reference-read.ru
---

# Сценарий RD-107: фиксация знаний следует reference с маршрутом фиксации

Английская версия: [RD-107-knowledge-capture-reference-read.md](RD-107-knowledge-capture-reference-read.md)

Поведенческий сценарий для reference-режима (issue #29): фича knowledge-capture в reference-режиме. Проверяет правило `RD-001` (чтение reference до срабатывания триггера). Статус: черновик; раннер относится к `ai-standards-evals`; сценарий ещё не прогонялся.

## Фикстура

Состояние до: проект, отрендеренный с `knowledge-capture` в reference-режиме; в сессии принято одно решение и завершена одна задача, оба факта описаны в контексте промпта.

## Включённые features

- `knowledge-capture` (reference mode)

## Prompt

```text
зафиксируй знания стандартным образом
```

## Ожидаемые наблюдаемые инварианты

1. Трассировка раннера показывает чтение агентом `.ai-standards/references/features/knowledge-capture.md` до любых записей (`RD-001`).
2. Фиксация создаёт decision record для принятого решения и task record для завершённой задачи в определённых reference каталогах.
3. Каждый новый документ в `docs/**` ложится с парой `.ru.md`, согласно reference.

## Запрещённые исходы

- Агент отвечает кратким пересказом в чате вместо долговечных записей.
- Записи ложатся в каталоги, которых reference не определяет.
- Документы создаются без локализованных пар.

## Наблюдения

- [fact] Сценарий фиксирует маршрут фиксации в reference-режиме knowledge-capture.

## Связи

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- локальная версия [[Сценарий RD-107: knowledge capture follows the capture routing reference]]
