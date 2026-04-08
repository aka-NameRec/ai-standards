## Multi-Lens Review
- Use a multi-lens review pass when a task benefits from aggressive simplification, cleanup, or structural refactoring of recently changed code.
- Treat this feature as a review-and-refactor workflow, not as a default code-generation mode.
- Activate it after the initial implementation or when the user explicitly asks for simplification, cleanup, deduplication, or structural improvement.

### Review Lenses
- Reuse: prefer existing project primitives, shared helpers, and imports over local duplication.
- Quality: preserve readability, stable contracts, type safety, and structural clarity.
- Efficiency: remove noise, dead weight, and avoidable verbosity when readability is not harmed.

### Orchestration
- Run the Reuse, Quality, and Efficiency lenses as separate review passes when the task is large enough to justify it.
- Synthesize their findings explicitly instead of blending them into one vague review.
- Resolve conflicts with this default priority:
  - Quality over Efficiency when safety, readability, or correctness is at risk.
  - Reuse over Efficiency when an existing shared primitive replaces local code cleanly.
  - Reuse over local novelty when a mature project abstraction already exists.
- Before applying aggressive simplifications, state the intended gains and the boundaries that must not change.

### Verification
- After merging the review findings, verify that no behavior, contract, or edge-case handling was silently removed.
- Preserve public API signatures unless the user explicitly requested a breaking change.
- Reject brevity that weakens typing, observability, or maintainability.
- Prefer reporting concrete structural gains such as reduced duplication, lower nesting, or simpler control flow.

### Normalization Rules
- Do not encode tool- or vendor-specific internal implementation claims as project rules unless they are publicly documented and durable.
- Keep numeric heuristics as local guidance or stack-specific overrides unless they are validated across multiple projects.
- Put framework-specific review heuristics into the relevant stack fragment instead of this shared feature.
- When adopting review logic from an external source, preserve the orchestration pattern and constraints, but normalize the heuristics into repository-neutral instructions.
