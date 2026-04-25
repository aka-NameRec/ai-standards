# DECISION: add-session-hygiene-feature

Russian localized version: [2026-04-25-add-session-hygiene-feature.ru.md](2026-04-25-add-session-hygiene-feature.ru.md)

## Status

Accepted

## Date

2026-04-25

## Context

Long chat sessions can accumulate context drift, stale assumptions, goal substitution, and hidden decisions. These risks are related to agent autonomy and usage economy, but they are not the same concern.

Existing process features covered adjacent problems:

- `autonomy-boundaries` defines stop conditions for long autonomous execution.
- `structured-artifacts` externalizes plans, contracts, and decisions.
- `conport` can preserve durable project memory across sessions.
- `agent-usage-hygiene` reduces avoidable context and usage waste.

The repository still needed a clean, reusable policy for warning about long-session risk, creating handoff summaries, and recommending a fresh chat when the active thread becomes less reliable than explicit artifacts.

## Decision

`ai-standards` adds `session-hygiene` as an opt-in process feature.

The feature defines:

- long-session warnings for context drift, stale assumptions, goal substitution, and lost constraints
- compact handoff summaries before continuing risky long sessions
- fresh-chat recommendations at phase boundaries or when context can no longer be summarized compactly
- re-reading relevant project rules, active context, and task artifacts when work enters a new phase
- durable memory and project artifacts as the home for critical constraints

The feature is included in the self-hosted manifest and starter project manifest so downstream projects can opt into it through normal manifest composition.

## Why

- separates session reliability from usage economy and autonomy governance
- gives agents a durable way to warn users before context drift becomes a correctness problem
- encourages compact handoffs instead of full transcript summaries
- preserves tool-neutrality by avoiding context-window or message-count assumptions
- strengthens continuity across fresh chats without requiring one specific artifact format

## Alternatives Considered

### Fold the policy into `autonomy-boundaries`

Rejected because session hygiene also applies to collaborative, non-autonomous, and review-only conversations. It is broader than long autonomous execution.

### Fold the policy into `agent-usage-hygiene`

Rejected because context reliability and usage economy have different priorities. A fresh chat can improve reliability even when token usage is not the main concern.

### Standardize hard message or token thresholds

Rejected because these limits are tool-specific and change over time. Projects may define local thresholds when they have evidence for them.

## Consequences

### Benefits

- downstream projects can opt into explicit long-session safeguards
- agents can recommend fresh chats without treating that as a failure
- handoff summaries become a standard reviewable bridge between sessions
- critical constraints are less likely to remain trapped in transient chat memory

### Costs Or Tradeoffs

- the repository carries another process feature and usage guide pair
- agents need judgment to avoid over-warning on ordinary medium-length chats
- projects with strict local chat limits may still need overrides

## Affected Modules

- `registry.toml`
- `fragments/process/session-hygiene.md`
- `README.md`
- `README.ru.md`
- `docs/session-hygiene-usage.md`
- `docs/session-hygiene-usage.ru.md`
- `ai.project.toml`
- `templates/project_manifest.toml`
- `AGENTS.md`
- `tests/test_ai_sync.py`

## Invariants And Constraints

- critical constraints must not live only in transient chat memory
- handoff summaries must be compact and reviewable
- confirmed state must be separated from assumptions and inferred context
- shared standards must avoid brittle numeric thresholds
- reloading rules should be targeted to the next slice, not broad context loading by default

## Verification

- `registry.toml` exposes the `session-hygiene` feature
- the rendered output includes the new process fragment when the feature is enabled
- usage guides exist in English and Russian
- README documents the feature in both languages
- self-hosted `AGENTS.md` renders successfully with the new feature enabled

## Related Artifacts

- [../session-hygiene-usage.md](../session-hygiene-usage.md)
- [../session-hygiene-usage.ru.md](../session-hygiene-usage.ru.md)
- [../../fragments/process/session-hygiene.md](../../fragments/process/session-hygiene.md)
- [../../ai.project.toml](../../ai.project.toml)
