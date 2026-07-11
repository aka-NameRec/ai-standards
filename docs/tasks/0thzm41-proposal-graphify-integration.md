# 0thzm41 — Proposal: Graphify integration into ai-standards

Russian localized version: [0thzm41-proposal-graphify-integration.ru.md](0thzm41-proposal-graphify-integration.ru.md)

> Status: Proposal — not yet accepted. Recorded for a later design-first pass.

## Context

`ai-standards` now standardizes usage policy and deployment for ConPort, Basic Memory, and Chroma (task `0ta01xp`). A structural code-analysis layer is the remaining gap. DevCats already uses Graphify (`graphify` CLI) for `broadleaf/backend`: `graphify update .` produces `graphify-out/graph.json` (~9k nodes / ~23k edges) and exposes `query` / `path` / `explain` operations over the code-structure graph.

Graphify is **descriptive** (it captures what the code structurally IS), which is a different nature from a **normative** module contract (what the code SHOULD be). This distinction governs the whole proposal.

## Proposed Scope

Add `graphify` as an **opt-in feature** (like `chroma`), scoped to two complementary uses:

1. **Module-map generation and validation.** `module-map.md` already exists in `structured-artifacts` as a descriptive artifact for orchestration-heavy, integration-heavy, migration-prone modules. Graphify is the natural generator/validator for it.
2. **Structural contract-invariant verification.** A module contract (`MODULE_CONTRACT.md`) declares structural facts (dependencies, layer, public API surface, forbidden callers). Graphify mechanically checks the actual graph against the declared facts and reports drift. The contract remains the normative rule; Graphify is the executor.

### Explicit Non-Goals

- Graphify does **not** replace authored module contracts. Non-goals, invariants, failure boundaries, and ownership are normative and cannot be derived from code structure.
- Graphify is **not** a default feature. It targets large, layered, integration-heavy codebases (broadleaf-scale); for small or medium projects it is overhead.
- Graphify does **not** store contracts. It stores a structural graph used to generate maps and verify contract facts.

## Deployment Skill Integration (fire-and-forget)

Graphify install and setup must be a step in the `deploy-ai-knowledge-stack` skill so the user can act on a "fire-and-forget" basis: the agent installs, configures, builds, and subsequently uses the graph without manual intervention.

When `graphify` is enabled in the manifest, the deployment skill performs:

1. **Install** the `graphify` CLI (via `uv tool install` / package manager), gated by feature `graphify` and verified with `graphify --help` (note: `graphify --version` is not supported).
2. **Configure** per-repo graph targets under `.ai-standards/` (a `graphify` section in `code-index.toml` or a dedicated config), declaring which roots get graphs and where `graphify-out/graph.json` lives.
3. **Build** the initial graph for each declared target (detached, checkpointed, checked once — same token discipline as the Chroma build; never synchronous polling).
4. **Wire** queries through the same freshness-gated wrapper that serves Chroma, so Graphify refresh and query share one operational entry point.

The skill must remain **modular**: Graphify deploys only when `graphify` is in the manifest features, and only for the declared targets.

## Graph Freshness Methodology

The graph must stay current on the same terms as Chroma and Basic Memory:

- **Freshness-gate**: every Graphify query refreshes the graph first (`graphify update .` on the target root) and blocks on a refresh failure, so queries never run against a stale graph.
- **Event-driven refresh triggers** (mirroring Basic Memory reindex and Chroma refresh): after `git pull`, `git merge`, `git rebase`, branch switch, or a large patch that changes structure; before structural queries, contract-invariant checks, or blast-radius/impact analysis.
- **Incremental**: prefer Graphify's incremental update over a full rebuild when supported; checkpoint per-target state under `.ai-standards/state/` (atomic, resumable) so an interrupted build resumes.
- **Never session-driven**: do not rebuild the graph in every session; refresh only on a health signal or a VCS/structure-change event.
- **Similarity/structure is not completeness**: structural results narrow investigation but do not prove completeness; exhaustive claims require exact search plus build/type/static checks (same rule as Chroma).

## Proposed Layout

ai-standards-managed Graphify artifacts live under `.ai-standards/`, consistent with Chroma:

```
.ai-standards/
├── scripts/
│   └── code_index.py        # extended with graphify refresh/query subcommands (or a sibling script)
├── graphify-out/            # per-repo graph.json (gitignored runtime, or repo-local per DevCats precedent)
└── state/                   # per-target graph state (gitignored runtime)
```

Configuration of graph targets is declared in the existing `.ai-standards/code-index.toml` under a `[[graph]]` section (DevCats precedent), so one config drives both Chroma collections and Graphify targets.

## Open Design Questions (for the later design-first pass)

- Per-language support boundaries and how to express them (Graphify coverage differs by language).
- Whether Graphify refresh/query lives in the existing `code_index.py` wrapper or a sibling script.
- Whether `graphify-out/` is workspace-central (`.ai-standards/`) or repo-local (DevCats used repo-local `broadleaf/backend/graphify-out/`).
- Contract structured-fact schema: which fields are machine-checkable (`depends_on`, `layer`, `public_api`, `forbidden_callers`) and how they are declared in `MODULE_CONTRACT.md` (frontmatter block vs separate structured file).
- Verification output format for contract-invariant drift (report-only vs failing check).

## Affected Modules (anticipated)

- `registry.toml` (`graphify` feature)
- `fragments/tools/graphify.md` + `docs/graphify-usage.md` (+ `.ru.md`)
- `templates/ai-infrastructure/` (wrapper extension + config `[[graph]]` section)
- `templates/ai-infrastructure/deploy-ai-knowledge-stack.*` (Graphify deployment step)
- `scripts/ai_sync.py` (feature-gated infra templates if new files are needed)
- `docs/decisions/` (decision record when accepted)

## Relation To Current Work

- Builds on the `0ta01xp` foundation (feature-gated templates, `.ai-standards/` namespace, freshness-gate wrapper, deployment skill).
- Does not block the `0ta01xp` merge, version bump, or release. Pursued as a separate task after the current change set is reviewed and released.

## Next Step

Open a dedicated branch and run a design-first pass (change plan + decision record) that resolves the open design questions above before implementation.
