<!--
Source provenance:
- Adopted on 2026-04-25 from a local workflow review of long chat risks.
- Adaptation goal: keep durable context-drift safeguards without encoding tool-specific context window behavior or brittle message-count limits.
-->

## Session Hygiene
- Warn the user when a long thread increases the risk of context drift, stale assumptions, goal substitution, or lost constraints.
- Before continuing a long session, produce a compact handoff summary with the current goal, decisions, touched files, risks, constraints, and next slice.
- Prefer starting a fresh chat when the work changes phase, the current context can no longer be summarized compactly, or the next slice depends on rules or decisions that should be reloaded explicitly.
- Do not rely on transient chat memory for critical constraints; move them into project artifacts, ConPort, or another durable memory mechanism.
- Re-read relevant project rules, active context, and task artifacts when a long session enters a new phase such as implementation, review, merge, or release.

### Long-Session Warning Triggers
- Warn when the agent notices repeated goal restatement, conflicting assumptions, stale decisions, or uncertainty about which constraints still apply.
- Warn when review would require reconstructing important decisions from a long conversation instead of from compact artifacts.
- Warn when the next step depends on old chat context that has not been captured in a task note, change plan, decision record, or active context entry.
- Avoid brittle numeric thresholds as shared defaults; projects may define local message, time, or token limits when they have evidence for them.

### Handoff Summary
- Keep handoff summaries short enough to paste into a new chat or task artifact.
- Include only current facts, accepted decisions, unresolved questions, verification status, and the recommended next bounded slice.
- Separate confirmed project state from assumptions or inferred context.
- Update durable memory only for decisions, progress, or lessons that should survive the session.
