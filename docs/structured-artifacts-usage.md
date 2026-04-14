# Structured Artifacts Usage Guide

Russian localized version: [structured-artifacts-usage.ru.md](structured-artifacts-usage.ru.md)

This guide explains how to use the `structured-artifacts` feature from `ai-standards` in downstream projects.

`structured-artifacts` standardizes a small set of Markdown artifacts that improve planning, module boundaries, and design history without turning the repository into an XML-driven workflow.

## Goals

Use `structured-artifacts` when you want the agent or team to:

- plan non-trivial changes before implementation
- make module boundaries and invariants explicit
- keep durable design choices visible in Git
- add optional navigation aids for truly hard-to-read flows

Typical outcomes:

- fewer hidden scope changes
- better review before coding starts
- clearer ownership and non-goals for important modules
- less need to reconstruct old design reasoning from commit archaeology

## What The Feature Includes

The feature standardizes these artifacts:

- `change-plan.md` for non-trivial implementation planning
- `MODULE_CONTRACT.md` for major, risky, shared, or non-obvious modules
- `decision-record.md` for durable architecture or operational choices
- `module-map.md` as an optional aid for orchestration-heavy or integration-heavy flows

All four are plain Markdown templates intended to be short, reviewable, and locally adaptable.

## What The Feature Explicitly Rejects

Do not treat the following as shared defaults:

- XML-heavy planning documents
- pseudo-XML knowledge overlays around code
- mandatory code graphs for every task
- pervasive block markers or file-local semantic scaffolding
- process files created for small local edits with obvious verification

If a specific project truly needs heavier artifacts, keep that policy local to the project instead of promoting it into `ai-standards`.

## When To Enable It

Add `structured-artifacts` when a project regularly uses agents for:

- architecture and integration changes
- cross-module refactors
- migration planning
- review-sensitive changes where invariants must be stated up front
- codebases where module boundaries are easy to misunderstand

It is less useful for:

- tiny local fixes
- obvious mechanical edits
- changes whose impact and verification fit comfortably in the task discussion itself

## Manifest Example

```toml
features = [
  "conport",
  "design-first-collaboration",
  "reasoning-hygiene",
  "structured-artifacts",
]
```

## When To Create Each Artifact

Create a change plan when:

- the task changes behavior across layers
- multiple dependent steps must happen in a safe order
- migration, rollout, or compatibility risk exists
- review before implementation would materially reduce risk

Create a module contract when:

- the module has important invariants
- several developers or agents will change it over time
- the ownership boundary is easy to blur
- the module is large enough that non-goals must be written down explicitly

Create a decision record when:

- the team is choosing between meaningful alternatives
- the answer to "why did we do it this way?" will matter later
- the decision should survive code review and commit history browsing

Create a module map only when:

- the flow is orchestration-heavy
- the module touches many dependencies or side effects
- onboarding or review repeatedly stalls on understanding the same area

## How To Think About A Module

Treat a module as the smallest change unit for which one responsibility contract and one set of invariants can be stated clearly.

Good module boundaries usually have:

- one main reason to change
- named inputs, outputs, and side effects
- a bounded dependency surface
- verification that can be discussed without holding the whole system in working memory

Bad module boundaries usually look like:

- "this area handles business logic"
- contracts that describe several unrelated responsibilities
- invariants that sprawl across half the codebase
- changes that always require re-explaining three neighboring areas

## Relationship To Other Features

- `design-first-collaboration` defines when intent, boundaries, and non-goals should be made explicit.
- `reasoning-hygiene` improves the quality of analysis behind those artifacts.
- `conport` stores active context, progress, and evolving project memory.
- `structured-artifacts` adds Git-reviewable documents for plans, contracts, and durable decisions.

## ConPort Versus Decision Records

Use ConPort for:

- active context
- recent progress
- lessons learned
- working rationale that may still evolve

Use a decision record for:

- a durable repository-facing decision
- a choice that future reviews or refactors must be able to cite
- a documented alternative analysis that should live with the codebase

Do not mirror every ConPort entry into a decision record.

## Practical Adoption Guidance

Start small:

1. Use `change-plan.md` first.
2. Add `MODULE_CONTRACT.md` only for one or two genuinely risky modules.
3. Introduce decision records only where "why" keeps getting lost.
4. Add `module-map.md` only after a real navigation problem appears.

The goal is not more paperwork. The goal is to reduce ambiguity exactly where ambiguity is expensive.
