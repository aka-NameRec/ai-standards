---
title: Agent Usage Hygiene Usage Guide
permalink: ai-standards/agent-usage-hygiene-usage
---

# Agent Usage Hygiene Usage Guide

Russian localized version: [agent-usage-hygiene-usage.ru.md](agent-usage-hygiene-usage.ru.md)

This guide explains how to use the `agent-usage-hygiene` feature from `ai-standards` in downstream projects.

`agent-usage-hygiene` is a reusable process feature for reducing avoidable agent usage by keeping context, exploration, and implementation slices focused.

The feature is tool-neutral. It does not encode vendor billing details, model-specific modes, or brittle numeric limits.

## Goals

Use `agent-usage-hygiene` when you want the agent or team to:

- avoid loading broad context when targeted discovery is enough
- keep implementation slices compact and reviewable
- activate a stricter economy mode when the user explicitly asks to conserve usage
- preserve correctness, safety, and required verification while reducing waste

Typical outcomes:

- fewer unnecessary file reads
- shorter and more focused intermediate explanations
- clearer handoffs between bounded slices
- less context drift in long sessions

## What The Feature Covers

The feature standardizes shared policy for:

- targeted repository discovery before broad inspection
- prompt-activated economy mode
- compact handoff summaries
- risk-based splitting of large work
- prioritizing correctness when economy and verification conflict

It intentionally does not standardize:

- vendor-specific billing controls
- model-specific fast or economy modes
- hard limits on file count, command count, or checkpoint frequency
- skipping tests or review steps solely to save usage

## Default Rule

Usage economy is context discipline, not lower engineering quality.

The agent should avoid waste, but it must not hide uncertainty, skip required verification, or choose a weaker solution because it is cheaper to explain.

## Economy Mode Activation

Economy mode becomes active only when the user explicitly asks for it in the current task or thread.

Typical activation phrases:

- `be economical`
- `preserve limits`
- `reduce token usage`
- `minimize context`
- `keep usage low`
- `be concise and usage-conscious`

Localized project prompts may define equivalent phrases in the team's working language.

Economy mode ends when:

- the current task ends
- the user explicitly disables it
- the agent reports that economy conflicts with correctness, safety, or required verification

## Economy Mode Behavior

In economy mode, prefer:

- one short scope clarification over broad speculative discovery
- search, diffs, logs, and targeted commands before reading large file sets
- focused file reads for the current slice
- compact progress updates
- targeted checks that prove the changed behavior
- handoff summaries instead of dragging a long thread forward indefinitely

Avoid:

- repository-wide reading without a clear reason
- long repeated summaries of context already captured in artifacts
- broad refactors hidden inside a usage-saving request
- skipping critical verification

## Relationship To Other Features

- `design-first-collaboration` defines change intent, boundaries, and non-goals before implementation.
- `reasoning-hygiene` keeps analysis focused on assumptions, risks, and verification.
- `autonomy-boundaries` prevents long sessions from drifting beyond reviewable slices.
- `structured-artifacts` provides change plans, contracts, and decision records that reduce transient context load.
- `conport` can preserve durable project memory outside the active model context.

`agent-usage-hygiene` does not replace these features. It makes their context-economy value explicit and adds prompt-activated economy behavior.

## Manifest Example

```toml
features = [
  "conport",
  "design-first-collaboration",
  "reasoning-hygiene",
  "autonomy-boundaries",
  "structured-artifacts",
  "agent-usage-hygiene",
]
```

## Practical Prompting Guidance

Good prompts:

- `Be economical: inspect only the files needed to diagnose this failing test, then propose the smallest fix.`
- `Keep usage low. First tell me the narrow slice you need to inspect before reading more files.`
- `Minimize context and produce a compact handoff summary after this slice.`
- `Use economy mode, but do not skip verification needed to prove the change.`

Avoid prompts that turn economy into lower quality:

- `Do not run tests to save tokens.`
- `Guess without reading files.`
- `Make it short even if important risks are omitted.`

Prefer asking the agent to explain conflicts explicitly:

- `If saving usage conflicts with correctness or verification, say so and prioritize correctness.`