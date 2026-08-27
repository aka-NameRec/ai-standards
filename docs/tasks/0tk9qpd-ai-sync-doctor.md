---
title: 'ai-sync doctor: Deterministic Knowledge-Tree Audit'
permalink: ai-standards/tasks/0tk9qpd-ai-sync-doctor
---

# ai-sync doctor: Deterministic Knowledge-Tree Audit

Task: `0tk9qpd` · Branch: `feature/0tk9ckw-archive-history-in-docs-tree` · 2026-08-24

Russian version: [0tk9qpd-ai-sync-doctor.ru.md](0tk9qpd-ai-sync-doctor.ru.md)

Related: [0tk9qoy-knowledge-genres.md](0tk9qoy-knowledge-genres.md) · [0tk9qpt-audit-knowledge-tree.md](0tk9qpt-audit-knowledge-tree.md)

## Why It Exists

A knowledge tree degrades mechanically: a rendering input lands inside the
indexed directory, an indexer stamps frontmatter onto it, a Basic Memory
project gets pointed at a repository root, permalinks get switched off. None of
these requires judgement to *detect* — so detection belongs to code, runs in
seconds, and can gate CI. `doctor` is that code. What requires judgement —
classifying a note, choosing a slug, splitting a mixed document — is left to
the [audit skill](0tk9qpt-audit-knowledge-tree.md); `doctor` deliberately does
not attempt it.

## What It Checks

**Rendering inputs** (always):

- `override-inside-knowledge-tree` (error) — a file listed in `local_overrides`
  lives inside the knowledge tree; an indexer can stamp frontmatter onto it and
  the next render would leak YAML into `AGENTS.md`.
- `override-carries-frontmatter` — an indexer already stamped a rendering input.

**Note health** (files inside the knowledge tree):

- `note-without-frontmatter` / `note-without-title` — a note Basic Memory will
  title from its file name;
- `note-title-heading-mismatch` — frontmatter `title` and `# H1` disagree;
- `note-name-against-convention` — file names in the dated directories
  (`domain`, `decisions`, `architecture` by default; configurable via
  `[basic_memory] dated_note_directories`) break `YYYY-MM-DD-topic-slug.md`;
- `note-without-observations` / `note-without-relations` — a note contributes
  nothing queryable to the graph;
- `note-unreadable` (error) — encoding damage instead of a crash.

**Indexer wiring** (only when the `basic-memory` feature is enabled; the
indexer config is read, never written):

- `indexed-repository-root` (error) — a Basic Memory project indexes a
  repository root instead of a knowledge tree;
- `knowledge-tree-not-indexed` — no project points at this tree;
- `permalinks-disabled` — `memory://` addressing and graph traversal are off;
- `other-indexed-repository-roots` — other projects index repository roots and
  therefore block global indexer settings.

Errors produce a non-zero exit code; warnings do not.

## How to Run It

```bash
ai-sync doctor --project-root <path>                  # report
ai-sync doctor --project-root <path> --fix            # apply mechanical repairs
```

Options: `--knowledge-tree` overrides the manifest's tree; `--indexer-config`
points at an alternative Basic Memory config (default `~/.basic-memory/config.json`);
`--override-directory` sets where `--fix` moves misplaced rendering inputs
(default `ai/`).

**What `--fix` does**: moves rendering inputs out of the tree and repoints the
manifest, strips indexer-stamped frontmatter, restores missing titles and
headings, prunes directories it empties. It re-runs the audit afterwards and
prints what remains. It warns when no git repository can undo it. After moving
a rendering input it asks for `ai-sync render`.

**What `--fix` refuses to do**: rename files (a meaningful slug is a naming
decision, and transliteration produces exactly the unreadable name the
convention exists to avoid) and touch note content. Those are the skill's work.

## When to Run It

- after `ai-sync init-project`, to confirm the scaffold landed correctly;
- in CI or as a pre-commit gate — exit code 1 on errors makes it a checkpoint;
- after changing the Basic Memory project setup or the manifest's
  `[basic_memory]` section;
- whenever retrieval behaves oddly — a wrong indexed root and disabled
  permalinks are the two most common silent failures.

It is a *diagnostic*, not a reviewer: a clean report says the tree is wired
correctly, not that its content is worth reading.

## Planned on This Branch

Per the [archive decision](../decisions/2026-08-24-archive-history-in-docs-tree.md),
`doctor` will additionally skip `docs/archive/**` when auditing notes and verify
that the active `.bmignore` carries the `archive/` exclusion — the boundary is
one conventional config line, and a lost line would otherwise silently pour
transcripts back into the graph.

## Observations

- [fact] `doctor` audits rendering-input placement and note health always, and indexer wiring when the `basic-memory` feature is enabled; the indexer config is read, never written.
- [fact] Errors produce a non-zero exit code, so the command can gate CI.
- [fact] `--fix` moves rendering inputs, restores titles and headings, strips indexer-stamped frontmatter, and prunes empty directories; it refuses renames and content edits.

## Relations

- relates_to [[DECISION: basic-memory-knowledge-tree-boundary]]
- relates_to [[The audit-knowledge-tree Skill: Judgment-Bearing Tree Repair]]
- localized counterpart of [[ai-sync doctor: детерминированный аудит дерева знаний]]
