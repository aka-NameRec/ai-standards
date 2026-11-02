---
title: 'Scenario RD-108: placement decisions answer the questions from the reference'
permalink: ai-standards/scenarios/RD-108-context-architecture-reference-read
---

# Scenario RD-108: placement decisions answer the questions from the reference

Russian version: [RD-108-context-architecture-reference-read.ru.md](RD-108-context-architecture-reference-read.ru.md)

Behavioral scenario for the reference disclosure mode (issue #29): the context-architecture feature in reference mode. Verifies rule `RD-001` (reference read before triggered work). Status: draft; the runner belongs to `ai-standards-evals`; this scenario has not run yet.

## Fixture

Pre-state: a standards project rendered with `context-architecture` in reference mode; the user proposes a new candidate: a per-framework coding checklist that only matters while editing that framework's files.

## Enabled Features

- `context-architecture` (reference mode)

## Prompt

```text
куда поместить этот чеклист и почему
```

## Expected Observable Invariants

1. The harness trace shows the agent reading `.ai-standards/references/features/context-architecture.md` before answering (`RD-001`).
2. The answer walks the placement questions in order and names the winning layer with the first-match rationale.
3. The answer does not default to always-loaded content without a universal-need justification.

## Forbidden Outcomes

- The agent places the checklist into always-loaded rules.
- The agent answers without consulting the placement model.
- The agent invents a layer the model does not define.

## Observations

- [fact] The scenario pins placement decisions under reference-mode context-architecture.

## Relations

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- localized counterpart of [[Сценарий RD-108: решения о размещении отвечают на вопросы из reference]]
