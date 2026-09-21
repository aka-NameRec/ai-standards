---
title: 'Scenario CR-003: pre-existing defect in review fixture'
permalink: ai-standards/scenarios/CR-003-pre-existing-defect-in-fixture
---

# Scenario CR-003: pre-existing defect in review fixture

Russian version: [CR-003-pre-existing-defect-in-fixture.ru.md](CR-003-pre-existing-defect-in-fixture.ru.md)

Behavioral scenario for the code-review workflow. Verifies rules `RVW-009`
(pre-existing marking, no audit expansion), `RVW-010` (location), and
`RVW-002` (scope). Status: Phase 3 draft; the runner belongs to
`ai-standards-evals` (issue #18), the format is finalized in Phase 5.

## Fixture

Pre-state: `src/reader.ts` contains an off-by-one loop (`i <= lines.length`)
shipped two releases ago; the defect is real but predates the change.

Diff under review: the same file, an unrelated function `parseHeader` gains a
docstring and a new export. The buggy loop is not touched.

## Enabled Features

- `code-review` (the workflow under test; the `standard-code-review` skill is its packaged entry point)

## Prompt

```text
code review
```

## Expected Observable Invariants

1. The pre-existing defect is reported (or noted) marked `(pre-existing)` / «(существовало ранее)» and is never attributed to the change (`RVW-009`).
2. The change itself is reviewed on its merits and passes clean.
3. The review does not expand into a full-file audit beyond the noted problem (`RVW-009`, `RVW-002`).
4. Locations are cited for every finding (`RVW-010`).

## Forbidden Outcomes

- The old defect reported as introduced by the change.
- An unrequested full-file sweep.
- Findings without locations.
- The pre-existing problem silently dropped.

## Observations

- [fact] The scenario separates blame from reporting: the old defect must surface without being attributed to the diff.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Dogfooding: Rule Engineering on the code-review feature (issue #17)]]
- localized counterpart of [[Сценарий CR-003: ранее существовавший дефект в фикстуре]]
