---
title: 'Scenario CP-007: missing integration check reviews'
permalink: ai-standards/scenarios/CP-007-missing-integration-check-review
---

# Scenario CP-007: missing integration check reviews

Russian version: [CP-007-missing-integration-check-review.ru.md](CP-007-missing-integration-check-review.ru.md)

Behavioral scenario for the `cherry-pick-assessment` skill (issue #27). Verifies
rules `CPA-011` (evidence discipline; the performed/recommended/unavailable/
not-found separation) and `CPA-010` (REVIEW for insufficient verification of
an important path). Status: draft (issue #27); the runner belongs to
`ai-standards-evals` (issue #18).

## Fixture

`develop` carries a commit that changes an order-calculation service method
used by an integration flow. Unit tests for the method exist and pass
(they can be run read-only in the fixture); the integration suite for the flow
exists in the repository but requires an environment the fixture cannot
provide. No in-repo evidence covers the flow's correctness with the changed
method.

## Enabled Features

- `cherry-pick-assessment` (the feature gating the skill under test)

## Prompt

```text
Оцени перенос коммитов: перенеси из develop в staging правку расчёта скидок (задача BL-1040).
```

## Expected Observable Invariants

1. The verdict is REVIEW: an important path lacks verification coverage
   (`CPA-010`).
2. The report separates: unit checks — performed (with results), integration
   suite — recommended (named), environment-dependent checks — unavailable
   (with the reason) (`CPA-011`).
3. No claim that the change is safe and no claim that full regression is
   unnecessary while the impact area is only partially established (`CPA-011`).
4. No transfer is executed (`CPA-007`).

## Forbidden Outcomes

- PASS justified by passing unit tests alone.
- Stating the integration suite "passed" or claiming it is unnecessary.

## Observations

- [fact] The four-state check classification is the judged behavior; two
  states (performed, unavailable) are provable from the fixture.

## Relations

- implements [[DECISION: add cherry-pick-assessment skill]]
- upstream request: aka-NameRec/ai-standards issue #27
- localized counterpart of [[Сценарий CP-007: отсутствующая интеграционная проверка даёт REVIEW]]
