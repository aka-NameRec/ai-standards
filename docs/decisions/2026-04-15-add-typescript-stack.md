---
title: 'DECISION: add-typescript-stack'
permalink: ai-standards/decisions/2026-04-15-add-typescript-stack
---

# DECISION: add-typescript-stack

Russian localized version: [2026-04-15-add-typescript-stack.ru.md](2026-04-15-add-typescript-stack.ru.md)

## Status

Accepted

## Date

2026-04-15

## Context

`ai-standards` already contains stack fragments for Python, FastAPI, Django, React, Vue, PostgreSQL, and Java Spring, but it had no reusable baseline fragment for TypeScript itself.

Review of `awesome-cursorrules`, official TypeScript documentation, and `typescript-eslint` guidance showed that there is enough durable language-level material to justify a shared `typescript` stack, but not enough consistency to justify importing framework-specific conventions into the same fragment.

The repository needs a reusable TypeScript layer that can be composed with `react`, `vue`, or future stacks such as `nestjs` without pulling in architecture-specific or UI-framework-specific rules by default.

## Decision

`ai-standards` adds a new shared `typescript` stack fragment focused on language-level and type-system guidance.

The fragment covers strict typing defaults, boundary typing, safe narrowing, precise optionality, modern module-boundary semantics, and explicit validation of untrusted input.

The fragment does not include React, Vue, Next.js, NestJS, or other framework-specific conventions, and it does not prescribe architecture patterns such as repository, factory, builder, or Result-type-based error handling.

## Why

- fills an existing gap between framework stacks and language-level guidance
- allows downstream projects to compose `typescript` with `react`, `vue`, and future TS-based stacks explicitly
- keeps the shared fragment reusable across frontend and backend repositories
- follows official TypeScript and `typescript-eslint` guidance more closely than upstream prompt collections alone
- avoids importing style dogma and framework coupling into the shared layer

## Alternatives Considered

### Keep TypeScript guidance embedded only inside framework stacks

Rejected because it duplicates language rules across stacks and leaves non-framework TypeScript projects without a reusable baseline.

### Add TypeScript rules by expanding `react` and `vue`

Rejected because language-level rules should remain composable and independent from specific UI frameworks.

### Import broader TypeScript prompt packs directly

Rejected because most upstream packs mix reusable TypeScript guidance with framework conventions, folder structures, architecture opinions, and rigid style rules that do not fit shared standards.

## Consequences

### Benefits

- downstream projects can adopt one clear TypeScript baseline without inheriting framework-specific rules
- TypeScript guidance now lives in one shared place and can be reused consistently
- existing `react` and `vue` stacks can stay focused on framework behavior instead of general TS language rules

### Costs Or Tradeoffs

- downstream projects still need additional stacks or local overrides for framework- and runtime-specific TS conventions
- the repository must maintain one more stack fragment and its documentation coverage

## Affected Modules

- `fragments/stacks/typescript.md`
- `registry.toml`
- `README.md`
- `README.ru.md`
- `tests/test_ai_sync.py`

## Invariants And Constraints

- the shared TypeScript stack must remain language-level and framework-neutral
- existing `core/error-handling` rules based on explicit exceptions remain in force
- architecture patterns such as repository layering or dependency injection are not mandated by the TypeScript stack
- framework-specific TS rules stay in the relevant stack fragments or future dedicated stacks

## Verification

- `registry.toml` exposes the new `typescript` stack
- `README.md` and `README.ru.md` list `typescript` among current stack fragments and show how it composes with other stacks
- renderer tests cover a manifest that includes the new `typescript` stack
- repository checks continue to pass

## Related Artifacts

- [../../fragments/stacks/typescript.md](../../fragments/stacks/typescript.md)
- [../../registry.toml](../../registry.toml)
- [../../README.md](../../README.md)
- [../../README.ru.md](../../README.ru.md)