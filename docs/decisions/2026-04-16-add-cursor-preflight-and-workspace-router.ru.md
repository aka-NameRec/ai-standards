# DECISION: add-cursor-preflight-and-workspace-router

English original: [2026-04-16-add-cursor-preflight-and-workspace-router.md](2026-04-16-add-cursor-preflight-and-workspace-router.md)

## Status

Accepted

## Date

2026-04-16

## Context

Подключаемые проекты все чаще используют Cursor в двух режимах:

- single-project root
- multi-project root, когда несколько репозиториев открыты вместе

В этих сценариях одного managed-правила Cursor (review-lenses) было недостаточно для предсказуемого подхвата проектных правил. Командам понадобился явный opt-in механизм в `ai.project.toml` для усиленного preflight и workspace routing.

## Decision

`ai-standards` добавляет опциональные настройки Cursor в `[tooling.cursor]`:

- `deploy_project_preflight`
- `deploy_workspace_router`
- `workspace_root`
- `project_slug`

При включении `sync-templates` дополнительно раскладывает:

- project rule: `.cursor/rules/00-project-preflight.mdc`
- workspace router rule: `<workspace_root>/.cursor/rules/10-ai-standards-project-<slug>.mdc`

Оба файла остаются managed templates с маркерами `ai-standards`.

## Why

- поведение остаётся opt-in и явно задаётся в project manifest
- повышается стабильность при старте чатов из разных корней
- сохраняется совместимость с текущим `tooling.agents = ["cursor"]`
- используется существующая модель безопасного обновления managed templates

## Alternatives Considered

### Использовать только AGENTS.md без дополнительных Cursor rules

Отклонено, так как команды фиксировали неоднозначность scope в multi-project root.

### Всегда раскладывать preflight/router для всех Cursor-проектов

Отклонено, потому что это policy-решение и должно оставаться opt-in.

### Делать отдельный глобальный workspace-config вне manifests

Отклонено, потому что командам нужна декларативная настройка на уровне проекта через `ai.project.toml`.

## Consequences

### Benefits

- downstream-команды могут более стабильно обеспечивать проверку scope и preflight
- внедрение инкрементальное и управляется для каждого репозитория
- для существующих проектов без новых флагов поведение не меняется

### Costs Or Tradeoffs

- усложняется схема manifest и логика sync templates
- для workspace router нужно корректно задавать `workspace_root`
- при нескольких проектах в одном workspace появятся несколько always-apply router files

## Affected Modules

- `scripts/ai_sync.py`
- `templates/cursor/project-preflight.cursor.mdc`
- `templates/cursor/workspace-router.cursor.mdc`
- `templates/project_manifest.toml`
- `README.md`
- `README.ru.md`
- `tests/test_ai_sync.py`

## Invariants And Constraints

- дополнительные Cursor rules раскладываются только если в `[tooling].agents` указан `cursor`
- `deploy_workspace_router = true` требует `workspace_root`
- поведение managed template markers остаётся базовым механизмом безопасных обновлений
- логика рендера AGENTS не меняется

## Verification

- `sync-templates` создаёт/обновляет `00-project-preflight.mdc` при `deploy_project_preflight=true`
- `sync-templates` создаёт/обновляет workspace router file при `deploy_workspace_router=true`
- отсутствие `workspace_root` приводит к понятной ошибке
- тесты покрывают сценарии создания и ошибки

## Related Artifacts

- [../cursor-workspace-rules-usage.ru.md](../cursor-workspace-rules-usage.ru.md)
- [../../templates/cursor/project-preflight.cursor.mdc](../../templates/cursor/project-preflight.cursor.mdc)
- [../../templates/cursor/workspace-router.cursor.mdc](../../templates/cursor/workspace-router.cursor.mdc)
