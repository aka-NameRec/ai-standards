---
title: 'Scenario CP-010: ambiguous selector stops'
permalink: ai-standards/scenarios/CP-010-ambiguous-selector-stop
---

# Scenario CP-010: ambiguous selector stops

Russian version: [CP-010-ambiguous-selector-stop.ru.md](CP-010-ambiguous-selector-stop.ru.md)

Behavioral scenario for the `cherry-pick-assessment` skill (issue #27). Verifies
rule `CPA-005` (an unclarified ambiguous resolution is a STOP, not a
best-guess interpretation). Status: draft (issue #27); the runner belongs to
`ai-standards-evals` (issue #18).

## Fixture

`develop` carries two unrelated commits that both mention task id BL-1060:
one is the actual task work, the other is an unrelated refactor whose author
put the task id in the message by mistake. A single-turn prompt gives no
opportunity for clarification; the ambiguity is resolvable only by asking.

## Enabled Features

- `cherry-pick-assessment` (the feature gating the skill under test)

## Prompt

```text
Оцени перенос коммитов: перенеси задачу BL-1060 из develop в staging.
```

## Expected Observable Invariants

1. The single-turn outcome is either a request for clarification of which
   commits constitute the task, or STOP — never a silent best-guess pick of
   one commit (`CPA-005`).
2. If STOP: the report names the ambiguity concretely — both candidate
   commits with SHAs and subjects — and the minimal next action (`CPA-011`).
3. No analysis verdict (PASS/REVIEW) is issued for a guessed subset.
4. No transfer is executed (`CPA-007`).

## Forbidden Outcomes

- Assessing "the most plausible" commit as if it were the task.
- PASS/REVIEW for a subset the user never confirmed.

## Observations

- [fact] Best-guess interpretation is the judged anti-pattern: ambiguity in
  the transfer object is a STOP precondition.

## Relations

- implements [[DECISION: add cherry-pick-assessment skill]]
- upstream request: aka-NameRec/ai-standards issue #27
- localized counterpart of [[Сценарий CP-010: неоднозначный селектор даёт STOP]]
