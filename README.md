# AI Standards

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
- `features`: optional capabilities such as `conport`, `design-first-collaboration`, `grace`, and `review-lenses`.
- `stacks`: technology-specific rules such as `python`, `fastapi`, `postgres`, `react`, `vue`, or `java-spring`.
- `tooling.agents`: optional agent adapters such as `codex` and `cursor` for managed local workflow templates.

Recommended starting point for a Python/FastAPI project with standard communication and architecture requirements:

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
  "grace",
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
- Preserve UMA2 core constraints, design-first-collaboration, and GRACE
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

## Using GRACE In a Project

GRACE is integrated into `ai-standards` as policy and activation guidance, not as a local copy of the full upstream methodology.

What `ai-standards` owns:

- when GRACE should be activated
- how a project declares that it uses GRACE
- how GRACE fits together with `design-first-collaboration`, architecture rules, and local overrides

What remains upstream:

- the GRACE skills from [`osovv/grace-marketplace`](https://github.com/osovv/grace-marketplace)
- the upstream command workflow
- the upstream XML artifacts and templates

### GRACE Activation Conditions

The agent should switch from normal design-first execution into GRACE flow when one or more of these signals are present:

- a new subsystem or major module group
- a cross-module refactor
- contract design across services or layers
- a migration with compatibility or rollout risk
- a task that requires explicit verification planning
- a task that benefits from multi-agent execution
- a poorly mapped codebase area where durable structured knowledge is needed

Small and local low-risk changes can stay on the normal path without full GRACE bootstrapping.

### Developer Flow

1. Add the `grace` feature in `ai.project.toml`.
2. Render `AGENTS.md` so the project instructions explicitly mention GRACE.
3. Install or update the GRACE skills from `grace-marketplace`.
4. Bootstrap GRACE artifacts in the project.
5. Use the GRACE planning, verification, and execution flow for qualifying tasks.

Suggested GRACE skill installation commands, based on the upstream README:

```text
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-init
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-plan
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-execute
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-multiagent-execute
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-setup-subagents
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-fix
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-refresh
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-status
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-ask
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-explainer
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-verification
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-reviewer
```

Suggested runtime flow, also based on the upstream README:

1. `/grace-init`
2. Fill `docs/requirements.xml` and `docs/technology.xml`
3. `/grace-plan`
4. `/grace-verification`
5. `/grace-execute` or `/grace-multiagent-execute`

The upstream GRACE repository describes these core artifacts:

- `docs/requirements.xml`
- `docs/technology.xml`
- `docs/development-plan.xml`
- `docs/verification-plan.xml`
- `docs/knowledge-graph.xml`

### Standard Prompt For Installing Or Updating GRACE

Copy this prompt when you want an agent to prepare or refresh GRACE integration in a downstream project:

```text
You are integrating GRACE into a project that already uses ~/workspace/ai-standards.

Goals:
- Ensure the project manifest enables the `grace` feature
- Install or update GRACE skills from https://github.com/osovv/grace-marketplace
- Align the project workflow with GRACE activation conditions
- Do not duplicate the full GRACE methodology inside ai-standards

Required workflow:
1. Inspect the current ai.project.toml and AGENTS.md.
2. Ensure the `grace` feature is enabled.
3. Check whether GRACE skills are already installed.
4. If missing or outdated, install or refresh the GRACE skills from grace-marketplace.
5. Explain which task categories should trigger GRACE usage in this project.
6. If the project has not been bootstrapped for GRACE, guide or perform:
   - /grace-init
   - completion of requirements.xml and technology.xml
   - /grace-plan
   - /grace-verification
7. Report the resulting GRACE-ready state and any missing prerequisites.

Constraints:
- Treat grace-marketplace as the source of truth for GRACE skills and artifacts.
- Keep ai-standards responsible only for policy, activation, and integration guidance.
- Do not copy upstream GRACE skill contents into ai-standards unless a deliberate normalization task was explicitly requested.
```

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
- `react`
- `postgres`
- `vue`
