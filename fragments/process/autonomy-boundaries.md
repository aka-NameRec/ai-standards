## Autonomy Boundaries
- Treat long autonomous execution as an exception, not the default mode of AI-assisted development.
- Allow long autonomous execution only when the design is already chosen, the scope is bounded, automated verification is strong, rollback is cheap, and the review remains cheaper than manual reimplementation.
- Keep critical task context outside the model's transient memory through explicit artifacts such as a task spec, change plan, decision record, module contract, or migration note.
- For long or high-risk execution, record a short session envelope with objective, scope, non-goals, architectural constraints, verification plan, stop conditions, and expected review artifacts.
- For a non-trivial autonomous slice, define one or more local checkpoints for the riskiest implementation points, not only the end-of-slice verification.
- Continue autonomously only while the next change still fits a small coherent patch with targeted verification for that patch.
- Stop and request review when local fixes stop converging inside the current slice, even if the high-level design direction has not changed.
- Stop when correctness depends on hidden or distributed reasoning that cannot be summarized around the changed fragment in a compact reviewable form.
- If a slice reveals new high-risk implementation hotspots that were not anticipated in the session envelope, either split the slice or request human confirmation before proceeding.

### Required Stop Conditions
- Stop and request human review when the task no longer fits the agreed design, scope, or invariants.
- Stop when a new abstraction, architectural layer, public contract change, integration strategy, or migration strategy becomes necessary.
- Stop when verification stops converging, logs or evidence contradict the design anchor, or repeated fixes start widening the scope.
- Stop when the blast radius grows materially beyond the declared scope or when rollback stops being cheap and predictable.
- Stop when the agent can no longer explain the architecture delta from the start of the task in a compact reviewable form.
- Stop when execution encounters a material design choice, contradictory requirements, widening scope, or evidence invalidating the agreed design: preserve the current state and request human direction rather than recording a new decision and continuing silently.

### Working State During Long Execution
- Long autonomous execution must periodically preserve externally reviewable task state at meaningful phase boundaries.
- Persisting task state does not authorize the agent to cross an existing autonomy boundary.
- Preserved state must be enough to resume from a fresh session without replaying the conversation, and compact enough to review before continuing.

### Sensitive Areas
- Do not make architecture, module-boundary, or cross-cutting refactor decisions autonomously during long execution.
- Do not make public API, schema, backward-compatibility, auth, authorization, secret-handling, or security-policy decisions autonomously during long execution.
- Do not perform destructive data changes, production operations, or other high-blast-radius actions without explicit human approval for that step.

### Review Output
- End long autonomous execution with a short summary of what changed, which checks ran, how the result still matches the design anchors, and which points still require human decision.
- If review would require the human to reverse-engineer hidden decisions from a large diff, autonomy has already gone too far and should have stopped earlier.
