# DECISION: add-dry-review-pass

Russian localized version: [2026-08-21-add-dry-review-pass.ru.md](2026-08-21-add-dry-review-pass.ru.md)

## Status

Accepted

## Date

2026-08-21

## Context

The `review-lenses` feature states its first lens as "prefer existing project primitives, shared helpers, and imports over local duplication". That wording only looks outward, at code the project already has, and it silently excludes the most common way duplication actually enters a repository.

Two reviews made the gap concrete. In the first, one change added the same new request-parsing helper to two endpoint modules. Both copies were new, so neither was an existing primitive, the lens read as satisfied, and the duplication passed review. In the second, a repository-wide pass missed three byte-identical single-purpose files: reading follows the diff, the largest files, or the hot paths, and small stable clones sit outside all three while linters do not report cross-file duplication by default.

Neither miss was a lapse of attention. In both cases the rule as written did not describe the case being reviewed.

## Decision

`review-lenses` gains `DRY` as its own pass, a sibling of the lenses rather than a bullet inside `Reuse`.

The pass is defined by five rules: check the reviewed change for duplication it introduces itself; apply the check at every scope, down to a single small diff; count one intent expressed two different ways in sibling files as duplication; read the surrounding convention before extracting duplicated new code into a shared primitive, because deleting the wrapper on both sides is sometimes the correct fix; and run a clone detector, rather than more reading, once the scope grows to a whole module, package, or repository.

The `Reuse` lens keeps its outward-looking wording and gains a half-line pointing at the inward direction, so the two are related on the page without being merged.

The pass is propagated to the three `simplify-review` adapters (`SKILL.md`, `claude.md`, `cursor.mdc`), each in that file's own voice and density, following the convention already used for `Scope`, `Quality`, `Efficiency`, and `Verification` in those files. A new test asserts that a `DRY` section exists in the fragment and in all three adapters, so the propagation cannot silently lapse.

## Why

- the failure was the wording of a rule, not the diligence of the reviewer, so the fix belongs in the wording
- an inward check is cheapest exactly where it was missing: on a small diff, before anything depends on either copy
- separating the pass from `Reuse` keeps each rule describing one direction, which is what makes either of them checkable
- delegating the repository-scale scan to a clone detector keeps an unexecutable instruction out of always-on context
- guarding propagation with a structural test costs one test and removes a whole class of silent drift

## Alternatives Considered

### Extend the `Reuse` bullet instead of adding a pass

Rejected. The lens is one line, and the two directions do not compress into one line without losing the part that was being missed. A reviewer reading "prefer existing primitives over local duplication" does not derive "and check whether you just wrote the same thing twice" from it — that is precisely what happened twice.

### Add `dry-review` as a separate feature

Rejected. A duplication pass is not independently useful; nobody would enable it without a review workflow. It would also cost a registry entry, a manifest entry in two files, its own adapters, and its own usage-guide pair, to gate four rules.

### Put the pass in a shared fragment referenced by several features, with adapters pointing at `AGENTS.md`

Rejected for now, though the mechanism supports it: `_append_fragment_id` deduplicates, so one fragment listed under two features renders once, and `stacks/layered-architecture` already sets that precedent on the stack side. The blocker is the adapters. They are currently self-contained restatements of the whole workflow, not pointers into the rendered instructions, and turning one section into a pointer would change that convention for a single rule. Worth revisiting as its own decision if more shared passes appear.

### Specify the repository-scale scan as prose over normalized content

Rejected. "Compare content with identifiers, formatting, and comments removed, across the whole surface" describes what a clone detector does. As a prose instruction in always-on context it is either ignored or performed for show, and it costs seven lines in every session of every project that enables the feature. Naming the tool and requiring its output to be triaged is shorter and actually verifiable.

## Consequences

### Benefits

- duplication introduced by the change under review is now covered by a rule that describes it
- the check applies at the scope where it is cheapest, instead of being reserved for large passes
- the clone-detector rule sets an expectation that scales with scope rather than growing prose
- the adapters cannot lose the pass without failing a test

### Costs Or Tradeoffs

- four rule surfaces state the pass in four wordings; the test guards presence, not agreement
- the repository-scale rule assumes a clone detector is available, and names none, since the choice is stack-specific
- `review-lenses` grows by one section in always-on context

## Affected Modules

- `fragments/process/review-lenses.md`
- `templates/review-lenses/simplify-review.SKILL.md`
- `templates/review-lenses/simplify-review.claude.md`
- `templates/review-lenses/simplify-review.cursor.mdc`
- `docs/review-lenses-usage.md`
- `docs/review-lenses-usage.ru.md`
- `CHANGELOG.md`
- `tests/test_ai_sync.py`

## Invariants And Constraints

- `Reuse` describes the outward direction and `DRY` the inward one; neither absorbs the other
- the `DRY` pass applies at every scope, including a single small diff
- the fragment and all three `simplify-review` adapters carry a `DRY` section
- repository-scale duplication detection is delegated to a tool, not specified as prose
- duplication is reported with the smallest primitive that would replace it, never as a bare list of files
- extraction is not the default fix; the surrounding convention decides between promoting and deleting

## Verification

- rendering with `review-lenses` enabled includes the `DRY` section
- the fragment and the three adapter templates each contain a `DRY` section, asserted by test
- both usage guides describe the pass and the `Reuse` / `DRY` split
- `uv run pytest` passes

## Related Artifacts

- [../review-lenses-usage.md](../review-lenses-usage.md)
- [../review-lenses-usage.ru.md](../review-lenses-usage.ru.md)
- [../../fragments/process/review-lenses.md](../../fragments/process/review-lenses.md)
