---
title: 'DECISION: add-agent-usage-hygiene-feature'
permalink: ai-standards/decisions/2026-04-25-add-agent-usage-hygiene-feature
---

# DECISION: add-agent-usage-hygiene-feature

Russian localized version: [2026-04-25-add-agent-usage-hygiene-feature.ru.md](2026-04-25-add-agent-usage-hygiene-feature.ru.md)

## Status

Accepted

## Date

2026-04-25

## Context

Token- and usage-based agent workflows make broad context loading, long autonomous sessions, repeated summaries, and unnecessary file inspection more visible as operational costs.

`ai-standards` already had related quality-oriented guidance:

- `reasoning-hygiene` focuses analysis on assumptions, risks, and verification.
- `autonomy-boundaries` keeps long execution bounded and reviewable.
- `structured-artifacts` externalizes plans, contracts, and decisions so critical context does not live only in the model's transient memory.

Those features reduce waste indirectly, but the repository did not yet name usage economy as a reusable process concern. The new rule needed to stay tool-neutral and avoid hard dependencies on Codex-specific modes, vendor billing details, or brittle numeric thresholds.

## Decision

`ai-standards` adds `agent-usage-hygiene` as an opt-in process feature.

The feature defines:

- usage economy as context discipline rather than lower engineering quality
- targeted discovery before broad context loading
- compact, reviewable implementation slices
- prompt-activated economy mode for usage-sensitive tasks
- correctness and required verification as higher priorities than usage reduction
- vendor-specific controls as local adapter or project override concerns

The feature is included in the self-hosted manifest and starter project manifest so downstream projects can adopt the guidance explicitly through normal manifest composition.

## Why

- makes the economy value of existing process rules explicit
- gives users a durable way to request "be economical" behavior without lowering quality
- preserves the repository's tool-neutral design
- avoids encoding Codex-specific controls into shared standards
- avoids fragile numeric limits such as fixed checkpoint counts or maximum file counts

## Alternatives Considered

### Add a few bullets to existing process features

Rejected because the prompt-activated economy mode is a distinct operating mode. Folding it into existing features would make activation semantics harder to find and test.

### Create a Codex-specific rule

Rejected because the project should not introduce deep tool-specific coupling for this concern. Codex-specific controls can live in local adapters or project overrides.

### Make economy mode always active

Rejected because some tasks require broad discovery, detailed explanation, or stronger verification. Economy mode should be explicit and reversible, not an invisible quality constraint.

## Consequences

### Benefits

- downstream projects can opt into reusable usage discipline
- users can activate stricter economy behavior with natural prompts
- broad context loading and long sessions now have explicit shared guidance
- correctness remains the non-negotiable priority

### Costs Or Tradeoffs

- the repository carries another process feature and usage guide pair
- downstream projects must decide whether they want the feature in their generated instructions
- tool-specific controls still need local adapters or overrides when a team wants them

## Affected Modules

- `registry.toml`
- `fragments/process/agent-usage-hygiene.md`
- `README.md`
- `README.ru.md`
- `docs/agent-usage-hygiene-usage.md`
- `docs/agent-usage-hygiene-usage.ru.md`
- `ai.project.toml`
- `templates/project_manifest.toml`
- `AGENTS.md`
- `tests/test_ai_sync.py`

## Invariants And Constraints

- usage economy must not reduce engineering quality
- required verification must not be skipped solely to save usage
- economy mode must be explicit and reversible
- shared rules must stay tool-neutral
- vendor-specific controls belong in local adapters or project overrides
- shared standards should avoid brittle numeric thresholds

## Verification

- `registry.toml` exposes the `agent-usage-hygiene` feature
- the rendered output includes the new process fragment when the feature is enabled
- usage guides exist in English and Russian
- README documents the feature in both languages
- self-hosted `AGENTS.md` renders successfully with the new feature enabled

## Related Artifacts

- [../agent-usage-hygiene-usage.md](../agent-usage-hygiene-usage.md)
- [../agent-usage-hygiene-usage.ru.md](../agent-usage-hygiene-usage.ru.md)
- [../../fragments/process/agent-usage-hygiene.md](../../fragments/process/agent-usage-hygiene.md)
- [../../ai.project.toml](../../ai.project.toml)