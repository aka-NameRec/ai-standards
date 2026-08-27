---
title: 'DECISION: add-agent-usage-hygiene-feature'
permalink: ai-standards/decisions/2026-04-25-add-agent-usage-hygiene-feature.ru
---

# DECISION: add-agent-usage-hygiene-feature

Англоязычный оригинал: [2026-04-25-add-agent-usage-hygiene-feature.md](2026-04-25-add-agent-usage-hygiene-feature.md)

## Статус

Accepted

## Дата

2026-04-25

## Контекст

Token- и usage-based agent workflows делают broad context loading, длинные автономные сессии, повторные summaries и ненужное чтение файлов более заметными операционными затратами.

В `ai-standards` уже были близкие quality-oriented guidance:

- `reasoning-hygiene` фокусирует анализ на assumptions, risks и verification.
- `autonomy-boundaries` удерживает длинное выполнение bounded и reviewable.
- `structured-artifacts` выносит plans, contracts и decisions во внешние артефакты, чтобы critical context не жил только в transient memory модели.

Эти features косвенно снижают waste, но репозиторий ещё не называл usage economy как переиспользуемую process concern. Новое правило должно было остаться tool-neutral и не вводить жёсткие зависимости от Codex-specific modes, vendor billing details или хрупких числовых thresholds.

## Решение

`ai-standards` добавляет `agent-usage-hygiene` как opt-in process feature.

Feature определяет:

- usage economy как context discipline, а не снижение engineering quality
- targeted discovery перед broad context loading
- компактные, reviewable implementation slices
- prompt-activated economy mode для usage-sensitive задач
- correctness и required verification как более высокий приоритет, чем usage reduction
- vendor-specific controls как concern для local adapters или project overrides

Feature включена в self-hosted manifest и starter project manifest, чтобы downstream-проекты могли явно принять guidance через обычную manifest composition.

## Почему

- явно формулирует economy value существующих process rules
- даёт пользователям устойчивый способ запросить поведение "будь экономным" без снижения качества
- сохраняет tool-neutral design репозитория
- не кодирует Codex-specific controls в shared standards
- избегает хрупких числовых лимитов вроде фиксированного числа checkpoints или максимального числа файлов

## Рассмотренные альтернативы

### Добавить несколько bullets в существующие process features

Отклонено, потому что prompt-activated economy mode является отдельным operating mode. Если встроить его в существующие features, activation semantics будет сложнее найти и проверить.

### Создать Codex-specific правило

Отклонено, потому что проект не должен вводить глубокую tool-specific coupling для этой concern. Codex-specific controls могут жить в local adapters или project overrides.

### Сделать economy mode всегда активным

Отклонено, потому что некоторые задачи требуют broad discovery, detailed explanation или stronger verification. Economy mode должен быть явным и обратимым, а не скрытым quality constraint.

## Последствия

### Плюсы

- downstream-проекты могут opt into reusable usage discipline
- пользователи могут включать более строгий economy behavior естественными prompts
- broad context loading и длинные сессии теперь имеют явное shared guidance
- correctness остаётся non-negotiable priority

### Минусы или цена

- в репозитории появляется ещё один process feature и пара usage guides
- downstream-проектам нужно решить, хотят ли они эту feature в generated instructions
- tool-specific controls всё равно требуют local adapters или overrides, если команда хочет их использовать

## Затронутые модули

- `registry.toml`
- `fragments/process/agent-usage-hygiene.md`
- `README.md`
- `README.ru.md`
- `docs/agent-usage-hygiene-usage.md`
- `docs/agent-usage-hygiene-usage.ru.md`
- `ai.project.toml`
- `templates/project_manifest.toml`
- `AGENTS.md`
- `tests/test_ai_sync.py`

## Инварианты и ограничения

- usage economy не должна снижать engineering quality
- required verification нельзя пропускать только ради экономии usage
- economy mode должен быть явным и обратимым
- shared rules должны оставаться tool-neutral
- vendor-specific controls должны жить в local adapters или project overrides
- shared standards должны избегать хрупких числовых thresholds

## Проверка

- `registry.toml` содержит feature `agent-usage-hygiene`
- рендеринг включает новый process fragment, когда feature подключён
- usage guides существуют на английском и русском
- README документирует feature на обоих языках
- self-hosted `AGENTS.md` успешно рендерится с включённым feature

## Связанные артефакты

- [../agent-usage-hygiene-usage.md](../agent-usage-hygiene-usage.md)
- [../agent-usage-hygiene-usage.ru.md](../agent-usage-hygiene-usage.ru.md)
- [../../fragments/process/agent-usage-hygiene.md](../../fragments/process/agent-usage-hygiene.md)
- [../../ai.project.toml](../../ai.project.toml)