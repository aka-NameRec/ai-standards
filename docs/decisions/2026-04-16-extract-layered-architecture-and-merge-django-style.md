---
title: 'DECISION: extract-layered-architecture-and-merge-django-style'
permalink: ai-standards/decisions/2026-04-16-extract-layered-architecture-and-merge-django-style
---

# DECISION: extract-layered-architecture-and-merge-django-style

Russian localized version: [2026-04-16-extract-layered-architecture-and-merge-django-style.ru.md](2026-04-16-extract-layered-architecture-and-merge-django-style.ru.md)

## Status

Accepted

## Date

2026-04-16

## Context

`ai-standards` already had a small cross-stack `core/architecture` fragment and several stack-specific architecture fragments, but it lacked reusable stack fragments for layered architecture itself.

That gap caused two problems:

- downstream manifests had to describe layered architecture indirectly or repeat stack names manually
- Django's HackSoft-derived opt-in guidance was split between `django-hacksoft-style` and `django-service-layer`, even though both described the same service-and-selector architectural family at different levels of detail

The repository also already favored stack composition through `registry.toml` aliases, as shown by existing compatibility aliases such as `java-spring` and `vue-query`.

## Decision

The repository introduces three reusable architecture stacks:

- `layered-architecture`
- `backend-layered-architecture`
- `frontend-layered-architecture`

The repository merges the previous `django-hacksoft-style` guidance into `django-service-layer` and removes the standalone `django-hacksoft-style` fragment and stack name.
The repository also removes the separate `django-naming` stack and keeps only the service-and-selector naming rule that naturally belongs to the HackSoft-derived style inside `django-service-layer`.

`django-service-layer` remains an explicit opt-in architectural style and keeps the HackSoft provenance link and framing inside the fragment itself.

The stack dependency is modeled through existing `registry.toml` composition rather than through a new manifest or fragment dependency mechanism. `django-service-layer` now expands to:

- `stacks/layered-architecture`
- `stacks/backend-layered-architecture`
- `stacks/django-service-layer`

## Why

- gives layered architecture a reusable cross-stack vocabulary without moving it into `core`
- keeps backend and frontend layering guidance separate enough to stay coherent
- simplifies downstream `ai.project.toml` composition for Django projects
- removes a split where one Django architectural style had two overlapping stack names
- removes an extra Django stack whose useful rule was already part of the same architectural style
- preserves the important opt-in and HackSoft-derived framing instead of flattening it into generic Django guidance

## Alternatives Considered

### Add a dedicated dependency mechanism to `ai.project.toml`

Rejected because `registry.toml` composition already expresses stack dependencies with less complexity.

### Keep both `django-hacksoft-style` and `django-service-layer`

Rejected because the overlap was large enough to make downstream composition noisy and the distinction unclear for most users.

### Move layered architecture rules into `core/architecture`

Rejected because backend-specific and frontend-specific layering guidance would make `core` less focused and less reusable.

## Consequences

### Benefits

- downstream projects can opt into shared layered architecture rules directly
- Django projects get one clearer opt-in stack for the HackSoft-derived service-and-selector style
- the repository uses one consistent composition story based on stack aliases in `registry.toml`

### Costs Or Tradeoffs

- the repository maintains more explicit architecture fragments
- downstream manifests that referenced `django-hacksoft-style` must switch to `django-service-layer`
- downstream manifests that referenced `django-naming` should drop that stack entry
- some older decision records and chat logs remain historical snapshots of the previous naming

## Affected Modules

- `fragments/stacks/layered-architecture.md`
- `fragments/stacks/backend-layered-architecture.md`
- `fragments/stacks/frontend-layered-architecture.md`
- `fragments/stacks/django-service-layer.md`
- `fragments/stacks/django-hacksoft-style.md`
- `fragments/stacks/django-naming.md`
- `registry.toml`
- `README.md`
- `README.ru.md`
- `tests/test_ai_sync.py`

## Invariants And Constraints

- `django-service-layer` must remain an opt-in architectural style, not a Django baseline
- the HackSoft source link and provenance must remain visible in `django-service-layer`
- stack dependencies should continue to be expressed through `registry.toml` composition rather than through a new manifest DSL
- general layered architecture guidance must stay separate from backend-specific and frontend-specific concretizations

## Verification

- `registry.toml` exposes the new layered architecture stack names
- `registry.toml` no longer exposes `django-hacksoft-style`
- `registry.toml` no longer exposes `django-naming`
- `django-service-layer` renders layered architecture, backend layering, and Django-specific service-layer guidance together
- `README.md` and `README.ru.md` document the new stack names and updated Django composition
- renderer tests cover the new composition

## Related Artifacts

- [../../fragments/stacks/layered-architecture.md](../../fragments/stacks/layered-architecture.md)
- [../../fragments/stacks/backend-layered-architecture.md](../../fragments/stacks/backend-layered-architecture.md)
- [../../fragments/stacks/frontend-layered-architecture.md](../../fragments/stacks/frontend-layered-architecture.md)
- [../../fragments/stacks/django-service-layer.md](../../fragments/stacks/django-service-layer.md)
- [../../registry.toml](../../registry.toml)
- [../../README.md](../../README.md)
- [../../README.ru.md](../../README.ru.md)