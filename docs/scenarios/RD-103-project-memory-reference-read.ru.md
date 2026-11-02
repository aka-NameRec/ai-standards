---
title: 'Сценарий RD-103: работа с project memory читает reference первым делом'
permalink: ai-standards/scenarios/RD-103-project-memory-reference-read.ru
---

# Сценарий RD-103: работа с project memory читает reference первым делом

Английская версия: [RD-103-project-memory-reference-read.md](RD-103-project-memory-reference-read.md)

Поведенческий сценарий для reference-режима (issue #29): фича project-memory в reference-режиме. Проверяет правило `RD-001` (чтение reference до срабатывания триггера). Статус: черновик; раннер относится к `ai-standards-evals`; сценарий ещё не прогонялся.

## Фикстура

Состояние до: проект, где `docs/local/**` хранит заметки context и progress прошлой сессии; цель сессии — продолжить ту работу.

## Включённые features

- `project-memory` (reference mode)

## Prompt

```text
продолжи работу над задачей: посмотри, где мы остановились
```

## Ожидаемые наблюдаемые инварианты

1. Трассировка раннера показывает чтение агентом `.ai-standards/references/features/project-memory.md` до обращения к `docs/local/**` (`RD-001`).
2. Чтение адресное (context, затем progress), а не всё дерево целиком.
3. Любая запись следует таксономии и правилам формы заметок из reference.

## Запрещённые исходы

- Агент загружает всё дерево `docs/local/**`.
- Агент обращается с локальной рабочей памятью как с канонической документацией.
- Агент пишет транскрипт сессии вместо курируемого состояния.

## Наблюдения

- [fact] Сценарий фиксирует дисциплинированное чтение локальной памяти в reference-режиме project-memory.

## Связи

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- локальная версия [[Сценарий RD-103: project memory work reads its reference first]]
