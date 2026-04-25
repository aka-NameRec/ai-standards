# Session Hygiene Usage Guide

Russian localized version: [session-hygiene-usage.ru.md](session-hygiene-usage.ru.md)

This guide explains how to use the `session-hygiene` feature from `ai-standards` in downstream projects.

`session-hygiene` is a reusable process feature for reducing context drift, stale assumptions, and goal substitution in long chat sessions.

The feature is tool-neutral. It does not encode a specific context window size, message count, or vendor-specific chat behavior.

## Goals

Use `session-hygiene` when you want the agent or team to:

- notice when a long thread becomes risky to continue
- preserve critical context outside transient chat memory
- create compact handoffs before starting a fresh chat
- reload project rules and task artifacts at phase boundaries
- avoid silently continuing from stale assumptions

Typical outcomes:

- fewer lost constraints
- clearer phase transitions between design, implementation, review, merge, and release
- better continuity across fresh chats
- more reviewable long-running work

## What The Feature Covers

The feature standardizes shared policy for:

- warning about long-session risk
- handoff summaries
- fresh-chat recommendations
- re-reading rules and artifacts when the work changes phase
- separating confirmed state from assumptions

It intentionally does not standardize:

- hard message-count, time, or token-count limits
- tool-specific context-window behavior
- automatic chat resets
- dumping the full conversation into a summary

Projects may add local thresholds when they have evidence that a specific tool, team, or workflow needs them.

## Long-Session Warning

The agent should warn the user when continuing the current thread increases the risk of:

- context drift
- stale assumptions
- goal substitution
- lost constraints
- hidden decisions that are hard to review

Warning is especially important when:

- the current goal has been restated several times
- older decisions conflict with newer instructions
- the agent is unsure which constraints still apply
- review would require reconstructing important context from a long conversation
- the next step depends on old chat context not captured in an artifact or durable memory

## Handoff Summary

Before continuing a risky long session, the agent should offer or produce a compact handoff summary.

Recommended fields:

- current goal
- accepted decisions
- touched files or modules
- active constraints and non-goals
- unresolved questions
- verification status
- known risks
- recommended next bounded slice

The summary should be short enough to paste into a new chat or project artifact.

Separate:

- confirmed project state
- user-approved decisions
- assumptions
- inferred context

Do not turn handoff into a full transcript.

## When To Start A Fresh Chat

Prefer starting a fresh chat when:

- the work changes phase, such as design to implementation, implementation to review, review to merge, or merge to release
- the current context can no longer be summarized compactly
- the next slice depends on project rules or decisions that should be reloaded explicitly
- the agent has warned about stale assumptions or goal drift
- the user wants to reduce context noise before a focused next step

A fresh chat should start with:

- the handoff summary
- relevant project rules
- active context or task artifacts
- the next bounded objective

## Reloading Rules And Durable Context

At phase boundaries, re-read relevant sources instead of relying only on chat memory:

- `AGENTS.md`
- project-local AI rules
- ConPort active context when available
- task notes or change plans
- decision records
- module contracts or migration notes

Reload only what is relevant to the next slice. Session hygiene should not become broad context loading by default.

## Relationship To Other Features

- `conport` stores active context, progress, and durable lessons between sessions.
- `structured-artifacts` provides change plans, decision records, and module contracts that make handoffs concrete.
- `autonomy-boundaries` defines when long autonomous execution must stop for human review.
- `reasoning-hygiene` keeps assumptions, edge cases, and verification points explicit.
- `agent-usage-hygiene` reduces avoidable context and usage waste.

`session-hygiene` focuses specifically on the reliability of the active chat session.

## Manifest Example

```toml
features = [
  "conport",
  "design-first-collaboration",
  "reasoning-hygiene",
  "autonomy-boundaries",
  "structured-artifacts",
  "session-hygiene",
]
```

## Practical Prompting Guidance

Good prompts:

- `This chat is getting long. Create a handoff summary and recommend whether we should continue here or start fresh.`
- `Before the next phase, re-read the project rules and summarize only the constraints that matter now.`
- `Prepare a new-chat handoff with goal, decisions, risks, verification status, and next slice.`
- `Warn me if you think context drift or stale assumptions are affecting this task.`

Avoid:

- `Continue from memory; no need to re-check rules.`
- `Summarize everything in the chat.`
- `Keep going even if the goal has changed.`

Prefer:

- `If continuing this thread is riskier than starting fresh, say so and produce a compact handoff.`
