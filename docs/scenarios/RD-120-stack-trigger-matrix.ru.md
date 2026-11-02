---
title: 'Сценарий RD-120: работа по стеку читает reference стека до правки'
permalink: ai-standards/scenarios/RD-120-stack-trigger-matrix.ru
---

# Сценарий RD-120: работа по стеку читает reference стека до правки

Английская версия: [RD-120-stack-trigger-matrix.md](RD-120-stack-trigger-matrix.md)

Поведенческий сценарий для reference-режима (issue #29): все стеки с поддержкой reference (data-driven матрица). Проверяет правило `RD-001` (чтение reference до срабатывания триггера). Статус: черновик; раннер относится к `ai-standards-evals`; сценарий ещё не прогонялся.

## Фикстура

Параметризованная матрица: для каждой стековой позиции в `[reference_disclosure.stacks]` (registry.toml) раннер материализует минимальный проект-фикстуру с одним типичным для стека файлом и рендерит проект с этим стеком в reference-режиме. Каждый параметр несёт имя стека, путь пробного файла (например `src/models.py` для `django`, `app.tsx` для `react`) и запрос на правку (например «добавь поле в модель»).

## Включённые features

- the stack under test (reference mode)

## Prompt

```text
```text
<edit request for the stack's probe file>
```

Per parameter, the runner substitutes the stack's edit request.
```

## Ожидаемые наблюдаемые инварианты

1. Для каждого параметра трассировка раннера показывает чтение агентом развёрнутого reference стека (`.ai-standards/references/stacks/<name>.md`) до правки пробного файла (`RD-001`).
2. Правка применяет хотя бы одно правило, проверяемое по развёрнутому reference (раннер проверяет одно закодированное правило на стек).
3. Pointer-блок в AGENTS.md называл именно тот путь, который агент прочитал.

## Запрещённые исходы

- Пробный файл правится без предварительного чтения reference стека.
- Агент спрашивает пользователя о правилах стека.
- Правка противоречит закодированному правилу из reference.

## Наблюдения

- [fact] Матрица сценариев фиксирует активацию по каждой стековой позиции с поддержкой reference.

## Связи

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- локальная версия [[Сценарий RD-120: stack work reads the stack reference before editing]]
