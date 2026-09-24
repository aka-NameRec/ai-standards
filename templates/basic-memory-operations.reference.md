# Basic Memory Operations Reference

Operational detail of the basic-memory feature. The always-loaded
`Basic Memory Usage` rules carry the routing (knowledge layers, dedicated
tree, genres), the note-shape rule, and the sync-hygiene triggers; this
reference carries the mechanics. Read it when operating the knowledge tree —
creating or renaming notes, masking bulk data, repairing, or reindexing. If
this file is absent, the project has not run `ai-sync sync-templates`; proceed
with the always-loaded rules.

## Masking Bulk Data

- Store binary and bulk-data files (images, PDFs, raw logs, CSV dumps) outside
  the knowledge tree. While they must stay beside the notes citing them, mask
  them via a `.gitignore` at the knowledge-tree root (the indexer's project
  home) or the global `~/.basic-memory/.bmignore` — gitignore-style patterns
  with no `!` exceptions.
- Reindex only after `ai-sync doctor` stops reporting them.

## Permalinks And Legacy Flags

- Keep permalink generation enabled once the knowledge tree holds only notes:
  `memory://` addressing and graph traversal resolve through permalinks, and a
  project without them degrades to plain search.
- Treat `ensure_frontmatter_on_sync=false` together with
  `disable_permalinks=true` as a fallback for a legacy tree that cannot be
  narrowed yet, not as the default. Either flag alone still lets sync rewrite
  files that already carry frontmatter, and the pair gives up `memory://`
  addressing.

## Naming And Renames

- When a tool derives the file name from the title, rename the file afterwards
  instead of accepting a name that breaks the `YYYY-MM-DD-topic-slug.md`
  convention (canonical dated artifacts only).
- A rename keeps the note's permalink unless the indexer is configured to
  recompute it; decide which of the two matters before renaming in bulk.

## Repair Tooling

- `ai-sync doctor --fix` reports how the project is wired, applies the repairs
  that need no judgement — moving rendering inputs out of the tree, restoring
  missing frontmatter titles and headings, pruning empty directories — and
  leaves naming and content decisions to review.
- `bm orphans` lists notes with no relation in either direction; the schema
  commands (`infer`, `validate`, `diff`) cover per-type field contracts and
  drift.

## Reindex Matrix

- After mass file moves, renames, deletes, interrupted indexing, or
  indexing-configuration changes, run an explicit project reindex.
- Use a full reindex after changing project routing, indexed root paths,
  permalink behavior, or frontmatter-sync policy.
- If project status reports interrupted or incomplete embeddings, rebuild
  embeddings before treating semantic search as up to date.
- After `git pull`, `git merge`, `git rebase`, branch switches, or other VCS
  operations that may change indexed Markdown, check sync health before
  relying on retrieved context.
