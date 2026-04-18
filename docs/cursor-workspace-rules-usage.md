# Cursor Workspace Rules Usage

Russian localized version: [cursor-workspace-rules-usage.ru.md](cursor-workspace-rules-usage.ru.md)

This guide explains how to use optional Cursor hardening from `ai.project.toml` to improve rule pickup consistency in single-project and multi-project roots.

## Manifest Configuration

Enable Cursor adapter and optional hardening flags:

```toml
[tooling]
agents = ["cursor"]

[tooling.cursor]
deploy_project_preflight = true
deploy_workspace_router = true
workspace_root = ".."
project_slug = "carbide-front"
```

Field semantics:

- `deploy_project_preflight`: deploys project-local always-apply preflight rule.
- `deploy_workspace_router`: deploys workspace-level always-apply router rule.
- `workspace_root`: path resolved relative to project root.
- `project_slug`: stable identifier used in router filename and content.

## Generated Files

With `sync-templates`, Cursor gets:

- `<project_root>/.cursor/rules/00-project-preflight.mdc`
- `<workspace_root>/.cursor/rules/10-ai-standards-project-<slug>.mdc` (when workspace router is enabled)

Both files are managed templates and include `Managed by ai-standards template` markers.

## Recommended Rollout

1. Enable only `deploy_project_preflight` first.
2. Validate chat behavior in normal single-project sessions.
3. Enable `deploy_workspace_router` for projects that are frequently used in umbrella workspaces.
4. Keep `project_slug` stable to avoid router filename churn.

## Safety Notes

- `deploy_workspace_router=true` requires `workspace_root`; sync fails fast otherwise.
- Workspace router assumes `project_root` is nested under `workspace_root`.
- If many projects deploy workspace router into the same root, multiple always-apply router files will coexist. Keep router text concise and scope-aware.

## Operational Commands

```bash
uv run python scripts/ai_sync.py sync-templates --project-root /path/to/project
uv run python scripts/ai_sync.py render --project-root /path/to/project
uv run python scripts/ai_sync.py check --project-root /path/to/project
```
