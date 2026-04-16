# DECISION: refresh-python-infrastructure-guidance

Russian localized version: [2026-04-16-refresh-python-infrastructure-guidance.ru.md](2026-04-16-refresh-python-infrastructure-guidance.ru.md)

## Status

Accepted

## Date

2026-04-16

## Context

`ai-standards` had grown Python guidance across multiple layers with unclear boundaries.

`python` language guidance lived partly in `fragments/core/python.md` and partly in `fragments/stacks/python.md`, which made the shared layering inconsistent: Python-specific rules appeared in `core`, while other language-specific guidance such as TypeScript already lived entirely in stack fragments.

The Django and FastAPI baselines also needed refinement. `fragments/stacks/fastapi.md` was too thin to serve as a durable shared baseline, while parts of the Django guidance mixed framework-neutral rules with project-specific architectural choices.

The strongest ambiguity was in the Django opt-in area. `django-drf.md` and `django-save-lifecycle.md` had imported HackSoft-derived and local project patterns as if they were shared defaults, even though several of those rules were actually optional architectural conventions rather than framework baselines.

## Decision

`ai-standards` consolidates Python-specific guidance into stack fragments and separates Django framework baselines from opinionated application-architecture patterns.

The repository removes `fragments/core/python.md` and keeps Python guidance in `fragments/stacks/python.md` as the single shared Python baseline.

The repository expands `fastapi` into a fuller framework baseline, refines `django` into a more neutral framework baseline, and softens `django-drf` so it no longer presents one local DRF style as the default shared rule set.

The repository removes `django-save-lifecycle` and replaces it with two explicit opt-in fragments:

- `django-hacksoft-style` for the HackSoft-derived service-and-selector architectural style
- `django-save-orchestration` for the optional unified `save()` wrapper pattern, including explicit guidance to use `transaction.on_commit` when post-save side effects depend on a successful commit

## Why

- keeps `core` focused on cross-technology engineering rules instead of language-specific guidance
- makes Python guidance easier to discover and evolve because it lives in one place
- strengthens FastAPI and Django baselines with more durable official-framework guidance
- avoids presenting local or opinionated Django/DRF conventions as universal best practices
- preserves useful architectural patterns by making them explicit opt-in fragments instead of hidden defaults

## Alternatives Considered

### Keep Python rules split between `core/python` and `stacks/python`

Rejected because it weakens the layering model and makes Python guidance harder to reason about.

### Keep `django-save-lifecycle` as a shared default fragment

Rejected because it mixes a useful project-level orchestration pattern with framework-baseline rules and overstates one local convention as a general best practice.

### Move unified `save()` orchestration into `django.md`

Rejected because the pattern is not a Django baseline. It is a reusable architectural convention that should be adopted explicitly and only where create/update orchestration is mostly symmetric.

## Consequences

### Benefits

- Python projects now depend on one clear shared Python baseline
- downstream Django projects can choose between neutral framework rules and explicit HackSoft-derived architecture layers
- the unified `save()` pattern remains reusable without being forced on every Django project
- decision boundaries between baseline rules and opt-in architecture styles are clearer in both code and documentation

### Costs Or Tradeoffs

- the repository maintains additional stack fragments and associated documentation
- downstream manifests that used `django-save-lifecycle` must switch to the new explicit stack names if they want the same style
- teams must make a more explicit choice about whether they want HackSoft-style layering and unified save orchestration

## Affected Modules

- `fragments/stacks/python.md`
- `fragments/stacks/django.md`
- `fragments/stacks/fastapi.md`
- `fragments/stacks/django-drf.md`
- `fragments/stacks/django-hacksoft-style.md`
- `fragments/stacks/django-save-orchestration.md`
- `fragments/stacks/django-save-lifecycle.md`
- `registry.toml`
- `README.md`
- `README.ru.md`
- `ai.project.toml`
- `templates/project_manifest.toml`
- `tests/test_ai_sync.py`
- `AGENTS.md`

## Invariants And Constraints

- Python-specific guidance must not live in `core`
- `django.md` and `django-drf.md` must remain baseline-oriented and avoid project-specific style dogma
- HackSoft-derived architecture rules must be explicit opt-in fragments
- unified `save()` orchestration must be documented as an optional convention rather than a universal best practice
- commit-dependent side effects in the unified `save()` pattern must use `transaction.on_commit`

## Verification

- Python guidance renders correctly without `core/python`
- `registry.toml` exposes `django-hacksoft-style` and `django-save-orchestration` and no longer exposes `django-save-lifecycle`
- `README.md` and `README.ru.md` show the new Django composition examples
- renderer tests cover the updated Python baseline, softened DRF guidance, and the new opt-in Django fragments
- repository checks continue to pass

## Related Artifacts

- [../../fragments/stacks/python.md](../../fragments/stacks/python.md)
- [../../fragments/stacks/django.md](../../fragments/stacks/django.md)
- [../../fragments/stacks/fastapi.md](../../fragments/stacks/fastapi.md)
- [../../fragments/stacks/django-drf.md](../../fragments/stacks/django-drf.md)
- [../../fragments/stacks/django-hacksoft-style.md](../../fragments/stacks/django-hacksoft-style.md)
- [../../fragments/stacks/django-save-orchestration.md](../../fragments/stacks/django-save-orchestration.md)
- [../../registry.toml](../../registry.toml)
- [../../README.md](../../README.md)
- [../../README.ru.md](../../README.ru.md)
