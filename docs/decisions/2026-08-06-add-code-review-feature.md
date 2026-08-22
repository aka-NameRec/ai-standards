# DECISION: add-code-review-feature

Russian localized version: [2026-08-06-add-code-review-feature.ru.md](2026-08-06-add-code-review-feature.ru.md)

## Status

Accepted

## Date

2026-08-06

## Context

A bare, unqualified "code review" chat request in a project bootstrapped from `ai-standards` needs to reliably run a review against the project's assembled rules, with the result reported in the same shape every time.

`ai-standards` already had `review-lenses`, but that feature is documented as explicit-activation policy: it expects a request naming the workflow, or a per-tool adapter such as the `simplify-review` skill. It also covers only a cleanup-oriented Reuse/Quality/Efficiency model, not correctness or conformance to the project's own architecture, error-handling, and stack rules.

No reusable rule combined a natural-language trigger with a report shape fixed across runs, tools, and models. The report additionally needs a tracked task reference when one exists, a short prose lead-in on what changed and how, per-finding severity and a cited violated rule grounded in a real file location, an explicit choice between chat output and a saved file, and full localization to the chat language.

## Decision

`ai-standards` adds `code-review` as an opt-in process feature (`fragments/process/code-review.md`, registered in `registry.toml`).

The feature separates two kinds of content, and that separation is the load-bearing part of this decision:

- **Reusable review standards, stated as rules.** What to check and in what priority; what makes a finding reportable (a concrete file location, a named violated rule, enough detail to act on, no invented rules, no padding); how to treat problems that predate the diff; default to reporting rather than editing.
- **The report shape, stated once as a worked example.** `templates/code-review-report.md` is a filled-in sample review that defines the sections, their order, the per-finding fields, and the severity markers. Prose constraints describing a format are replaced by the format itself. The file is deployed into each project that enables the feature, as `.ai-standards/code-review-report.md`, through the agent-agnostic `INFRA_TEMPLATES` channel that already serves `chroma` — so it needs no `tooling.agents` adapter and the fragment only has to point at it.

Around the example sit six short operating rules: severity markers (🔴 blocking, 🟡 should fix, 🔵 optional, ✅ fixed, with a `→ fixed:` or `→ left as-is:` tail written onto the finding's own line); full localization to the chat language with the wordless markers exempt; chat output by default and a file only on request; a later "resend the report" reclassifying findings already on record instead of re-reviewing from scratch; a task reference that prefers a full link over a bare id whenever the tracker base is knowable — from the session, the project's own rules, or a `tracker_url` entry under `[metadata]` in the manifest, which already renders into the generated file's header, so the host stays with the organisation using the standard rather than in this repository; and one report per repository when a task spans several of them, since each repository gets its own pull request.

The feature is included in the self-hosted manifest and the starter project manifest, and ships with bilingual usage documentation, so downstream projects adopt it through normal manifest composition without any tool-specific setup.

## Why

- closes the gap with an addition that fits the existing manifest/registry/fragment architecture rather than a tool-specific hack
- keeps the trigger and the report shape tool-neutral by living in the rendered `AGENTS.md`/`CLAUDE.md`, so every tool that reads that file behaves the same and no `tooling.agents` adapter is needed
- keeps the format load-bearing but cheap to own: one worked example instead of a specification restated in several documents
- leaves `review-lenses` untouched, so projects that use only cleanup passes see no behavior change

## Alternatives Considered

### Fold the trigger into `review-lenses`

Rejected. Three downstream projects use `review-lenses` without `code-review`; merging would hand them a natural-language auto-trigger and a mandatory report shape nobody asked for there, silently changing a documented contract on their next render. The duplication actually worth removing was the format being restated in several files inside `code-review`, not the existence of two features — merging would have fixed the wrong duplication.

### Ship a Claude-specific auto-invoked Skill instead of an `AGENTS.md` rule

Rejected as the primary mechanism. A skill only reaches tools that have a skill mechanism, and it requires `tooling.agents` entries that downstream manifests mostly leave empty; tools that read only `AGENTS.md` would lose the feature. A skill remains a reasonable future addition for context economy, but the rule has to work without one.

### Leave the format to project-local overrides

Rejected. The repository's own guidance sends single-project rules to local overrides, but this format is wanted by every project in the organization; distributing it across per-project overrides would recreate exactly the duplication this repository exists to remove.

### Specify the format with prose constraints instead of a worked example

Rejected after the constraint-based version grew to roughly forty lines of imperatives ("always this section order", "never open with findings", "state None found.") and still left gaps. It was revised repeatedly, and because the same specification was restated in the fragment, both usage guides, and both decision records, every wording change cost five synchronized edits and twice broke the test. Public prompting guidance for review agents also reports that a worked example outperforms zero-shot constraints. The example is now the single source of truth.

### Inline the worked example in the fragment

Rejected once the deployment path was clear. Inlining costs about twenty-six lines of always-on context in every session of every project that enables the feature, and buys nothing that deployment does not: `INFRA_TEMPLATES` is gated on the feature alone, so the file lands without any adapter declaration. Deployment does introduce two failure modes, and both are handled rather than ignored — a project that has not run `sync-templates` would leave the pointer dangling, so the fragment carries a short fallback ordering and an instruction to say the file is missing; and a locally edited copy is skipped by the sync as unmanaged, which is recorded below as an accepted drift risk.

### Blanket-suppress issues found outside the diff

Rejected as too blunt. Silently dropping every out-of-scope finding — the initial normalization of the Codex/Cloudflare "don't blame the diff" guidance — throws away real signal the reviewer already has. Surfacing it with a `(pre-existing)` label keeps the signal without blaming the current change, and an explicit scope narrowing switches it off.

## Consequences

### Benefits

- a bare "code review" request behaves consistently across sessions, tools, and models
- the format is defined in one place, so changing it is a single-file edit
- no tool-specific adapter or setup is required
- composes cleanly with `review-lenses`, which keeps its own activation and scope

### Costs Or Tradeoffs

- another process feature and usage-guide pair to maintain
- the report shape is a separate deployed file, so enabling the feature now needs `ai-sync sync-templates` in addition to `render`; the fragment degrades to a fallback ordering when that step is missed
- a project can edit its deployed copy, which the sync then skips as unmanaged; that allows deliberate local customization at the price of silent drift from the shared shape
- downstream projects must opt in through their manifest; nothing in the rendering pipeline forces adoption

## Affected Modules

- `registry.toml`
- `fragments/process/code-review.md`
- `README.md`
- `README.ru.md`
- `docs/code-review-usage.md`
- `docs/code-review-usage.ru.md`
- `ai.project.toml`
- `templates/project_manifest.toml`
- `templates/code-review-report.md`
- `scripts/ai_sync.py`
- `AGENTS.md`
- `tests/test_ai_sync.py`

## Invariants And Constraints

- the report shape is defined by `templates/code-review-report.md` and nowhere else. Exactly two places enumerate the full section list, both in the fragment and both unavoidable: the fallback ordering for a project that never synced the template, and the localization mapping. A rule may address a single section by name; no file outside the fragment may enumerate the shape
- reporting is the default; editing code requires an explicit user request
- a finding without a concrete file location or without a mapped rule must not be reported
- a task reference is never invented; the line is omitted when none is known, and a URL is emitted only when its base is actually knowable
- a multi-repository change never produces a single combined report; one report per repository, because one report goes into one pull request
- a pre-existing issue is surfaced and labelled, not silently dropped, unless the user narrowed scope
- ✅ marks only genuinely fixed findings; one left alone deliberately keeps its coloured marker
- the whole report follows one language per session; the wordless markers are the only exception
- the default file-save path must not silently promote a report into canonical documentation
- the feature must stay tool-neutral and must not change `review-lenses` activation or scope

## Verification

- `registry.toml` exposes the `code-review` feature
- rendering with `code-review` enabled includes the fragment, its activation rule, and the pointer to `.ai-standards/code-review-report.md`
- `sync-templates` deploys the report template to a project that enables `code-review` even with no `tooling.agents` declared, and skips it when the feature is off
- usage guides exist in English and Russian and do not restate the format
- README documents the feature in both languages
- self-hosted `AGENTS.md` renders successfully with the feature enabled

## Related Artifacts

- [../code-review-usage.md](../code-review-usage.md)
- [../code-review-usage.ru.md](../code-review-usage.ru.md)
- [../../fragments/process/code-review.md](../../fragments/process/code-review.md)
- [../../fragments/process/review-lenses.md](../../fragments/process/review-lenses.md)
- [../../templates/code-review-report.md](../../templates/code-review-report.md)
- [../../ai.project.toml](../../ai.project.toml)

## Research Sources

- [Custom Code Review rules for Codex — OpenAI Developers](https://developers.openai.com/blog/custom-code-review-rules-for-codex)
- [OpenAI Codex PR review agent system prompt (gist)](https://gist.github.com/cbh123/ce4893a10ed2b87a89d9114b08118a08)
- [Orchestrating AI Code Review at scale — Cloudflare Blog](https://blog.cloudflare.com/ai-code-review/)
- [5 Prompt Patterns for AI-Assisted Code Review — SurePrompts](https://sureprompts.com/blog/prompt-patterns-code-review)
- [Code review comments are the rules you forgot to write down — Marco Gomiero](https://www.marcogomiero.com/posts/2026/code-review-agents-update/)
