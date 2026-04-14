# Reasoning Hygiene Usage Guide

Russian localized version: [reasoning-hygiene-usage.ru.md](reasoning-hygiene-usage.ru.md)

This guide explains how to use the `reasoning-hygiene` feature from `ai-standards` in downstream projects.

`reasoning-hygiene` is a reusable process feature for improving answer quality on complex or ambiguous tasks without relying on model-specific prompt tricks.

The feature is intentionally narrow. It does not try to optimize for every model quirk. It standardizes only the durable parts that remain useful across tools and model versions.

## Goals

Use `reasoning-hygiene` when you want the agent to:

- break down a non-trivial task before acting
- surface assumptions and edge cases early
- expose uncertainty as concrete gaps and risks
- avoid decorative personas and brittle prompt folklore

Typical outcomes:

- fewer hidden assumptions
- clearer verification boundaries
- better handoff between discovery, decision, and implementation
- less dependence on unstable prompt wording tricks

## What The Feature Includes

The feature standardizes these behaviors:

- step-by-step structure for complex tasks
- explicit assumptions, edge cases, and verification points
- self-review framed as missing evidence or remaining risks
- task-specific roles only when they add real constraints or decision criteria

## What The Feature Explicitly Rejects

Do not treat the following as shared engineering standards:

- monetary incentives or "tip" prompts
- emotional pressure such as career stakes or urgency theater
- challenge prompts such as "prove me wrong"
- generic persona fluff like "you are a helpful expert"
- kitchen-sink prompting that stacks many manipulative cues together

These tactics may influence some model outputs, but they are not durable enough for repository-wide reusable policy.

## When To Enable It

Add `reasoning-hygiene` when a project regularly uses agents for:

- architecture and design exploration
- multi-step debugging
- implementation planning with non-trivial verification
- code review or analysis where hidden assumptions are costly

It is less useful for:

- simple mechanical edits
- deterministic transformations with obvious acceptance criteria
- tightly constrained tasks where the surrounding workflow already forces structured verification

## Manifest Example

```toml
features = [
  "conport",
  "design-first-collaboration",
  "reasoning-hygiene",
]
```

## Relationship To Other Features

- `design-first-collaboration` defines how to surface intent, boundaries, non-goals, and tradeoffs.
- `reasoning-hygiene` improves the quality of analysis within that flow.
- `conport` stores durable lessons and project memory after significant work.
- `structured-artifacts` adds lightweight Git-reviewable plans, contracts, and decision records when the task needs more explicit structure.

## Practical Prompting Guidance

Good prompts usually ask for structure and evidence directly.

Examples:

- `Break this migration plan into steps, assumptions, rollback risks, and verification points.`
- `Review this design and call out hidden assumptions, edge cases, and what still needs proof.`
- `Act as a PostgreSQL performance reviewer. Focus on tradeoffs, failure modes, and what should be benchmarked.`

Avoid asking for confidence theater when what you need is actionable uncertainty reporting.

Prefer:

- `List the weak points in this reasoning and what should be verified.`

Over:

- `Rate your confidence from 0 to 1.`
