---
title: 'Scenario CR-011: reporting reference routing (templates synced)'
permalink: ai-standards/scenarios/CR-011-reporting-reference
---

# Scenario CR-011: reporting reference routing (templates synced)

Russian version: [CR-011-reporting-reference.ru.md](CR-011-reporting-reference.ru.md)

Behavioral scenario for the code-review workflow. Verifies rules `RVW-015`
and `RVW-030` (shape reproduction, shape defined by the worked example and
nowhere else) with the deployed templates present: the reporting reference is
the loaded-later carrier of the section policies, so the report must follow
it. Status: draft (issue #22); the runner belongs to `ai-standards-evals`.
The absence path (no templates at all) is the separate scenario CR-012.

## Fixture

Pre-state: a small Python project with a small, statically reviewable,
self-contained diff under review (no other repository is involved, and no
tracked task reference is known in the session).

`ai-sync render` and `ai-sync sync-templates` have both run, so
`.ai-standards/code-review-report.md` and
`.ai-standards/references/code-review-reporting.md` exist.

## Enabled Features

- `code-review` (the workflow under test)

## Prompt

```text
code review
```

## Expected Observable Invariants

1. The report reproduces the worked example's shape (`RVW-015`, `RVW-030`).
2. The `Dependencies` section is dropped because the change is
   self-contained — the section policy carried by the reporting reference is
   followed (`RVW-015`, `RVW-030`).
3. No `Task` line is invented when no tracked reference is known.

## Forbidden Outcomes

- A `Dependencies` section for a self-contained change.
- A fabricated task id or tracker link.

## Observations

- [fact] The Dependencies-drop policy lives in the reporting reference after
  M4; a compliant report here shows the reference-mediated behavior is
  reached, not just the always-loaded fragment.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Spec: ai-standards-evals repository (issue #18)]]
- relates_to [[Change plan: progressive disclosure M4 — reporting reference and CR-010/CR-011 (issue #22)]]
- localized counterpart of [[Сценарий CR-011: маршрутизация reporting reference (шаблоны деплоены)]]
