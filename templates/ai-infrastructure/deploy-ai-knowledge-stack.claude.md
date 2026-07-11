---
description: Deploy the AI knowledge stack (ConPort, Basic Memory, Chroma) in this project.
argument-hint: [layers: conport,basic-memory,chroma]
---

Deploy the AI knowledge stack in this project following the deploy-ai-knowledge-stack playbook. Deploy only the layers enabled in `ai.project.toml` (or the layers named in $ARGUMENTS if provided).

# Deploy AI Knowledge Stack

This skill deploys the AI knowledge stack in a project: ConPort (operational context), Basic Memory (documentation retrieval), and Chroma (semantic code search). It follows an order that eliminates the setup races observed in a prior production deployment (synchronous polling burn, Basic Memory bootstrap race and destructive reset, cloud-routing errors, ConPort detection walk-up, and inconsistent MCP wiring).

## Stack Model

| Layer | Tool | Purpose | Store |
|---|---|---|---|
| 0 | `docs/` (Git) | durable source of truth | Markdown |
| 1 | Basic Memory | retrieval over documentation | BM sqlite + embeddings |
| 2 | ConPort | transient operational context | ConPort sqlite |
| 3 | Chroma | semantic code search | Chroma PersistentClient sqlite |

Invariant: the three vector/data stores (ConPort internal vectors, Chroma code index, Basic Memory embeddings) are never mixed.

## Token Discipline

- Read the project layout once and summarize; do not re-read large trees every turn.
- Never poll a long index build synchronously. Run it detached, checkpoint, and check once.
- Keep each step a small, reviewable patch with targeted verification.

## Playbook (order matters — eliminates races)

### 1. Pre-flight
- Determine the project root, the documentation path (usually `docs/`), and the source roots to index.
- Read `ai.project.toml` if present; deploy only the enabled layers (`conport`, `basic-memory`, `chroma`).
- Confirm with the user which BM project name and which Chroma collections to create.

### 2. ConPort
- Create `context_portal/` at the project root FIRST, before relying on workspace detection (else detection walks up to a parent such as `$HOME`).
- Use the project root absolute path as the `workspace_id`. Initialize ConPort.
- (Optional) Consolidate from existing per-repo databases via export/import; retain sources as rollback.

### 3. Basic Memory
- Create the BM project BEFORE any search: `bm project add <name> <docs-path>`. Handle "already exists" idempotently.
- Never run `db reset`. Set `ensure_frontmatter_on_sync=false`. Force LOCAL mode (`cloud_api_key` null, local routing).
- Build: `bm reindex --full -p <name>`. Constrain MCP per-workspace (`bm mcp --project <name>`).

### 4. Chroma
- Local `PersistentClient` (no Docker) by default. Managed wrapper + config under `.ai-standards/`:
  - `.ai-standards/scripts/code_index.py` — freshness-gated wrapper (refresh before query, block on failure).
  - `.ai-standards/code-index.toml` — collections, roots, chunking.
- Cross-file batched upsert + atomic resumable manifest (tmp+replace, per-file content hash).
- Run the initial build DETACHED, checkpoint, check once. Do NOT poll.
- `.gitignore` `.ai-standards/chroma/` and `.ai-standards/state/`; keep the script and config tracked.

### 5. MCP Wiring (consistent across clients)
- Wire consistently in every client used. ConPort: `workspace_id` = project root. Basic Memory: `--project <name>`. Chroma: wrapper-only.
- Apply to both Kilo (`kilo.json`) and Codex (`.codex/config.toml`) when both are used.

### 6. Verify
- `bm status --project <name>` clean; `bm doctor` passes; ConPort `get_active_context` resolves to project root; Chroma collection counts non-zero.
- Record a decision record and ConPort decision/progress entries.

## Stop Conditions
- Stop if an existing deployed stack conflicts with this plan.
- Stop before any destructive operation (BM `db reset`, dropping a Chroma collection with data) — ask first.
- Stop if MCP wiring cannot be made consistent across the clients in use.
