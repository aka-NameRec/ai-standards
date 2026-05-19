# Task 0tf9ncz: basic memory policy proposal

Russian localized version: [0tf9ncz-basic-memory-policy-proposal.ru.md](0tf9ncz-basic-memory-policy-proposal.ru.md)

## Status

Prepared as a change proposal. Not implemented in shared fragments yet.

## Goal

Define the minimal `ai-standards` changes needed to make the following memory model official:

- `docs/decisions/**`, `docs/architecture/**`, and module contracts are canonical project knowledge.
- Canonical documentation changes require an explicit user request.
- `docs/ai-memory/**` is agent-managed working memory.
- `Basic Memory` is the preferred retrieval and indexing layer over Git-tracked Markdown knowledge.
- `ConPort` is downgraded from durable project memory to transient session memory and handoff storage.

## Files To Change

- [../../fragments/tools/conport.md](../../fragments/tools/conport.md)
- [../../fragments/process/structured-artifacts.md](../../fragments/process/structured-artifacts.md)
- [../../fragments/process/session-hygiene.md](../../fragments/process/session-hygiene.md)
- [../session-hygiene-usage.md](../session-hygiene-usage.md)
- [../session-hygiene-usage.ru.md](../session-hygiene-usage.ru.md)
- [../structured-artifacts-usage.md](../structured-artifacts-usage.md)
- [../structured-artifacts-usage.ru.md](../structured-artifacts-usage.ru.md)
- [../../README.md](../../README.md)
- [../../README.ru.md](../../README.ru.md)

## Required Policy Changes

### 1. Reframe ConPort as transient memory

Current shared wording treats ConPort as durable project memory for decisions, progress, glossary terms, and active context.

Required change:

- Keep the requirement to load relevant ConPort context at the start of a task when available.
- Replace durable-memory wording with transient operational-memory wording.
- Limit the intended use of ConPort to session handoff, active context, recent progress, investigation state, and compact next-step summaries.
- State explicitly that durable project knowledge must live in Git-tracked Markdown, not only in ConPort.

Suggested wording for `fragments/tools/conport.md`:

```md
## ConPort Usage
- At the start of each task or session, load relevant ConPort context when the MCP server is available.
- Use ConPort for transient operational memory such as active context, recent progress, investigation state, and session handoffs.
- Do not treat ConPort as the canonical source of durable project truth.
- Record durable architectural, operational, and module-boundary knowledge in Git-tracked Markdown artifacts.
- Prefer targeted retrieval over large context dumps.
- Before logging substantial new knowledge, align with the user if the workspace follows a confirmation-based ConPort workflow.
- After significant work, update ConPort with the result, rationale, and next steps when the user wants the memory synchronized.
```

### 2. Introduce canonical vs working memory language

The current shared rules separate decision records from ConPort, but they do not define an explicit canonical-documentation layer versus an agent-managed working-memory layer.

Required change:

- Define canonical documentation as Git-tracked project knowledge.
- Define agent working memory as non-canonical but reviewable Markdown.
- Make `docs/ai-memory/**` the recommended location for agent-managed memory in downstream projects that opt into this model.

Suggested wording for `fragments/process/structured-artifacts.md`:

```md
## Decision Records
- Create a short decision record when an architectural or operational choice will matter for future changes and code review.
- Use decision records and module contracts for durable repository history.
- Use agent working memory for evolving context, temporary findings, and notes that are not yet accepted as canonical documentation.
- Keep one decision record focused on one choice, its rationale, alternatives, and consequences.
```

Add a new section after `Decision Records`:

```md
## Canonical Documentation And Agent Working Memory
- Treat `docs/decisions/**`, `docs/architecture/**`, `MODULE_CONTRACT.md`, and equivalent local artifacts as canonical project knowledge.
- Treat `docs/ai-memory/**` as agent-managed working memory rather than canonical truth.
- Durable conclusions must be promoted from working memory into canonical documentation only on explicit user request.
- Working memory should link to canonical documents when they already exist instead of duplicating them.
```

### 3. Protect canonical docs from autonomous edits

The current shared rules encourage structured artifacts but do not explicitly prohibit silent edits to canonical documentation during unrelated implementation work.

Required change:

- Add a write policy that blocks autonomous edits to canonical documentation.
- Allow autonomous edits only in agent working memory.
- Require deduplication and contradiction checks before canonical documentation changes.

Suggested wording for `fragments/process/structured-artifacts.md`:

```md
## Canonical Documentation Write Policy
- Do not modify canonical documentation unless the user explicitly asks to record, update, reconcile, supersede, or remove durable project knowledge.
- Before modifying canonical documentation, search related decision records, architecture docs, module contracts, and agent working memory.
- Prefer updating an existing canonical document over creating a duplicate.
- If new knowledge contradicts existing canonical documentation, do not silently resolve the conflict unless the user has already made the decision in the current task.
- When a decision supersedes an older one, preserve the old document as historical context and add a clear supersession link.
```

### 4. Update session hygiene to prefer project artifacts and working memory

The current session-hygiene language still names ConPort as one of the default durable-memory destinations.

Required change:

- Change the preferred target from `ConPort or another durable memory mechanism` to `project artifacts, agent working memory, or another durable memory mechanism`.
- Keep ConPort as an optional handoff mechanism, not the primary durable-memory target.

Suggested changes for `fragments/process/session-hygiene.md`:

- Replace:
  `Do not rely on transient chat memory for critical constraints; move them into project artifacts, ConPort, or another durable memory mechanism.`
- With:
  `Do not rely on transient chat memory for critical constraints; move them into project artifacts, agent working memory, ConPort handoff notes, or another durable memory mechanism.`

- Replace:
  `Update durable memory only for decisions, progress, or lessons that should survive the session.`
- With:
  `Update durable memory only for decisions, progress, lessons, or working-memory notes that should survive the session, and keep canonical versus non-canonical status explicit.`

### 5. Update usage guides to describe the new memory stack

The usage guides currently describe ConPort and structured artifacts in a way that still centers ConPort as the reusable durable-memory feature.

Required change:

- `session-hygiene` guide should say the agent reloads relevant project artifacts, module contracts, decision records, and ConPort handoff only as needed.
- `structured-artifacts` guide should define when knowledge belongs in a decision record, a module contract, or `docs/ai-memory/**`.
- Add examples that distinguish:
  - canonical decision promotion by explicit request
  - routine autonomous updates in `docs/ai-memory/**`
  - optional ConPort handoff synchronization

### 6. Mention Basic Memory as the preferred retrieval layer

`ai-standards` currently has no shared wording for `Basic Memory`.

Required change:

- Mention `Basic Memory` in `README.md` and `README.ru.md` as an example of a Git-friendly retrieval layer for Markdown knowledge.
- Keep the wording tool-agnostic enough that downstream projects may use another Markdown indexing layer if needed.
- Do not make `Basic Memory` mandatory in the core fragments.

Suggested README wording:

```md
- Prefer Git-tracked Markdown as the source of durable project knowledge.
- A Markdown indexing and retrieval layer such as Basic Memory may be used to search and reuse that knowledge efficiently across sessions.
- Keep canonical documentation and agent-managed working memory distinct even when the same retrieval layer indexes both.
```

## Non-Goals

- Do not automatically add `Basic Memory` setup instructions, CLI commands, or MCP-specific operational steps into core fragments.
- Do not remove ConPort support from `ai-standards`; keep it as an optional transient-memory feature.
- Do not force every project to adopt `docs/ai-memory/**`; allow equivalent local paths through project-specific rules.

## Implementation Order

1. Update `fragments/tools/conport.md`.
2. Update `fragments/process/structured-artifacts.md`.
3. Update `fragments/process/session-hygiene.md`.
4. Refresh the English and Russian usage guides.
5. Refresh `README.md` and `README.ru.md`.
6. Regenerate the repository `AGENTS.md` and run renderer and test checks.

## Verification

When implemented, verify with:

- `uv run python scripts/ai_sync.py render --project-root .`
- `uv run python scripts/ai_sync.py check --project-root .`
- `uv run ruff check`
- `uv run mypy`
- `uv run python -m pytest`

## Expected Outcome

After implementation, `ai-standards` will officially support a memory model where:

- Git-tracked Markdown is the durable project knowledge source of truth.
- canonical documentation is protected from autonomous edits;
- agent working memory remains writable without extra friction;
- `Basic Memory` fits naturally as a retrieval layer;
- `ConPort` remains useful, but no longer competes with canonical project knowledge.