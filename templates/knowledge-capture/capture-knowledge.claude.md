---
name: capture-knowledge
description: Capture a finished working session into the project's durable memory the standard way — sync ConPort state, write a decision record for every accepted choice, a task record for completed tasks, a module contract when a major module changed, README links for new maintained docs. Use when the user asks to «зафиксируй знания стандартным образом», зафиксировать решения или задачи, or "capture the session knowledge".
argument-hint: [what to capture]
---
# Capture Knowledge

Turn a working session into the durable memory the standard way. The user's request to capture IS the explicit write permission this procedure needs; without it, nothing here runs.

## Route By Content

- A choice was accepted → decision record under `docs/decisions/**` (or `docs/architecture/**`), `YYYY-MM-DD-topic-slug.md`, alternatives mandatory.
- A task completed → task record under `docs/tasks/`, named `<task-id>-<topic>.md`; most sessions need one summary document, not one per subtask.
- A major, risky, or shared module changed or grew a distinct contract → `MODULE_CONTRACT.md` next to it (ownership, non-goals, inputs, outputs, invariants, failure boundaries, verification).
- New maintained documentation under `docs/` → add its README link and its Russian localized pair in the same change set (`<name>.ru.md`); `-log-` chat exports are exempt and live in `docs/archive/**`.
- Operational state (current focus, progress, handoff) → the tracker (ConPort), never canonical docs.

## Write To The Tree

Every new note needs no repair from birth:

- frontmatter `title` in the document's own language, repeated as the `# H1`;
- close with `## Observations` and `## Relations` sections;
- observations only from the text itself — claims someone could disagree with; relations to notes whose titles already exist;
- English original + `.ru.md` pair updated in the same change set;
- relative repository links only.

## Mirror To The Tracker

- Update active context so a fresh session can resume without rereading the chat.
- Log decisions with a pointer to their record files, and progress entries DONE/TODO.
- The tracker is transient: it references canonical docs, it does not replace them.

## Verify Before Reporting

- `ai-sync doctor --project-root <path>` reports zero errors.
- Rendering stays idempotent (`ai-sync render` changes nothing).
- Basic Memory status is clean and search finds the new documents.

## Never

- Never push or commit without explicit user approval of the message.
- Never synthesize observations or invent note titles that do not exist yet as relation targets.
- Never batch content edits; capture writes new material — it does not rewrite existing prose.

## Report

List what was written where (files, records), what the user still owes (commit approval, missing sources), and what was skipped with a reason.
