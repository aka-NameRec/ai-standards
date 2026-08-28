---
title: Module Contract Gate Usage Guide
permalink: ai-standards/module-contract-gate-usage
---

# Module Contract Gate Usage Guide

Russian localized version: [module-contract-gate-usage.ru.md](module-contract-gate-usage.ru.md)

This guide covers when to enable the `module-contract-gate` feature and what it changes for an adopting project.

## Why This Feature Exists

Module contracts were covered at two points only: the policy for creating them (`structured-artifacts`) and review-time enforcement (`code-review`, the standard review skill). Nothing obliged an agent to discover and apply contracts at the moment code was written, so a contract could exist and still be ignored by the change that violated it — the failure this feature closes. Rationale and placement: [the placement decision](decisions/2026-08-28-module-contract-gate-feature-placement.md).

## Activation

Enable the feature in `ai.project.toml` — conventionally right after `structured-artifacts`, so the rendered section lands directly after Module Contracts — then render:

```bash
uv run ai-sync render --project-root /path/to/project
```

The feature is a registry composite: it also carries `structured-artifacts`, because a discovery gate without the contracts policy it polices makes no sense. Enabling both is deduplicated; enabling the gate on a project that somehow lacked the contracts policy adds it.

## What It Changes

The gate is a write-time duty, not a review pass:

- **Discovery at task start, proportionally.** One cheap check establishes whether the project declares contract artifacts at all; a declared absence completes discovery, and the agent says so in one line. Only projects that declare contracts pay for the full index query and repository scan — and when the index is missing or stale, the agent says so before scanning, so the cost is a decision, not a surprise.
- **Coverage per touched file.** Before editing, the agent decides whether the file is covered — by explicit naming, by directory, by data flow, by affected responsibilities, or by tests exercising contract behavior. Unclear coverage is treated as relevant and read.
- **Contracts constrain the change.** Scope, allowed behavior changes, error handling, compatibility, required verification; a change that contradicts a contract stops and reports instead of being implemented silently.
- **Re-discovery on triggers.** New module or layer, contract files moving in the diff, new classes joining the edit set, verification failures suggesting a misunderstood boundary.
- **A short contract note** in the implementation summary: what was read, what was covered, whether the contract survives, what was verified against it.

The strict rule stays absolute: no production-code edit before discovery for the touched files completes. Basic Memory satisfies discovery only as an index; canonical contracts are read from the repository.

## What It Does Not Do

It does not create contracts — creation policy stays with `structured-artifacts`, and most modules correctly have no contract. It does not duplicate review: the code-review workflow and the `standard-code-review` skill check changed modules against contracts after the fact, which is exactly what the gate complements. And it does not touch projects that do not enable it — an ai-standards update changes nothing for them.

## Relationship To The Update Workflow

The update skill (`update-ai-standards`) announces this feature to older deployments from the `[feature_meta]` `since` marker in `registry.toml`, with a recommendation against the project's stacks. Enabling it remains an explicit per-project choice, made either at update time or directly in the manifest.
