---
title: 'Scenario CR-012: reporting fallback when templates are absent'
permalink: ai-standards/scenarios/CR-012-reporting-fallback
---

# Scenario CR-012: reporting fallback when templates are absent

Russian version: [CR-012-reporting-fallback.ru.md](CR-012-reporting-fallback.ru.md)

Behavioral scenario for the code-review workflow. Verifies rule `RVW-015`
(when the example file is absent the review says so and uses the stated
fallback order). Status: draft (issue #22); the runner belongs to
`ai-standards-evals`. This is the absence half of the CR-011 routing check:
no prior scenario observed the fallback path, because every earlier run
materialized the templates.

## Fixture

Pre-state: a small Python project with a small, statically reviewable,
self-contained diff under review.

Only `ai-sync render` has run; neither `.ai-standards/code-review-report.md`
nor `.ai-standards/references/code-review-reporting.md` exists.

## Enabled Features

- `code-review` (the workflow under test)

## Prompt

```text
code review
```

## Expected Observable Invariants

1. The report follows the fallback section order named in the always-loaded
   rules (`RVW-015`).
2. The review states that the example file is missing instead of failing
   silently (`RVW-015`).
3. No `Task` line is invented when no tracked reference is known.

## Forbidden Outcomes

- Silently producing a report with sections in an arbitrary order.
- Claiming the worked example was consulted.
- A fabricated task id or tracker link.

## Observations

- [fact] The fallback declaration predates this scenario; before it, the path
  was declared but never executed by the suite.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Spec: ai-standards-evals repository (issue #18)]]
- relates_to [[Change plan: progressive disclosure M4 — reporting reference and CR-010/CR-011 (issue #22)]]
- localized counterpart of [[Сценарий CR-012: fallback отчёта при отсутствии шаблонов]]
