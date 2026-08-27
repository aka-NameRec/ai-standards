---
title: Code Review Usage Guide
permalink: ai-standards/code-review-usage
---

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

Five dimensions, each its own section, reported in priority order: Correctness, Architecture & Conventions, Reuse, Efficiency, Quality. Correctness and conventions come first because a review that opens with cleanup suggestions while missing a real bug is not useful. The three cleanup lenses keep separate headings rather than sharing one, so a reader looking only for duplication does not have to read past readability notes to find it.

Three rules shape what actually gets reported, and all three exist to keep the output trustworthy rather than voluminous:

- **Evidence.** A finding needs a concrete file location and a named violated rule. Without either, it is not reported. This mirrors public prompting guidance from production AI review pipelines (see the sources in the project's decision record), which reward evidence-backed findings and penalize speculative ones.
- **Read the code, not the diff.** Before claiming that something duplicates an existing helper or reuses the wrong primitive, open the file being referred to. The diff shows what changed, not what is already there, and a claim about the surrounding code cannot be checked from it.
- **No padding.** Fewer high-confidence findings beat a full-looking list. An honestly empty section is a better outcome than a manufactured nitpick.

Problems that predate the diff are still surfaced, marked `(pre-existing)` so they do not read as blame for the current change. Reporting one does not obligate a fix — that decision stays with the author, and it can be tracked as a follow-up instead of expanding the patch.

## What Was Verified, And What Was Not

The report ends with `Verification`: the checks that actually ran, with their commands and results, and an explicit list of what was not checked.

The second half is the part that carries the weight. A report that lists passing backend tests and says nothing about the frontend reads as though the whole change was verified. Naming the gap — "backend tests pass, 34 of them; migrations and the uploader UI not checked" — turns an invisible assumption into a decision the reviewer can make.

`Dependencies` follows, and only when the change actually needs a change in another repository. For a self-contained change the section is dropped rather than filled with "none".

## Fixing While Reviewing

The workflow reports by default, with one narrow exception: a fix whose safety can be established by reading alone, without running anything. Wrong translations, typos, a missing `.gitignore` entry, an import that disagrees with the rest of the file — these are cheaper to fix than to describe, and they become ✅ findings with a `→ fixed:` tail so the fix stays on the record.

Everything else is reported and left alone. Migrations, lock files, dependencies, build configuration, public contracts, the git index, and anything that would need a test run to be sure about. Refactors are on this list too, however obviously correct: choosing to restructure code is the author's decision, not a defect the reviewer gets to resolve.

The order matters. Review first, then fix, then write the report, so the report describes the code as it stands after the fixes rather than as it was found.

## Task Reference And Multi-Repository Changes

The report leads with the tracked task when one exists, and prefers a full link over a bare id. The link is only emitted when its base is actually knowable — from the session, from the project's own rules, or from a `tracker_url` entry under `[metadata]` in `ai.project.toml`, which renders into the header of the generated `AGENTS.md` where the agent can read it:

```toml
[metadata]
tracker_url = "https://tracker.example.com/browse/"
```

Keeping that value in the project manifest rather than in `ai-standards` is deliberate: the tracker host belongs to the organisation using the standard, not to the standard itself.

When one task spans several repositories, the workflow produces one report per repository rather than a combined one, because each repository gets its own pull request and each report is pasted into a different description. Those reports name the repository in the heading (`## Code Review — <repository>`), keep file paths relative to that repository's root, and list the siblings under `Dependencies`, so a reviewer looking at a single pull request still knows the change is part of a set.

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