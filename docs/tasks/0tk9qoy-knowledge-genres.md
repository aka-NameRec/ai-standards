---
title: 'Knowledge Genres: Applying the Two-Genre Model'
permalink: ai-standards/tasks/0tk9qoy-knowledge-genres
---

# Knowledge Genres: Applying the Two-Genre Model

Task: `0tk9qoy` · Branch: `feature/0tk9ckw-archive-history-in-docs-tree` · 2026-08-24

Russian version: [0tk9qoy-knowledge-genres.ru.md](0tk9qoy-knowledge-genres.ru.md)

Related: [decision: problem-and-solution-space-notes](../decisions/2026-08-20-problem-and-solution-space-notes.md) · [0tk9qpd-ai-sync-doctor.md](0tk9qpd-ai-sync-doctor.md) · [0tk9qpt-audit-knowledge-tree.md](0tk9qpt-audit-knowledge-tree.md)

This document is written for both the agent and the human. It turns the two-genre
decision into a working method: what goes where, who writes it, and how to tell
the genres apart in practice.

## The Two Genres

**Problem-space knowledge** is the business as it exists: its rules, its
language, why a figure is computed the way it is. It is *discovered* — from
domain experts, regulations, agreements — never designed. It stays true whatever
the code does. Home: `docs/domain/**`.

**Solution-space knowledge** is what the team chose to build and why. It is
*chosen*, it carries rejected alternatives, and it dies with the implementation
it describes. Home: `docs/decisions/**` and `docs/architecture/**`.

The split is by directory, not by frontmatter `type`, on purpose: the path is
what a reader (human or agent) sees before opening the file, and the authority
rule must hold at that moment:

> If a `docs/domain/**` document disagrees with the code, **the code is wrong**.
> If a `docs/decisions/**` document disagrees with the code, either may be —
> the decision may be outdated, or the code may have drifted.

An agent that cannot tell which side wins will default to editing the document
to match the code, which silently makes the code the authority on how the
business works. The genre boundary is what prevents that.

## Who Writes What

**`docs/domain/**` — the human is the source; the agent is the scribe.**

- The human states the rule: in conversation, in a review, in a requirements
  document, in a regulation.
- The agent may capture it into a note **only** with its source recorded: who
  stated it, which document or agreement, when it was confirmed. A problem-space
  note without a source is a defect.
- The agent must **not** derive domain truth from the code. Reading the code and
  inferring "the business rounds sick leave up" produces a solution-space
  observation; it becomes domain knowledge only when a human or a verbatim
  source confirms it.
- Updates follow the same rule: when a rule changes, the note records the new
  source and date, not just the new text.

**`docs/decisions/**` — the agent drafts, the human decides.**

- The agent drafts the record: context, the chosen option, the rejected
  alternatives, the consequences. Alternatives are mandatory — a decision
  without them is a defect.
- The choice itself belongs to the human; the canonical-documentation write
  policy (explicit user request) applies.
- When a decision is superseded, it is marked and linked, not rewritten.

**Neither genre**: tasks, issues, merge requests, and per-session notes are
delivery vehicles, not subjects. Their history lives in the tracker. Most tasks
change how the product works, not what it is required to be, and therefore
produce no documentation at all. Historical chat exports live in
`docs/archive/**` (see the [archive decision](../decisions/2026-08-24-archive-history-in-docs-tree.md)).

## Entry Tests

Before writing any note, three gates:

1. **Stable over volatile.** Requirements and business rules outlive the designs
   that serve them. If a document would need editing after every refactor, the
   volatile half has leaked in — split it.
2. **Already in the artifacts.** Assume the knowledge exists in code, tracker,
   or prose; make explicit *where it lives* instead of restating it. Restating
   creates a second copy that will drift.
3. **The disagreement test.** State an observation only if someone could
   disagree with it. "`str(digit)` converts a number to a string" is a
   restatement; "numeric ids are serialized as strings because the external API
   rejects integers" is knowledge.

## Linking the Genres

The genres are linked, not merged:

- a decision `implements` the domain rule it serves — the reasoning is
  traversable from either side of the graph;
- a domain rule `derived_from` its verbatim source, when one exists;
- a rule with nothing implementing it is either unbuilt or dead — the link is
  what makes that visible.

## Common Cases

| Situation | Action |
|---|---|
| A business rule surfaces in chat | Confirm the source with the user, write a `docs/domain/**` note with source and date |
| The team makes a design choice | Draft a decision record with alternatives; link `implements` to the rule served |
| A note mixes a rule and its design | Split it: the rule keeps its source, the design keeps its alternatives; link the halves |
| An agent "discovers" a rule from code | It has not — confirm with a human or a verbatim source first |
| No `docs/domain/` exists | Not a violation: the project's business rules are simply not written down yet |
| A task finishes | Usually no note at all; durable content folds into the document owning the subject |

## Observations

- [fact] Problem-space knowledge in `docs/domain/**` is discovered from humans or verbatim sources; the agent records it only together with its source, and a note without one is a defect.
- [fact] An agent must not derive domain truth from the code; a code-derived statement becomes domain knowledge only after a human or a verbatim source confirms it.
- [fact] In `docs/decisions/**` the agent drafts the record and the human makes the choice; rejected alternatives are mandatory.
- [fact] A `docs/domain/**` document outranks the code, while a `docs/decisions/**` document does not.

## Relations

- relates_to [[DECISION: problem-and-solution-space-notes]]
- relates_to [[ai-sync doctor: Deterministic Knowledge-Tree Audit]]
- localized counterpart of [[Жанры знаний: применение двухжанровой модели]]
