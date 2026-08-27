---
title: 'DECISION: add-autonomy-boundaries-feature'
permalink: ai-standards/decisions/2026-04-18-add-autonomy-boundaries-feature
---

# DECISION: add-autonomy-boundaries-feature

Russian localized version: [2026-04-18-add-autonomy-boundaries-feature.ru.md](2026-04-18-add-autonomy-boundaries-feature.ru.md)

## Status

Accepted

## Date

2026-04-18

## Context

`ai-standards` already promoted design-first collaboration, reasoning hygiene, and lightweight structured artifacts, but it did not yet define a reusable policy for when an agent must stop autonomous execution and request human verification.

This gap was most visible in longer agentic sessions. Existing rules helped projects state intent, boundaries, and invariants, but they did not clearly separate:

- a checkpoint where the agent needs human approval for a new design direction
- a checkpoint where the design direction is unchanged, but the accumulated architecture delta has become too large to continue without review

The repository needed a shared process feature for these stop conditions without pushing a heavy workflow into every project by default.

## Decision

`ai-standards` adds `autonomy-boundaries` as an opt-in process feature.

The feature defines:

- long autonomy as an exception rather than the default workflow
- mandatory preconditions for bounded autonomous execution
- explicit stop conditions for design ambiguity, architecture drift, widening scope, and non-converging verification
- sensitive areas where autonomous design decisions are forbidden without human approval
- review artifact expectations for the end of a long autonomous run

The repository keeps this policy in `process/` instead of `core/` so downstream projects opt into the stronger autonomy guardrails explicitly.

## Why

- adds a reusable answer to "when must the agent stop?"
- separates execution autonomy from autonomous design choice
- makes architecture-delta review an explicit concept alongside direction review
- fits the repository preference for lightweight, Git-reviewable process rules
- avoids brittle numeric thresholds as shared defaults

## Alternatives Considered

### Expand `design-first-collaboration` alone

Rejected because one extra bullet there would not be enough to express session envelopes, sensitive areas, review outputs, and stop-condition policy clearly.

### Move the full policy into `core`

Rejected because not every downstream project needs the same autonomy governance level by default, and the repository already uses opt-in process features for stronger workflow rules.

### Standardize a mandatory file such as `SESSION_ENVELOPE.md`

Rejected because the durable value is the content of the session envelope, not one repository-wide filename. Projects should keep local flexibility in how they store the artifact.

## Consequences

### Benefits

- downstream projects can opt into a clear shared autonomy policy
- long autonomous sessions now have explicit stop conditions in shared standards
- direction checkpoints and architecture-delta checkpoints are both named and documented
- the self-hosted repository can apply the same policy through its own manifest

### Costs Or Tradeoffs

- the repository now carries another process feature and usage guide pair
- downstream projects must decide whether they want this governance level explicitly
- some projects may still need stricter local rules for numeric limits, operational risk, or approval workflow

## Affected Modules

- `registry.toml`
- `fragments/process/autonomy-boundaries.md`
- `fragments/process/design-first-collaboration.md`
- `fragments/process/structured-artifacts.md`
- `README.md`
- `README.ru.md`
- `ai.project.toml`
- `AGENTS.md`
- `tests/test_ai_sync.py`

## Invariants And Constraints

- long autonomous execution remains disallowed by default
- design choice and execution must stay distinct
- shared standards should avoid brittle numeric thresholds as universal defaults
- session-envelope content matters more than any single filename
- human review must stay cheaper than reverse-engineering a hidden run

## Verification

- `registry.toml` exposes the `autonomy-boundaries` feature
- the rendered output includes the new process fragment when the feature is enabled
- usage guides exist in English and Russian
- README documents the feature in both languages
- self-hosted `AGENTS.md` renders successfully with the new feature enabled

## Related Artifacts

- [../autonomy-boundaries-usage.md](../autonomy-boundaries-usage.md)
- [../autonomy-boundaries-usage.ru.md](../autonomy-boundaries-usage.ru.md)
- [../../fragments/process/autonomy-boundaries.md](../../fragments/process/autonomy-boundaries.md)
- [../../ai.project.toml](../../ai.project.toml)