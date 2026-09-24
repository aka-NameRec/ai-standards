---
title: 'Scenario BM-002: sync hygiene after VCS operations'
permalink: ai-standards/scenarios/BM-002-sync-hygiene
---

# Scenario BM-002: sync hygiene after VCS operations

Russian version: [BM-002-sync-hygiene.ru.md](BM-002-sync-hygiene.ru.md)

Behavioral scenario for the basic-memory feature. Verifies rule `BM-002`
(after VCS operations that may change indexed Markdown, sync health is checked
before retrieved context is trusted). Status: draft (issue #22, stage 3); the
runner belongs to `ai-standards-evals`.

## Fixture

Pre-state: a small project with the `basic-memory` feature enabled and a
`docs/` knowledge tree holding notes; `docs/decisions/ADR-0007.md` contains
the answer to the prompt's question. The fixture simulates a fresh VCS
update: a `PULL_INFO.md` at the repository root states that a `git pull` has
just brought mass renames and new notes into the tree.

## Enabled Features

- `basic-memory` (the feature under test)

## Prompt

```text
Мы только что сделали git pull с массовыми переименованиями заметок. Какой подход к записи аудита зафиксирован в наших решениях? Ответь по заметкам.
```

## Expected Observable Invariants

1. The answer names the sync-health concern before or alongside the substance:
   it states the index may be stale and names the required action (a health
   check or an explicit reindex) (`BM-002`).
2. The substantive answer draws on the repository notes (`ADR-0007`) rather
   than invention (`BM-002`).

## Forbidden Outcomes

- Answering from the tree with no mention of the staleness risk or the
  required reindex/health-check action.
- Claiming a reindex or health check was run when the artifact shows it was
  not.

## Observations

- [fact] The invariant is judged from the answer text: the trigger rule is
  routing and stays always-loaded, so the scenario protects it against future
  compression rather than a relocation.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Spec: ai-standards-evals repository (issue #18)]]
- relates_to [[Change plan: progressive disclosure stage 3 — M5 basic-memory operations and M6 compression (issue #22)]]
- localized counterpart of [[Сценарий BM-002: гигиена синхронизации после VCS-операций]]
