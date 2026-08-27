---
title: Autonomy Boundaries Usage Guide
permalink: ai-standards/autonomy-boundaries-usage
---

# Autonomy Boundaries Usage Guide

Russian localized version: [autonomy-boundaries-usage.ru.md](autonomy-boundaries-usage.ru.md)

This guide explains how to use the `autonomy-boundaries` feature from `ai-standards` in downstream projects.

`autonomy-boundaries` adds reusable rules for deciding when an agent may continue autonomously and when it must stop and request human verification.

The goal is not to maximize autonomy.
The goal is to keep autonomy reviewable, bounded, reversible, and architecturally safe.

## Goals

Use `autonomy-boundaries` when you want the agent or team to:

- distinguish bounded execution from hidden design work
- define when the agent must stop instead of silently improvising
- keep long autonomous runs anchored to explicit project artifacts
- make architecture drift and blast-radius growth visible before they become expensive

Typical outcomes:

- fewer silent design changes
- earlier review when scope starts drifting
- better separation between execution and decision-making
- cheaper post-run review because the result stays compressible

## What The Feature Covers

The feature standardizes shared policy for:

- when long autonomous execution is allowed in principle
- what prerequisites must exist before it starts
- which stop conditions must force a human checkpoint
- which areas are too sensitive for autonomous design decisions
- what review artifact set should exist at the end of the run

It is intentionally a process feature, not a stack rule and not a tool-specific adapter.

## Default Rule

Long autonomous execution is disallowed by default.

The preferred development model remains:

1. design-first alignment
2. bounded implementation
3. human review
4. next bounded cycle

Enable this feature when a project wants reusable guardrails for the exceptional cases where the agent may work longer without intermediate approval.

## When Long Autonomous Execution Is Allowed

Allow a long autonomous run only when all of the following are true:

- the design is already chosen
- the scope is bounded by written artifacts
- automated verification is strong enough to distinguish progress from drift
- rollback is cheap and predictable
- the blast radius is small and known
- the resulting review is still cheaper than manual reimplementation

If any of these properties is missing, split the task into shorter reviewed cycles instead.

## Session Envelope

Before a long autonomous run starts, record a short session envelope in a change plan, task note, or equivalent artifact.

Minimum fields:

- objective
- scope
- non-goals
- architectural constraints
- verification plan
- stop conditions
- expected review artifacts

The feature does not require one mandatory filename. Keep the artifact local to the project workflow.

## Direction Checkpoints Versus Architecture Delta Checkpoints

This distinction matters in practice.

### Direction Checkpoint

Stop and request review when the agent must choose the direction of change rather than execute an already chosen design.

Examples:

- selecting between two plausible module boundaries
- deciding whether a new abstraction should exist at all
- choosing a migration strategy
- redefining a contract to make implementation easier

### Architecture Delta Checkpoint

Stop and request review even if the design direction is unchanged, once the accumulated architecture delta becomes significant enough that it should be re-approved by a human.

Examples:

- more modules are touched than originally declared
- new cross-boundary dependencies appear
- the change now spans another subsystem
- the reviewer would need a non-trivial walk-through to understand the resulting structure

This second checkpoint is what prevents "the direction stayed the same" from turning into unchecked structural drift.

## Mandatory Stop Conditions

At minimum, stop when:

- the task no longer fits the agreed design, scope, or invariants
- a new abstraction, layer, public contract change, integration strategy, or migration strategy becomes necessary
- verification stops converging
- logs, failing checks, or evidence contradict the design anchor
- the blast radius grows materially beyond the declared scope
- rollback stops being cheap or predictable
- the architecture delta can no longer be summarized compactly for review

Projects may add stricter local thresholds, but `ai-standards` should avoid promoting brittle numeric limits as shared defaults.

## Local Checkpoints Inside A Slice

Long autonomous work is not supposed to run as one blind stretch inside an approved slice.

Add local checkpoints when the current slice contains risky implementation points such as:

- contract-sensitive edits
- state transitions
- index or boundary logic
- schema or data mapping
- cross-boundary calls

The slice should continue only while the next step still looks like a small coherent patch with targeted verification. If local fixes stop converging, or if the current slice reveals several unplanned hotspots, stop and either split the slice or ask for review.

## Sensitive Areas

Do not allow long autonomous design decisions in these areas without explicit human approval:

- architecture and module boundaries
- public APIs and backward compatibility
- schema and data migration strategy
- authentication and authorization
- secret handling and security policy
- production operations and other high-blast-radius automation

These are not merely "be careful" areas. They are review points.

## Relationship To Other Features

- `design-first-collaboration` defines how intent, boundaries, and non-goals are established.
- `reasoning-hygiene` improves the quality of the agent's self-review and evidence handling.
- `structured-artifacts` provides the change plans and decision records that can carry the session envelope.
- `conport` stores active context, recent findings, and evolving memory between runs.

`autonomy-boundaries` tells the agent when to stop leaning on those inputs and request human verification.

## Practical Adoption Guidance

Start with process, not automation:

1. Enable the feature in project instructions.
2. Add a short session envelope format to the local workflow.
3. Define two or three project-local stop conditions for sensitive areas.
4. Review whether the agent actually stops early enough when the task drifts.

Only after that should a team consider more automated autonomy modes.