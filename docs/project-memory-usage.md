---
title: Project Memory Usage Guide
permalink: ai-standards/project-memory-usage
---

# Project Memory Usage Guide

Russian localized version: [project-memory-usage.ru.md](project-memory-usage.ru.md)

This guide explains how to use the `project-memory` feature from `ai-standards` in downstream projects.

`project-memory` gives local cross-session working memory a standard home and lifecycle: `docs/local/**`, gitignored by default, with a fixed taxonomy, a write policy, a read policy, and an explicit promotion path into canonical documentation.

## Goals

Use `project-memory` when you want the agent or team to:

- preserve task state across sessions without polluting Git history or canonical docs
- resume yesterday's task from a compact resume point instead of replaying a chat
- keep provisional decisions and investigations separate from accepted project decisions
- record discovered project patterns as working knowledge that can be superseded

Typical outcomes:

- canonical documentation stays free of session state
- a new session starts from a targeted retrieval, not a memory dump
- provisional knowledge has a visible status and an explicit promotion path

## Memory Areas

| Area | Path | Canonical? | Committed? |
|---|---|---|---|
| canonical project knowledge | `docs/domain/**`, `docs/decisions/**`, `docs/architecture/**` | yes | yes |
| local working memory | `docs/local/**` | never | no (gitignored by default) |

Two hard rules follow:

- Never treat local working memory as canonical project documentation.
- Do not write temporary task state, speculative findings, or session continuation data into canonical documentation merely to preserve agent context.

## Taxonomy

| Category | Question it answers | Lifecycle / fields |
|---|---|---|
| `context/` | what are we trying to accomplish | goal, scope, constraints, phase, next step |
| `decisions/` | what was decided locally, and why | `provisional` → `confirmed` → `superseded` / `rejected` |
| `progress/` | where did the work stop | `done`, `current`, `blocked`, `next` |
| `patterns/` | what reusable property was discovered | validated against source; superseded on contrary evidence |
| `investigations/` | what is being investigated, what evidence exists | `open` → `resolved` / `abandoned` |
| `handoffs/` | how to resume without replaying the chat | goal, confirmed state, open questions, next action |

The semantic categories are the standard; the physical split into directories may be configured per project.

A local `confirmed` decision means confirmed for the current work context. It does not automatically become a canonical decision record.

## Write Policy

Memory is a curated state store, not an execution log.

Write when the information: will be needed in a later session; materially affects further decisions; is expensive to reconstruct; is the result of an investigation; explains the current status; captures an unresolved question or blocker; or is a confirmed reusable project pattern.

Do not write: what a single obvious file already says; transient tool output; reasoning detail; what already exists canonically; a guess with no useful role; a duplicate that changes no state.

## Read Policy

Query local memory by the current goal, relevant entities, modules, concepts, decisions, and task identifiers — never `read docs/local/**` at session start. To continue previous work: retrieve the relevant context, then the current progress, then the relevant decisions; open patterns and investigations only as the current step requires.

## Promotion

Promotion from local memory to canonical documentation is an explicit semantic operation, never an automatic synchronization step:

```text
capture → retrieve/update → validate → discard | retain local → promote? → canonical docs
```

Promote only knowledge that has become durable, and only when the user or the project workflow permits the corresponding canonical artifact. For example, `docs/local/decisions/catalog-indexing.md` may eventually become `docs/decisions/2026-09-18-incremental-catalog-indexing.md` — after validation and with the user's explicit request.

## Note Shape And Doctor

Minimal frontmatter: `title`, `type`, `status`, `updated`, plus `source` when the note records a discovered fact. Canonical-note requirements — dated file names, `## Observations` and `## Relations` sections — do not apply inside `docs/local/**`.

`ai-sync doctor` audits the local area with relaxed canonical rules (readability only) and warns when the area exists without a covering `.gitignore` pattern (`local-memory-not-gitignored`). Add `/docs/local/` to `.gitignore` when enabling the feature.

## Relationship To Other Features

- `retrieval-routing` routes "previous task state" and "prior local decisions" queries to this memory.
- `basic-memory` is the recommended retrieval layer over the area; the feature works without it (plain files), which is exactly the capability/implementation split.
- `session-hygiene` defines when state must be preserved or reloaded; `project-memory` defines what and how.
- `structured-artifacts` owns reviewable canonical artifacts; promotion from local memory follows its write policy.
- `knowledge-capture` syncs local context/progress/handoff notes as part of the standard capture flow.

## Manifest Example

```toml
features = [
  "retrieval-routing",
  "basic-memory",
  "project-memory",
  "structured-artifacts",
  "session-hygiene",
]

# Optional: relocate the local area inside the knowledge tree.
# [project_memory]
# local_tree = "local"
```

## Observations

- [fact] The taxonomy and lifecycle are tool-independent; plain files under `docs/local/**` satisfy them, and `basic-memory` adds targeted retrieval on top.
- [fact] `doctor` relaxes canonical-note rules inside the local area and warns when the area is not gitignored, so local memory and canonical knowledge cannot silently mix.

## Relations

- relates_to [[DECISION: memory and retrieval reorganization]]
- relates_to [[Retrieval Routing Usage Guide]]
- localized counterpart of [[Руководство по использованию project-memory]]
