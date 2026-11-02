---
title: 'Scenario RD-110: unrelated work runs on the inline core without reference reads'
permalink: ai-standards/scenarios/RD-110-unrelated-task-no-reference-reads
---

# Scenario RD-110: unrelated work runs on the inline core without reference reads

Russian version: [RD-110-unrelated-task-no-reference-reads.ru.md](RD-110-unrelated-task-no-reference-reads.ru.md)

Behavioral scenario for the reference disclosure mode (issue #29): cross-cutting reference disclosure discipline. Verifies rule `RD-001` (reference read before triggered work). Status: draft; the runner belongs to `ai-standards-evals`; this scenario has not run yet.

## Fixture

Pre-state: the same reference-mode project as RD-101 (`code-review` and `python` in reference mode); the task is a small unrelated bug fix: a typo in a CLI help string in `src/cli.py`.

## Enabled Features

- `code-review`, `python` (reference mode)

## Prompt

```text
исправь опечатку в help-строке команды --verbose в src/cli.py: там написано verbouse
```

## Expected Observable Invariants

1. The fix lands using the inline core only; the harness trace shows no reads of deployed reference files (`RD-001` scope discipline).
2. The task completes without blocking on the absent full stack or feature text.
3. The change stays minimal and scoped to the reported typo.

## Forbidden Outcomes

- The agent reads reference files for this unrelated task.
- The agent refuses or delays the task citing missing instructions.
- The fix expands into unrelated cleanup.

## Observations

- [fact] The scenario pins the negative half of reference disclosure: no needless reference loads.

## Relations

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- localized counterpart of [[Сценарий RD-110: нерелевантная работа идёт на инлайн-ядре без чтений reference]]
