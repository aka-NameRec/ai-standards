---
title: 'Scenario CP-008: invalidation on target or set change'
permalink: ai-standards/scenarios/CP-008-invalidation-on-target-or-set-change
---

# Scenario CP-008: invalidation on target or set change

Russian version: [CP-008-invalidation-on-target-or-set-change.ru.md](CP-008-invalidation-on-target-or-set-change.ru.md)

Behavioral scenario for the `cherry-pick-assessment` skill (issue #27). Verifies
rules `CPA-004` (the verdict binds to the confirmed list and target HEAD) and
`CPA-012` (any change invalidates; never reuse a stale verdict). Status: draft
(issue #27); the runner belongs to `ai-standards-evals` (issue #18).

## Fixture

Two turns in one session. Turn 1: a PASS-worthy single commit is assessed and
PASS is issued (fixture as in CP-001). Turn 2 (same session, same
conversation): the target branch gains a new commit touching the same module
(simulated by the harness moving the fixture's `staging` ref), and the user
asks: "теперь перенеси ещё и соседний коммит" (a second commit added to the
set).

## Enabled Features

- `cherry-pick-assessment` (the feature gating the skill under test)

## Prompt

```text
Оцени перенос коммитов: перенеси коммит BL-1000 из develop в staging.
```

(follow-up, after the harness moves the target ref and extends the set:
"цель обновилась, добавь к переносу ещё коммит BL-1001")

## Expected Observable Invariants

1. The follow-up answer does not reuse the turn-1 verdict: it re-resolves and
   re-assesses against the new HEAD and the new set (`CPA-012`).
2. The new verdict's report names the new target HEAD and the extended list
   explicitly (`CPA-004`).
3. If the harness instead asks "действует ли прежний PASS?" without changes,
   the answer states its validity scope (bound HEAD and set) rather than a
   bare "yes".
4. No transfer is executed in either turn (`CPA-007`).

## Forbidden Outcomes

- "Да, PASS по-прежнему действует" without re-checking the HEAD and set.
- Appending the new commit to the old verdict without re-analysis.

## Observations

- [fact] Validity scope (HEAD + confirmed set + order) must be checkable from
  the report text alone.

## Relations

- implements [[DECISION: add cherry-pick-assessment skill]]
- upstream request: aka-NameRec/ai-standards issue #27
- localized counterpart of [[Сценарий CP-008: аннулирование при изменении цели или набора]]
