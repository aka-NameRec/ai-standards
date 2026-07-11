# 0ta01xp — AI infrastructure deployment skill and Chroma standard

Russian localized version: [0ta01xp-ai-infrastructure-deployment-skill.ru.md](0ta01xp-ai-infrastructure-deployment-skill.ru.md)

## Goal

Add a `chroma` feature and a reusable deployment skill to `ai-standards` so the AI knowledge stack (ConPort, Basic Memory, Chroma, optionally Graphify) is standardized in both usage policy and deployment. Eliminate the per-project rediscovery of an expensive, race-prone setup.

## Scope

### In scope

- `chroma` usage fragment and bilingual usage guide.
- `chroma` registry entry and opt-in manifest entry.
- Deployment skill propagated to four agents (Codex, Claude, Kilo, Cursor), feature-gated by `chroma`.
- `.ai-standards/` infra templates: generalized `code_index.py` and `code-index.toml`, synced when `chroma` is enabled.
- `claude` and `kilo` agent adapters in `ai_sync.py`; optional `feature` gate on agent templates.
- `simplify-review` propagated to `claude` and `kilo` for consistency.
- Per-workspace Basic Memory isolation rule (`--project`) in the `basic-memory` fragment and usage guide.
- `conport-usage` bilingual guide (filling the existing gap).
- Self-hosted manifest enables `chroma`; regenerated `AGENTS.md`.
- Bilingual decision record, task spec, README updates, and tests.

### Out of scope

- Docker-first Chroma deployment (local `PersistentClient` is the default; Docker remains a documented option).
- Graphify generalization (mentioned as optional in the skill, not templated here).
- Migrating existing downstream workspaces (cockpit and other existing workspaces) to the new layout — separate follow-up.
- Committing, version bump, and release tagging — handled per the release workflow after review.

## Touched Modules

- `registry.toml`
- `fragments/tools/chroma.md`
- `fragments/tools/basic-memory.md`
- `docs/chroma-usage.md` (+ `.ru.md`)
- `docs/basic-memory-usage.md` (+ `.ru.md`)
- `docs/conport-usage.md` (+ `.ru.md`)
- `templates/project_manifest.toml`
- `templates/ai-infrastructure/` (skill variants, `scripts/code_index.py`, `code-index.toml`)
- `ai.project.toml`
- `scripts/ai_sync.py`
- `tests/test_ai_sync.py`
- `README.md` (+ `.ru.md`)
- `AGENTS.md` (regenerated)

## Proposed Structure

- `AgentTemplate` gains `feature: str | None = None`; templates with a feature sync only when that feature is enabled.
- New `INFRA_TEMPLATES` tuple of agent-agnostic templates (gated by feature) synced alongside agent templates.
- `sync_project_templates` extends to gate agent templates by feature and to sync `INFRA_TEMPLATES`.
- Deployment skill source files live in `templates/ai-infrastructure/`; the `code_index.py` template is generalized from a battle-tested reference implementation (paths under `.ai-standards/`, cross-file batching, atomic resumable manifest).

## Flow

1. Decision record + task spec (design-first artifacts).
2. Chroma fragment + bilingual usage guide; registry and manifest wiring.
3. Basic Memory isolation rule + usage-guide section; ConPort usage guide.
4. Deployment skill (three source variants) + `code_index.py` + `code-index.toml` templates.
5. `ai_sync.py` changes (claude/kilo adapters, feature gate, INFRA_TEMPLATES) + tests.
6. Enable `chroma` in self-hosted manifest; regenerate `AGENTS.md`.
7. README updates; run `render`/`check`/`ruff`/`mypy`/`pytest`.

## Risks

- Generalizing `code_index.py` without a live workspace to test the full Chroma build against — mitigate by keeping the proven reference algorithm intact and only abstracting paths/config.
- Adding a `feature` gate could change `sync_project_templates` result ordering and break existing exact-list test assertions — mitigate by gating new templates only (existing `simplify-review` stays ungated), so non-`chroma` manifests are unaffected.
- Four-agent frontmatter differences — mitigate with one shared `SKILL.md` for codex+kilo, plus cursor and claude variants.

## Invariants

- Existing tests for non-`chroma` manifests must pass unchanged.
- `simplify-review` continues to sync for `codex` and `cursor` exactly as before.
- Git-tracked Markdown remains the source of truth; the three vector stores stay separate.

## Acceptance Criteria

- [ ] `chroma` feature renders a Chroma section in `AGENTS.md`.
- [ ] `chroma-usage` and `conport-usage` guides exist in EN and RU.
- [ ] `sync-templates` propagates the deployment skill to all four agents when `chroma` is enabled.
- [ ] `sync-templates` creates `.ai-standards/scripts/code_index.py` and `.ai-standards/code-index.toml` when `chroma` is enabled and skips them otherwise.
- [ ] `claude` and `kilo` are accepted agents; unsupported agents still raise `SyncError`.
- [ ] `render`, `check`, `ruff`, `mypy`, `pytest` all pass.

## Verification

- Automated: `pytest`, `ruff`, `mypy`, `ai-sync check`.
- Manual: inspect rendered `AGENTS.md` Chroma section; inspect a dry-run `sync-templates` output in a temp project.
- Observability: ConPort decision + progress entries; this task spec and the decision record.

## Outcome

- Delivered the `chroma` feature (fragment + bilingual usage guide), registry and manifest wiring, and a feature-gated deployment skill propagated to four agents (Codex, Claude, Kilo, Cursor).
- Added `claude` and `kilo` agent adapters; `AgentTemplate` gained an optional `feature` gate; `INFRA_TEMPLATES` materializes `.ai-standards/scripts/code_index.py` and `.ai-standards/code-index.toml` when `chroma` is enabled.
- `code_index.py` generalized from a battle-tested reference implementation (Chroma-only, paths under `.ai-standards/`, cross-file batched upsert, atomic resumable manifest).
- Extended `basic-memory` with per-workspace `--project` isolation; added the `conport-usage` bilingual guide.
- Verification: `render`/`check` pass, `AGENTS.md` includes Chroma and Basic Memory isolation sections; `ruff`, `mypy`, and `pytest` (45 tests, +4 new) pass.
- Deviation: `simplify-review` was added to `kilo` (reuses the existing SKILL.md source) but deferred for `claude` (would need a dedicated command source); noted as follow-up.
- Follow-up: commit on the working branch (message approval pending), version bump and release tagging per the release workflow, and migrating cockpit and other existing workspaces to the new layout.
