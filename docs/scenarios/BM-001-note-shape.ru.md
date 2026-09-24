---
title: 'Сценарий BM-001: форма заметки при создании'
permalink: ai-standards/scenarios/BM-001-note-shape.ru
---

# Сценарий BM-001: форма заметки при создании

Английская версия: [BM-001-note-shape.md](BM-001-note-shape.md)

Поведенческий сценарий для feature basic-memory. Проверяет правило `BM-001`
(заметка пишется так, что не требует починки). Статус: draft (issue #22,
этап 3); раннер принадлежит `ai-standards-evals`. Исход проверяется по файловой
системе фикстуры; живой сервер Basic Memory не требуется, а запись через
внешнее хранилище памяти вместо файла репозитория — запрещённый исход.

## Фикстура

Пре-состояние: небольшой проект с включённой feature `basic-memory`;
`docs/decisions/` существует и содержит один прежний decision record в
канонической форме; шаблоны синхронизированы, существует
`.ai-standards/references/basic-memory-operations.md`.

## Включённые features

- `basic-memory` (проверяемая feature)

## Prompt

```text
Зафиксируй решение в docs/decisions: внутренние сервисы переходят с REST на gRPC. Создай файл заметки в репозитории по стандарту проекта.
```

## Ожидаемые наблюдаемые инварианты

1. Под `docs/decisions/` появился новый Markdown-файл с датированным именем
   `YYYY-MM-DD-<topic-slug>.md` (`BM-001`).
2. Файл несёт frontmatter `title` на русском, а заголовок `# ` повторяет этот
   title (`BM-001`).
3. Тело заметки закрывается секциями `## Observations` и `## Relations`, причём
   в `## Observations` есть хотя бы одно содержательное наблюдение (`BM-001`).

## Запрещённые исходы

- Заметка записана во внешнее хранилище памяти вместо файла репозитория в
  `docs/decisions/`.
- Недатированное имя или имя без осмысленного слага для decision record.
- Отсутствующий или нерусский frontmatter `title`, заголовок, не повторяющий
  его, или отсутствующие `## Observations` / `## Relations`.

## Наблюдения

- [fact] Инварианты проверяются по файловой системе фикстуры; раннеру не нужен
  сервер Basic Memory.

## Связи

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Spec: ai-standards-evals repository (issue #18)]]
- relates_to [[План изменений: этап 3 прогрессивного раскрытия — M5 basic-memory operations и M6 компрессия (issue #22)]]
- localized counterpart of [[Scenario BM-001: note shape on create]]
