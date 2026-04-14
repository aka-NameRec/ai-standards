# AI Standards

## Contents

- [Layout](#layout)
- [Quick Start](#quick-start)
- [Manifest-Only Configuration](#manifest-only-configuration)
- [Project-Specific Rules](#project-specific-rules)
- [Agent Adapters](#agent-adapters)
- [Import External Rules](#import-external-rules)
- [Using Reasoning Hygiene In a Project](#using-reasoning-hygiene-in-a-project)
- [Using Review Lenses In a Project](#using-review-lenses-in-a-project)
- [Using Structured Artifacts In a Project](#using-structured-artifacts-in-a-project)
- [Project Flow](#project-flow)
- [Versioning](#versioning)
- [Current Stack Fragments](#current-stack-fragments)

Centralized AI instruction infrastructure for project-specific `AGENTS.md` generation.

Russian localized version: [README.ru.md](README.ru.md)

## Layout

- `fragments/`: reusable instruction fragments grouped by domain.
- `templates/`: starter files copied into downstream projects.
- `scripts/ai_sync.py`: CLI that renders and validates `AGENTS.md`.
- `registry.toml`: maps feature and stack names to fragment paths.

## Quick Start

```bash
uv run python scripts/ai_sync.py init-project --project-root /path/to/project
uv run python scripts/ai_sync.py render --project-root /path/to/project
uv run python scripts/ai_sync.py check --project-root /path/to/project
uv run python scripts/ai_sync.py sync-templates --project-root /path/to/project
```

## Manifest-Only Configuration

`ai-standards` does not use named profiles. Each downstream project declares the exact instruction dependencies it needs in `ai.project.toml`.

Use four layers:

- `fragments`: direct core rules that should always be rendered.
- `features`: optional capabilities such as `conport`, `design-first-collaboration`, `reasoning-hygiene`, `review-lenses`, and `structured-artifacts`.
- `stacks`: technology-specific rules such as `python`, `fastapi`, `sqlalchemy`, `django`, `postgres`, `react`, `vue`, or `java-spring`.
- `tooling.agents`: optional agent adapters such as `codex` and `cursor` for managed local workflow templates.

Recommended starting point for a Python/FastAPI project with standard communication, planning, and architecture requirements:

```toml
version = "2026.03"

fragments = [
  "core/base",
  "core/git-workflow",
  "core/architecture",
  "core/error-handling",
  "core/python",
]

features = [
  "conport",
  "design-first-collaboration",
  "reasoning-hygiene",
  "structured-artifacts",
]

stacks = [
  "python",
  "fastapi",
  "postgres",
]

local_overrides = [
  "docs/ai/project-rules.md",
]

optional_local_overrides = [
  "docs/ai/private-rules.local.md",
]

[tooling]
agents = ["codex", "cursor"]
```

Choose dependencies explicitly. If a rule belongs only to one project, keep it in a local override instead of turning it into a shared fragment.

Stack composition examples:

```toml
# FastAPI + SQLAlchemy + PostgreSQL
stacks = [
  "python",
  "fastapi",
  "sqlalchemy",
  "postgres",
]
```

```toml
# Django API project
stacks = [
  "python",
  "django",
  "django-service-layer",
  "django-naming",
  "django-drf",
  "django-save-lifecycle",
  "postgres",
]
```

```toml
# Django server-rendered project
stacks = [
  "python",
  "django",
  "django-service-layer",
  "django-save-lifecycle",
  "postgres",
]
```

Architecture note:

- Use `sqlalchemy` with service plus repository-style data access. This matches the shared `core/architecture` rules directly and is the default fit for FastAPI and similar Python services.
- Use `django` when the project follows Django conventions and the ORM itself is the persistence abstraction. In that stack, services and selectors interact with models through the Django ORM instead of adding a separate repository layer.

`tooling.agents` does not change the rendered `AGENTS.md`. It declares which agent-specific companion templates should be kept in sync inside the downstream project.

## Project-Specific Rules

Keep rules that must apply only inside one project in that project repository.

Recommended layout in a downstream project:

```text
project/
  ai.project.toml
  AGENTS.md
  .codex/skills/review-lenses/simplify-review/SKILL.md
  .cursor/rules/simplify-review.mdc
  docs/ai/project-rules.md
  docs/ai/private-rules.local.md
```

Use the manifest to compose both shared and project-local rules:

```toml
local_overrides = [
  "docs/ai/project-rules.md",
]

optional_local_overrides = [
  "docs/ai/private-rules.local.md",
]
```

Guidance:

- Put team-visible, repository-specific rules into `docs/ai/project-rules.md`.
- Create `docs/ai/private-rules.local.md` only on machines where you need it.
- Do not move project-only rules into `~/workspace/ai-standards`.
- Keep reusable stack, process, and tool rules in this repository instead.
- Add `docs/ai/private-rules.local.md` to the downstream project's `.gitignore`.

`optional_local_overrides` are skipped if the file does not exist, so local private rules do not block rendering.

## Agent Adapters

`AGENTS.md` remains the shared project-wide source of truth for general instructions.

Some tools also need local workflow adapters for reusable skills or rules. Declare those adapters in `ai.project.toml`:

```toml
[tooling]
agents = ["codex", "cursor"]
```

Supported adapters:

- `codex`: installs managed skill templates under `.codex/skills/`
- `cursor`: installs managed rule templates under `.cursor/rules/`

Commands:

- `init-project` copies the starter manifest, local override templates, and any managed agent adapters already declared in `ai.project.toml`.
- `sync-templates` updates managed agent adapters declared in `ai.project.toml`.
- `render` still renders only `AGENTS.md`.

Managed adapter files include an `ai-standards` marker. `sync-templates` updates only files it manages directly or plain copies of the upstream template, and skips locally customized unmanaged files.

## Import External Rules

Do not copy external rule sets directly into `ai-standards`. Normalize and adopt only the reusable parts.

Recommended import flow:

1. Read the external source and summarize its structure.
2. Extract candidate rules.
3. Classify each rule as `keep`, `adapt`, or `reject`.
4. Reject vague, project-specific, redundant, or conflicting rules.
5. Normalize accepted rules into concise imperative instructions.
6. Place them in the correct fragment under `fragments/`.
7. Update `registry.toml` if a new stack or feature is introduced.
8. Record provenance near the imported fragment.
9. Run `uv run ruff check`, `uv run mypy`, and `uv run pytest`.

### Standard Import Prompt

Copy this prompt when you want an agent to adopt rules from an external source:

```text
You are updating ~/workspace/ai-standards.

Task:
Adopt reusable rules from the external source below into ai-standards without copying blindly.

Source:
<URL>

Target:
- Add or update the most appropriate fragment under fragments/
- Update registry.toml if a new stack/feature must be registered
- Preserve UMA2 core constraints, design-first-collaboration, reasoning-hygiene, and structured-artifacts
- Do not import project-specific, vague, redundant, or conflicting rules

Required workflow:
1. Read the source and summarize its structure.
2. Extract candidate rules.
3. Classify each candidate as:
   - keep as reusable
   - adapt
   - reject
4. For every rejected item, state why it was rejected.
5. Normalize accepted rules into concise, imperative instructions matching ai-standards style.
6. Avoid duplicates with existing fragments.
7. Add provenance notes in the fragment header or adjacent documentation:
   - source URL
   - adoption date
   - adaptation notes
8. If the source suggests a new stack, create a new stack fragment and register it.
9. Run project checks after changes.
10. In the final report, show:
   - files changed
   - adopted rules
   - rejected rules
   - conflicts or ambiguities needing human review

Constraints:
- Prefer paraphrase and normalization over direct copying.
- Keep only rules that are durable and broadly reusable.
- Preserve existing behavior unless the imported rules justify a clear improvement.
- If a source rule conflicts with UMA2 architecture or error-handling rules, reject it unless explicitly approved.
```

## Using Reasoning Hygiene In a Project

`reasoning-hygiene` is an optional feature for improving analysis quality on complex or ambiguous tasks without relying on model-specific prompt tricks.

Use `reasoning-hygiene` when a project benefits from reusable rules for:

- explicit step-by-step breakdowns on non-trivial tasks
- surfacing assumptions, edge cases, and verification points
- self-review framed as gaps, risks, and missing evidence
- task-specific roles that add real constraints instead of generic persona fluff

`ai-standards` owns the durable policy:

- which reasoning behaviors are worth standardizing
- which prompt patterns are too brittle or model-specific to normalize
- how this feature complements `design-first-collaboration`, `conport`, and `structured-artifacts`

Detailed operational guidance lives in:

- English guide: [docs/reasoning-hygiene-usage.md](docs/reasoning-hygiene-usage.md)
- Russian guide: [docs/reasoning-hygiene-usage.ru.md](docs/reasoning-hygiene-usage.ru.md)

Keep emotional pressure, incentives, challenge prompts, and other prompt folklore out of this shared feature unless they become durable, cross-model policy with clear evidence.

## Using Review Lenses In a Project

`review-lenses` is an optional feature for aggressive review-and-refactor passes over recent changes.

Use `review-lenses` when a task benefits from an explicit post-implementation review or cleanup pass focused on:

- `Reuse`
- `Quality`
- `Efficiency`

`ai-standards` owns the reusable policy:

- when the workflow should be activated
- the lens model itself
- conflict priorities between the lenses
- verification expectations after aggressive cleanup

Keep vendor internals, undocumented tool behavior, brittle numeric heuristics, and framework-specific details out of this shared feature unless they are separately normalized and validated.

Detailed operational guidance lives in:

- English guide: [docs/review-lenses-usage.md](docs/review-lenses-usage.md)
- Russian guide: [docs/review-lenses-usage.ru.md](docs/review-lenses-usage.ru.md)

Ready-to-copy downstream templates:

- [templates/review-lenses/simplify-review.SKILL.md](templates/review-lenses/simplify-review.SKILL.md)
- [templates/review-lenses/simplify-review.cursor.mdc](templates/review-lenses/simplify-review.cursor.mdc)

When a downstream project declares `tooling.agents`, use `sync-templates` to keep these adapter templates aligned with the current repository version instead of copying them manually.

## Using Structured Artifacts In a Project

`structured-artifacts` is an optional feature for lightweight planning and boundary-setting artifacts that stay readable in Git and code review.

Use `structured-artifacts` when a project benefits from reusable rules for:

- change planning before non-trivial implementation
- explicit module boundaries and invariants for major or risky areas
- Git-tracked decision records for durable design choices
- optional module maps for orchestration-heavy or integration-heavy flows

This feature intentionally rejects XML-heavy planning, pseudo-XML knowledge overlays, and mandatory machine-oriented code graphs as shared standards.

Detailed operational guidance lives in:

- English guide: [docs/structured-artifacts-usage.md](docs/structured-artifacts-usage.md)
- Russian guide: [docs/structured-artifacts-usage.ru.md](docs/structured-artifacts-usage.ru.md)

Ready-to-copy downstream templates:

- [templates/change-plan.md](templates/change-plan.md)
- [templates/module-contract.md](templates/module-contract.md)
- [templates/decision-record.md](templates/decision-record.md)
- [templates/module-map.md](templates/module-map.md)

## Project Flow

1. Keep reusable standards in this repository.
2. Add `ai.project.toml` to each downstream project.
3. Render `AGENTS.md` from the manifest when you want to adopt updates.
4. Review the diff in the downstream project before committing.

## Versioning

Pin the desired standards version in `ai.project.toml`:

```toml
version = "2026.03"
```

The renderer embeds the requested version and the source path into the generated file header.

## Current Stack Fragments

- `python`
- `fastapi`
- `sqlalchemy`
- `django`
- `django-service-layer`
- `django-naming`
- `django-drf`
- `django-save-lifecycle`
- `react`
- `postgres`
- `vue`
- `java-spring`
