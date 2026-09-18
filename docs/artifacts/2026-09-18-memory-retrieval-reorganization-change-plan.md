---
title: 'Change plan: memory and retrieval reorganization (issue #16)'
permalink: ai-standards/artifacts/2026-09-18-memory-retrieval-reorganization-change-plan
---

# Change plan: memory and retrieval reorganization (issue #16)

Status: in progress. Branch `rules-change/16-memory-retrieval-reorganization`.
Accepted decisions and verification points: this plan plus the session summary
in issue #16.

## Goal

Split three concerns the standards currently mix — project memory, knowledge
retrieval, and code retrieval/intelligence — by removing ConPort, introducing a
tool-neutral `retrieval-routing` policy layer, and giving local cross-session
working memory a standard home (`docs/local/**`) with a fixed taxonomy.

Source proposal: `docs/archive/20260913-122716-proposal-memory-retrieval-reorganization.md`.
Epic follow-up (phases 6–7): issue #19.

## Scope

- In scope (phases 1–5, one release 2.4.0, one branch):
  - Phase 1: remove the `conport` feature and every living reference to it;
    rename `deploy-ai-knowledge-stack` to `deploy-ai-retrieval-stack` (gate
    stays `chroma` until phase 2); add a retire mechanism for renamed managed
    templates; add the ConPort → `docs/local` migration instructions to
    `update-ai-standards`.
  - Phase 2: new feature `retrieval-routing` (rules R1–R6, capability
    awareness, capability-vs-implementation split); switch the deployment-skill
    gate to `retrieval-routing`; policy tests.
  - Phase 3: new feature `project-memory` (`docs/local/**` taxonomy:
    context, decisions, progress, patterns, investigations, handoffs;
    write/read policy; explicit promotion); relaxed `doctor` audit for the
    local-memory area; manifest key `local_memory_tree`.
  - Phase 4: integrations — `session-hygiene` (WHEN vs WHAT/HOW),
    `structured-artifacts` (reviewable artifacts only), `agent-usage-hygiene`,
    `autonomy-boundaries`, `chroma`, `knowledge-capture`.
  - Phase 5: experimental feature `structural-code-intelligence` plus the
    A/B/C evaluation methodology artifact. No deployment infrastructure.
- Out of scope: phases 6–7 (issue #19), Graphify deployment, automatic
  promotion of any local memory, multi-agent semantics beyond the minimal
  provenance fields.

## Touched Modules

- `scripts/ai_sync.py` (template registry, retire mechanism, doctor local-memory area)
- `fragments/**` (conport removed; retrieval-routing, project-memory,
  structural-code-intelligence added; integrations reworked)
- `registry.toml`, `templates/project_manifest.toml`, `ai.project.toml`
- `templates/ai-infrastructure/**` (deployment skill rework and rename)
- `templates/knowledge-capture/**`, `templates/standards-update/**` (ConPort-free wording, migration step)
- `tests/test_ai_sync.py`, `tests/test_bump_version.py`
- `README.md` / `README.ru.md`, usage docs under `docs/` (living references only)
- Decision record (new) + supersession notes on the 2026-08-24 role-separation decision and the knowledge-stack-roles overview

## Proposed Structure

- Feature graph after the change:
  `retrieval-routing` — connecting policy layer;
  `basic-memory` — Markdown retrieval layer (canonical + local);
  `project-memory` — tool-independent local memory taxonomy and lifecycle;
  `chroma` — semantic code search; `structural-code-intelligence` —
  experimental graph capability.
- `project-memory` is deliberately separate from `basic-memory`: the
  capability must not depend on one implementation (works best with
  basic-memory, but does not require it).
- Deployment skill becomes capability-based: deploys only the layers enabled
  in the manifest.

## Flow

1. Phase 1 (this branch): remove ConPort; rework and rename the deployment
   skill; retire mechanism; migration instructions; decision record.
2. Phase 2: `retrieval-routing` fragment + registry + gate switch + tests.
3. Phase 3: `project-memory` fragment + doctor changes + tests.
4. Phase 4: integration fragments + usage docs.
5. Phase 5: experimental fragment + evaluation artifact; release 2.4.0
   (`bump-version`), close #16, then migrate downstream projects.

## Risks

- Removing `conport` breaks `render` for downstream manifests that still name
  it (`SyncError` on unknown feature). Mitigation: migration instructions in
  `update-ai-standards`; all nine local projects migrated before the release
  is announced.
- Renamed templates leave orphan copies in projects. Mitigation: retire
  mechanism removes marker-detected managed copies; unmanaged files are never
  touched.
- `doctor` currently applies canonical-note rules to every `.md` in the tree;
  local memory would drown in warnings. Mitigation: relaxed audit for the
  local-memory area (phase 3).

## Invariants

- Living documentation, fragments, manifests, and templates contain no ConPort
  references; dated history (decisions, tasks, archive, CHANGELOG) keeps them
  with explicit supersession links where the record describes current shape.
- Render stays idempotent; unknown features/agents still fail at load; managed
  detection stays marker-based; `--fix` behaviour is unchanged.
- Local working memory is never treated as canonical documentation; promotion
  stays an explicit operation.
- One release: no intermediate state ships without a replacement for `conport`.

## Acceptance Criteria

- [ ] `rg -i conport` over the repository matches only dated history
      (`docs/decisions/**`, `docs/tasks/**`, `docs/archive/**`, `CHANGELOG.md`).
- [ ] Rendered `AGENTS.md` carries no ConPort section; a policy test guards it.
- [ ] Retire mechanism tested: managed copies of renamed templates are
      removed, unmodified user files survive.
- [ ] Migration instructions present in all three `update-ai-standards`
      template variants (EN wording; templates are not localized).
- [ ] Phases 2–5 acceptance criteria from issue #16 (routing rules, taxonomy,
      relaxed doctor, integrations, experimental capability) covered by tests.
- [ ] Release 2.4.0 tagged; downstream projects migrated.

## Verification

- Automated: `uv run python scripts/ai_sync.py render/check --project-root .`,
  `uv run ruff check`, `uv run mypy`, `uv run python -m pytest`.
- Manual: `rg -i conport` audit; behavioral scenarios A–E on this repository
  as the reference configuration at iteration end.

## Outcome

- Pending. Filled at iteration close.

## Observations

- [fact] The iteration splits project memory, knowledge retrieval, and code intelligence into separate features; the phase order follows issue #16, and phases 6–7 are tracked in issue #19.

## Relations

- relates_to [[DECISION: memory and retrieval reorganization]]
- relates_to [[Knowledge Stack Roles]]
