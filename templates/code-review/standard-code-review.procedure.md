# Code Review Procedure

Full pass-by-pass procedure for the standard code review workflow (the
`standard-code-review` skill). The always-loaded `Code Review` rules carry the
reporting invariants (evidence, no-padding, marker semantics, report shape);
this reference carries the detail of each pass and the fixing policy. When
this file is present in the deployed skill, follow it instead of
reconstructing the passes from the section names.

## Passes

### Correctness

Logic errors first: missed edge cases, and failure paths that ignore the
`Error Handling` rules in force in the project. Read the changed conditions
and their boundaries against the behavior the surrounding code and tests
imply.

### Architecture & Conventions

Violations of the project's architecture rules and of any active stack
fragments. Check the changed modules against their active module contracts
(records under `docs/architecture/**` marked `type: module-contract` in the
frontmatter; a root-level `MODULE_CONTRACT.md` is a legacy form still worth
reading — ownership, non-goals, invariants), against accepted decision records
under `docs/architecture/**`, and against the module map when one exists; a
violation cites the exact contract clause it breaks. A changed major module
with no contract is reported as a `(no contract)` note — a gap to fill, not a
defect.

### Reuse

Code that should have reused an existing project primitive, and duplication
the change introduces on its own. Two new copies added by one change satisfy
"prefer existing primitives", because neither copy is an existing primitive,
and are duplication all the same; so is one intent expressed two different
ways in sibling files.

### Efficiency

Avoidable cost, such as repeated queries, per-row or per-render work that
could be hoisted, and client-side handling of something the server should do.
Judge it against realistic data volumes and say when the cost is currently
free.

### Quality

Readability, contract stability, test coverage of edge cases, and traps that
only surface in production.

## Pre-existing Problems

Report a notable problem that predates the diff as well, marked
`(pre-existing)` so it does not read as blame for this change. Whether to fix
it stays the author's call; it can be offered as a follow-up instead, and it
must not expand into an unrequested audit of the surrounding code.

## Finding Reportability

- It cites a concrete file, and a line when one is available. No location, no
  finding.
- It names the specific rule or requirement it violates. If nothing maps, say
  so instead of inventing a rule.
- It was checked against the code, not against the diff. Before writing that
  something duplicates `X` or reuses `Y`, open `X` and `Y`; before writing
  about a query pattern, a migration risk, or a uniqueness constraint, open
  the model and the configuration. An unverified claim is either verified or
  not written.
- It is detailed enough that another agent could apply the fix without asking
  a clarifying question.
- Prefer fewer, high-confidence findings. An honestly empty section, stated
  as "None found.", beats a manufactured nitpick, and a risky suggestion is
  reported rather than guessed at.

## Fixing While Reviewing

- Reporting stays the default. The one exception is a small fix whose safety
  can be established by reading alone, without running anything: make it, and
  record it as a ✅ finding with a `→ fixed:` tail like any other.
- Safe to fix without asking: wrong or missing translations, typos in
  user-facing strings and comments, a defensive tightening that cannot change
  behaviour on current data, a missing `.gitignore` entry for generated junk,
  and plain inconsistencies with the surrounding code such as the wrong import
  or the wrong constant.
- Report instead of fixing: anything touching migrations, lock files,
  dependencies, or build configuration; changes to public types and contracts
  other code depends on; refactors, however obviously correct, because that is
  the author's decision and not a defect; the state of the git index; and
  anything whose safety would need a test run to establish.
- Review first, then fix, then write the report, so the report describes the
  state after the fixes. List the fixes in the chat as well, separately from
  the report, so they can be reviewed on their own.
