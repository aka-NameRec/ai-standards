# Code Review Usage Guide

Russian localized version: [code-review-usage.ru.md](code-review-usage.ru.md)

This guide covers when to reach for the `code-review` feature and how it relates to the other quality mechanisms in `ai-standards`.

It deliberately does not restate the report format. That format is defined once, by the worked example in [templates/code-review-report.md](../templates/code-review-report.md), so there is exactly one place to read it and one place to change it.

## Why This Feature Exists

Without it, a bare "do a code review" prompt produces a different shape and a different depth of scrutiny every time, depending on the tool, the model, and the phrasing of the moment. `code-review` fixes that by making the trigger, the checked dimensions, and the report shape part of the project's rendered instructions rather than an ad hoc chat convention.

It is not a replacement for tests, linters, type checks, or human review. It is a standard way to ask an agent for a structured second pass.

## Activation

Enable the feature in `ai.project.toml`, then run both commands:

```bash
uv run ai-sync render --project-root /path/to/project
uv run ai-sync sync-templates --project-root /path/to/project
```

`render` puts the rules into `AGENTS.md` (or the Claude Code `CLAUDE.md` bridge); `sync-templates` deploys the worked example to `.ai-standards/code-review-report.md`, which the rules point at. The template channel is agent-agnostic, so no slash command, custom skill, or `tooling.agents` adapter is needed — the workflow behaves the same in Claude Code, Codex, Cursor, and any other tool that reads the generated instructions file.

If `sync-templates` is skipped, the agent says the example is missing and falls back to the section order named in the fragment, so the report degrades rather than breaking.

A bare, unqualified request triggers it: `code review`, `review this`, `сделай ревью`, `проверь код`, and similar. A request that already narrows scope, mode, or lens — an explicit `review-lenses` prompt, or "just check for bugs" — takes priority instead.

## What The Review Covers

Five dimensions, reported in priority order: Correctness, Architecture & Conventions, then Reuse, Quality, and Efficiency. Correctness and conventions come first because a review that opens with cleanup suggestions while missing a real bug is not useful.

Two rules shape what actually gets reported, and both exist to keep the output trustworthy rather than voluminous:

- **Evidence.** A finding needs a concrete file location and a named violated rule. Without either, it is not reported. This mirrors public prompting guidance from production AI review pipelines (see the sources in the project's decision record), which reward evidence-backed findings and penalize speculative ones.
- **No padding.** Fewer high-confidence findings beat a full-looking list. An honestly empty section is a better outcome than a manufactured nitpick.

Problems that predate the diff are still surfaced, marked `(pre-existing)` so they do not read as blame for the current change. Reporting one does not obligate a fix — that decision stays with the author, and it can be tracked as a follow-up instead of expanding the patch.

## Relationship To Review Lenses

`code-review` and `review-lenses` are complementary, and a project can enable either or both:

| | `code-review` | `review-lenses` |
|---|---|---|
| Activation | automatic, on a plain request | explicit, by naming the workflow or its adapter |
| Scope | correctness and conventions plus cleanup | cleanup only (Reuse / Quality / Efficiency) |
| Output | fixed report shape | findings grouped by lens |
| Best for | interactive review in chat | deliberate cleanup passes, and CI |

Enabling `review-lenses` does not change what a bare "code review" request does, and asking explicitly for a review-lenses pass does not go through the `code-review` report shape. See [review-lenses-usage.md](review-lenses-usage.md) for its own guidance and its adapter templates.

## CI Integration

Prefer `review-lenses` in `review-only` mode for automated, non-interactive review; it is already documented for that purpose and ships adapter templates. Reserve `code-review` for interactive sessions where a developer types the request directly.

## Relationship To Other Quality Mechanisms

`code-review` complements rather than replaces human review, deterministic linters and type checks, tests, and the project's own architecture, error-handling, and stack rules — which this workflow checks against rather than restates.
