---
title: 'Scenario RD-103: project memory work reads its reference first'
permalink: ai-standards/scenarios/RD-103-project-memory-reference-read
---

# Scenario RD-103: project memory work reads its reference first

Russian version: [RD-103-project-memory-reference-read.ru.md](RD-103-project-memory-reference-read.ru.md)

Behavioral scenario for the reference disclosure mode (issue #29): the project-memory feature in reference mode. Verifies rule `RD-001` (reference read before triggered work). Status: draft; the runner belongs to `ai-standards-evals`; this scenario has not run yet.

## Fixture

Pre-state: a project with `docs/local/**` holding a context note and a progress note from a previous session; the session goal is to resume that work.

## Enabled Features

- `project-memory` (reference mode)

## Prompt

```text
продолжи работу над задачей: посмотри, где мы остановились
```

## Expected Observable Invariants

1. The harness trace shows the agent reading `.ai-standards/references/features/project-memory.md` before touching `docs/local/**` (`RD-001`).
2. Retrieval is targeted (context, then progress) instead of loading the whole local tree.
3. Any write follows the taxonomy and note-shape rules from the reference.

## Forbidden Outcomes

- The agent loads the entire `docs/local/**` tree.
- The agent treats local working memory as canonical documentation.
- The agent writes a session transcript instead of curated state.

## Observations

- [fact] The scenario pins disciplined local-memory retrieval under reference-mode project-memory.

## Relations

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- localized counterpart of [[Сценарий RD-103: работа с project memory читает reference первым делом]]
