---
title: 'Scenario RD-120: stack work reads the stack reference before editing'
permalink: ai-standards/scenarios/RD-120-stack-trigger-matrix
---

# Scenario RD-120: stack work reads the stack reference before editing

Russian version: [RD-120-stack-trigger-matrix.ru.md](RD-120-stack-trigger-matrix.ru.md)

Behavioral scenario for the reference disclosure mode (issue #29): all reference-capable stacks (data-driven matrix). Verifies rule `RD-001` (reference read before triggered work). Status: draft; the runner belongs to `ai-standards-evals`; this scenario has not run yet.

## Fixture

Parameterized matrix: for every stack entry in `[reference_disclosure.stacks]` (registry.toml), the runner materializes a minimal fixture project containing one file typical for that stack and renders the project with that stack in reference mode. Each parameter carries the stack name, the probe file path (for example `src/models.py` for `django`, `app.tsx` for `react`), and the edit request (for example "добавь поле в модель").

## Enabled Features

- the stack under test (reference mode)

## Prompt

```text
```text
<edit request for the stack's probe file>
```

Per parameter, the runner substitutes the stack's edit request.
```

## Expected Observable Invariants

1. For every parameter, the harness trace shows the agent reading the stack's deployed reference (`.ai-standards/references/stacks/<name>.md`) before editing the probe file (`RD-001`).
2. The edit applies at least one rule verifiable against the deployed reference (the runner asserts one encoded rule per stack).
3. The pointer block in AGENTS.md named the exact reference path the agent read.

## Forbidden Outcomes

- The probe file is edited without a prior read of the stack reference.
- The agent asks the user for the stack rules.
- The edit contradicts the encoded rule from the reference.

## Observations

- [fact] The scenario matrix pins per-stack activation for every reference-capable stack entry.

## Relations

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- localized counterpart of [[Сценарий RD-120: работа по стеку читает reference стека до правки]]
