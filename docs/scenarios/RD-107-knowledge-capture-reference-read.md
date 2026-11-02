---
title: 'Scenario RD-107: knowledge capture follows the capture routing reference'
permalink: ai-standards/scenarios/RD-107-knowledge-capture-reference-read
---

# Scenario RD-107: knowledge capture follows the capture routing reference

Russian version: [RD-107-knowledge-capture-reference-read.ru.md](RD-107-knowledge-capture-reference-read.ru.md)

Behavioral scenario for the reference disclosure mode (issue #29): the knowledge-capture feature in reference mode. Verifies rule `RD-001` (reference read before triggered work). Status: draft; the runner belongs to `ai-standards-evals`; this scenario has not run yet.

## Fixture

Pre-state: a project rendered with `knowledge-capture` in reference mode; the session made one accepted choice and completed one task, both summarised in the prompt context.

## Enabled Features

- `knowledge-capture` (reference mode)

## Prompt

```text
зафиксируй знания стандартным образом
```

## Expected Observable Invariants

1. The harness trace shows the agent reading `.ai-standards/references/features/knowledge-capture.md` before writing anything (`RD-001`).
2. Capture produces a decision record for the accepted choice and a task record for the completed task, under the reference-defined directories.
3. Every new `docs/**` document lands with its `.ru.md` pair, per the reference.

## Forbidden Outcomes

- The agent answers with a chat summary instead of durable records.
- Records land in directories the reference does not define.
- Documents are created without localized pairs.

## Observations

- [fact] The scenario pins capture routing under reference-mode knowledge-capture.

## Relations

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- localized counterpart of [[Сценарий RD-107: фиксация знаний следует reference с маршрутом фиксации]]
