---
title: 'DECISION: problem-and-solution-space-notes'
permalink: ai-standards/decisions/2026-08-20-problem-and-solution-space-notes
---

# DECISION: problem-and-solution-space-notes

Russian localized version: [2026-08-20-problem-and-solution-space-notes.ru.md](2026-08-20-problem-and-solution-space-notes.ru.md)

## Status

Accepted

## Date

2026-08-20

## Context

The `basic-memory` feature standardized where knowledge lives and how it is indexed, but said nothing about what belongs in it. Two failure modes followed, both observed in practice.

Agents write a note per task. The habit reads as diligence and produces a graph whose entries have one reader — whoever wrote them — after which they rot and begin contradicting the code.

Agents also write notes that restate the code. `str(digit) converts a number to a string` is the shape of it: nobody can disagree with the statement, any reader of the line already knows it, and it becomes silently wrong the moment the line changes. Upstream guidance makes this worse rather than better, since it asks for substantive prose and one fact per observation without saying what does not belong.

A third problem sits underneath both. A document that mixes a business rule with the design serving it cannot be reviewed, because the halves answer to different authorities. Worse, an agent finding a mismatch between such a document and the code cannot tell which side is wrong, and defaults to updating the document — which makes the code the authority on how the business works.

## Decision

Knowledge notes are written in two genres, kept apart and linked rather than merged.

Problem-space knowledge is the business as it exists: its rules, its language, why a figure is computed the way it is. It is discovered rather than designed, it stays true whatever the code does, and a note carries its source — who stated the rule, which regulation or agreement, when it was confirmed. It has no alternatives, because nothing was chosen.

Solution-space knowledge is what the team chose to build and why. A note carries the options it rejected and the consequences it accepts, and it dies with the implementation it describes.

A decision `implements` the rule it serves, so the reasoning stays traversable from either side, and a rule with nothing implementing it is either unbuilt or dead.

The genres get separate directories rather than only a `type` in frontmatter: problem-space knowledge in `docs/domain/**`, solution-space knowledge in `docs/decisions/**` and `docs/architecture/**`. The path is what an agent sees before it opens a file, and the rule that the code is never the authority on problem-space knowledge has to hold at that moment. A tree with no `domain/` is not a violation — it is a project whose business rules are not written down yet.

Decisions are not split further among themselves: architectural, design, tooling, and policy decisions share one format, and significance decides whether a decision is worth recording rather than which category it falls into.

Three tests govern what is written at all. Prefer stable knowledge over volatile, since requirements outlive design decisions and a document mixing them inherits the shorter life. Assume the knowledge is already in the artifacts and make it explicit where it lives instead of restating it. State an observation only if someone could disagree with it.

A task, an issue, and a merge request are delivery vehicles whose history already lives in the tracker. They are not subjects, and most tasks therefore produce no documentation at all.

## Why

- the split tells an agent where the document wins and the code must be fixed instead, which no altitude rule alone can express
- different obligations per genre are checkable: a problem-space note without a source is a defect, and so is a decision without alternatives
- linking rather than merging keeps the connection explicit and traversable instead of held in someone's head
- the stable-versus-volatile axis explains why mixed documents feel perpetually stale, which is otherwise blamed on discipline
- naming the task as a non-subject removes the most common source of graph bloat at its root

## Alternatives Considered

### Keep one undifferentiated note format and rely on review

Rejected. Review catches an unsourced business rule only when a reviewer happens to know it is a business rule. Making the genre explicit turns that into a field that tooling can check.

### Split decisions by category, so domain decisions sit apart from architectural ones

Rejected, and this was the initial proposal. The MADR project generalized its own acronym from "Markdown Architectural Decision Record" to "Markdown Any Decision Record" precisely because the boundaries between decision categories are fuzzy and significance is the useful axis. The split worth making is between decisions and discovered facts, not among decisions.

### Write no content rules and let each project decide

Rejected. Both failure modes above appeared independently across projects using the feature, so the guidance is reusable rather than local.

## Consequences

### Benefits

- an agent can tell which documents it may reconcile with the code and which it may not
- per-genre obligations give the schema system something concrete to validate
- the volume of written documentation drops, since most tasks stop producing any
- the reasoning behind a rule and the design serving it stay connected through the graph

### Costs Or Tradeoffs

- existing documents that mix the genres have to be split, and the split is a judgement call
- none of these rules is mechanically checkable by the renderer; they rely on the model reading them and on review
- classifying a note as problem or solution space is occasionally genuinely ambiguous, and a mechanism implementing a business constraint has to be cut in two

## Affected Modules

- `fragments/tools/basic-memory.md`
- `scripts/ai_sync.py`
- `README.md`
- `README.ru.md`
- `templates/project_manifest.toml`
- `docs/basic-memory-usage.md`
- `docs/basic-memory-usage.ru.md`
- `templates/knowledge-tree/audit-knowledge-tree.SKILL.md`
- `templates/knowledge-tree/audit-knowledge-tree.claude.md`
- `templates/knowledge-tree/audit-knowledge-tree.cursor.mdc`
- `AGENTS.md`

## Invariants And Constraints

- a problem-space note carries its source; a solution-space note carries its rejected alternatives
- the code never becomes the authority on problem-space knowledge
- one source of truth per fact, referenced rather than copied
- decisions share a single format regardless of category
- delivery artifacts are never subjects of notes

## Verification

- the rendered `AGENTS.md` carries the two-genre rule and the tests that follow from it
- the usage guides exist in English and Russian with the same structure
- the audit skill classifies by genre and proposes splitting mixed documents

## Related Artifacts

- [../basic-memory-usage.md](../basic-memory-usage.md)
- [2026-08-20-basic-memory-knowledge-tree-boundary.md](2026-08-20-basic-memory-knowledge-tree-boundary.md)
- [2026-05-19-add-basic-memory-feature.md](2026-05-19-add-basic-memory-feature.md)