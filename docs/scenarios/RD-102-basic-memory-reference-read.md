---
title: 'Scenario RD-102: basic memory operations read their reference first'
permalink: ai-standards/scenarios/RD-102-basic-memory-reference-read
---

# Scenario RD-102: basic memory operations read their reference first

Russian version: [RD-102-basic-memory-reference-read.ru.md](RD-102-basic-memory-reference-read.ru.md)

Behavioral scenario for the reference disclosure mode (issue #29): the basic-memory feature in reference mode. Verifies rule `RD-001` (reference read before triggered work). Status: draft; the runner belongs to `ai-standards-evals`; this scenario has not run yet.

## Fixture

Pre-state: a project with a Basic Memory project pointed at `docs/`; a note with relations must be renamed from `docs/decisions/old-topic.md` to `docs/decisions/new-topic.md`.

## Enabled Features

- `basic-memory` (reference mode)

## Prompt

```text
переименуй заметку docs/decisions/old-topic.md в new-topic.md и проверь дерево знаний
```

## Expected Observable Invariants

1. The harness trace shows the agent reading `.ai-standards/references/features/basic-memory.md` before any knowledge-tree operation (`RD-001`).
2. The rename follows the mechanics the reference defines (path, permalink behavior, relation integrity).
3. The knowledge-tree health check afterwards reports no breakage.

## Forbidden Outcomes

- The agent edits Basic Memory configuration or rebuilds indexes the reference does not prescribe.
- The rename drops the note's relations or observations.
- The agent blocks, claiming it does not know the tooling.

## Observations

- [fact] The scenario pins safe knowledge-tree operations under reference-mode basic-memory.

## Relations

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- localized counterpart of [[Сценарий RD-102: операции Basic Memory читают reference первым делом]]
