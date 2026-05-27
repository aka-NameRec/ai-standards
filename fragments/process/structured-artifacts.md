## Lightweight Structured Artifacts
- For non-trivial changes, create a short change plan before implementation.
- Use lightweight artifacts to clarify scope, boundaries, invariants, dependencies, and verification.
- Keep artifact overhead proportional to the task; do not create process files for small local edits with obvious verification.
- Prefer short Markdown artifacts that are reviewable in Git over machine-oriented XML or deeply nested formats.

## Change Plans
- Create a change plan when the task involves architecture decisions, multiple dependent steps, migration risk, behavior changes across layers, or non-trivial verification.
- Keep the plan focused on goal, scope, touched modules, intended structure, risks, invariants, and verification.
- For long autonomous execution, add a short session envelope covering non-goals, architectural constraints, stop conditions, and expected review artifacts.
- Update the outcome section after implementation only when the original plan meaningfully guided the work.

## Module Contracts
- Treat a module as the smallest change unit for which one responsibility contract and one set of invariants can be stated clearly.
- Create `MODULE_CONTRACT.md` only for major, risky, shared, or architecturally non-obvious modules.
- Use the contract to state ownership, non-goals, inputs, outputs, dependencies, invariants, failure boundaries, and verification.
- Do not create a contract for every folder, CRUD endpoint, or thin wrapper by default.

## Decision Records
- Create a short decision record when an architectural or operational choice will matter for future changes and code review.
- Use decision records and module contracts for durable repository history.
- Use agent working memory for evolving context, temporary findings, and notes that are not yet accepted as canonical documentation.
- Keep one decision record focused on one choice, its rationale, alternatives, and consequences.
- Unless a project defines a stricter local convention, name files under `docs/decisions/**` and `docs/architecture/**` as `YYYY-MM-DD-<topic-slug>.md`.

## Canonical Documentation And Agent Working Memory
- Treat `docs/decisions/**`, `docs/architecture/**`, `MODULE_CONTRACT.md`, and equivalent local artifacts as canonical project knowledge.
- Treat `docs/ai-memory/**` as agent-managed working memory rather than canonical truth.
- Durable conclusions must be promoted from working memory into canonical documentation only on explicit user request.
- Working memory should link to canonical documents when they already exist instead of duplicating them.

## Canonical Documentation Write Policy
- Do not modify canonical documentation unless the user explicitly asks to record, update, reconcile, supersede, or remove durable project knowledge.
- Before modifying canonical documentation, search related decision records, architecture docs, module contracts, and agent working memory.
- Prefer updating an existing canonical document over creating a duplicate.
- If new knowledge contradicts existing canonical documentation, do not silently resolve the conflict unless the user has already made the decision in the current task.
- When a decision supersedes an older one, preserve the old document as historical context and add a clear supersession link.

## Optional Maps And Anchors
- Use `module-map.md` only for orchestration-heavy, integration-heavy, migration-prone, or repeatedly confusing modules.
- Do not require module maps for ordinary modules that are already understandable from code and tests.
- Allow local block anchors only for generated zones, temporary migration blocks, or patch-sensitive areas with a clear operational need.
- Do not standardize pervasive file-local semantic scaffolding or history comments across the codebase.

## Rejected Formalism
- Do not introduce XML-heavy planning artifacts, mandatory code graphs, or pseudo-XML knowledge overlays as shared standards.
- If a project truly needs heavier machine-oriented artifacts, opt into them with explicit local rules instead of promoting them into ai-standards.
