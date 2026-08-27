---
title: 'DECISION: add-tanstack-query-stack'
permalink: ai-standards/decisions/2026-04-16-add-tanstack-query-stack
---

# DECISION: add-tanstack-query-stack

Russian localized version: [2026-04-16-add-tanstack-query-stack.ru.md](2026-04-16-add-tanstack-query-stack.ru.md)

## Status

Accepted

## Date

2026-04-16

## Context

`ai-standards` now distinguishes between frontend framework baselines such as `react` and `vue`, full-stack runtimes such as `nextjs` and `nuxt`, and tooling or architecture stacks such as `vite` and `fsd`.

One common frontend concern was still missing: a reusable server-state and cache-synchronization layer for applications that rely on TanStack Query rather than ad hoc fetch-and-state patterns.

Official TanStack Query guidance shows enough durable, cross-framework practices to justify a shared stack:

- TanStack Query manages server state, not every form of local UI state
- stable query keys and centralized query-client boundaries matter for predictable caching
- mutation flows should deliberately revalidate, update, or reconcile affected cache entries
- optimistic updates are useful but should remain explicit and reversible
- SSR prefetching, dehydration, and hydration belong at application boundaries

Vue projects also commonly refer to the adapter as `vue-query`, even though the maintained package and guidance live under TanStack Query.

## Decision

`ai-standards` adds a shared `tanstack-query` stack fragment and a `vue-query` compatibility alias.

The `tanstack-query` fragment stays framework-neutral and focuses on server-state boundaries, query-key discipline, mutation invalidation, optimistic updates, hydration boundaries, and centralized query-client ownership.

The `vue-query` stack name is implemented as a registry alias for `tanstack-query` plus `vue`, so downstream Vue manifests can use the familiar name without forcing a second near-duplicate fragment.

## Why

- adds a reusable server-state baseline that composes cleanly with `react`, `vue`, `nextjs`, or `nuxt`
- keeps TanStack Query rules in one shared place instead of duplicating them across framework stacks
- supports the common `vue-query` naming convention without introducing duplicated maintenance surface

## Alternatives Considered

### Encode TanStack Query rules directly inside `react` and `vue`

Rejected because TanStack Query is optional and should stay composable instead of becoming implicit framework guidance.

### Add separate `tanstack-query` and `vue-query` fragments

Rejected because the durable guidance is mostly shared, while Vue-specific behavior is already covered by the `vue` fragment and framework runtime fragments such as `nuxt`.

### Keep TanStack Query guidance only in project-local overrides

Rejected because the query-key, invalidation, and hydration rules are durable enough to recur across multiple repositories.

## Consequences

### Benefits

- downstream projects can declare `typescript` + `react` + `tanstack-query` explicitly
- Vue projects can use the familiar `vue-query` name without giving up shared stack composition
- shared frontend guidance now covers a common server-state layer directly

### Costs Or Tradeoffs

- teams still need local rules for domain-specific query factories, caching lifetimes, and error UX details
- the alias approach means `vue-query` remains a naming convenience rather than an independently evolving stack

## Affected Modules

- `fragments/stacks/tanstack-query.md`
- `registry.toml`
- `README.md`
- `README.ru.md`
- `tests/test_ai_sync.py`

## Invariants And Constraints

- `tanstack-query` remains framework-neutral and server-state-oriented
- Vue-specific component and composable behavior stays in `vue` and `nuxt`
- `vue-query` remains a compatibility alias, not a separate source fragment

## Verification

- renderer tests cover `tanstack-query` with React
- renderer tests cover the `vue-query` alias composition
- `registry.toml`, `README.md`, and `README.ru.md` document the new stack name and alias

## Related Artifacts

- [../../fragments/stacks/tanstack-query.md](../../fragments/stacks/tanstack-query.md)
- [../../registry.toml](../../registry.toml)
- [../../README.md](../../README.md)
- [../../README.ru.md](../../README.ru.md)