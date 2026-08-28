---
title: '0tkhikr — ai-standards 2.2.0 release session'
permalink: ai-standards/tasks/0tkhikr-ai-standards-2-2-0-release-session
---

# 0tkhikr — ai-standards 2.2.0 release session

Russian version: [0tkhikr-ai-standards-2-2-0-release-session.ru.md](0tkhikr-ai-standards-2-2-0-release-session.ru.md)

Date: 2026-08-28 · Branch: committed directly to `main` by user decision (commits `f6206b1`, `aab626e`, `fc2e9a9`, `8891313`, `9b1b0a8`, `c29fb57`, `9ae2d23`, `73c6c10`; release commit and tag `2.2.0-2026-08-28` follow this record)

## Trigger

A contributor draft on module-contract discovery (`docs/archive/0tkgv0g-module-contract-discovery-gate.md`, exchange with the contributor on 2026-07-28) awaited promotion; the maintainer additionally requested a rule-set version line in code-review reports, a defined standards-update workflow («обнови ai-standards» had been underdefined at four points), promotion of the cockpit-local response language rule, and the 2.2.0 release.

## What Was Done

- **Version line in the code-review report** (`f6206b1`): every report opens with `ai-standards <version>` taken from the generated instructions header, so a pasted report records which rule set the review ran under.
- **Standards-update workflow** (`fc2e9a9`, `8891313`): the `update-ai-standards` skill deploys with every deployment that declares agents — no feature toggle; enabled features re-render silently, features added since the pinned version are announced from `[feature_meta].since` with recommendations against the project's stacks, and only confirmed features are enabled. `[feature_meta]` added to `registry.toml`; pin drift is reported (`check` fails, `render`/`update` warn, `doctor` echoes `standards-version-drift`); bootstrap lives in the release notes.
- **Module-contract discovery gate** (`aab626e`, `9b1b0a8`, `c29fb57`, `9ae2d23`): placement decision (separate opt-in feature, not an extension of `structured-artifacts`), then the `module-contract-gate` feature — a registry composite carrying the contracts policy; strict rule near-verbatim, proportional task-start discovery, conditional Basic Memory steps, escalation through `Autonomy Boundaries`. Enabled for ai-standards and cockpit.
- **`response-language-style` feature** (`73c6c10`): natural Russian replies, no anglicisms with common equivalents, no slang, abbreviation discipline, verbatim technical names. Opt-in; promoted from the cockpit-local rule, whose block became a short carrier line in cockpit's override.
- **Release 2.2.0**: housekeeping (6 merged branches and `pr-3` deleted, stale worktrees pruned), `bump-version save --part minor` (2.2.0, 2026-08-28), CHANGELOG `Unreleased` → `[2.2.0] — 2026-08-28` with the Upgrade Notes bootstrap section, test fixture version bumped.

## Verification

103 tests passed; `mypy` strict and `ruff` clean; `ai-sync check` green for ai-standards and cockpit; `doctor` zero errors in both; renders idempotent. The release commit and tag follow this record.

## Deliberately Not Done

- The gate and the language style stay opt-in — no default-on for adopters (placement decision of the same date).
- No usage guide for `response-language-style`: the fragment is self-contained, like the core fragments.
- No Basic Memory index notes for module contracts were written; the fragment defines what such entries should carry, populating indexes is a per-project task.
- Stale remote branch `origin/feature/0tkf6ym-capture-knowledge` left for the maintainer's explicit deletion approval.

## Context For The Next Session

- Push approval per batch is still the maintainer's call; this session's commits ride on batches the maintainer pushed directly.
- The update skill announces `code-review`, `knowledge-capture`, `module-contract-gate`, and `response-language-style` to deployments pinned below 2.2.0 once the tag is pushed.
- Hygiene backlog (notes without observations/relations, bilingual H1 duplicates) unchanged by design.

## Observations

- [decision] The module-contract discovery gate ships as the opt-in `module-contract-gate` feature; the update skill announces it to older deployments from `[feature_meta].since`.
- [decision] The update skill deploys without a feature toggle, because it maintains ai-standards itself rather than a project process.
- [fact] A bare «обнови ai-standards» request now has a defined procedure: silent refresh of enabled features, digest of new features since the pin, one confirmation, pin bump, verification.
- [fact] `ai-sync check` fails while `ai_standards_version` disagrees with the source in use; `render`/`update` warn and `doctor` reports the drift.

## Relations

- relates_to [[DECISION: module-contract-gate-feature-placement]]
- relates_to [[DECISION: standards-update-workflow]]
- relates_to [[Module Contract: scripts/ai_sync.py]]
- relates_to [[0tkgosq — Standard Code Review Skill and Contract Checks]]
