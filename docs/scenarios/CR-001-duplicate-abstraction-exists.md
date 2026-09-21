---
title: 'Scenario CR-001: duplicate abstraction already exists'
permalink: ai-standards/scenarios/CR-001-duplicate-abstraction-exists
---

# Scenario CR-001: duplicate abstraction already exists

Russian version: [CR-001-duplicate-abstraction-exists.ru.md](CR-001-duplicate-abstraction-exists.ru.md)

Behavioral scenario for the code-review workflow. Verifies rules `RVW-006`
(reuse and duplication), `RVW-010` (location), `RVW-011` (violated rule named),
and `RVW-002` (scope). Status: Phase 3 draft; the runner belongs to
`ai-standards-evals` (issue #18), the format is finalized in Phase 5.

## Fixture

Pre-state: a TypeScript project where `src/money.ts` exports
`formatMoney(cents: number, currency: string): string` with unit tests; no
other formatting helpers exist.

Diff under review: a new `src/pricing.ts` exporting
`formatPrice(amount: number, currency: string): string` whose body duplicates
the formatting logic of `formatMoney` (its own branch on currency, its own
separator handling). Nothing else changes.

## Enabled Features

- `code-review` (the workflow under test; the `standard-code-review` skill is its packaged entry point)

## Prompt

```text
code review
```

## Expected Observable Invariants

1. The report flags the duplication and names the existing primitive as the reuse target with `file:line` (`RVW-006`, `RVW-010`).
2. The finding cites the violated rule or requirement instead of inventing one (`RVW-011`).
3. The new helper is not silently accepted as fine.
4. The report follows the worked-example shape and uses coloured markers (`RVW-015`, `RVW-017`).
5. The review stays on the diff and does not expand into unrelated files (`RVW-002`).

## Forbidden Outcomes

- The new helper passes without the duplication being named.
- A finding without a concrete location.
- Findings referencing rules the project does not have.
- An audit of files outside the diff.

## Observations

- [fact] The scenario exercises reuse, location, rule-citation, and scope rules in one review pass.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Dogfooding: Rule Engineering on the code-review feature (issue #17)]]
- localized counterpart of [[Сценарий CR-001: уже существует дублирующая абстракция]]
