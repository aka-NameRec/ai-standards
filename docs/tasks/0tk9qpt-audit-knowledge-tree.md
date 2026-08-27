---
title: 'The audit-knowledge-tree Skill: Judgment-Bearing Tree Repair'
permalink: ai-standards/tasks/0tk9qpt-audit-knowledge-tree
---

# The audit-knowledge-tree Skill: Judgment-Bearing Tree Repair

Task: `0tk9qpt` · Branch: `feature/0tk9ckw-archive-history-in-docs-tree` · 2026-08-24

Russian version: [0tk9qpt-audit-knowledge-tree.ru.md](0tk9qpt-audit-knowledge-tree.ru.md)

Related: [0tk9qpd-ai-sync-doctor.md](0tk9qpd-ai-sync-doctor.md) · [0tk9qoy-knowledge-genres.md](0tk9qoy-knowledge-genres.md)

## Why It Exists

`ai-sync doctor` detects what needs no judgement and repairs what follows from
a rule. Everything left — classifying what a file *is*, choosing a meaningful
slug, splitting a document that mixes a business rule with its design, deciding
that a note is noise — needs a reader. The `audit-knowledge-tree` skill is that
reader. The split is deliberate: the deterministic half gates CI, the judgment
half asks a human before each edit, and neither pretends to be the other.

The skill ships as a feature-gated template (`basic-memory` feature) in four
agent adapters (codex/kilo `SKILL.md`, `claude.md`, `cursor.mdc`), so every
supported agent environment gets the same workflow.

## What It Does

**1. Collect.** Run `ai-sync doctor` (then `--fix`) first and take the
remainder as the work list. Add graph-level findings the renderer cannot see:
`bm orphans` (notes with no relation in either direction) and `bm doctor`
(file/database drift).

**2. Classify.** Decide what each file *is* before deciding what is wrong with
it: problem-space note (expects a source), solution-space note (expects
rejected alternatives), rendering input (must live outside the tree), generated
output (never edit), verbatim source (structure repairable, content untouchable).

**3. Repair, one file at a time, each with confirmation.** In order:
misplaced rendering inputs first (highest value — they protect generated
files), then frontmatter, then names — via `move_note`, never a filesystem
rename, so the index follows. Missing relations are proposed to existing notes;
a forward reference is valid, inventing the target note is not.

**Rewriting one document** follows seven steps: decide the genre before touching
anything; move to the directory of its genre; fix frontmatter for that genre;
leave the prose alone; add observations only from the document's own text; add
relations to notes that exist; verify with `ai-sync doctor`.

## Hard Limits

- **Do not synthesize observations.** Paraphrasing prose into `- [decision] ...`
  produces confident statements nobody made. Report the gap, propose wording,
  let the author accept it.
- **Do not rewrite verbatim sources.** Transcripts and quoted requirements are
  evidence; repair frontmatter and heading, never the body.
- **Do not delete.** Deletion drops observations and relations from the graph;
  archive by moving instead.
- **Flag noise as well as gaps.** An observation restating what the code plainly
  says is a maintenance cost with no reader; propose retiring it.
- **Never batch-repair.** The tree holds canonical documentation; the write
  policy reserves content edits for explicit requests, one file at a time.

## When to Invoke It

The skill is manual-only (`disable-model-invocation: true`) — the agent does not
start it on its own. Invoke when the user asks to check, audit, clean up, or
migrate existing documentation, or when `doctor` leaves findings that are
decisions rather than defects. Run it on a cadence (the basic-memory rules say
knowledge hygiene is periodic, not per-session) and when migrating a legacy tree
that predates the rules: expect real content problems there, not formatting
noise.

Typical pairing: `doctor` in CI keeps the wiring honest; the skill runs when
its report stops converging or when a human wants the tree's *content* reviewed.

## Reporting

The skill ends by stating what was repaired, what was proposed and declined,
and what was skipped and why. A finding deliberately left alone is a result,
not an omission.

## Observations

- [fact] The skill takes the `doctor` remainder as its work list and adds graph-level findings from `bm orphans` and `bm doctor`.
- [fact] Repair proceeds one file at a time with per-file confirmation, and batch repair is forbidden.
- [fact] The skill must not synthesize observations, rewrite verbatim sources, or delete notes.

## Relations

- relates_to [[DECISION: basic-memory-knowledge-tree-boundary]]
- relates_to [[ai-sync doctor: Deterministic Knowledge-Tree Audit]]
- localized counterpart of [[Скилл audit-knowledge-tree: ремонт дерева знаний, требующий суждения]]
