## Retrieval Routing

Stored knowledge is not conversation context. Retrieve it when relevant; do not preload it merely because it exists. Keep accumulated project knowledge outside the active context by default and retrieve only the smallest relevant subset the current task needs.

- Before broad repository exploration, determine what information is missing and query the narrowest available knowledge source capable of answering it.
- When an enabled retrieval capability directly matches the current information need, use it before falling back to broader manual exploration.
- Route retrieval according to the kind of information required, not according to tool familiarity.
- Retrieval narrows the evidence set; it does not establish correctness or completeness by itself.
- Verify retrieved claims against their authoritative source before relying on them for implementation or review when correctness matters.
- Prefer narrow retrieval before broad retrieval, and broad retrieval before indiscriminate repository scanning.
- At the start of non-trivial discovery, identify which enabled retrieval capabilities match the task before choosing an exploration strategy; do not invoke every capability ceremonially — use one when it can materially narrow the search.

### Routing Table

| Information need | Preferred source |
|---|---|
| previous task state, prior local decisions, discovered project patterns, unresolved investigations | project memory (local working memory) |
| canonical project decisions, architecture, and domain rules | Git-tracked documentation under `docs/domain/**`, `docs/decisions/**`, `docs/architecture/**` |
| semantic code discovery, analogous implementations, unknown implementation location | semantic code search (Chroma) |
| exact symbol or file already known | direct source access |
| call or dependency paths, impact analysis across modules | structural code intelligence (when enabled) |
| final verification | canonical docs, source code, and tests |

### Capability And Implementation

- Capabilities are named independently of the tools implementing them: project memory may be backed by Basic Memory, semantic code search by Chroma, structural code intelligence by a graph tool.
- Swapping an implementation backend must not require rewriting these behavioral rules.
