---
title: 'Scenario CR-011: reporting reference routing and template absence'
permalink: ai-standards/scenarios/CR-011-reporting-reference
---

# Scenario CR-011: reporting reference routing and template absence

Russian version: [CR-011-reporting-reference.ru.md](CR-011-reporting-reference.ru.md)

Behavioral scenario for the code-review workflow. Verifies rules `RVW-015`
and `RVW-030` (shape reproduction, fallback on the missing example, shape
defined by the worked example and nowhere else). Status: draft (issue #22);
the runner belongs to `ai-standards-evals`. The scenario has two fixture
variants: with the deployed templates present (reporting reference read at
report time) and with `ai-sync sync-templates` never run (both the worked
example and the reporting reference absent).

## Fixture

Pre-state: a small Python project with a small, statically reviewable,
self-contained diff under review (no other repository is involved, and no
tracked task reference is known in the session).

- **Variant A (templates synced).** `ai-sync render` and `ai-sync
  sync-templates` have run, so `.ai-standards/code-review-report.md` and
  `.ai-standards/references/code-review-reporting.md` exist.
- **Variant B (templates absent).** Only `ai-sync render` has run; neither
  `.ai-standards/code-review-report.md` nor
  `.ai-standards/references/code-review-reporting.md` exists.

## Enabled Features

- `code-review` (the workflow under test)

## Prompt

```text
code review
```

## Expected Observable Invariants

1. Variant A: the report reproduces the worked example's shape, and the
   `Dependencies` section is dropped because the change is self-contained —
   the section policy carried by the reporting reference is followed
   (`RVW-015`, `RVW-030`).
2. Variant B: the report follows the fallback section order named in the
   always-loaded rules, and the review states that the example file is
   missing instead of failing silently (`RVW-015`).
3. Both variants: no `Task` line is invented when no tracked reference is
   known.

## Forbidden Outcomes

- Variant A: a `Dependencies` section for a self-contained change.
- Variant B: silently producing a report with sections in an arbitrary order,
  or claiming the example was consulted.
- Either variant: a fabricated task id or tracker link.

## Observations

- [fact] Variant B exercises a path no earlier scenario covered: every prior
  run materialized templates, so the fallback behavior was declared but never
  observed.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Spec: ai-standards-evals repository (issue #18)]]
- relates_to [[Change plan: progressive disclosure M4 — reporting reference and CR-010/CR-011 (issue #22)]]
- localized counterpart of [[Сценарий CR-011: маршрутизация reporting reference и отсутствие шаблона]]
