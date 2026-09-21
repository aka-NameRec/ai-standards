---
title: 'Scenario CR-009: missing error-path test'
permalink: ai-standards/scenarios/CR-009-missing-error-path-test
---

# Scenario CR-009: missing error-path test

Russian version: [CR-009-missing-error-path-test.ru.md](CR-009-missing-error-path-test.ru.md)

Behavioral scenario for the code-review workflow. Verifies rule `RVW-008`
(quality: test coverage of edge cases). Status: draft (issue #18); the runner
belongs to `ai-standards-evals`.

## Fixture

Pre-state: a small Python project with a config-parsing module and its tests.

Diff under review: `src/config.py` adds `parse_timeout(text: str) -> int`
which raises `ValueError` for non-positive or non-numeric values; the new
tests cover only the success path (`"30"` → `30`).

## Enabled Features

- `code-review` (the workflow under test; the `standard-code-review` skill is its packaged entry point)

## Prompt

```text
code review
```

## Expected Observable Invariants

1. The uncovered error branch is reported as a meaningful Quality concern (`RVW-008`).
2. The finding is scoped to the error path of the changed behavior, not to every changed line (`RVW-008`).
3. Locations are cited for the uncovered branch (`RVW-010`).

## Forbidden Outcomes

- The untested error branch passes without a Quality finding.
- A blanket demand for tests on cosmetic or unchanged lines.
- Manufactured findings in unrelated dimensions.

## Observations

- [fact] The scenario draws the line between meaningful coverage gaps and mechanical test demands.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Spec: ai-standards-evals repository (issue #18)]]
- localized counterpart of [[Сценарий CR-009: отсутствующий тест:error-пути]]
