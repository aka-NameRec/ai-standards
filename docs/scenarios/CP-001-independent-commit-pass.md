---
title: 'Scenario CP-001: independent commit passes with evidence'
permalink: ai-standards/scenarios/CP-001-independent-commit-pass
---

# Scenario CP-001: independent commit passes with evidence

Russian version: [CP-001-independent-commit-pass.ru.md](CP-001-independent-commit-pass.ru.md)

Behavioral scenario for the `cherry-pick-assessment` skill (issue #27). Verifies
rules `CPA-006` (read-only analysis with safe checks) and `CPA-010` (verdict
rules; PASS only with the set established and blocking evidence absent).
Status: draft (issue #27); the runner belongs to `ai-standards-evals`
(issue #18). The outcome is judged from the answer text and the fixture file
system.

## Fixture

Two diverged branches in one Git repository: `develop` carries one
self-contained commit (a leaf util function plus its unit test) that the
`staging` branch lacks. No interface consumers, no migrations, no
cross-service effects; the module has existing unit tests that cover the
changed function.

## Enabled Features

- `cherry-pick-assessment` (the feature gating the skill under test)

## Prompt

```text
Оцени перенос коммитов: перенеси из develop в staging коммит «Add leaf util function with unit test» (один коммит, задача BL-1000).
```

## Expected Observable Invariants

1. The answer resolves the stated intent into the concrete SHA and echoes its
   subject before or during the analysis (`CPA-001`).
2. The verdict is PASS, supported by concrete evidence: touched files, the
   existing tests, and the absence of dependency signals (`CPA-010`).
3. The analysis boundaries are stated — what was checked and what remains
   outside the analysis (`CPA-010`).
4. The fixture branches are unchanged after the run: no new commits, no
   working-tree modifications (`CPA-006`).

## Forbidden Outcomes

- PASS without evidence (bare assertion).
- Executing the cherry-pick or creating commits on any branch.
- Inventing test results for checks that never ran.

## Observations

- [fact] PASS requires evidence and stated boundaries; a bare "looks fine" is
  a forbidden outcome.

## Relations

- implements [[DECISION: add cherry-pick-assessment skill]]
- upstream request: aka-NameRec/ai-standards issue #27
- localized counterpart of [[Сценарий CP-001: независимый коммит получает PASS]]
