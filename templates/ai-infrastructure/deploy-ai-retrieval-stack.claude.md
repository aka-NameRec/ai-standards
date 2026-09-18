---
description: Deploy the AI retrieval stack (Basic Memory, Chroma) in this project.
argument-hint: [layers: basic-memory,chroma]
---

Deploy the AI retrieval stack in this project following the deploy-ai-retrieval-stack playbook. Deploy only the layers enabled in `ai.project.toml` (or the layers named in $ARGUMENTS if provided).

# Deploy AI Retrieval Stack

This skill deploys the AI retrieval stack in a project: Basic Memory (documentation retrieval, including local working memory) and Chroma (semantic code search). It is capability-based and follows an order that eliminates the setup races observed in a prior production deployment (synchronous polling burn, Basic Memory bootstrap race and destructive reset, cloud-routing errors, and inconsistent MCP wiring). A structural code-intelligence layer may join the stack later; deploy it only when its feature is explicitly enabled.

ConPort is no longer part of the stack. If the project still carries a `context_portal/` directory or a ConPort MCP server, follow the migration instructions in the `update-ai-standards` skill (migrate data into `docs/local/**`, then decommission); do not deploy or initialize ConPort here.

## Stack Model

| Layer | Tool | Purpose | Store |
|---|---|---|---|
| 0 | `docs/` (Git) | durable source of truth for canonical knowledge | Markdown |
| 1 | Basic Memory | retrieval over documentation and local working memory | BM sqlite + embeddings |
| 2 | Chroma | semantic code search | Chroma PersistentClient sqlite |

Invariant: the data stores (Chroma code index, Basic Memory embeddings) are never mixed. Canonical knowledge (`docs/domain/**`, `docs/decisions/**`, `docs/architecture/**`) and local working memory (`docs/local/**`, gitignored by default) live in one tree but never mix their roles: local memory is never canonical.

## Token Discipline

- Read the project layout once and summarize; do not re-read large trees every turn.
- Never poll a long index build synchronously. Run it detached, checkpoint, and check once.
- Keep each step a small, reviewable patch with targeted verification.

## Playbook (order matters — eliminates races)

### 1. Pre-flight
- Determine the project root, the documentation path (usually `docs/`), and the source roots to index.
- Read `ai.project.toml` if present; deploy only the enabled layers (`basic-memory`, `chroma`).
- Confirm with the user which BM project name and which Chroma collections to create.

### 2. Basic Memory
- Create the BM project BEFORE any search: `bm project add <name> <docs-path>`. Handle "already exists" idempotently.
- Point the project at a dedicated knowledge tree, never a repository root. Leave permalinks enabled; `ensure_frontmatter_on_sync=false` plus `disable_permalinks=true` is a legacy-tree fallback only.
- Never run `db reset`. Force LOCAL mode (`cloud_api_key` null, local routing).
- Build: `bm reindex --full -p <name>`. Constrain MCP per-workspace (`bm mcp --project <name>`).
- When the project enables local working memory, make sure `/docs/local/` is in `.gitignore`.

### 3. Chroma
- Local `PersistentClient` (no Docker) by default. Managed wrapper + config under `.ai-standards/`:
  - `.ai-standards/scripts/code_index.py` — freshness-gated wrapper (refresh before query, block on failure).
  - `.ai-standards/code-index.toml` — collections, roots, chunking.
- Cross-file batched upsert + atomic resumable manifest (tmp+replace, per-file content hash).
- Run the initial build DETACHED, checkpoint, check once. Do NOT poll.
- `.gitignore` `.ai-standards/chroma/` and `.ai-standards/state/`; keep the script and config tracked.

### 4. MCP Wiring (consistent across clients)
- Wire consistently in every client used. Basic Memory: `--project <name>`. Chroma: wrapper-only.
- Apply to both Kilo (`kilo.json`) and Codex (`.codex/config.toml`) when both are used.

### 5. Verify
- `bm status --project <name>` clean; `bm doctor` passes; Chroma collection counts non-zero.
- Record a decision record for the deployment; operational state goes into local working memory (`docs/local/**`), never canonical docs.

## Stop Conditions
- Stop if an existing deployed stack conflicts with this plan.
- Stop before any destructive operation (BM `db reset`, dropping a Chroma collection with data) — ask first.
- Stop if MCP wiring cannot be made consistent across the clients in use.
- Stop if a legacy ConPort installation is detected (`context_portal/`): migrate its data first, then decommission with the user's confirmation.
