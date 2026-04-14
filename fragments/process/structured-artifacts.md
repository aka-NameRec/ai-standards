## Lightweight Structured Artifacts
- For non-trivial changes, create a short change plan before implementation.
- Use lightweight artifacts to clarify scope, boundaries, invariants, dependencies, and verification.
- Keep artifact overhead proportional to the task; do not create process files for small local edits with obvious verification.
- Prefer short Markdown artifacts that are reviewable in Git over machine-oriented XML or deeply nested formats.

## Change Plans
- Create a change plan when the task involves architecture decisions, multiple dependent steps, migration risk, behavior changes across layers, or non-trivial verification.
- Keep the plan focused on goal, scope, touched modules, intended structure, risks, invariants, and verification.
- Update the outcome section after implementation only when the original plan meaningfully guided the work.

## Module Contracts
- Treat a module as the smallest change unit for which one responsibility contract and one set of invariants can be stated clearly.
- Create `MODULE_CONTRACT.md` only for major, risky, shared, or architecturally non-obvious modules.
- Use the contract to state ownership, non-goals, inputs, outputs, dependencies, invariants, failure boundaries, and verification.
- Do not create a contract for every folder, CRUD endpoint, or thin wrapper by default.

## Decision Records
- Create a short decision record when an architectural or operational choice will matter for future changes and code review.
- Use decision records for durable repository history; use ConPort for active context, progress, and evolving project memory.
- Keep one decision record focused on one choice, its rationale, alternatives, and consequences.

## Optional Maps And Anchors
- Use `module-map.md` only for orchestration-heavy, integration-heavy, migration-prone, or repeatedly confusing modules.
- Do not require module maps for ordinary modules that are already understandable from code and tests.
- Allow local block anchors only for generated zones, temporary migration blocks, or patch-sensitive areas with a clear operational need.
- Do not standardize pervasive file-local semantic scaffolding or history comments across the codebase.

## Rejected Formalism
- Do not introduce XML-heavy planning artifacts, mandatory code graphs, or pseudo-XML knowledge overlays as shared standards.
- If a project truly needs heavier machine-oriented artifacts, opt into them with explicit local rules instead of promoting them into ai-standards.
