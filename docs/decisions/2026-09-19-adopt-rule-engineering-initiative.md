---
title: 'DECISION: adopt the Rule Engineering initiative'
type: decision
permalink: ai-standards/decisions/2026-09-19-adopt-rule-engineering-initiative
---

# DECISION: adopt the Rule Engineering initiative

## Status

- Accepted

## Date

- 2026-09-19

## Context

Proposal `docs/archive/20260917-000618-proposal-rule-engineering-skill-engineering-context-architecture-evals.md`
(filed as issue #17) argues that `ai-standards` must standardize how required
knowledge is selected, placed, loaded, and verified rather than maximize how
much knowledge is always loaded. The repository currently has one
source-specific normalization flow (README `Import External Rules`), no formal
placement model, no skill validation discipline, and no behavior-level
verification. The executable eval infrastructure is deliberately split into a
separate specification, `ai-standards-evals` (issue #18), so methodology and
infrastructure can be accepted or rejected independently. The user accepted
the initiative direction, the #17/#18 scope split, and `docs/scenarios/` as
the home of scenario contracts on 2026-09-19.

## Decision

Adopt the initiative as phased work in this repository (phases 0–9 in the
proposal's order), starting with Phase 0 (baseline) and Phase 1 (the
`rule-engineering` feature) on branch `rules-change/17-rule-engineering`:

1. Rule Engineering becomes the single universal process for any normative
   rule regardless of source; external importing is one of its special cases.
2. A rule is acceptable only when it satisfies the quality properties
   (atomic, unambiguous, actionable, properly scoped, observable, unique at
   behavioral-overlap level, non-conflicting with explicit precedence,
   correct abstraction level, portable) and defines at least one form of
   validation.
3. Existing rules are not mass-rewritten; adoption is incremental.
4. Minification of `AGENTS.md` happens only after a safe routing mechanism
   and regression evals exist (Phase 8).
5. Scenario contracts live under `docs/scenarios/`; scenario execution
   belongs to `ai-standards-evals` (issue #18).

## Why

- The main invariant of the standard becomes enforceable: delivery of the
  right, unambiguous, verifiable instruction at the right moment, not
  maximal always-loaded volume.
- A single process closes the quality gap between external and internal rules.
- The phase order makes every later step depend on already verified
  primitives (baseline → rule engineering → traceability → dogfooding →
  placement model → eval contract → skills → skill evals → minification →
  cross-agent matrix).
- The #17/#18 split keeps this repository's scope methodological; execution
  infrastructure cannot be rejected together with the methodology or vice versa.

## Alternatives Considered

- Reject or defer the proposal: keeps the standards accumulating instructions
  with no verification path; rejected by the user.
- Rewrite existing rules immediately while introducing the process: high risk,
  no baseline to compare against; contradicts the proposal's own sequencing.
- Build the eval harness inside this repository first: merges methodology with
  infrastructure; rejected in favor of the approved #17/#18 split.

## Consequences

- Benefits: measurable rule quality bar, observable-behavior requirement for
  every normative rule, a placement discipline that later justifies
  `AGENTS.md` reduction, and a pilot path through `standard-code-review`.
- Costs or tradeoffs: every future rule change becomes a longer, deliberate
  procedure; the full initiative spans many releases; `feature_meta` pins
  (`2.5.0` for `rule-engineering`) must be kept truthful at release time.

## Affected Modules

- `fragments/process/**` (new `rule-engineering`; later `context-architecture`)
- `registry.toml`, `ai.project.toml`, rendered `AGENTS.md`
- `templates/**` (later: `skill-engineering` domain)
- `docs/scenarios/**` (later: scenario contracts)
- `docs/artifacts/**`, `docs/decisions/**` (initiative records)

## Invariants And Constraints

- No mass rewrite of existing rules during Phase 1.
- Shared policy stays vendor-neutral; harness mechanics stay in adapters.
- The `ai-sync` module contract is untouched: content-only changes over
  existing inputs.
- Scenario contracts are defined here; scenario execution is not.

## Verification

- Phases 0–1 (this branch): baseline artifact recorded; `rule-engineering`
  feature rendered and covered by tests; `uv run pytest`, `uv run mypy
  scripts/`, idempotent `uv run ai-sync render --project-root .`,
  `uv run ai-sync doctor --project-root .` zero errors.
- Later phases verify through their own change plans and artifacts against
  the recorded baseline.

## Related Artifacts

- Proposal: `docs/archive/20260917-000618-proposal-rule-engineering-skill-engineering-context-architecture-evals.md`
- Issues: #17 (this initiative), #18 (`ai-standards-evals` spec)
- Baseline: `docs/artifacts/2026-09-19-rule-engineering-baseline.md`
- Change plan: `docs/artifacts/2026-09-19-rule-engineering-change-plan.md`
