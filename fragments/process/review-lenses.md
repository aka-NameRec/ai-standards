## Multi-Lens Review
- Use a multi-lens review pass when a task benefits from aggressive simplification, cleanup, or structural refactoring of recently changed code.
- Treat this feature as a review-and-refactor workflow, not as a default code-generation mode.
- Activate it after the initial implementation or when the user explicitly asks for simplification, cleanup, deduplication, or structural improvement.

### Review Lenses
- Reuse: prefer existing project primitives, shared helpers, and imports over local duplication, and catch duplication that the reviewed change introduces on its own.
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

### DRY
- Check the reviewed change for duplication it introduces itself, not only the surrounding code for primitives it failed to reuse. Two new copies added by a single change are the common case, and the "prefer existing primitives" framing does not describe it, because neither copy is an existing primitive yet.
- Apply this check at every scope, down to a single small diff, where duplication is also cheapest to remove because nothing depends on either copy yet.
- Treat one intent expressed two different ways in sibling files as duplication as well, such as a helper function in one module and an equivalent inline expression in the next; besides the copy, it establishes a second convention for a single decision.
- Before extracting duplicated new code into a shared primitive, check how the surrounding code solves the same problem: when the established convention is to inline the operation, deleting the wrapper is the correct fix rather than promoting it to a shared module.
- Run a clone detector over the reviewed surface when the scope is a whole module, package, or repository, and triage its output rather than relying on clones surfacing while reading; reading follows the diff, the largest files, and the hot paths, and small stable clones sit outside all three. Report each group by the smallest primitive that would replace it, and separate genuine clones from repetition a framework requires, such as routing entry points or generated code.

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
