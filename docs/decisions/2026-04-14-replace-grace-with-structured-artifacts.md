# DECISION: replace-grace-with-structured-artifacts

Russian localized version: [2026-04-14-replace-grace-with-structured-artifacts.ru.md](2026-04-14-replace-grace-with-structured-artifacts.ru.md)

## Status

Accepted

## Date

2026-04-14

## Context

The repository previously documented GRACE as an integrated heavy workflow. Review of the methodology and its XML-centered execution model showed that the core useful ideas are planning, explicit boundaries, invariants, and durable decisions, while the XML-heavy artifact set and workflow bootstrapping add unnecessary ceremony for shared standards.

## Decision

`ai-standards` stops promoting GRACE as a shared feature or recommended workflow.

The repository standardizes a lighter replacement through the `structured-artifacts` feature, Markdown templates, and supporting guidance.

## Why

- preserves the useful planning and boundary-setting ideas
- removes XML-heavy workflow coupling from shared standards
- keeps artifacts reviewable in Git and understandable to humans
- fits the repository direction of low-noise, reusable, cross-project rules

## Alternatives Considered

### Keep GRACE integration and document lighter usage

Rejected because it keeps the repository tied to a workflow design that is still centered on heavier artifacts and bootstrapping.

### Keep GRACE as an optional heavy path beside lightweight artifacts

Rejected because it keeps mixed signals in README, templates, and project bootstrap while offering limited practical value for downstream projects.

## Consequences

### Benefits

- the repository has one clear planning-and-structure story
- downstream projects no longer receive GRACE bootstrap guidance by default
- lightweight structured artifacts become the first-class reusable pattern

### Costs Or Tradeoffs

- historical log documents still mention GRACE and remain as context only
- downstream projects that explicitly relied on old GRACE guidance must migrate to the new feature set

## Affected Modules

- `registry.toml`
- `fragments/process/structured-artifacts.md`
- `fragments/tools/conport.md`
- `scripts/ai_sync.py`
- `templates/`
- `README.md`
- `README.ru.md`

## Invariants And Constraints

- shared standards must remain readable in Git and code review
- heavy XML-oriented artifacts are not shared defaults
- durable repository-facing choices may use decision records
- ConPort remains the place for active context, progress, and evolving project memory

## Verification

- `registry.toml` no longer exposes a `grace` feature
- `README.md` and `README.ru.md` no longer recommend GRACE integration
- `structured-artifacts` templates and usage guides exist in English and Russian
- renderer checks continue to pass

## Related Artifacts

- [../structured-artifacts-usage.md](../structured-artifacts-usage.md)
- [../structured-artifacts-usage.ru.md](../structured-artifacts-usage.ru.md)
- [../../ai.project.toml](../../ai.project.toml)
- [../ai/project-rules.md](../ai/project-rules.md)
