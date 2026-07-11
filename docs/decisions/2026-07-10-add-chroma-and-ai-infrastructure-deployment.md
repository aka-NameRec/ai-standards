# DECISION: add-chroma-and-ai-infrastructure-deployment

Russian localized version: [2026-07-10-add-chroma-and-ai-infrastructure-deployment.ru.md](2026-07-10-add-chroma-and-ai-infrastructure-deployment.ru.md)

## Status

Accepted

## Date

2026-07-10

## Context

`ai-standards` already standardizes usage policy for `conport` and `basic-memory`, and both have a rendered fragment plus (for Basic Memory) a usage guide. Two gaps remained:

1. **No Chroma standard.** Semantic code search over repository source was deployed ad hoc in downstream workspaces (notably in a large multi-repository workspace) but was absent from `ai-standards`: no fragment, no registry entry, no usage guide, no skill. Chroma appeared only as an undocumented gitignored runtime artifact under `context_portal/` produced by ConPort's own internal vector store, which is a different concern.
2. **No deployment skill.** `ai-standards` standardizes how to *use* tools ("when the MCP server is available") but never how to *deploy* them. A real-world setup session (GPT-5 family) burned roughly 22.8 million tokens — about 80% of a five-hour window — almost entirely on infrastructure: synchronous polling of a long Chroma build, a per-file embedding bottleneck and a mid-build manifest crash, a Basic Memory bootstrap race that ended in a destructive database reset, recurring cloud-routing errors, ConPort workspace detection walking up to `$HOME`, and inconsistent MCP wiring across clients (Kilo lacked the ConPort server that Codex had).

The team's goal is to unify the AI knowledge stack and its deployment so the expensive setup is done once and reused, instead of rediscovered per project.

## Decision

`ai-standards` adds a `chroma` feature and a reusable deployment skill that together standardize both the usage policy and the deployment of the AI knowledge stack (ConPort, Basic Memory, Chroma, and optionally Graphify).

### Canonical AI knowledge stack

The stack is four layers with three deliberately separate vector stores:

| Layer | Tool | Purpose | Store |
|---|---|---|---|
| 0 | `docs/` (Git) | durable source of truth | Markdown |
| 1 | Basic Memory | retrieval over documentation Markdown | BM sqlite + embeddings |
| 2 | ConPort | transient operational context | ConPort sqlite (+ internal vectors) |
| 3 | Chroma | semantic code search | Chroma PersistentClient sqlite |
| (4) | Graphify | structural code navigation | optional, per-repo graph |

Invariant: ConPort internal vectors, the Chroma code index, and Basic Memory embeddings are never mixed.

### Chroma usage policy (`fragments/tools/chroma.md`)

- Chroma is a semantic code-search layer, separate from ConPort and Basic Memory stores.
- All queries go through a freshness-gate wrapper that refreshes before querying and blocks on refresh failure.
- Similarity narrows an investigation but does not prove completeness; exhaustive claims require exact search plus build or static checks.
- Indexing is incremental by content hash with an atomic, resumable manifest.
- Local `PersistentClient` (embedded sqlite, no Docker) is the default; Docker is optional for shared or CI use.

### Deployment skill (`templates/ai-infrastructure/`)

A manually invoked skill, propagated to four agents (Codex, Claude, Kilo, Cursor), that deploys the stack in a project following an order that eliminates the races observed in a prior large-scale deployment:

1. Token-cheap pre-flight: read layout once and summarize; never poll.
2. ConPort: create `context_portal/` before relying on detection (else it walks to `$HOME`); `workspace_id` is the project root.
3. Basic Memory: `bm project add` before any search; never `db reset`; `ensure_frontmatter_on_sync=false`; force local mode (disable cloud routing); constrain the MCP server per-workspace with `--project`.
4. Chroma: local `PersistentClient` from a generalized `code_index.py` template with cross-file batched upsert and an atomic resumable manifest; run the build detached and check once.
5. MCP wiring consistent across clients (Kilo `kilo.json` and Codex `.codex/config.toml`).
6. Verify with `bm status`, `bm doctor`, ConPort active context, and collection counts.

### Per-project infra namespace

ai-standards-managed infrastructure in a downstream project lives under `.ai-standards/`, not mixed into the project's own `scripts/`:

```
.ai-standards/
├── scripts/code_index.py   # managed template (generalized from a production reference implementation)
├── code-index.toml         # managed starter config (collections, roots, chunking)
├── chroma/                 # runtime sqlite (gitignored)
└── state/                  # manifest.json (gitignored)
```

### Propagation changes

- `registry.toml` exposes `chroma = ["tools/chroma"]`.
- `templates/project_manifest.toml` lists `chroma` as opt-in (commented).
- `ai_sync.py` gains `claude` and `kilo` agent adapters alongside `codex` and `cursor`; agent templates gain an optional `feature` gate; enabling `chroma` in a manifest renders the usage fragment, syncs the `.ai-standards/` infra templates, and propagates the deployment skill for the enabled agents.

## Why

- turns an expensive, error-prone one-off setup into a repeatable, race-free deployment that any agent can run with minimal token cost;
- makes Chroma a first-class, documented standard instead of an undocumented side effect;
- keeps the three vector stores explicitly separated so retrieval stays precise instead of noisy;
- extends agent support to the four common environments (Codex, Claude, Kilo, Cursor) so the skill reaches every tool the team uses.

## Alternatives Considered

### Keep deployment knowledge only in the original `code_index.py`

Rejected because the implementation would be rediscovered per project, and the race conditions and token-cost traps are operational, not project-specific. They belong in a shared standard.

### Run Chroma as a Docker service by default

Rejected for the default because local embedded `PersistentClient` is zero-ops, needs no port or server process, and stays isolated per workspace. Docker remains an opt-in for shared or CI scenarios.

### Propagate the deployment skill only to Codex and Cursor

Rejected because the team operates in Kilo (and now Claude). Limiting propagation to two agents would leave the primary working environment without the skill.

### Gate the deployment skill on a new `ai-infrastructure` feature instead of `chroma`

Considered and deferred. `chroma` is the natural trigger because the code-index infrastructure and the deployment skill's primary value (race-free Chroma build plus BM/ConPort bootstrap) are most needed when semantic code search is enabled. The skill itself remains modular and deploys only the layers enabled in the manifest.

## Consequences

### Benefits

- a downstream project enables `chroma` and gets usage rules, infra templates, and a deployment skill in one step;
- the token-cost traps from that deployment (synchronous polling, per-file upsert, manifest crash, BM reset, cloud routing, detection walk-up, MCP drift) are encoded as preventive ordering in the skill;
- four agent environments receive managed skill copies through `ai-sync sync-templates`.

### Costs Or Tradeoffs

- the repository carries a new feature, usage guide pair, skill templates, an infra script template, and additional `ai_sync.py` logic with tests;
- the `code_index.py` template must be generalized from the original production implementation and maintained as the reference;
- teams that enable `chroma` must run the deployment skill to materialize the infrastructure.

## Affected Modules

- `registry.toml`
- `fragments/tools/chroma.md`
- `fragments/tools/basic-memory.md`
- `docs/chroma-usage.md`
- `docs/chroma-usage.ru.md`
- `docs/basic-memory-usage.md`
- `docs/basic-memory-usage.ru.md`
- `docs/conport-usage.md`
- `docs/conport-usage.ru.md`
- `docs/decisions/2026-07-10-add-chroma-and-ai-infrastructure-deployment.md`
- `docs/decisions/2026-07-10-add-chroma-and-ai-infrastructure-deployment.ru.md`
- `docs/tasks/0ta01xp-ai-infrastructure-deployment-skill.md`
- `docs/tasks/0ta01xp-ai-infrastructure-deployment-skill.ru.md`
- `templates/project_manifest.toml`
- `templates/ai-infrastructure/deploy-ai-knowledge-stack.SKILL.md`
- `templates/ai-infrastructure/deploy-ai-knowledge-stack.cursor.mdc`
- `templates/ai-infrastructure/deploy-ai-knowledge-stack.claude.md`
- `templates/ai-infrastructure/scripts/code_index.py`
- `templates/ai-infrastructure/code-index.toml`
- `ai.project.toml`
- `scripts/ai_sync.py`
- `tests/test_ai_sync.py`
- `README.md`
- `README.ru.md`
- `AGENTS.md`

## Invariants And Constraints

- Git-tracked Markdown remains the source of durable project knowledge.
- ConPort internal vectors, the Chroma code index, and Basic Memory embeddings remain separate stores.
- Chroma similarity narrows investigation but never proves completeness on its own.
- The deployment skill must never reset a Basic Memory database as a recovery step.
- ai-standards-managed infrastructure in a downstream project lives under `.ai-standards/`.

## Verification

- `registry.toml` exposes the `chroma` feature.
- rendered output includes the Chroma fragment when the feature is enabled.
- usage guides for `chroma` and `conport` exist in English and Russian.
- `ai-sync sync-templates` propagates the deployment skill to `codex`, `claude`, `kilo`, and `cursor` when `chroma` is enabled.
- `ai-sync sync-templates` creates `.ai-standards/scripts/code_index.py` and `.ai-standards/code-index.toml` when `chroma` is enabled and skips them otherwise.
- self-hosted `AGENTS.md` renders successfully with the feature enabled.
- `ruff`, `mypy`, and `pytest` pass.

## Related Artifacts

- [../chroma-usage.md](../chroma-usage.md)
- [../chroma-usage.ru.md](../chroma-usage.ru.md)
- [../conport-usage.md](../conport-usage.md)
- [../conport-usage.ru.md](../conport-usage.ru.md)
- [../../fragments/tools/chroma.md](../../fragments/tools/chroma.md)
- [../tasks/0ta01xp-ai-infrastructure-deployment-skill.md](../tasks/0ta01xp-ai-infrastructure-deployment-skill.md)
- [2026-05-19-add-basic-memory-feature.md](2026-05-19-add-basic-memory-feature.md)
