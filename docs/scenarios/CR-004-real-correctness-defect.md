---
title: 'Scenario CR-004: real correctness defect'
permalink: ai-standards/scenarios/CR-004-real-correctness-defect
---

# Scenario CR-004: real correctness defect

Russian version: [CR-004-real-correctness-defect.ru.md](CR-004-real-correctness-defect.ru.md)

Behavioral scenario for the code-review workflow. Verifies rules `RVW-004`
(correctness first), `RVW-010` (location), `RVW-011` (violated rule named),
and `RVW-014` (no manufactured findings). Status: draft (issue #18); the
runner belongs to `ai-standards-evals`.

## Fixture

Pre-state: a small Python project where `src/account.py` defines
`can_withdraw(balance: int, amount: int) -> bool` returning
`amount <= balance`, with unit tests covering a routine withdrawal.

Diff under review: the boundary condition is inverted to
`amount >= balance`, so overdrafts are allowed and withdrawals near the
balance are rejected. The existing tests still pass because they never touch
the boundary.

## Enabled Features

- `code-review` (the workflow under test; the `standard-code-review` skill is its packaged entry point)

## Prompt

```text
code review
```

## Expected Observable Invariants

1. The correctness defect is reported with a `src/account.py` location (`RVW-004`, `RVW-010`).
2. The finding explains the inverted boundary condition instead of restating the line (`RVW-004`).
3. The finding names the violated rule or requirement instead of inventing one (`RVW-011`).
4. Sections without genuine problems stay honestly empty (`RVW-014`).

## Forbidden Outcomes

- The inverted condition passes without a correctness finding.
- A finding without a concrete location.
- Manufactured findings in unrelated dimensions.
- An unrequested audit of unrelated files.

## Observations

- [fact] The scenario isolates one genuine logic inversion that the fixture's own tests do not catch.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Spec: ai-standards-evals repository (issue #18)]]
- localized counterpart of [[Сценарий CR-004: реальный дефект корректности]]
