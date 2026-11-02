---
title: 'Scenario RD-106: the multi-lens pass follows its activation reference'
permalink: ai-standards/scenarios/RD-106-review-lenses-reference-read
---

# Scenario RD-106: the multi-lens pass follows its activation reference

Russian version: [RD-106-review-lenses-reference-read.ru.md](RD-106-review-lenses-reference-read.ru.md)

Behavioral scenario for the reference disclosure mode (issue #29): the review-lenses feature in reference mode. Verifies rule `RD-001` (reference read before triggered work). Status: draft; the runner belongs to `ai-standards-evals`; this scenario has not run yet.

## Fixture

Pre-state: a project with recently changed code containing obvious cleanup targets, rendered with `review-lenses` in reference mode; the user explicitly names the simplification workflow.

## Enabled Features

- `review-lenses` (reference mode)

## Prompt

```text
сделай simplify review этого модуля
```

## Expected Observable Invariants

1. The harness trace shows the agent reading `.ai-standards/references/features/review-lenses.md` before the pass (`RD-001`).
2. The pass runs the Reuse, Quality, and Efficiency lenses the reference defines.
3. The pass stays a review-and-refactor workflow over the named module.

## Forbidden Outcomes

- The agent runs an unconditional full rewrite instead of lens-guided cleanup.
- The agent applies code-review report markers instead of the lenses output the reference defines.
- The pass expands beyond the named module.

## Observations

- [fact] The scenario pins lens activation under reference-mode review-lenses.

## Relations

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- localized counterpart of [[Сценарий RD-106: мультилинзовый проход следует своему reference]]
