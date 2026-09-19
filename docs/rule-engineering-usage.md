---
title: Rule Engineering Usage Guide
permalink: ai-standards/rule-engineering-usage
---

# Rule Engineering Usage Guide

Russian localized version: [rule-engineering-usage.ru.md](rule-engineering-usage.ru.md)

This guide covers when to enable the `rule-engineering` feature and what it changes for an adopting project.

## Why This Feature Exists

Until now the only shipped normalization process was the import flow for
external rule sets: extract candidates, classify as `keep`/`adapt`/`reject`,
normalize, place. It applied to external sources only. Rules born inside a
project, rules rewritten over time, and skill content had no quality bar: no
atomicity or ambiguity check, no uniqueness or conflict procedure, and no
requirement that compliance be observable or validated. Rule Engineering
replaces that source-specific flow with one process for every normative rule,
whatever its origin, and makes external importing one special case of it.

## Activation

Enable the feature in `ai.project.toml` and render:

```bash
uv run ai-sync render --project-root /path/to/project
```

The feature has no hard dependencies. It composes naturally with
`code-review` (rules are reviewed against observable behavior) and with any
retrieval capability (detailed guidance lives in documentation, not in
always-loaded context).

## What It Changes

The process runs at rule-creation and rule-change time:

- **One flow for every source.** External best practices, project-internal
  insights, reasoning/review/architecture/harness rules, and skill content all
  pass through the same engineering flow; an existing rule passes through it
  again on a material change. A small, evidence-backed wording correction does
  not require the full flow.
- **Nine quality properties.** Atomic, unambiguous, actionable, properly
  scoped, observable, unique (checked at lexical, semantic, and behavioral
  overlap levels — behavioral decides), non-conflicting (with explicit
  precedence when needed), correct abstraction level, portable.
- **Interpretation surface.** Wording is chosen to minimize the number of
  material decisions an agent must invent between reading a rule and acting on
  it — but not where the task genuinely requires contextual judgment.
- **Validation is mandatory.** Every rule defines at least one of: static
  validation, deterministic assertion, behavioral scenario, human rubric,
  cross-agent comparison. A rule with none stays out.
- **Context placement is part of engineering.** The flow ends with selecting
  the layer that delivers the knowledge at the right moment — always-loaded
  rule, skill, skill reference, retrieval, script/tool, project knowledge, or
  adapter.

## What It Does Not Do

It does not rewrite existing rules: adoption is incremental, and existing
content keeps its behavior when the feature is enabled. It does not define the
formal placement model — that arrives with the planned `context-architecture`
feature — nor any execution machinery for the validation forms: scenario
contracts will live under `docs/scenarios/` in the standards repository, and
scenario execution belongs to the separate `ai-standards-evals` specification
(issue #18).

## Relationship To Import External Rules

The import flow documented in the repository README becomes a special case:
its candidate-extraction and normalization steps remain, but every candidate
now continues through the Rule Engineering properties, placement decision, and
validation requirement instead of stopping at "normalize and place".

## Relationship To The Update Workflow

The update skill (`update-ai-standards`) announces this feature to older
deployments from the `[feature_meta]` `since` marker (`2.5.0`) in
`registry.toml`. Enabling it remains an explicit per-project choice, made
either at update time or directly in the manifest.
