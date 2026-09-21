---
title: 'Dogfooding: Rule Engineering on the code-review feature (issue #17)'
permalink: ai-standards/artifacts/2026-09-21-code-review-rule-engineering-dogfooding
---

# Dogfooding: Rule Engineering on the code-review feature (issue #17)

Status: complete (2026-09-21, branch `rules-change/17-rule-engineering`).
Phase 3 of the change plan
`docs/artifacts/2026-09-19-rule-engineering-change-plan.md`: Rule Engineering
applied to a real existing feature — the `code-review` fragment and the
`standard-code-review` skill.

## Method

The Rule Engineering flow (feature `rule-engineering`, rules `RE-001`–`RE-006`)
was applied to `fragments/process/code-review.md`: decomposition into atomic
normative behaviors, then the ambiguity (interpretation surface), uniqueness
(lexical / semantic / behavioral overlap), conflict/precedence, abstraction
level, portability, and observability checks. The result is mapped as
`RVW-001`–`RVW-032` in `rule_map.toml`, each with a one-line expected
observable behavior.

## Decomposition

32 atomic behaviors across the fragment's sections: activation and scope
(`RVW-001`–`RVW-003`), the five check passes plus pre-existing marking
(`RVW-004`–`RVW-009`), reportable-finding criteria (`RVW-010`–`RVW-014`),
report shape and content (`RVW-015`–`RVW-025`), the small-fix exception
(`RVW-026`–`RVW-028`), relationships to lenses/skill (`RVW-029`), and
normalization (`RVW-030`–`RVW-032`). The `standard-code-review` skill is
packaging (a superset entry point), not additional normative rules; its restated
lens rules are covered by the overlap findings below.

## Findings

- **Atomicity.** One borderline case kept intact: the Architecture & Conventions pass (`RVW-005`) packs contracts, decision records, the module map, and the `(no contract)` convention into one rule. Splitting it yields five micro-rules with one shared trigger and no independent violation modes; the pass is the unit reviewers execute. The Russian translation table rides `RVW-022` as a lookup appendix of the language rule, not a separate norm.
- **Ambiguity (interpretation surface).** Two deliberate judgment domains found: "realistic data volumes" (`RVW-007`) and the small-fix boundary as experienced before the `Fixing While Reviewing` lists resolve it. Both are genuine contextual-judgment territory; forcing them narrower would fake precision. No rewording required.
- **Uniqueness / overlap.** Three overlaps examined, none is duplication: (1) the first Report Shape bullet and the first Normalization bullet look lexically close but state two different norms — reproduce the shape (`RVW-015`) versus the shape has no other definition (`RVW-030`); (2) the Reuse pass (`RVW-006`) overlaps the two extra DRY rules the skill restates — the boundary and precedence are explicit in `RVW-029`, and the skill is packaging by design; (3) the report-language rule (`RVW-022`) and the `response-language-style` feature govern different objects (the report document vs chat replies).
- **Conflicts / precedence.** None. The reporting default (`RVW-003`) and the fixing exception (`RVW-026`–`RVW-028`) form an explicit carve-out, not a conflict; the report destination rule (`RVW-024`) defers to file saving only on request.
- **Portability.** No vendor or harness assumptions in the shared rules; `RVW-032` enforces the boundary, and the one harness-dependent input (the deployed report example file) has an explicit fallback (`RVW-015`).
- **Observability.** Every mapped rule has a formulatable outcome. Validation assignment: behavioral scenarios for the core (`CR-001` → `RVW-006`, `CR-002` → `RVW-014`/`RVW-015`/`RVW-019`, `CR-003` → `RVW-009`), policy-style static assertions for shape and normalization rules in later phases.

🔵 `fragments/process/code-review.md:1-13` — the HTML provenance comment renders into every enabling project's `AGENTS.md` (the renderer strips frontmatter, not HTML comments), putting source metadata into always-loaded context — violates: Context Placement (`RE-006`), left as-is: moving provenance into stripped frontmatter changes the renderer contract and needs its own decision; candidate follow-up for a later phase.

## Conclusion

No rule changes required: the fragment already satisfies the nine properties at pass level — expected, since it was normalized under the 2026-08-06 decision that anticipated several Rule Engineering demands (evidence rule, no-padding, fixed shape). Phase 3 delivers the decomposition, the `RVW-*` mapping, and the first three behavioral scenario contracts (`docs/scenarios/CR-001`–`CR-003`, both languages), wired to the map by policy tests.

## Verification

- `uv run pytest`: 132 passed (5 new map/scenario policy tests included); the 4 known pre-existing failures unrelated to this work.
- `uv run ruff check`, `uv run mypy scripts/` clean; render idempotent; `ai-sync doctor` zero errors.
- Scenario-map wiring enforced by tests: every `scenarios` reference in `rule_map.toml` resolves to a contract file with a localized pair.
