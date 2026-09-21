---
title: Context Architecture Usage Guide
permalink: ai-standards/context-architecture-usage
---

# Context Architecture Usage Guide

Russian localized version: [context-architecture-usage.ru.md](context-architecture-usage.ru.md)

This guide covers when to enable the `context-architecture` feature and what it changes for an adopting project.

## Why This Feature Exists

Rule Engineering (`rule-engineering`) ends by selecting a context layer, but
until now the layers themselves had no formal definition: "always-loaded
rule", "skill", "reference", "retrieval", "script/tool", "project knowledge",
and "adapter" were folk categories. Without a formal placement model, every
addition drifts back into always-loaded text by default, and `AGENTS.md` grows
into a dump of everything the project once knew. This feature fixes the model:
seven layers with purposes, an ordered set of placement questions, and a
control-plane invariant for what always-loaded instructions may carry.

## Activation

Enable the feature in `ai.project.toml` — conventionally right after
`rule-engineering`, because it formalizes the layer selection that flow ends
with — then render:

```bash
uv run ai-sync render --project-root /path/to/project
```

No hard dependencies; it composes with `rule-engineering` and with any
retrieval capability the project enables.

## What It Changes

- **Placement becomes a checked step.** Every addition to the standards or the
  project's instructions answers the placement questions in order, first match
  wins, and the tie-break is explicit: prefer the layer that loads latest
  while still guaranteeing the knowledge arrives when needed.
- **The control plane stays a control plane.** Always-loaded instructions
  carry universal invariants, routing, mandatory gates, precedence, discovery
  instructions, and minimum completion requirements — never task-specific
  operational detail.
- **Reduction is gated.** Shrinking always-loaded content is performed only
  with a behavior-preserving comparison against the current state, so context
  savings never purchase lost behavior.

## What It Does Not Do

It does not move anything by itself: adopting the feature changes decisions
about new knowledge and starts a classification review, but any physical
reduction of always-loaded content is a separate, evaluated change. It does
not define scenario execution — the behavior-preserving comparisons belong to
the `ai-standards-evals` specification (issue #18).

## Relationship To Rule Engineering

Rule Engineering's flow ends with "select context layer"; this feature is the
model that step consults. The placement questions are the formal instrument;
the flow records the decision. Enabling one without the other leaves a gap:
engineering without placement has no target layers, and placement without
engineering has no quality bar for what gets placed.
