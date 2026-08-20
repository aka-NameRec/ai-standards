---
name: audit-knowledge-tree
description: Audit and repair a Basic Memory knowledge tree — misplaced rendering inputs, missing or inconsistent frontmatter, notes absent from the graph, and file names that break the project convention. Use when the user asks to check, audit, clean up, or migrate existing documentation.
disable-model-invocation: true
---

# Audit Knowledge Tree

Bring an existing documentation tree in line with the knowledge-tree rules. Legacy trees predate the rules, so expect real content problems rather than formatting noise.

## Default Mode Is Diagnosis

Report first, repair only on explicit confirmation, one file at a time.

Moving a note between folders is cheap and reversible. Editing its body is not: the knowledge tree holds canonical documentation, and the project's own write policy reserves those edits for an explicit user request. Never batch-repair a tree because the report looked long.

## 1. Collect Mechanical Findings

Run the deterministic pass before reading anything:

```bash
ai-sync doctor --project-root <path>          # report
ai-sync doctor --project-root <path> --fix    # apply what needs no judgement
```

It reports misplaced `local_overrides`, indexed roots pointed at a repository instead of a knowledge tree, disabled permalinks, missing or mismatched frontmatter, file names against the convention, and notes with no observations or relations. Findings marked `(fixable)` are repaired by `--fix`: rendering inputs move out of the tree and the manifest is repointed, missing frontmatter titles and headings are restored, empty directories are pruned.

Run `--fix` first, then work the remainder. Everything left needs a decision, which is why it was left. Take that list as the work list instead of walking the tree by hand.

Add graph-level findings the renderer cannot see:

```bash
bm orphans -p <project>    # notes with no relation in either direction
bm doctor                  # file/database drift
```

## 2. Classify Each File

Decide what the file is before deciding what is wrong with it:

| Kind | Signal | Expectation |
|------|--------|-------------|
| Problem-space note | states a rule of the business | a source: who stated it, which regulation or agreement, when confirmed |
| Solution-space note | states what the team chose | the alternatives rejected and the consequences accepted |
| Note (either genre) | lives in the knowledge tree | frontmatter `title`, matching `# H1`, observations, relations |
| Rendering input | listed in `local_overrides` | must live outside the tree; no frontmatter needed |
| Generated output | carries a generated-by marker | must live outside the tree; never edit |
| Verbatim source | `type: spec`, transcripts, quoted requirements | structure may be repaired, content must not |

## 3. Repair

Work through the findings in this order, confirming each change:

- **Misplaced rendering input** — move it out of the tree and update the manifest path. Highest value: it protects generated files.
- **Missing or mismatched frontmatter** — add `title`, align it with the `# H1`, set `type` to match the folder.
- **File name against convention** — use `move_note`, never a filesystem rename: it moves the file and updates the index together.
- **Missing relations** — propose links to notes that already exist; a forward reference to a note that does not exist yet is valid and resolves on creation.
- **Missing observations** — see the limit below.
- **Note that mixes the genres** — a business rule and the design that serves it in one document. Split it: the rule keeps its source, the design keeps its alternatives, and a relation links them. Mixed documents cannot be reviewed, because the two halves answer to different authorities.
- **Note that documents a task rather than a subject** — a per-task, per-merge-request or per-session entry. Its durable content, if any, belongs in the document that owns the subject. Propose folding it in and retiring the entry, rather than leaving two places to maintain.

Prefer `edit_note` and `move_note` over direct file writes, so the index never drifts from disk.

## Limits

**Do not synthesize observations.** An observation is a claim about the domain. Paraphrasing prose into `- [decision] ...` produces confident statements nobody made. Report the gap, propose wording, and let the author accept it.

**Flag noise as well as gaps.** An observation that restates what the code plainly says is a maintenance cost with no reader. Propose retiring it, applying the same test in reverse: could anyone disagree with this, and would it survive the next refactor?

**Respect verbatim sources.** A transcript or a quoted requirement is evidence. Repair its frontmatter and heading if needed, never its body. When a project marks such files, honour the marker.

**Do not delete.** Archive by moving to a folder that records the status; deletion drops the note's observations and relations from the graph.

## 4. Report

State what was repaired, what was proposed and declined, and what was skipped and why. A finding left alone on purpose is a result, not an omission.
