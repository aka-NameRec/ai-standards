<!-- Source: internal Django/DRF project conventions -->
<!-- Imported: 2026-04-16 -->
<!-- Motivation: reduce duplicated create/update orchestration when lifecycle steps are mostly symmetric -->
<!-- Use when: the project intentionally adopts a unified save wrapper and the team applies it consistently within a module or app -->
<!-- Do not use when: create/update behavior diverges materially in permissions, invariants, side effects, or audit rules; Django and DRF standard hooks remain valid on their own -->

## Django Save Orchestration

### Scope
- This fragment is an opt-in orchestration pattern, not a Django baseline or a replacement for Django and DRF standard hooks.
- Use it only when create and update orchestration are mostly symmetric and the team adopts the convention consistently.
- Do not mix this wrapper pattern with competing save-hook conventions inside the same module or app.

### DRF Pattern
- In DRF, `perform_create()` and `perform_update()` may delegate to a shared local `save()` method instead of duplicating near-identical orchestration logic.
- Distinguish create from update explicitly via instance state, such as `serializer.instance is None`, instead of spreading the same branching logic across multiple hooks.
- Keep the shared `save()` method focused on orchestration around the persistence boundary; business rules still belong in the project's chosen application layer.

### Django CBV Pattern
- In Django class-based views, `form_valid()` may delegate to a shared local `save()` method when the project adopts this pattern consistently.
- Use the wrapper to centralize repeated pre-save and post-save orchestration, not to hide domain decisions inside the view layer.

### Side Effects
- When post-save work depends on a successful transaction commit, schedule it with `transaction.on_commit` instead of running it immediately after persistence.
- Use explicit function calls for project-internal workflows; reserve signals for cross-cutting events that must fire regardless of the entry point.
