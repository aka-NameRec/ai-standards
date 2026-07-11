## Chroma Usage
- Use Chroma as a semantic code-search layer over repository source files when the project explicitly enables this feature.
- Keep the Chroma code index separate from ConPort internal vectors and from Basic Memory embeddings; the three stores are never mixed.
- Route all Chroma queries through a freshness-gate wrapper that refreshes the index before querying and blocks when a refresh fails, so retrieval never runs against a stale index.
- Treat similarity results as investigation narrowing, not as proof of completeness; exhaustive or correctness-critical claims require exact search plus build, type, or static checks.
- Keep indexing incremental by content hash with an atomic, resumable manifest so interrupted builds resume without re-embedding unchanged files.
- Prefer a local `PersistentClient` (embedded storage, no server process) for developer workspaces; use a Docker deployment only for shared or CI scenarios.
- Do not poll a long index build synchronously; run it detached, checkpoint progress, and check once.
- Keep ai-standards-managed indexing infrastructure under `.ai-standards/` so it does not mix with project-owned scripts.
