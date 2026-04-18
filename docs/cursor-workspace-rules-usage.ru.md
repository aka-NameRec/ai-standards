# Руководство по workspace-правилам Cursor

English original: [cursor-workspace-rules-usage.md](cursor-workspace-rules-usage.md)

Этот документ описывает, как использовать опциональный режим усиления Cursor из `ai.project.toml`, чтобы повысить предсказуемость подхвата правил в single-project и multi-project корнях.

## Конфигурация manifest

Включите Cursor adapter и дополнительные флаги:

```toml
[tooling]
agents = ["cursor"]

[tooling.cursor]
deploy_project_preflight = true
deploy_workspace_router = true
workspace_root = ".."
project_slug = "carbide-front"
```

Смысл полей:

- `deploy_project_preflight`: раскладывает project-local always-apply preflight rule.
- `deploy_workspace_router`: раскладывает workspace-level always-apply router rule.
- `workspace_root`: путь, вычисляемый относительно project root.
- `project_slug`: стабильный идентификатор для имени и содержимого router file.

## Генерируемые файлы

После `sync-templates` для Cursor появляются:

- `<project_root>/.cursor/rules/00-project-preflight.mdc`
- `<workspace_root>/.cursor/rules/10-ai-standards-project-<slug>.mdc` (если включён workspace router)

Оба файла являются managed templates и содержат marker `Managed by ai-standards template`.

## Рекомендуемое внедрение

1. Сначала включите только `deploy_project_preflight`.
2. Проверьте поведение чатов в обычных single-project сессиях.
3. Для проектов, которые часто используются в umbrella workspace, включите `deploy_workspace_router`.
4. Держите `project_slug` стабильным, чтобы не создавать лишний churn в именах router files.

## Замечания по безопасности

- При `deploy_workspace_router=true` обязательно задавайте `workspace_root`, иначе sync завершится с ошибкой.
- Workspace router предполагает, что `project_root` вложен в `workspace_root`.
- Если несколько проектов раскладывают workspace router в один корень, будет несколько always-apply router files. Держите эти правила короткими и строго scope-aware.

## Операционные команды

```bash
uv run python scripts/ai_sync.py sync-templates --project-root /path/to/project
uv run python scripts/ai_sync.py render --project-root /path/to/project
uv run python scripts/ai_sync.py check --project-root /path/to/project
```
