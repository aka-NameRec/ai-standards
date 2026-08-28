---
title: 'DECISION: module-contract-gate-feature-placement'
permalink: ai-standards/decisions/2026-08-28-module-contract-gate-feature-placement
---

# DECISION: module-contract-gate-feature-placement

Russian localized version: [2026-08-28-module-contract-gate-feature-placement.ru.md](2026-08-28-module-contract-gate-feature-placement.ru.md)

## Status

Accepted

## Date

2026-08-28

## Context

A contributor draft, `docs/archive/0tkgv0g-module-contract-discovery-gate.md`, defines a module-contract discovery gate: before editing production code, the agent must run contract discovery (Basic Memory as an index, canonical contracts read from the repository), decide coverage per touched file, re-run discovery on defined triggers, report the contract note, and never edit before discovery completes. The draft grew out of a contributor exchange (2026-07-28) on a growing project where a module contract existed but an agent never read it before editing, and where having Basic Memory configured turned out not to mean agents query it.

The gap the draft addresses is real. Existing coverage of module contracts has two layers only: a creation policy (`structured-artifacts` — what a contract is, when to write one) and review-time enforcement (`code-review`, the standard review skill — checking changed modules against contracts after the code is written). No rule obliges an agent to discover and apply contracts at the moment code is written.

During review of the draft, a placement question arose: if accounting for module contracts is foundational, why not fold the gate into the existing Module Contracts section of `structured-artifacts` instead of adding a feature? This record answers that question and fixes the placement.

## Decision

The gate ships as its own opt-in feature, `module-contract-gate`, backed by a `process/module-contract-gate` fragment. It is not folded into `structured-artifacts`.

Adopters enable it with one line in the `features` list of `ai.project.toml`, conventionally right after `structured-artifacts`. Render order follows the manifest feature list, so the rendered section lands directly after Module Contracts — the adjacency the contributor asked for, achieved without touching the foundation fragment. The feature may be wired as a registry composite that also lists `process/structured-artifacts`; fragment deduplication already handles projects that enable both.

The promoted fragment keeps the draft's strict rule near-verbatim and adjusts the rest of the draft for shared-standard use:

- Task Start is proportional: a cheap check whether the project declares any contract artifacts may complete discovery with a negative result; the duty to say so when no index is available and direct scanning is needed stays.
- Basic Memory steps are conditional on Basic Memory being enabled; Basic Memory remains an index, canonical contracts are read from the repository.
- The stop-when-change-contradicts-contract duty references the `autonomy-boundaries` stop conditions instead of restating them.
- Reporting is one short contract note in the implementation summary, not a second report.

## Why

- Rendered instructions are flat: every line of an enabled fragment reaches every adopter of that fragment. `structured-artifacts` is broadly enabled, so a gate folded into it would become mandatory for all of them through a routine standards update — no manifest change, no consent, no CHANGELOG-visible choice. The feature registry exists precisely so heavyweight process ships as opt-in (precedent: `code-review`, `autonomy-boundaries`, `chroma`).
- The gate's Task Start references a module-contract index. A project with `structured-artifacts` but without `basic-memory` would receive instructions to check an index that cannot exist there and to report its absence on every task — text pointing at machinery the project never deployed, burning tokens in the exact way the draft tries to prevent.
- The two fragments govern different responsibilities: `structured-artifacts` is about creating artifacts, the gate is about consuming them while editing code. The dependency is one-way — the gate presumes the contracts policy, the policy is complete without the gate — and a feature boundary expresses a one-way dependency naturally.
- An unproven mechanism should be tunable and rollback-able per project. Promoting a proven feature into a base fragment later is cheap; extracting a rule from a broadly enabled fragment that adopters already rely on is expensive.

Predictability does not depend on placement. The foundation is the three layers that already exist — contracts get created for significant modules, they are canonical, review enforces them — plus the missing write-time layer the gate adds. Enabling the feature restores the full stack per project.

## Alternatives Considered

### Fold the gate into the Module Contracts section of `structured-artifacts`

Rejected, for the four reasons under Why. The deciding one is the first: placement in a broadly enabled fragment converts a per-project process choice into a silent default for every adopter.

### Enforce contracts only at review time

Rejected as the sole mechanism — that is the status quo. Review-time checks see contract violations after they are written; the gate exists to stop the agent from writing them in the first place. The two mechanisms are complementary, not alternatives.

### Enable the gate by default for every project that has `structured-artifacts`

Deferred to the standards-update workflow decision. New features may be recommended at update time with per-feature confirmation, but enabling stays an explicit per-project act; silent enabling on update would reopen the problem recorded here.

## Consequences

### Benefits

- adopters choose their process load; a standards update changes nothing for a project that does not opt in
- the Basic Memory dependency is expressed where it belongs — conditional text plus the manifest choice
- the gate can iterate and be rolled back per project before any promotion into a base fragment

### Trade-offs

- adopters must add one manifest line to receive the gate; a project that updates blind receives nothing new. The follow-up update workflow exists to make that step visible and cheap.

### Follow-ups

- promote the draft into the `module-contract-gate` feature (placement accepted here; implementation pending)
- define the standards-update workflow — what a bare "update ai-standards" request does: refresh enabled features, digest new features since the pinned version, confirm per feature before enabling. Separate decision record to follow.

## Observations

- [decision] The module-contract discovery gate ships as the opt-in `module-contract-gate` feature, not as an extension of `structured-artifacts`.
- [decision] The gate's strict rule stays near-verbatim; Task Start becomes proportional, and Basic Memory steps stay conditional on the feature being enabled.
- [fact] Render order of `AGENTS.md` sections follows the manifest `features` list order, so the gate lands directly after Module Contracts when listed right after `structured-artifacts`.

## Relations

- relates_to [[DECISION: standards-update-workflow]]
- relates_to [[0tkgosq — Standard Code Review Skill and Contract Checks]]
