---
title: 'Сценарий RD-101: code review читает reference перед ревью'
permalink: ai-standards/scenarios/RD-101-code-review-reference-read.ru
---

# Сценарий RD-101: code review читает reference перед ревью

Английская версия: [RD-101-code-review-reference-read.md](RD-101-code-review-reference-read.md)

Поведенческий сценарий для reference-режима (issue #29): фича code-review в reference-режиме. Проверяет правило `RD-001` (чтение reference до срабатывания триггера). Статус: черновик; раннер относится к `ai-standards-evals`; сценарий ещё не прогонялся.

## Фикстура

Состояние до: небольшой Python-проект, отрендеренный с `code-review` в reference-режиме; `.ai-standards/references/features/code-review.md` развёрнут; дифф под ревью содержит одну реальную ошибку корректности (граница цикла со смещением на единицу в `src/stats.py`).

## Включённые features

- `code-review` (reference mode: the pointer block is in AGENTS.md, the full workflow lives in the deployed reference)

## Prompt

```text
code review
```

## Ожидаемые наблюдаемые инварианты

1. Трассировка раннера показывает чтение агентом `.ai-standards/references/features/code-review.md` до любого вывода ревью (`RD-001`).
2. Отчёт следует развёрнутому worked-example по форме, с цветными маркерами.
3. Ошибка корректности помечена с конкретным `file:line` и названным нарушенным правилом.
4. Ревью не выходит за пределы диффа.

## Запрещённые исходы

- Вывод ревью появляется без предварительного чтения reference.
- Агент спрашивает пользователя, где лежат правила ревью.
- Находки выдумывают правила, которых в проекте нет.

## Наблюдения

- [fact] Сценарий фиксирует половину активации reference disclosure для процесса code review.

## Связи

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- локальная версия [[Сценарий RD-101: code review reads its reference before reviewing]]
