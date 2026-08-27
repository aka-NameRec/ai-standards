---
title: 'DECISION: add-nextjs-nuxt-vite-fsd-stacks'
permalink: ai-standards/decisions/2026-04-16-add-nextjs-nuxt-vite-fsd-stacks
---

# DECISION: add-nextjs-nuxt-vite-fsd-stacks

Russian localized version: [2026-04-16-add-nextjs-nuxt-vite-fsd-stacks.ru.md](2026-04-16-add-nextjs-nuxt-vite-fsd-stacks.ru.md)

## Status

Accepted

## Date

2026-04-16

## Context

`ai-standards` already had baseline stack fragments for `react`, `vue`, and `typescript`, but it did not yet distinguish between:

- React and Vue as UI framework baselines
- Next.js and Nuxt as full-stack framework environments with server and rendering rules
- Vite as a directly owned build and dev-server environment
- Feature-Sliced Design as an opt-in architectural discipline for larger frontends

That gap made it difficult to express common frontend combinations precisely. A downstream project could request `react` or `vue`, but there was no reusable shared layer for App Router boundaries, Nuxt server routes, Vite environment handling, or slice/public-API constraints in Feature-Sliced Design.

Review against current official Next.js, Nuxt, Vite, and Feature-Sliced Design documentation showed enough durable guidance to justify separate composable stacks:

- Next.js: App Router, Server Components by default, server/client boundaries, explicit caching, route-level loading and error states, and Server Actions vs route handlers.
- Nuxt: SSR-friendly data composables, Nitro server boundaries, runtime config handling, route rules, and hydration-safe client-only code.
- Vite: `import.meta.env`, alias consistency, deliberate plugin usage, and build-specific rather than application-specific configuration.
- FSD: layer hierarchy, slice isolation, public APIs, purpose-based segmentation, and explicit avoidance of dumping unrelated code into `shared`.

## Decision

`ai-standards` adds four new stack fragments: `nextjs`, `nuxt`, `vite`, and `fsd`.

These stacks are intentionally composable:

- `nextjs` complements `react` and usually `typescript`
- `nuxt` complements `vue` and usually `typescript`
- `vite` complements frontend stacks only when the repository directly owns Vite configuration
- `fsd` remains an opt-in architecture stack that can compose with React or Vue projects when the complexity justifies it

The repository also updates `registry.toml`, `README.md`, `README.ru.md`, and renderer tests to cover the new stack names and composition examples.

## Why

- separates UI-framework guidance from full-stack framework and tooling guidance
- allows downstream manifests to describe modern frontend setups more accurately
- keeps `react` and `vue` fragments focused on framework behavior instead of platform-specific concerns
- adds a reusable place for FSD rules without forcing that architecture on every frontend project

## Alternatives Considered

### Expand `react` and `vue` with Next.js, Nuxt, Vite, and FSD rules

Rejected because those concerns are environment- and architecture-specific and should stay composable.

### Add only `nextjs` and `nuxt`

Rejected because Vite and FSD also have enough durable guidance to justify reusable fragments, and downstream projects commonly need them independently of Next.js or Nuxt.

### Keep FSD only as project-local guidance

Rejected because the import hierarchy, public API, and layering constraints are durable enough to be reused across multiple frontend repositories when teams choose that architecture.

## Consequences

### Benefits

- downstream projects can compose `typescript` + `react` + `nextjs`, `typescript` + `vue` + `nuxt`, or `vite` + `fsd` explicitly
- shared frontend rules now reflect the distinction between framework, platform, tooling, and architecture
- the repository gains a cleaner path for future stacks such as `tanstack-query`, `storybook`, or framework-specific testing stacks if needed

### Costs Or Tradeoffs

- more stack fragments increase maintenance cost
- some projects may over-compose stacks unless their manifests stay disciplined
- `fsd` remains intentionally high-level and does not encode every naming convention or folder template from community starter kits

## Affected Modules

- `fragments/stacks/nextjs.md`
- `fragments/stacks/nuxt.md`
- `fragments/stacks/vite.md`
- `fragments/stacks/fsd.md`
- `registry.toml`
- `README.md`
- `README.ru.md`
- `tests/test_ai_sync.py`

## Invariants And Constraints

- `react` and `vue` stay framework-level, not platform-level
- `nextjs`, `nuxt`, and `vite` stay focused on durable environment behavior rather than transient version trivia
- `fsd` stays opt-in and architecture-oriented; it must not silently become a mandatory frontend baseline
- general TypeScript rules remain in the shared `typescript` fragment

## Verification

- renderer tests cover manifests that include `nextjs`, `nuxt`, `vite`, and `fsd`
- `registry.toml` lists the new stacks
- `README.md` and `README.ru.md` document the new stack names and composition guidance

## Related Artifacts

- [../../fragments/stacks/nextjs.md](../../fragments/stacks/nextjs.md)
- [../../fragments/stacks/nuxt.md](../../fragments/stacks/nuxt.md)
- [../../fragments/stacks/vite.md](../../fragments/stacks/vite.md)
- [../../fragments/stacks/fsd.md](../../fragments/stacks/fsd.md)
- [../../registry.toml](../../registry.toml)
- [../../README.md](../../README.md)
- [../../README.ru.md](../../README.ru.md)