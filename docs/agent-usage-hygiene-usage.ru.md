---
title: Руководство по Agent Usage Hygiene
permalink: ai-standards/agent-usage-hygiene-usage.ru
---

# Руководство по Agent Usage Hygiene

Англоязычный оригинал: [agent-usage-hygiene-usage.md](agent-usage-hygiene-usage.md)

Это руководство объясняет, как использовать feature `agent-usage-hygiene` из `ai-standards` в подключаемых проектах.

`agent-usage-hygiene` — это переиспользуемая process-feature для снижения лишнего agent usage за счёт фокусировки контекста, исследования и implementation slices.

Feature остаётся tool-neutral. Она не кодирует vendor billing details, model-specific modes или хрупкие числовые лимиты.

## Цели

Используйте `agent-usage-hygiene`, когда хотите, чтобы агент или команда:

- не загружали широкий контекст, когда достаточно targeted discovery
- держали implementation slices компактными и reviewable
- включали более строгий economy mode только по явному запросу пользователя
- сохраняли correctness, safety и обязательную verification при снижении waste

Типовые результаты:

- меньше ненужного чтения файлов
- более короткие и сфокусированные промежуточные объяснения
- более понятные handoffs между bounded slices
- меньше context drift в длинных сессиях

## Что покрывает feature

Feature стандартизует shared policy для:

- targeted repository discovery перед широким inspection
- prompt-activated economy mode
- компактных handoff summaries
- risk-based splitting для большой работы
- приоритета correctness, когда economy конфликтует с verification

Feature сознательно не стандартизует:

- vendor-specific billing controls
- model-specific fast или economy modes
- жёсткие лимиты на число файлов, команд или частоту checkpoints
- пропуск тестов или review steps только ради экономии usage

## Базовое правило

Usage economy — это context discipline, а не снижение engineering quality.

Агент должен избегать waste, но не должен скрывать uncertainty, пропускать обязательную verification или выбирать более слабое решение только потому, что его дешевле объяснить.

## Активация Economy Mode

Economy mode включается только когда пользователь явно просит об этом в текущей задаче или thread.

Типовые фразы активации:

- `будь экономным`
- `помни о лимитах`
- `экономь токены`
- `минимизируй контекст`
- `keep usage low`
- `be concise and usage-conscious`

Локализованные project prompts могут определить эквивалентные фразы на рабочем языке команды.

Economy mode заканчивается, когда:

- текущая задача завершена
- пользователь явно отключает режим
- агент сообщает, что economy конфликтует с correctness, safety или обязательной verification

## Поведение в Economy Mode

В economy mode предпочитайте:

- одно короткое уточнение scope вместо широкого speculative discovery
- search, diffs, logs и targeted commands перед чтением больших наборов файлов
- focused file reads для текущего slice
- компактные progress updates
- targeted checks, которые доказывают изменённое поведение
- handoff summaries вместо бесконечного протягивания длинного thread

Избегайте:

- repository-wide чтения без понятной причины
- длинных повторных summaries контекста, уже зафиксированного в artifacts
- broad refactors, скрытых внутри запроса на экономию usage
- пропуска критичной verification

## Связь с другими features

- `design-first-collaboration` определяет change intent, boundaries и non-goals до реализации.
- `reasoning-hygiene` удерживает анализ на assumptions, risks и verification.
- `autonomy-boundaries` не даёт длинным сессиям расползаться за пределы reviewable slices.
- `structured-artifacts` даёт change plans, contracts и decision records, которые снижают transient context load.
- `conport` может сохранять durable project memory вне активного model context.

`agent-usage-hygiene` не заменяет эти features. Она явно формулирует их context-economy value и добавляет prompt-activated economy behavior.

## Пример manifest

```toml
features = [
  "conport",
  "design-first-collaboration",
  "reasoning-hygiene",
  "autonomy-boundaries",
  "structured-artifacts",
  "agent-usage-hygiene",
]
```

## Практические prompt patterns

Хорошие prompts:

- `Будь экономным: посмотри только файлы, нужные для диагностики этого failing test, затем предложи минимальный fix.`
- `Помни о лимитах. Сначала скажи, какой узкий slice нужно изучить, прежде чем читать больше файлов.`
- `Минимизируй контекст и сделай компактный handoff summary после этого slice.`
- `Используй economy mode, но не пропускай verification, нужную для доказательства изменения.`

Избегайте prompts, которые превращают economy в снижение качества:

- `Не запускай тесты, чтобы сэкономить токены.`
- `Угадай без чтения файлов.`
- `Сделай коротко, даже если важные риски будут опущены.`

Лучше просить агента явно сообщать о конфликтах:

- `Если экономия usage конфликтует с correctness или verification, скажи об этом и приоритизируй correctness.`