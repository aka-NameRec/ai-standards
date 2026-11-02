---
title: 'DECISION: add-agents-md-progressive-disclosure'
permalink: ai-standards/decisions/2026-11-02-add-agents-md-progressive-disclosure
---

# DECISION: add-agents-md-progressive-disclosure

Russian localized version: [2026-11-02-add-agents-md-progressive-disclosure.ru.md](2026-11-02-add-agents-md-progressive-disclosure.ru.md)

## Status

Accepted

## Date

2026-11-02

## Context

Downstream users order multiple features and stacks from the manifest, and the rendered `AGENTS.md` grows past what Codex loads. Codex bounds all project instruction content with `project_doc_max_bytes` (default 32 768 bytes) summed across every `AGENTS.md` on the project-root-to-cwd chain, and silently truncates whatever exceeds the budget — the tail of the rules is dropped with no warning to the user. Kilo and omp have no hard limit, but both load the file eagerly, so the surplus sits in the system prompt of every session.

Measured with real `ai-sync render` runs: a light order (core + one stack + one feature) renders to 6.8K; a mid order (nine features + python + django) to 42.8K; a heavy order (seventeen features + eleven stack fragments) to 70.7K; the self-hosted manifest renders to 56.8K. In the heavy render, process/tool features weigh 47.2K and stack fragments 18.8K, so no single category owns the problem.

The repository already ships the two ingredients this decision builds on: `INFRA_TEMPLATES` deploys feature-gated managed files into `.ai-standards/references/` through `sync-templates`, and several fragments already carry `### Reference` sections pointing at those files. The `ai-sync` module contract forbids generating content beyond assembling existing fragments, overrides, and templates, so any inline replacement for moved-out content must itself be declared, authored content.

## Decision

`ai-standards` adds a reference disclosure mode (progressive disclosure) for stacks and heavyweight features.

- **Manifest surface.** Two new optional lists in `ai.project.toml`: `reference_features` and `reference_stacks`. `registry.toml` carries the capability metadata. Unknown names are rejected at load, like unknown features today. A manifest without the new keys renders byte-for-byte as before.
- **Pointer blocks.** For every item in reference mode the renderer emits a compact authored block (~300 bytes) instead of the fragment: a heading, one or two imperative trigger rules naming when the full rules apply, the reference path, and two or three critical invariants. Pointer blocks are authored next to their fragments as declared content — the renderer only assembles them, per the module contract.
- **Deployment.** `sync-templates` deploys the full fragment text as `.ai-standards/references/stacks/<name>.md` and `.ai-standards/references/features/<name>.md`, gated by the same manifest flag, carrying the managed marker. The fragment remains the single source of truth; nothing is duplicated by hand.
- **Composition.** Inline (behavioral core): `core/*`, response-language-style, retrieval-routing, design-first-collaboration, reasoning-hygiene, autonomy-boundaries, structured-artifacts, module-contract-gate, session-hygiene, agent-usage-hygiene. Reference mode: all stacks, plus code-review, basic-memory, project-memory, chroma, rule-engineering (which covers skill-engineering), review-lenses, knowledge-capture, and context-architecture. context-architecture goes to reference mode rather than a skill because skill activation is agent-dependent and unverified on Codex and omp, while pointer-plus-read is deterministic everywhere agents can read files; moving it into a skill later stays cheap because `rule_map.toml` already anchors rules through `source`.
- **Budget warning.** `render` and `check` emit a non-fatal warning when the rendered file exceeds 32 768 bytes, stating that Codex loads project docs up to that budget and silently truncates the rest. The threshold is a named constant; no configuration.
- **Provenance comments.** The multi-line `Source provenance` comments inside fragments are no longer rendered. Fragment origin is already named in the rendered `<!-- Fragments: ... -->` header, and the comments remain in the fragment sources in this repository.

Expected outcome: the mid order renders to ~18.8K and the heavy order to ~27.6K, leaving ~5.2K of headroom under the Codex budget, and roughly half of the always-loaded system prompt is freed in every agent.

## Why

- closes the Codex truncation failure mode with the architecture the standards already prescribe: conditional detail moves out of always-loaded content, which `context-architecture` defines as the placement model
- reuses the existing deployment channel and reference-file pattern instead of inventing a new one, so no new tool-specific adapter is needed
- keeps the mechanism deterministic and agent-neutral: every agent that can read a file follows a pointer block; skill activation, imports, and per-directory `AGENTS.md` discovery all differ per agent and are therefore not load-bearing here
- makes the 32 KiB Codex budget an enforced, visible constraint instead of a silent failure

## Alternatives Considered

### Skills as the primary mechanism

Rejected for now. Skills load on demand in Kilo, but skill activation semantics on Codex and omp were not verified for this decision, and the production users of the standards require deterministic behavior. Skills remain the delivery channel for procedural features (standard-code-review, autonomous-task-run) and stay untouched. A pointer block can later point at, or be replaced by, a skill without changing the rule map.

### Nested per-directory `AGENTS.md` files

Rejected as a mechanism. Codex concatenates every `AGENTS.md` from the project root down to the working directory into the same budget, so nesting saves nothing there; Kilo loads nested files lazily on file access while omp composes them eagerly — the behavior diverges per agent exactly where the standard needs one behavior.

### `@path` / `@import` imports

Rejected. omp expands `@path` tokens inline and Claude expands `@import` inline, so they relocate text without saving context.

### Raise `project_doc_max_bytes` in downstream configs

Rejected as the answer. It is per-user configuration the standards cannot rely on, and it does nothing for the eager context cost in Kilo and omp.

## Consequences

- Every item moved into reference mode trades guaranteed in-context presence for trigger-plus-read compliance. That compliance is behavior, not decoration: the release gate in `ai-standards-evals` gains trigger-compliance scenarios for each moved item before the feature ships.
- `rule_map.toml` anchors for moved rules retarget through `source` to the deployed reference files, and the policy tests keep the map consistent.
- The self-hosted manifest becomes the first real consumer; its rendered size drops from 56.8K to ~27K.

## Affected Modules

- `scripts/ai_sync.py` — manifest parsing, fragment resolution, pointer-block assembly, reference deployment, budget warning, provenance stripping
- `registry.toml`, `templates/project_manifest.toml` — capability metadata and starter manifest keys
- `fragments/**` — pointer blocks authored alongside moved fragments (bodies unchanged)
- `rule_map.toml`, `tests/test_rule_map.py`, `tests/test_ai_sync.py`
- `docs/scenarios/**` — new `RD-*` behavioral scenario contracts
- self-hosted `ai.project.toml` — first consumer of the new lists

## Invariants And Constraints

- A manifest without the new keys renders byte-for-byte as before; rendering stays idempotent.
- No content generation: pointer blocks and reference files are assembled from authored sources; the fragment is the single source of truth.
- The budget warning is non-fatal and never blocks a render.
- The `ai-sync` module contract is updated with the new inputs, outputs, and invariants before implementation.

## Verification

- `uv run pytest`, `uv run mypy scripts/`, render idempotency, `ai-sync doctor` on the self-hosted tree.
- Size acceptance: light/mid/heavy reference manifests measured under 32 768 bytes.
- `ai-standards-evals` regression suite green on the candidate revision, including the new `RD-*` trigger-compliance scenarios; that suite is the release gate.

## Related Artifacts

- [issue #29](https://github.com/aka-NameRec/ai-standards/issues/29)
- [Change plan: reference-mode rendering](../../docs/artifacts/2026-11-02-reference-mode-rendering-change-plan.md)
- [Module contract: scripts/ai_sync.py](../architecture/2026-09-01-module-contract-ai-sync.md)
- Codex evidence: `codex-rs/core/src/agents_md.rs` (truncation behavior) and the `project_doc_max_bytes` entry (default 32768) in the official Codex config schema
