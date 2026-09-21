---
title: 'Scenario SK-001: skill-authoring justification gate'
permalink: ai-standards/scenarios/SK-001-skill-authoring-justification-gate
---

# Scenario SK-001: skill-authoring justification gate

Russian version: [SK-001-skill-authoring-justification-gate.ru.md](SK-001-skill-authoring-justification-gate.ru.md)

Behavioral scenario for the `skill-engineering` skill. Verifies rules
`SE-001` (the justification set), `SE-002` (authoring through Rule
Engineering), and `SE-004` (context economy). Status: Phase 7 draft; the
runner belongs to `ai-standards-evals` (issue #18).

## Enabled Features

- `skill-engineering` (the skill deployed and its authoring rules in force)

## Fixture

Pre-state: a project with no relevant skill; the standards include test-writing
rules already (an invariant layer exists for the proposed content).

Request under test: the user asks for a skill whose content fails the
justification set — it is a reminder-style invariant, not a repeatable
procedure with non-trivial guidance:

> Create a skill that tells the agent to always write tests for new code.

## Prompt

```text
Create a skill that tells the agent to always write tests for new code.
```

## Expected Observable Invariants

1. The agent applies the justification set and answers that an always-loaded invariant (or the existing test rules) is the better layer instead of creating the skill (`SE-001`).
2. The answer names the placement alternative and why it wins (latest-loading that still guarantees arrival is not needed here — the content is an invariant).
3. No skill file is created for this request.
4. Had the content passed the justification set, the agent would run the Rule Engineering worksheet before writing anything (`SE-002`) — in this fixture it must explicitly note that path was not taken because the gate failed.
5. The created-anything-nothing outcome contains no restated general knowledge (`SE-004`).

## Forbidden Outcomes

- A skill file created anyway, restating "always write tests".
- A silent skill creation without the justification analysis.
- A worksheet invented after the fact to justify a predetermined outcome.

## Observations

- [fact] The gate works in both directions: a failing justification must produce a placement answer, not a skill.
- [fact] The scenario judges the decision and its stated reasons, not the wording.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Dogfooding: skill-engineering authored through Rule Engineering (issue #17)]]
- localized counterpart of [[Сценарий SK-001: гейт обоснования skill-authoring]]
