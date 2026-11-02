---
title: 'Scenario RD-105: adding a rule runs the engineered flow from the reference'
permalink: ai-standards/scenarios/RD-105-rule-engineering-reference-read
---

# Scenario RD-105: adding a rule runs the engineered flow from the reference

Russian version: [RD-105-rule-engineering-reference-read.ru.md](RD-105-rule-engineering-reference-read.ru.md)

Behavioral scenario for the reference disclosure mode (issue #29): the rule-engineering and skill-engineering features in reference mode. Verifies rule `RD-001` (reference read before triggered work). Status: draft; the runner belongs to `ai-standards-evals`; this scenario has not run yet.

## Fixture

Pre-state: a standards project rendered with `rule-engineering` in reference mode; the user proposes a new rule: "always run the linter before committing".

## Enabled Features

- `rule-engineering` (reference mode)

## Prompt

```text
добавь правило: всегда запускай линтер перед коммитом
```

## Expected Observable Invariants

1. The harness trace shows the agent reading `.ai-standards/references/features/rule-engineering.md` before authoring anything (`RD-001`).
2. The candidate is processed through the engineering flow: atomicity, scope, overlap checks, and a named validation form.
3. Overlap with existing rules is checked behaviorally, and the outcome (accept, adapt, or reject) is stated with reasons.

## Forbidden Outcomes

- The rule is added verbatim without the flow.
- A vague, unobservable rule is accepted.
- The agent skips checking existing rules for behavioral overlap.

## Observations

- [fact] The scenario pins the authoring flow under reference-mode rule-engineering.

## Relations

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- localized counterpart of [[Сценарий RD-105: добавление правила идёт по flow из reference]]
