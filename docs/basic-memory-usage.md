# Basic Memory Usage Guide

Russian localized version: [basic-memory-usage.ru.md](basic-memory-usage.ru.md)

This guide explains how to use the `basic-memory` feature from `ai-standards` in downstream projects.

`basic-memory` standardizes how a project should use Basic Memory as a Markdown-first retrieval layer without letting it become an uncontrolled source of architectural truth.

## Goals

Use `basic-memory` when you want the agent or team to:

- keep durable project knowledge in Git-tracked Markdown
- search that knowledge efficiently across sessions through Basic Memory
- distinguish canonical documentation from agent-managed working memory
- avoid accidental documentation drift from indexing side effects
- reindex intentionally after repository events that can stale the graph

Typical outcomes:

- less hidden knowledge trapped in chat history
- better reuse of existing project notes and decisions
- fewer duplicate documentation files
- clearer boundaries between reviewed truth and agent scratch space

## What The Feature Covers

The feature standardizes shared policy for:

- using Basic Memory as a retrieval layer, not as the canonical source of truth
- separating canonical documentation from working memory
- checking for duplication or contradiction before canonical documentation updates
- keeping the indexed knowledge tree free of rendering inputs and machine-owned files
- deciding what earns a place in the knowledge base, and what is noise that still has to be maintained
- keeping the base in shape over time: duplicates, supersession, archiving
- deciding when filesystem auto-sync is enough and when explicit reindexing is required

It intentionally does not standardize:

- one mandatory folder layout inside the knowledge tree
- a specific Basic Memory cloud or local deployment mode
- one universal schema for every note type
- automatic promotion of working notes into canonical documentation

## Canonical Documentation Versus Working Memory

Treat the following as canonical documentation:

- `docs/decisions/**`
- `docs/architecture/**`
- `MODULE_CONTRACT.md`
- equivalent local artifacts that define accepted constraints, contracts, or decisions

Treat the following as working memory:

- `docs/ai-memory/**`
- investigation notes
- handoff notes
- implementation gotchas
- temporary findings that are still evolving

Canonical documentation should change only on explicit user request. Working memory may be updated autonomously when it helps preserve useful context.

## Knowledge Tree Boundaries

Point a Basic Memory project at a dedicated knowledge tree, such as `docs/`, and never at a repository root.

A repository root is not a knowledge base. Basic Memory indexes every file it can read, so a root-level project pulls vendored dependencies, build artifacts, generated metadata, and office documents into the graph as if they were notes. Retrieval quality drops, and every one of those files becomes a candidate for frontmatter injection.

Inside the knowledge tree, every file is a note. That has a direct consequence for rendering inputs: a `local_overrides` file is concatenated verbatim into the generated `AGENTS.md`, so frontmatter written into it by an indexer would surface in the middle of the agent instruction file. Keep such inputs outside the tree — `ai/project-rules.md` rather than `docs/ai/project-rules.md`. `ai-sync init-project` scaffolds them there.

The same rule covers templates, generated output, and any other machine-owned Markdown.

## Frontmatter And Permalinks

Basic Memory can write frontmatter during sync. On a clean knowledge tree that is desirable: permalinks are what `memory://` addressing and graph traversal resolve through, and a project without them degrades to plain search.

So keep permalink generation on once the tree holds only notes, and accept the one-time migration commit that adds `permalink:` to existing files.

Two flags disable the write path, and they are a fallback for a legacy tree that cannot be narrowed yet, not a default:

- `ensure_frontmatter_on_sync=false`
- `disable_permalinks=true`

Both are needed together. `ensure_frontmatter_on_sync=false` alone stops frontmatter being added to files that lack it, while files that already carry frontmatter still get rewritten. The pair also gives up `memory://` addressing, so record that trade-off before choosing it.

Note that file names do not drive retrieval. A note is identified by its frontmatter `title`; the file name only supplies a fallback title for files that have none. File naming is therefore a house convention, free to follow the project's own rules.

## Two Genres Of Knowledge

Domain-driven design draws the line this project follows. The **problem space** is the business as it exists: the activities it performs, the rules it operates under, the language it uses. You do not design it — you discover it from domain experts and sources, and it stays true whatever the code does. The **solution space** is the software built to serve it, where design decisions are made.

Keeping the two apart matters most for what an agent is allowed to change. When a document mixes them, an agent that finds a mismatch between the document and the code cannot tell which one is wrong. For a solution-space note, updating it to match the code is usually right. For a problem-space rule it is a catastrophe: the code silently becomes the authority on how accounting works. Separation is how you tell an agent where the document wins and the code must be fixed instead.

The two genres carry different obligations:

| | Problem space | Solution space |
|---|---|---|
| Kind of statement | discovered fact | chosen option |
| Must carry | its source: who stated it, which regulation or agreement, when confirmed | the alternatives rejected and the consequences accepted |
| Changes when | the business or the law changes | the implementation changes |
| Confirmed by | domain experts, regulations, contracts | the team |
| Verified against | the original source | the code and its tests |

They are linked, not merged. A decision `implements` the rule it serves, so the reasoning is traversable from either side, and a problem-space rule with nothing implementing it is either unbuilt or dead.

Do not split decisions further among themselves. Architectural, design, tooling, and policy decisions share one format — the MADR project generalized its own acronym from "Markdown Architectural Decision Record" to "Markdown Any Decision Record" for exactly this reason, since the category boundaries are fuzzy and significance is what decides whether a decision is worth recording. The split worth making is between decisions and discovered facts, not among decisions.

## Stable And Volatile Knowledge

Living documentation practice supplies the second axis: requirements and high-level goals are more stable than design decisions, and a document that mixes the two inherits the shorter life. The symptom is easy to spot — if a document needs editing after every refactor, volatile knowledge has leaked into it.

The same practice gives the rule that keeps notes from multiplying: most of the knowledge worth sharing is **already in the artifacts**, just not in a convenient form. Make it explicit where it lives rather than restating it in a note that then has to be kept true. And keep one source of truth for any fact, referencing it from anywhere else rather than copying it.

## What Earns A Place In The Knowledge Base

The failure mode is not an empty knowledge base. It is a knowledge base full of statements nobody needed, each of which still has to be read, reviewed, and kept true.

A note earns its place when a competent reader could not get the same answer faster by opening the code. Two observations about the same line:

```
- [fact] str(digit) converts a number to a string
- [decision] Numeric ids are serialized as strings because the external API rejects integers
```

The first is a restatement. Nobody can disagree with it, it is obvious to anyone reading the line, and it becomes silently wrong the moment the line changes. The second is knowledge: it survives the refactor, it explains a choice that looks wrong without context, and someone could argue against it.

Record: decisions together with the options they rejected; rules of the business and where they came from; constraints invisible in the code, such as legal, contractual, or operational limits; failure modes that were actually hit; and agreements between people.

Do not record: restatements of code; implementation detail that the next refactor invalidates; the note's own prose paraphrased into observations; or speculation presented as fact. Name uncertainty as uncertainty instead — that is itself worth recording.

## The Task Is Not A Subject

A task, an issue, or a merge request is a delivery vehicle. Its history already lives in the tracker, and nobody will later look it up as a subject.

Most tasks therefore produce no documentation — not because something was missed, but because they change **how** the product works rather than **what** it is required to do:

> A new requirement widens existing business behaviour — a stage added to a workflow, a rule that changes who may do what.

That is problem-space knowledge. It goes into the document that already describes that behaviour, and it needs a source. No note is created about the task that delivered it.

> The design was obvious: a couple of models and a service, following the pattern the codebase already uses.

Nothing is written. No option was rejected, so there is no decision to record, and the code carries the rest perfectly well.

The habit to avoid is one note per task, per merge request, or per session. It feels diligent and produces a graph whose entries have exactly one reader — whoever wrote them — after which they rot in place and start contradicting the code.

Prefer extending an existing document over creating a new one. A new document is justified by a new subject, not by a new task.

## Keeping The Base In Shape

Hygiene runs on a cadence, not every session, and the two layers have different rules.

Agent-managed working memory may be pruned autonomously: merge duplicates, split a note that grew past one concept, retire what no longer holds.

Canonical documentation is append-and-supersede. A decision that no longer applies is marked superseded with a link to its replacement rather than rewritten, so the earlier reasoning stays readable and the record of why it changed survives.

Archive rather than delete. Deleting a note drops its observations and relations from the graph, which quietly removes context from every note that pointed at it. Move it to a folder that records the status and keep the links intact.

Reach for the indexer's own tooling before writing your own: `bm orphans` lists notes with no relation in either direction, and the schema commands infer, validate, and diff per-type field contracts. `ai-sync doctor` covers the structural half and leaves these to it.

## Workspace Isolation

Basic Memory must be scoped to a single project per workspace so retrieval returns only the current project's artifacts instead of a noisy mix from unrelated projects.

- Constrain the MCP server to one project (for example `bm mcp --project <project>` or the equivalent per-workspace MCP configuration).
- Disable the Basic Memory MCP server in workspaces that do not have a project, so queries never fall back to a shared default dump.
- Reserve cross-project search for an explicit, intentional action from a meta-project; it is not the default retrieval mode.

This keeps each project's knowledge layer precise and prevents the "common dump" problem where results mix artifacts from unrelated projects.

## Reindexing Policy

Normal file edits inside indexed directories should rely on Basic Memory's regular filesystem sync.

Run a status check after:

- `git pull`
- `git merge`
- `git rebase`
- branch switch or checkout
- applying a large patch that changes many indexed Markdown files

Run an explicit project reindex after:

- mass file renames, moves, or deletes inside indexed directories
- interrupted indexing or incomplete embeddings
- changing the indexed root path for a project
- changing permalink behavior or frontmatter-sync policy
- first-time indexing of an existing large documentation tree

Prefer these operational patterns:

- `bm status --project <project>`
- `bm reindex --project <project>`
- `bm reindex --project <project> --embeddings`
- `bm reindex --project <project> --full`

Use the narrowest reindex that resolves the reported problem.

## Relationship To Other Features

- `structured-artifacts` defines which Markdown artifacts count as plans, decision records, and module contracts.
- `session-hygiene` defines when the agent should reload relevant durable context between phases or chats.
- `conport` remains useful for transient operational context and handoff storage.
- `design-first-collaboration` keeps intent, boundaries, and non-goals explicit before implementation.

`basic-memory` complements these features by making Git-tracked Markdown easier to retrieve and reuse. It does not replace reviewable documentation or explicit human decisions.

## Manifest Example

```toml
features = [
  "conport",
  "basic-memory",
  "structured-artifacts",
  "session-hygiene",
]
```

## Practical Prompting Guidance

Good prompts:

- `Search our Basic Memory notes before creating a new design note.`
- `Check whether this decision already exists in docs/decisions or ai-memory before writing anything new.`
- `After this merge, check Basic Memory status and reindex only if the docs graph is stale.`
- `Record this implementation gotcha in working memory, not in canonical documentation.`

Avoid:

- `Promote everything from working notes into docs/decisions.`
- `Let Basic Memory rewrite repository docs however it wants.`
- `Reindex from scratch in every session whether needed or not.`

Prefer:

- `Use Basic Memory to search first, then update the smallest correct Markdown artifact.`
