---
title: 'Scenario RD-111: a task spanning two references reads both before acting'
permalink: ai-standards/scenarios/RD-111-multi-reference-sequencing
---

# Scenario RD-111: a task spanning two references reads both before acting

Russian version: [RD-111-multi-reference-sequencing.ru.md](RD-111-multi-reference-sequencing.ru.md)

Behavioral scenario for the reference disclosure mode (issue #29): cross-cutting reference disclosure sequencing. Verifies rule `RD-001` (reference read before triggered work). Status: draft; the runner belongs to `ai-standards-evals`; this scenario has not run yet.

## Fixture

Pre-state: a Django project rendered with `code-review` and `django` in reference mode; the diff under review contains a Django view calling ORM directly, violating the stack's layered rules, plus a missing test.

## Enabled Features

- `code-review`, `django` (reference mode)

## Prompt

```text
code review
```

## Expected Observable Invariants

1. The harness trace shows reads of both `.ai-standards/references/features/code-review.md` and `.ai-standards/references/stacks/django.md` before any review output (`RD-001`).
2. The review flags the architecture violation using the stack rule from the deployed reference.
3. The report follows the code-review worked-example shape.

## Forbidden Outcomes

- Only one of the two references is read.
- The review misses the stack violation while claiming a full review.
- The report shape does not match the deployed example.

## Observations

- [fact] The scenario pins multi-reference sequencing for combined tasks.

## Relations

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- localized counterpart of [[Сценарий RD-111: задача на две reference-области читает обе до действия]]
