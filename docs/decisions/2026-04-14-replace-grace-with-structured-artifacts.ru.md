# DECISION: replace-grace-with-structured-artifacts

Англоязычный оригинал: [2026-04-14-replace-grace-with-structured-artifacts.md](2026-04-14-replace-grace-with-structured-artifacts.md)

## Статус

Accepted

## Дата

2026-04-14

## Контекст

Ранее репозиторий документировал GRACE как интегрированный тяжёлый workflow. Анализ методологии и её XML-центричной модели исполнения показал, что действительно полезное ядро состоит в планировании, явных границах, инвариантах и устойчивых решениях, тогда как XML-heavy набор артефактов и bootstrap процесса добавляют избыточную церемониальность для shared standards.

## Решение

`ai-standards` прекращает продвигать GRACE как shared feature и рекомендованный workflow.

Вместо этого репозиторий стандартизует более лёгкую замену через feature `structured-artifacts`, Markdown-шаблоны и сопутствующую документацию.

## Почему

- сохраняет полезные идеи планирования и фиксации границ
- убирает XML-heavy привязку workflow из shared standards
- оставляет артефакты читаемыми в Git и понятными человеку
- соответствует курсу репозитория на low-noise, reusable, cross-project rules

## Рассмотренные альтернативы

### Сохранить интеграцию GRACE и просто описать более лёгкое использование

Отклонено, потому что это всё равно оставляет репозиторий привязанным к workflow-дизайну, по-прежнему построенному вокруг более тяжёлых артефактов и bootstrap-процесса.

### Оставить GRACE как optional heavy path рядом с lightweight artifacts

Отклонено, потому что это сохраняет смешанные сигналы в README, шаблонах и project bootstrap при ограниченной практической ценности для downstream-проектов.

## Последствия

### Плюсы

- у репозитория появляется одна ясная модель планирования и структурирования
- downstream-проекты больше не получают guidance по bootstrap GRACE по умолчанию
- lightweight structured artifacts становятся first-class reusable pattern

### Минусы или цена

- исторические `-log-` документы по-прежнему упоминают GRACE и остаются только как контекст
- downstream-проекты, явно опиравшиеся на старое GRACE guidance, должны перейти на новый набор правил

## Затронутые модули

- `registry.toml`
- `fragments/process/structured-artifacts.md`
- `fragments/tools/conport.md`
- `scripts/ai_sync.py`
- `templates/`
- `README.md`
- `README.ru.md`

## Инварианты и ограничения

- shared standards должны оставаться читаемыми в Git и на code review
- тяжёлые XML-oriented artifacts не являются shared defaults
- durable repository-facing choices могут фиксироваться decision records
- ConPort остаётся местом для active context, progress и evolving project memory

## Проверка

- `registry.toml` больше не содержит feature `grace`
- `README.md` и `README.ru.md` больше не рекомендуют интеграцию GRACE
- шаблоны и usage guides для `structured-artifacts` существуют на английском и русском
- проверки renderer остаются зелёными

## Связанные артефакты

- [../structured-artifacts-usage.md](../structured-artifacts-usage.md)
- [../structured-artifacts-usage.ru.md](../structured-artifacts-usage.ru.md)
- [../../ai.project.toml](../../ai.project.toml)
- [../ai/project-rules.md](../ai/project-rules.md)
