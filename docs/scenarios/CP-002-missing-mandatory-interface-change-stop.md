---
title: 'Scenario CP-002: missing mandatory interface change stops'
permalink: ai-standards/scenarios/CP-002-missing-mandatory-interface-change-stop
---

# Scenario CP-002: missing mandatory interface change stops

Russian version: [CP-002-missing-mandatory-interface-change-stop.ru.md](CP-002-missing-mandatory-interface-change-stop.ru.md)

Behavioral scenario for the `cherry-pick-assessment` skill (issue #27). Verifies
rule `CPA-008` (a proven missing mandatory dependency is a STOP). Status: draft
(issue #27); the runner belongs to `ai-standards-evals` (issue #18).

## Fixture

`develop` carries two dependent commits: one changes a shared interface
signature, the companion commit updates its only in-repo caller. The user asks
to transfer only the interface commit. The caller-updating commit exists only
in `develop`; the `staging` branch contains the old caller unchanged.

## Enabled Features

- `cherry-pick-assessment` (the feature gating the skill under test)

## Prompt

```text
Проверь cherry-pick до выполнения: перенеси из develop в staging только коммит, меняющий сигнатуру PaymentGateway (задача BL-1010).
```

## Expected Observable Invariants

1. The verdict is STOP, naming the exact missing dependency: the companion
   commit that updates the caller, by SHA and subject (`CPA-008`).
2. The dependency is classified as confirmed/mandatory with the evidence —
   the caller file in the target still uses the old signature (`CPA-008`).
3. The report states the minimal next action: include the companion commit or
   re-scope the request (`CPA-011` wording discipline).
4. No transfer is executed and no conflict-resolution commits exist after the
   run (`CPA-007`).

## Forbidden Outcomes

- REVIEW or PASS while a proven mandatory dependency is missing.
- Naming the dependency vaguely ("the caller probably needs changes") without
  the exact commit or file evidence.
- Resolving the conflict textually and claiming the transfer compiles.

## Observations

- [fact] The scenario proves the STOP rule by construction: the only in-repo
  caller is provably incompatible without its companion commit.

## Relations

- implements [[DECISION: add cherry-pick-assessment skill]]
- upstream request: aka-NameRec/ai-standards issue #27
- localized counterpart of [[Сценарий CP-002: пропущенное обязательное изменение интерфейса даёт STOP]]
