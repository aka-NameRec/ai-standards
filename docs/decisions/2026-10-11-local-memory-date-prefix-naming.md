---
title: 'DECISION: local-memory-date-prefix-naming'
permalink: ai-standards/decisions/2026-10-11-local-memory-date-prefix-naming
---

# DECISION: local-memory-date-prefix-naming

Russian localized version: [2026-10-11-local-memory-date-prefix-naming.ru.md](2026-10-11-local-memory-date-prefix-naming.ru.md)

## Status

Accepted

## Date

2026-10-11

## Context

User issue #23 reported a real devcats case (2026-10-11): parallel agent
sessions created local notes under `docs/local/**` in three competing naming
conventions in one day — timestamp prefixes (`20261011-170555-…`), timestamp
plus topic, and topic-only or topic-with-suffix-date names — while canonical
dated artifacts in the same tree always follow `YYYY-MM-DD-<topic-slug>.md`.
Local working memory is browsed, sorted, and linked next to canonical
`docs/decisions/**`, so the notation split breaks date sorting, adds
syntactic noise, and ignites per-session disputes about the "right"
convention. The promotion path makes it worse: a local note moved into
canonical documentation had to be renamed, breaking human recognition of the
file.

Two existing rules explicitly exempted the local area from dated naming and
therefore conflicted with the candidate rule (the issue's own claim of "no
conflict" did not hold): the `project-memory` fragment's Note Shape clause
("dated file names … do not apply inside the local memory area") and the
`basic-memory` fragment's Note Shape clause ("living documents and working
memory do not" follow the canonical convention).

## Decision

1. Adopt one naming standard for the local memory area: every Markdown
   document an agent creates there is named `YYYY-MM-DD-<topic>.md` — exactly
   the notation of canonical dated artifacts. The date is the note's creation
   date; content updates never rename the note; a hygiene merge keeps the
   older date.
2. The target function is the promotion path: a local note whose name already
   follows the canonical notation moves into canonical documentation under
   the same file name, and cross-area name collisions stay rare.
3. The two conflicting clauses are narrowed in the same change set, not
   extended around: canonical-note *body* requirements (`## Observations`,
   `## Relations`, frontmatter shape) still do not apply inside the local
   area, but the date-prefix file naming now does.
4. `ai-sync doctor` reports `local-note-without-date-prefix` — a WARNING,
   never auto-fixed (the ai-sync module contract forbids note renames in
   `--fix`). Existing non-conforming notes migrate opportunistically during
   working-memory hygiene; no bulk migration is mandated.
5. The rule is traced as `PM-001` in `rule_map.toml` with the behavioral
   scenario contract `docs/scenarios/PM-001-local-note-date-prefix.md`
   (execution belongs to `ai-standards-evals`, issue #18).

## Why

- One notation shared with canonical dated artifacts removes the convention
  dispute by construction instead of arbitrating between three conventions.
- Preserving the file name across promotion keeps the human-facing identity
  of a note stable — the cost the devcats case actually paid.
- Report-only enforcement keeps legacy trees green in CI while the
  agent-side rule blocks the behavior where it originates.

## Alternatives Considered

### Keep the exemption, standardize only by local project rules

Rejected: the cockpit project already had to add a local override rule to fix
one notation — exactly the per-workspace duplication the standards exist to
prevent.

### Timestamp-prefix notation (`YYYYMMDD-HHMMSS-`)

Rejected: it sorts by name before the canonical notation only within the same
prefix style, carries noise digits no human reads back, and still differs
from the canonical artifact notation, so promotion would keep renaming files.

### Bulk migration of existing non-conforming notes

Rejected as a mandate: local memory is agent-managed working state, renames
regenerate Basic Memory permalinks, and the value of renaming an old note
rarely exceeds the churn. Doctor reports the misses; hygiene renames them
opportunistically.

## Consequences

### Benefits

- One naming notation across local and canonical dated artifacts; promotion
  preserves file names.
- Deterministic static validation (filename regex), a doctor warning, and a
  behavioral scenario give the rule three validation forms.
- Legacy trees keep passing CI: the finding is a warning.

### Trade-offs

- Enforcement is advisory for existing notes; a tree that ignores the report
  keeps its mixed names.
- Notes that legitimately predate the rule keep non-conforming names until
  hygiene touches them.

## Observations

- [decision] Local memory files follow the canonical date-prefix notation
  `YYYY-MM-DD-<topic>.md` so promotion into canonical documentation keeps the
  file name; the date is the note's creation date.
- [decision] Doctor reports `local-note-without-date-prefix` as a
  report-only warning; renaming stays outside `--fix` by the ai-sync module
  contract.
- [fact] Two existing clauses (project-memory Note Shape, basic-memory Note
  Shape) explicitly exempted local memory from dated naming and had to be
  narrowed — the issue's "no conflict" claim did not hold.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Module Contract: scripts/ai_sync.py]]
- relates_to [[Scenario PM-001: local note naming on create]]
- relates_to [[DECISION: non-note-data-file-doctor-policy]]
