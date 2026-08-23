---
description: Review recent code changes through the Reuse, Quality, and Efficiency lenses. Use when the user asks for simplification, cleanup, deduplication, or a behavior-preserving structural refactor.
argument-hint: [files or diff scope]
---

Review the recent code changes (the current diff, or the files named in $ARGUMENTS) through the Reuse, Quality, and Efficiency lenses. Keep the scope narrow and avoid unrelated cleanup. Prefer a concrete patch over generic advice.

## Reuse

- Prefer existing helpers, shared utilities, and exported primitives over duplicated local code.
- Suggest or apply reuse only when it makes the resulting code clearer and easier to maintain.

## DRY

- Look inward as well: a change that adds two copies of the same new helper satisfies "prefer existing primitives" while introducing exactly the duplication that should not reach the main branch.
- One intent expressed two different ways in sibling files counts too — a helper in one module, an equivalent inline expression in the next.
- Check the surrounding convention before extracting a shared helper. When the convention is to inline the operation, delete the wrapper on both sides instead of promoting it.
- Reach for a clone detector once the scope grows past the diff to a whole module or repository.

## Quality

- Preserve behavior, public contracts, readability, and type safety.
- Prefer simpler control flow, clearer names, and coherent decomposition.
- Do not change public APIs unless the user explicitly asks for it.

## Efficiency

- Remove dead debug code, redundant comments, and avoidable boilerplate.
- Compress noise, not intent.
- Do not optimize for brevity if it harms readability.

## Conflict Resolution

- `Quality` beats `Efficiency`.
- `Reuse` beats `Efficiency` when a stable shared primitive cleanly replaces local code.
- Report risky suggestions instead of applying them silently.

## Verification

- Check that no logic was rationalized away.
- Preserve error handling, edge cases, and observability that still matter.
- If the change is risky, ask for confirmation or return findings before editing.

## Output

- Prefer a concrete patch over generic advice.
- Briefly summarize structural gains such as less duplication, flatter control flow, or clearer boundaries.
