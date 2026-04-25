# DECISION: add-session-hygiene-feature

Англоязычный оригинал: [2026-04-25-add-session-hygiene-feature.md](2026-04-25-add-session-hygiene-feature.md)

## Статус

Accepted

## Дата

2026-04-25

## Контекст

Длинные chat sessions могут накапливать context drift, stale assumptions, goal substitution и hidden decisions. Эти риски связаны с agent autonomy и usage economy, но не являются той же самой concern.

Существующие process features покрывали соседние проблемы:

- `autonomy-boundaries` определяет stop conditions для long autonomous execution.
- `structured-artifacts` выносит plans, contracts и decisions во внешние артефакты.
- `conport` может сохранять durable project memory между сессиями.
- `agent-usage-hygiene` снижает avoidable context и usage waste.

Репозиторию всё ещё нужна была чистая, переиспользуемая policy для предупреждений о long-session risk, создания handoff summaries и рекомендации fresh chat, когда active thread становится менее надёжным, чем explicit artifacts.

## Решение

`ai-standards` добавляет `session-hygiene` как opt-in process feature.

Feature определяет:

- long-session warnings для context drift, stale assumptions, goal substitution и lost constraints
- compact handoff summaries перед продолжением рискованных длинных сессий
- fresh-chat recommendations на phase boundaries или когда context уже нельзя compactly summarize
- повторное чтение relevant project rules, active context и task artifacts при переходе работы в новую фазу
- durable memory и project artifacts как место для critical constraints

Feature включена в self-hosted manifest и starter project manifest, чтобы downstream-проекты могли opt into неё через обычную manifest composition.

## Почему

- отделяет session reliability от usage economy и autonomy governance
- даёт агентам устойчивый способ предупреждать пользователей до того, как context drift станет correctness problem
- поощряет compact handoffs вместо full transcript summaries
- сохраняет tool-neutrality, избегая assumptions о context-window или message-count
- усиливает continuity между fresh chats без требования одного конкретного artifact format

## Рассмотренные альтернативы

### Встроить policy в `autonomy-boundaries`

Отклонено, потому что session hygiene применяется также к collaborative, non-autonomous и review-only разговорам. Она шире, чем long autonomous execution.

### Встроить policy в `agent-usage-hygiene`

Отклонено, потому что context reliability и usage economy имеют разные приоритеты. Fresh chat может улучшить reliability даже тогда, когда token usage не является главной concern.

### Стандартизовать жёсткие message или token thresholds

Отклонено, потому что такие лимиты tool-specific и меняются со временем. Проекты могут задавать local thresholds, когда у них есть evidence.

## Последствия

### Плюсы

- downstream-проекты могут opt into explicit long-session safeguards
- агенты могут рекомендовать fresh chats, не считая это failure
- handoff summaries становятся стандартным reviewable bridge между сессиями
- critical constraints с меньшей вероятностью останутся запертыми в transient chat memory

### Минусы или цена

- в репозитории появляется ещё один process feature и пара usage guides
- агентам нужно judgment, чтобы не over-warn на обычных medium-length chats
- проектам со строгими local chat limits всё ещё могут понадобиться overrides

## Затронутые модули

- `registry.toml`
- `fragments/process/session-hygiene.md`
- `README.md`
- `README.ru.md`
- `docs/session-hygiene-usage.md`
- `docs/session-hygiene-usage.ru.md`
- `ai.project.toml`
- `templates/project_manifest.toml`
- `AGENTS.md`
- `tests/test_ai_sync.py`

## Инварианты и ограничения

- critical constraints не должны жить только в transient chat memory
- handoff summaries должны быть compact и reviewable
- confirmed state должен отделяться от assumptions и inferred context
- shared standards должны избегать хрупких numeric thresholds
- reloading rules должен быть targeted для next slice, а не broad context loading by default

## Проверка

- `registry.toml` содержит feature `session-hygiene`
- рендеринг включает новый process fragment, когда feature подключён
- usage guides существуют на английском и русском
- README документирует feature на обоих языках
- self-hosted `AGENTS.md` успешно рендерится с включённой feature

## Связанные артефакты

- [../session-hygiene-usage.md](../session-hygiene-usage.md)
- [../session-hygiene-usage.ru.md](../session-hygiene-usage.ru.md)
- [../../fragments/process/session-hygiene.md](../../fragments/process/session-hygiene.md)
- [../../ai.project.toml](../../ai.project.toml)
