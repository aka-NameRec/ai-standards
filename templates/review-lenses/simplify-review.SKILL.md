---
name: simplify-review
description: Review recent code changes through the Reuse, Quality, and Efficiency lenses. Use when the user asks for simplification, cleanup, deduplication, or a behavior-preserving structural refactor.
disable-model-invocation: true
---

# Simplify Review

Run this workflow after implementation or when the user explicitly asks for cleanup or simplification.

## Scope

- Default to the current diff or the files explicitly named by the user.
- If the scope is unclear, infer the smallest reasonable set of changed files instead of broadening the task.
- Do not expand into unrelated cleanup.

## Lenses

### Reuse

- Look for duplicated logic, parallel helpers, or local implementations that should reuse an existing project primitive.
- Prefer clean imports and existing shared modules over new local abstractions.
- Do not introduce deeper or more confusing dependency chains just to remove a few lines.

### Quality

- Preserve readability, stable contracts, and type safety.
- Prefer simpler control flow, clearer names, and smaller coherent units when that reduces maintenance cost.
- Do not change public API signatures unless the user explicitly asked for it.

### Efficiency

- Remove redundant comments, dead debug code, and avoidable boilerplate.
- Reduce noise and verbosity when readability does not get worse.
- Do not turn readable code into code golf.

## Conflict Resolution

- If `Quality` and `Efficiency` conflict, choose `Quality`.
- If `Reuse` and `Efficiency` conflict, choose `Reuse` when the shared primitive is mature and local replacement is clean.
- If a suggestion is valuable but risky, report it instead of applying it.

## Verification

- Verify that no behavior, contract, edge-case handling, or important observability was removed.
- Preserve existing behavior unless the user explicitly requested a change.
- If tests exist and the task justifies it, run focused checks for the touched area.

## Response Shape

When editing:

1. State the intended gains before major edits if they are not obvious.
2. Apply only the smallest coherent patch needed.
3. Summarize the structural gains at the end.

When not editing:

1. Report findings grouped by `Reuse`, `Quality`, and `Efficiency`.
2. Mark risky or non-trivial suggestions separately.
3. Keep recommendations concrete and file-specific.
