# ConPort Usage Guide

Russian localized version: [conport-usage.ru.md](conport-usage.ru.md)

This guide explains how to use the `conport` feature from `ai-standards` in downstream projects.

`conport` standardizes ConPort as transient operational memory for active context, recent progress, investigation state, and session handoffs — without treating it as the canonical source of durable project truth.

## Goals

Use `conport` when you want the agent or team to:

- preserve active context and recent progress across sessions
- hand off investigation state between agents or chats without re-deriving it
- keep durable architectural knowledge in Git-tracked Markdown, not in ConPort
- retrieve targeted operational context instead of dumping everything

Typical outcomes:

- faster session restarts with accurate context
- less lost investigation state between handoffs
- clearer separation between transient memory and reviewed truth

## What The Feature Covers

The feature standardizes shared policy for:

- using ConPort as transient operational memory and handoff storage
- treating Git-tracked Markdown as the canonical source of durable truth
- targeted retrieval over large context dumps
- capturing durable lessons only when they prevent a class of error

It intentionally does not standardize:

- one mandatory ConPort schema for every project
- a specific confirmation workflow (projects may opt into one locally)
- automatic promotion of ConPort notes into canonical documentation

## Workspace Identity

ConPort identifies a workspace by its root path. Use the project root absolute path as the `workspace_id`:

- the workspace is the project root directory
- `context_portal/` lives at the project root and is gitignored runtime state

Create `context_portal/` before relying on ConPort workspace detection. Without it, detection can walk up the directory tree to a parent (such as the home directory) and bind the workspace to the wrong root.

## Transient Memory, Not Canonical Truth

ConPort is transient operational memory. Durable architectural, operational, and module-boundary knowledge belongs in Git-tracked Markdown artifacts:

- decision records (`docs/decisions/**`)
- module contracts (`MODULE_CONTRACT.md`)
- architecture docs (`docs/architecture/**`)

ConPort complements these artifacts; it does not replace them. Promote durable conclusions from ConPort into canonical documentation only on explicit user request.

## Durable Lessons

After meaningful corrections or repeated mistakes, capture only durable lessons that can prevent the same class of error. Record the pattern, the preventive rule, and the scope where it applies. Do not create mechanical memory churn for one-off or low-signal corrections.

## Relationship To Other Features

- `basic-memory` is a retrieval layer over Git-tracked Markdown documentation.
- `chroma` is a semantic code-search layer over source files.
- `structured-artifacts` defines which Markdown artifacts count as plans, decision records, and module contracts.
- `session-hygiene` defines when to reload relevant durable context between phases or chats.

`conport` complements these features by preserving transient operational context and handoffs. It does not replace reviewable documentation or explicit human decisions.

## Manifest Example

```toml
features = [
  "conport",
  "basic-memory",
  "chroma",
  "structured-artifacts",
  "session-hygiene",
]
```

## Practical Prompting Guidance

Good prompts:

- `Load ConPort active context at the start of this task.`
- `Record this progress and the next step in ConPort for the handoff.`
- `Capture this as a durable lesson only if it prevents a class of error.`

Avoid:

- `Treat ConPort as the source of truth for architecture.`
- `Dump the entire ConPort database into context.`
- `Promote ConPort notes into docs/decisions without explicit approval.`

Prefer:

- `Targeted retrieval of the relevant ConPort context, then act.`
