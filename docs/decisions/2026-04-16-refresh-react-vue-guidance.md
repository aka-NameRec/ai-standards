---
title: 'DECISION: refresh-react-vue-guidance'
permalink: ai-standards/decisions/2026-04-16-refresh-react-vue-guidance
---

# DECISION: refresh-react-vue-guidance

Russian localized version: [2026-04-16-refresh-react-vue-guidance.ru.md](2026-04-16-refresh-react-vue-guidance.ru.md)

## Status

Accepted

## Date

2026-04-16

## Context

The existing `react` and `vue` stack fragments in `ai-standards` were unevenly maintained.

The Vue fragment already contained useful baseline guidance, but it mixed durable framework rules with some older or underspecified wording. The React fragment was too thin to serve as a realistic shared baseline for modern React projects composed with the new `typescript` stack.

Review against current official React and Vue documentation showed several durable recommendations that should be reflected explicitly:

- React emphasizes pure rendering, deriving state during render when possible, using Effects only for external synchronization, and avoiding unnecessary manual memoization.
- Modern React also provides official APIs for external-store subscriptions and non-urgent rendering work that should influence shared guidance without turning the fragment into framework-specific micro-prescriptions.
- Vue 3 guidance centers on Composition API with `<script setup>`, explicit composable conventions, computed-first derived state, SSR-safe side effects, and deliberate performance work such as stable props and list virtualization.

The repository needs React and Vue fragments that are modern enough to be useful, but still durable, composable, and free from short-lived style dogma.

## Decision

`ai-standards` refreshes the `react` and `vue` stack fragments to align them with current official guidance and common production practices.

The updated React fragment now covers pure rendering, minimal and derived state, Effects as an escape hatch, custom Hooks for reusable stateful logic, restraint around manual memoization, external-store integration boundaries, and deliberate use of transition APIs.

The updated Vue fragment keeps Composition API as the baseline and adds `<script setup>`, computed-first state derivation, stronger composable conventions, SSR-safe side-effect handling, explicit component contracts, and more concrete performance guidance.

## Why

- makes the React stack usable as a real shared baseline instead of a placeholder
- keeps framework guidance aligned with current official recommendations rather than older prompt-pack defaults
- improves composition with the shared `typescript` stack by keeping language-level rules separate from framework rules
- adds durable guardrails around common frontend failure modes such as redundant state, Effect overuse, unstable props, and leaky side effects

## Alternatives Considered

### Leave React and Vue fragments mostly unchanged

Rejected because the current React fragment is materially incomplete, and the current Vue fragment misses several modern conventions that are now standard enough to encode.

### Expand framework fragments with project architecture rules

Rejected because `ai-standards` should keep React and Vue guidance reusable across different frontend architectures and state-management choices.

### Add highly specific rules for React Compiler, Server Components, Vue macros, or individual libraries

Rejected because those topics are either environment-dependent, too fast-moving, or too specific for a durable shared baseline.

## Consequences

### Benefits

- downstream projects get more actionable React and Vue baselines with less local patching
- the React fragment now complements the shared `typescript` stack rather than duplicating it
- the Vue fragment better reflects current Vue 3 conventions and official performance guidance

### Costs Or Tradeoffs

- some teams with legacy Options API or heavy manual memoization patterns may need local overrides
- the repository must keep monitoring framework guidance so these fragments stay durable instead of drifting again

## Affected Modules

- `fragments/stacks/react.md`
- `fragments/stacks/vue.md`
- `tests/test_ai_sync.py`

## Invariants And Constraints

- `react` and `vue` remain framework-specific fragments, not a place for general TypeScript rules
- the fragments stay focused on durable conventions, not transient toolchain fashion or code style trivia
- architecture-specific choices such as folder layout, query libraries, and design systems remain project-local unless they become broadly reusable standards

## Verification

- renderer tests assert the new React wording around Effects and external-store boundaries
- renderer tests assert the new Vue wording around `<script setup>`, computed-first derivation, and composable return conventions
- repository checks continue to pass

## Related Artifacts

- [../../fragments/stacks/react.md](../../fragments/stacks/react.md)
- [../../fragments/stacks/vue.md](../../fragments/stacks/vue.md)
- [../../tests/test_ai_sync.py](../../tests/test_ai_sync.py)