# DECISION: add-basic-memory-feature

Англоязычный оригинал: [2026-05-19-add-basic-memory-feature.md](2026-05-19-add-basic-memory-feature.md)

## Status

Accepted

## Date

2026-05-19

## Context

Репозиторий уже использовал `conport`, `structured-artifacts` и `session-hygiene` для сохранения project context между сессиями. Этой комбинации всё ещё не хватало одного важного элемента: общего стандарта для retrieval и indexing Git-tracked Markdown knowledge.

Команда хотела модель памяти, в которой:

- canonical project knowledge живёт в Git-tracked Markdown
- `docs/decisions/**` и module contracts защищены от autonomous edits
- agent-managed working memory может развиваться с меньшим трением
- Basic Memory может индексировать и искать Markdown knowledge между сессиями
- ConPort остаётся полезным, но только как transient operational memory и handoff storage

Во время настройки Basic Memory репозиторий также увидел практический риск: default frontmatter injection может массово менять tracked Markdown files, что конфликтует с проектами, где documentation changes должны быть явными reviewable changes.

## Decision

`ai-standards` добавляет `basic-memory` как opt-in tool feature.

Feature определяет:

- Basic Memory как retrieval и indexing layer поверх Git-tracked Markdown
- явное разделение canonical documentation и agent-managed working memory
- рекомендацию предпочитать `ensure_frontmatter_on_sync=false` для существующих Git-tracked documentation trees
- reindexing triggers, привязанные к repository events и indexing health, а не механически к каждой сессии
- совместную работу Basic Memory, ConPort, structured artifacts и session hygiene

Self-hosted manifest включает эту feature, чтобы собственный сгенерированный `AGENTS.md` репозитория уже отражал новую policy.

## Why

- превращает Markdown-first project knowledge в явный shared workflow, а не в локальную договорённость
- выравнивает retrieval с Git review и repository-owned documentation
- снижает риск неконтролируемого documentation churn из-за побочных эффектов sync в Basic Memory
- сохраняет semantic search и reuse knowledge без превращения индекса в source of truth
- даёт downstream projects переиспользуемую policy, когда достаточно auto-sync, а когда нужен reindex

## Alternatives Considered

### Оставить guidance по Basic Memory только в README

Отклонено, потому что retrieval policy, правила canonical-versus-working-memory и reindexing triggers должны переиспользоваться в сгенерированном `AGENTS.md`, а не быть только частью repository prose.

### Встроить правила Basic Memory в `conport`

Отклонено, потому что ConPort и Basic Memory решают разные задачи. ConPort теперь является transient operational memory; Basic Memory — это Markdown retrieval layer поверх repository knowledge.

### Разрешить default frontmatter injection для всех индексируемых репозиториев

Отклонено, потому что существующая Git-tracked documentation может не допускать массовых metadata edits без явного review и approval.

## Consequences

### Benefits

- downstream projects могут opt into ясный Markdown-first memory workflow
- canonical documentation получает более сильную защиту от autonomous edits
- working-memory notes могут по-прежнему быстро развиваться под управлением агента
- reindexing становится привязанным к конкретным repository events и health checks

### Costs Or Tradeoffs

- репозиторий несёт ещё одну optional feature и пару usage guides
- команды должны осознанно ставить и эксплуатировать Basic Memory, когда включают эту feature
- проектам, которые полагаются на Basic Memory-managed frontmatter, могут понадобиться local overrides

## Affected Modules

- `registry.toml`
- `fragments/tools/basic-memory.md`
- `README.md`
- `README.ru.md`
- `docs/basic-memory-usage.md`
- `docs/basic-memory-usage.ru.md`
- `docs/structured-artifacts-usage.md`
- `docs/structured-artifacts-usage.ru.md`
- `docs/session-hygiene-usage.md`
- `docs/session-hygiene-usage.ru.md`
- `ai.project.toml`
- `AGENTS.md`
- `tests/test_ai_sync.py`

## Invariants And Constraints

- Git-tracked Markdown остаётся source of durable project knowledge
- Basic Memory является retrieval и indexing layer, а не canonical source of truth
- canonical documentation нельзя менять автономно без явного user request
- проекты должны предпочитать no-frontmatter-injection defaults, если только они явно не хотят Basic Memory-managed metadata
- reindexing policy должна быть event-driven и health-driven, а не механически session-driven

## Verification

- `registry.toml` публикует feature `basic-memory`
- рендер включает fragment Basic Memory, когда feature активна
- usage guides существуют на английском и русском
- README документирует feature на обоих языках
- self-hosted `AGENTS.md` успешно рендерится с включённой feature

## Related Artifacts

- [../basic-memory-usage.md](../basic-memory-usage.md)
- [../basic-memory-usage.ru.md](../basic-memory-usage.ru.md)
- [../../fragments/tools/basic-memory.md](../../fragments/tools/basic-memory.md)
- [../../ai.project.toml](../../ai.project.toml)
- [2026-04-25-add-session-hygiene-feature.ru.md](2026-04-25-add-session-hygiene-feature.ru.md)
