---
description: Audit and repair a Basic Memory knowledge tree — misplaced rendering inputs, missing or inconsistent frontmatter, notes absent from the graph, and file names that break the project convention. Use when the user asks to check, audit, clean up, or migrate existing documentation.
argument-hint: [knowledge tree path or project name]
---

Audit the knowledge tree named in $ARGUMENTS (default: the project's `docs/`) and report what is wrong with it. Repair only what the user confirms, one file at a time — the tree holds canonical documentation, so editing a body is not a reversible formatting fix.

## 1. Collect Mechanical Findings

- `ai-sync doctor --project-root <path>` — misplaced `local_overrides`, indexed roots pointed at a repository instead of a knowledge tree, disabled permalinks, missing or mismatched frontmatter, file names against the convention, non-note data files (images, PDFs, raw logs, CSV dumps), notes with no observations or relations.
- `ai-sync doctor --project-root <path> --fix` — applies every finding marked `(fixable)`. Run it first; what remains needs a decision.
- `bm orphans -p <project>` — notes with no relation in either direction.
- `bm doctor` — file/database drift.

Use that output as the work list instead of walking the tree by hand.

## 2. Classify Each File

- **Problem-space note** — states a rule of the business; must carry its source. **Solution-space note** — states what the team chose; must carry rejected alternatives and consequences. A document mixing the two is split, and a relation links the halves.
- **Note** (either genre) — expects frontmatter `title`, matching `# H1`, observations, relations.
- **Rendering input** (listed in `local_overrides`) — must live outside the tree; no frontmatter needed.
- **Data file** (images, PDFs, raw logs, CSV dumps — anything not Markdown) — move out of the tree, or mask via a `.gitignore` at the tree root while notes cite it; never delete silently.
- **Generated output** (carries a generated-by marker) — must live outside the tree; never edit.
- **Verbatim source** (`type: spec`, transcripts, quoted requirements) — structure may be repaired, content must not.

## 3. Repair In This Order

1. Misplaced rendering input — move it out of the tree, update the manifest path.
2. Data file inside the tree — move it out, or mask it via a `.gitignore` at the tree root (`*.png`, `raw/` — no `!` negation). Never delete silently; reindex only after `ai-sync doctor` stops reporting it.
3. Missing or mismatched frontmatter — add `title`, align it with the `# H1`, set `type` to match the folder.
4. File name against convention — `move_note`, never a filesystem rename.
5. Missing relations — propose links to notes that already exist.
6. Missing observations — report the gap and propose wording only.

Prefer `edit_note` and `move_note` over direct file writes.

## Rewriting One Document

Repeat per file, with a confirmation each time; do not batch.

1. **Decide the genre first** — discovered from the business, or chosen by the team? A document that does both is split before anything else happens to it.
2. **Move it to the directory of its genre** with `move_note`, renaming to the convention in the same move. The slug is chosen by a person, never transliterated.
3. **Fix frontmatter for that genre** — `title` matching the heading, a source and confirmation date for problem space, a status for a decision.
4. **Leave the prose alone.** Compressing it into bullets destroys the reasoning; a verbatim source is untouched beyond frontmatter and heading.
5. **Add observations from the document's own text** — only claims someone could disagree with, and only ones the document already makes.
6. **Add relations to notes that exist** — `implements` from a decision to the rule it serves, `derived_from` from a rule to its source.
7. **Verify with `ai-sync doctor`.** What remains is a decision, not a defect.

## Limits

- Never synthesize observations: an observation is a claim about the domain, and paraphrasing prose into one invents statements nobody made.
- Never rewrite a verbatim source; repair its frontmatter and heading only.
- Never delete a note; archive it by moving it to a status folder.

Close with what was repaired, what was proposed and declined, and what was skipped and why.
