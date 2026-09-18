<!--
Source provenance:
- Adopted on 2026-04-25 from a local workflow review of token-based agent usage.
- Adaptation goal: keep durable context-economy rules without encoding vendor-specific billing, model modes, or brittle numeric limits.
-->

## Agent Usage Hygiene
- Treat usage economy as context discipline, not as permission to reduce engineering quality.
- Prefer targeted discovery through search, diffs, logs, and focused file reads before loading broad context.
- Treat targeted retrieval as part of context discipline: consult the narrowest enabled knowledge source before re-reading broad or unchanged material.
- Keep task scope narrow enough that the next patch remains reviewable and verifiable.
- Use the most targeted verification that still proves the change; do not skip required verification to save usage.
- Avoid repeating large summaries or re-reading unchanged context when a compact reference or handoff summary is enough.

### Economy Mode Activation
- Enter economy mode only when the user explicitly asks to be economical, preserve limits, reduce token usage, minimize context, keep usage low, or similar.
- In economy mode, minimize broad exploration, long explanations, repeated summaries, and unnecessary file reads.
- If economy conflicts with correctness, safety, or required verification, state the conflict and prioritize correctness.
- End economy mode when the current task ends or when the user explicitly disables it.

### Economy Mode Behavior
- Start broad tasks by narrowing the scope or proposing a small reviewable slice.
- Prefer repository search, targeted commands, existing artifacts, and focused file reads over manual inspection of large file sets.
- Split work when the next change no longer fits a compact patch with targeted verification.
- Use compact handoff summaries when continuing in a long thread would make the context harder to review.
- Keep tool- or vendor-specific usage controls in local adapters or project overrides instead of this shared feature.
