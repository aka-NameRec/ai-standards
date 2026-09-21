---
title: 'Scenario CR-005: new internal duplication without a prior helper'
permalink: ai-standards/scenarios/CR-005-new-internal-duplication
---

# Scenario CR-005: new internal duplication without a prior helper

Russian version: [CR-005-new-internal-duplication.ru.md](CR-005-new-internal-duplication.ru.md)

Behavioral scenario for the code-review workflow. Verifies rule `RVW-006`
(reuse and duplication). It discriminates DRY from Reuse: the change
introduces the duplication itself, and no reusable abstraction existed
before. Status: draft (issue #18); the runner belongs to
`ai-standards-evals`.

## Fixture

Pre-state: a small Python project with two independent report modules and no
date-range formatting helper anywhere.

Diff under review: the patch adds `src/csv_export.py` and `src/json_export.py`,
each carrying its own identical private `format_period(start, end)`
implementation (same rounding, same separator handling, same empty-range
behavior).

## Enabled Features

- `code-review` (the workflow under test; the `standard-code-review` skill is its packaged entry point)

## Prompt

```text
code review
```

## Expected Observable Invariants

1. The new duplication between the two modules is flagged as a DRY/Quality concern (`RVW-006`).
2. The finding does not claim that an existing reusable project abstraction was ignored — none exists.
3. Locations in both new modules are cited (`RVW-006`, `RVW-010`).

## Forbidden Outcomes

- The duplicated helper passes without the duplication being named.
- A finding asserting that an existing helper was bypassed.
- A finding without concrete locations.

## Observations

- [fact] Scenario CR-001 (an abstraction already exists) and this scenario separate Reuse from DRY: only the change itself introduces the duplication here.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Spec: ai-standards-evals repository (issue #18)]]
- localized counterpart of [[Сценарий CR-005: новое внутреннее дублирование без готового помощника]]
