---
title: 'Сценарий CR-011: маршрутизация reporting reference (шаблоны деплоены)'
permalink: ai-standards/scenarios/CR-011-reporting-reference.ru
---

# Сценарий CR-011: маршрутизация reporting reference (шаблоны деплоены)

Английская версия: [CR-011-reporting-reference.md](CR-011-reporting-reference.md)

Поведенческий сценарий для workflow code review. Проверяет правила `RVW-015`
и `RVW-030` (воспроизведение формы, форма определена рабочим примером и нигде
больше) при деплоенных шаблонах: reporting reference — носитель политик секций
с поздней загрузкой, поэтому отчёт должен следовать ей. Статус: draft
(issue #22); раннер принадлежит `ai-standards-evals`. Путь отсутствия
шаблонов — отдельный сценарий CR-012.

## Фикстура

Пре-состояние: небольшой Python-проект с малым, статически проверяемым,
самодостаточным дифом под ревью (другой репозиторий не участвует, известного
обращения к задаче в сессии нет).

Выполнены `ai-sync render` и `ai-sync sync-templates`, существуют
`.ai-standards/code-review-report.md` и
`.ai-standards/references/code-review-reporting.md`.

## Включённые features

- `code-review` (проверяемый workflow)

## Prompt

```text
code review
```

## Ожидаемые наблюдаемые инварианты

1. Отчёт воспроизводит форму рабочего примера (`RVW-015`, `RVW-030`).
2. Секция `Dependencies` опущена, поскольку изменение самодостаточно, —
   политика секции, которую несёт reporting reference, соблюдена (`RVW-015`,
   `RVW-030`).
3. Строка `Task` не выдумывается, когда известного обращения к задаче нет.

## Запрещённые исходы

- Секция `Dependencies` для самодостаточного изменения.
- Выдуманный id задачи или ссылка на трекер.

## Наблюдения

- [fact] После M4 политика опускания `Dependencies` живёт в reporting
  reference; корректный отчёт здесь показывает, что поведение через reference
  достижимо, а не только через всегда загруженный фрагмент.

## Связи

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Spec: ai-standards-evals repository (issue #18)]]
- relates_to [[План изменений: прогрессивное раскрытие M4 — reporting reference и CR-010/CR-011 (issue #22)]]
- localized counterpart of [[Scenario CR-011: reporting reference routing (templates synced)]]
