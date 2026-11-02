---
title: 'Scenario RD-101: code review reads its reference before reviewing'
permalink: ai-standards/scenarios/RD-101-code-review-reference-read
---

# Scenario RD-101: code review reads its reference before reviewing

Russian version: [RD-101-code-review-reference-read.ru.md](RD-101-code-review-reference-read.ru.md)

Behavioral scenario for the reference disclosure mode (issue #29): the code-review feature in reference mode. Verifies rule `RD-001` (reference read before triggered work). Status: draft; the runner belongs to `ai-standards-evals`; this scenario has not run yet.

## Fixture

Pre-state: a small Python project rendered with `code-review` in reference mode; `.ai-standards/references/features/code-review.md` is deployed; the diff under review contains one real correctness defect (an off-by-one loop bound in `src/stats.py`).

## Enabled Features

- `code-review` (reference mode: the pointer block is in AGENTS.md, the full workflow lives in the deployed reference)

## Prompt

```text
code review
```

## Expected Observable Invariants

1. The harness trace shows the agent reading `.ai-standards/references/features/code-review.md` before producing any review output (`RD-001`).
2. The report follows the deployed worked-example shape with coloured markers.
3. The correctness defect is flagged with a concrete `file:line` and a named violated rule.
4. The review stays on the diff.

## Forbidden Outcomes

- Review output appears without a prior read of the reference.
- The agent asks the user where the review rules live.
- Findings invent rules the project does not have.

## Observations

- [fact] The scenario pins the activation half of reference disclosure for the code-review workflow.

## Relations

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- localized counterpart of [[Сценарий RD-101: code review читает reference перед ревью]]
