# DECISION: add-cursor-preflight-and-workspace-router

Russian localized version: [2026-04-16-add-cursor-preflight-and-workspace-router.ru.md](2026-04-16-add-cursor-preflight-and-workspace-router.ru.md)

## Status

Accepted

## Date

2026-04-16

## Context

Downstream projects increasingly use Cursor in both:

- single-project roots
- multi-project roots where several repositories are opened together

In those scenarios, relying only on one managed Cursor rule (for review-lenses) was not enough to make project-scope rule pickup predictable. Teams needed an explicit way to opt into stronger project and workspace routing behavior from `ai.project.toml`.

## Decision

`ai-standards` adds optional Cursor deployment controls under `[tooling.cursor]`:

- `deploy_project_preflight`
- `deploy_workspace_router`
- `workspace_root`
- `project_slug`

When enabled, `sync-templates` additionally deploys:

- project rule: `.cursor/rules/00-project-preflight.mdc`
- workspace router rule: `<workspace_root>/.cursor/rules/10-ai-standards-project-<slug>.mdc`

Both rules are managed templates with standard `ai-standards` markers.

## Why

- keeps this behavior opt-in and explicit at project manifest level
- improves consistency when chats are opened from different roots
- keeps compatibility with existing `tooling.agents = ["cursor"]` workflow
- reuses the existing managed-template safety model (update/skip unmanaged)

## Alternatives Considered

### Use only AGENTS.md and no additional Cursor rules

Rejected because teams reported ambiguous scope behavior in multi-project roots and wanted a deployment-time hardening option.

### Always deploy preflight/router for every Cursor project

Rejected because this is a workflow policy choice and should remain opt-in.

### Add a separate global workspace config outside manifests

Rejected because teams wanted project-owned declarative configuration in `ai.project.toml`.

## Consequences

### Benefits

- downstream teams can enforce scope confirmation and preflight rules more consistently
- rollout is incremental and controlled per repository
- no behavior change for existing projects until `[tooling.cursor]` flags are enabled

### Costs Or Tradeoffs

- manifest schema and template sync logic become more complex
- workspace routing requires correct `workspace_root` configuration
- multiple projects in one workspace can produce multiple always-apply router files

## Affected Modules

- `scripts/ai_sync.py`
- `templates/cursor/project-preflight.cursor.mdc`
- `templates/cursor/workspace-router.cursor.mdc`
- `templates/project_manifest.toml`
- `README.md`
- `README.ru.md`
- `tests/test_ai_sync.py`

## Invariants And Constraints

- additional Cursor rules are deployed only when `cursor` is listed in `[tooling].agents`
- `deploy_workspace_router = true` requires `workspace_root`
- managed template marker behavior remains the source of truth for safe updates
- this change does not alter AGENTS rendering logic

## Verification

- `sync-templates` creates/updates `00-project-preflight.mdc` when `deploy_project_preflight=true`
- `sync-templates` creates/updates workspace router file when `deploy_workspace_router=true`
- missing `workspace_root` raises a clear sync error
- tests cover creation and failure cases

## Related Artifacts

- [../cursor-workspace-rules-usage.md](../cursor-workspace-rules-usage.md)
- [../../templates/cursor/project-preflight.cursor.mdc](../../templates/cursor/project-preflight.cursor.mdc)
- [../../templates/cursor/workspace-router.cursor.mdc](../../templates/cursor/workspace-router.cursor.mdc)
