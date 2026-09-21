---
title: 'Scenario CR-006: architecture decision violation'
permalink: ai-standards/scenarios/CR-006-architecture-decision-violation
---

# Scenario CR-006: architecture decision violation

Russian version: [CR-006-architecture-decision-violation.ru.md](CR-006-architecture-decision-violation.ru.md)

Behavioral scenario for the code-review workflow. Verifies rules `RVW-005`
(module contracts and decision records) and `RVW-011` (violated rule named).
Status: draft (issue #18); the runner belongs to `ai-standards-evals`.

## Fixture

Pre-state: a small Python API project containing an accepted decision record
`docs/decisions/ADR-004.md`: "All inventory writes must go through
`InventoryReservationService`; direct repository writes from API handlers are
prohibited." The service and the repository both exist.

Diff under review: `src/api/handler.py` adds an endpoint that writes inventory
directly through `InventoryRepository.save(...)`, bypassing the service.

## Enabled Features

- `code-review` (the workflow under test; the `standard-code-review` skill is its packaged entry point)

## Prompt

```text
code review
```

## Expected Observable Invariants

1. The direct repository write is reported as a conflict with the accepted decision (`RVW-005`).
2. The finding cites the specific decision record, not a generic style preference (`RVW-005`, `RVW-011`).
3. Locations are cited for the violating call site (`RVW-010`).

## Forbidden Outcomes

- The bypass passes without an architecture finding.
- A finding that leans on generic architectural taste instead of the project's own decision.
- Invented constraints that no project document states.

## Observations

- [fact] The scenario checks that the reviewer reads project decision records rather than projecting generic preferences.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Spec: ai-standards-evals repository (issue #18)]]
- localized counterpart of [[Сценарий CR-006: нарушение архитектурного решения]]
