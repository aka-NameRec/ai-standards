# Review Lenses Usage Guide

Russian localized version: [review-lenses-usage.ru.md](review-lenses-usage.ru.md)

This guide explains how to apply the `review-lenses` feature from `ai-standards` in real development workflows.

The feature defines one reusable review model with three lenses:

- `Reuse`
- `Quality`
- `Efficiency`

The feature is intended for behavior-preserving cleanup and structural improvement of recent changes. It is not the default mode for every task and it is not a replacement for basic tests, linters, or normal code review.

## Goals

Use `review-lenses` when you want the agent to do one or both of the following:

- review a change through a stable multi-lens methodology
- apply safe cleanup and structural improvements without changing intended behavior

Typical outcomes:

- less duplication
- clearer control flow
- fewer noisy comments and debug leftovers
- better reuse of existing project primitives
- a more concrete review than generic "looks good / maybe refactor" feedback

## Two Modes

`review-lenses` should be used in two explicit modes.

### 1. Review-Only

In `review-only` mode, the agent analyzes the target diff or files and reports findings, but does not edit code.

Use this mode when:

- running checks in CI
- preparing a PR review summary
- evaluating risky or large diffs before making changes
- you want findings first and edits later

Expected output:

- findings grouped by `Reuse`, `Quality`, and `Efficiency`
- risky items called out separately
- concrete structural recommendations
- no code modifications

This mode is the recommended integration point for CI.

### 2. Fix

In `fix` mode, the agent is allowed to edit code, but only within the review-lenses constraints.

Use this mode when:

- a developer explicitly asks for cleanup or simplification
- the implementation already works and now needs structural polishing
- a review surfaced safe, behavior-preserving improvements
- the developer wants the agent to apply the smallest coherent patch instead of only reporting issues

Expected output:

- a focused patch
- preserved behavior and public contracts
- a short summary of structural gains

This mode should usually be triggered manually, not automatically in CI.

## Typical Development Scenarios

### After Initial Implementation

The developer first gets the feature working, then runs `review-lenses` in `fix` mode to reduce duplication, flatten control flow, and remove noise.

This is one of the highest-value scenarios.

### Before Commit or PR

The developer or reviewer runs `review-lenses` in `review-only` mode on the current diff to get a structured second pass before sharing the change.

This is useful when the code is probably correct, but the structure may still be weak.

### During Review of a Noisy Diff

Use `review-only` when a diff is hard to read because of repeated helpers, overly imperative logic, debug leftovers, or cleanup debt mixed into the change.

The goal is to get precise recommendations before deciding whether to rewrite anything.

### Manual Cleanup Pass

Use `fix` mode when the user explicitly asks for:

- simplification
- cleanup
- deduplication
- structural refactoring without behavior change

This is the preferred manual activation path for Codex and Cursor.

### CI Review Gate

Use `review-only` mode in CI when you want:

- a structured AI review artifact
- findings posted to a PR or build log
- a non-blocking or blocking quality signal, depending on team policy

CI should report, not silently rewrite code.

## Activation Model

`review-lenses` is policy, not an autonomous background process.

It becomes active only when one of the following mechanisms makes it active in the current tool:

- a rendered `AGENTS.md` includes the `review-lenses` feature
- a local managed or custom skill/rule adapter implements the workflow
- the current chat prompt explicitly asks for a review-lenses pass

In practice, activation should be considered explicit unless the tool is configured to auto-attach the workflow.

## Tool-Specific Activation

### Codex

For Codex, the usual pattern is:

1. Include `review-lenses` in the project standards so the policy is present in generated instructions.
2. Declare `codex` in `[tooling].agents` or add an equivalent local workflow artifact if your setup uses a custom layout.
3. Trigger it with an explicit chat request.

Typical prompts:

- `Run a review-lenses pass on my current changes in review-only mode.`
- `Review the changed files through Reuse, Quality, and Efficiency. Preserve public APIs.`
- `Run simplify-review in fix mode and apply only safe cleanup changes.`

Operational guidance:

- default to explicit activation
- use `review-only` for CI and for cautious review
- use `fix` manually when a developer wants edits

### Cursor

For Cursor, the usual pattern is:

1. Include `review-lenses` in generated project instructions.
2. Declare `cursor` in `[tooling].agents` or add a project rule in `.cursor/rules/`, for example `simplify-review.mdc`.
3. Choose whether the rule is manual or more automatic based on its type and scope.

Typical prompts:

- `Use the simplify-review rule in review-only mode for this diff.`
- `Use the simplify-review rule and propose the smallest safe fix patch.`

Operational guidance:

- prefer explicit rule invocation at first
- use automatic attachment only when the team is confident that the scope is narrow and the behavior is stable
- keep `fix` mode manual unless there is a very controlled automation design

### Claude Code

Claude can use the same methodology through a local skill such as `.claude/skills/simplify-review/SKILL.md`.

The usage pattern is the same:

- `review-only` for analysis and reporting
- `fix` for explicit manual cleanup

Claude is not special here; it is just another transport for the same workflow.

## Automatic vs Explicit Activation

As a default team policy:

- `review-only` may be automated in CI or attached automatically in tightly scoped tooling contexts
- `fix` should remain explicit and developer-triggered

Why:

- `review-only` is safe because it reports
- `fix` can change code and should therefore have clear human intent behind it

Recommended default:

- local chat usage: explicit
- CI usage: automated `review-only`
- repository-wide automatic `fix`: avoid

## CI Integration Guidance

`review-lenses` fits CI best in `review-only` mode.

Recommended CI responsibilities:

- run deterministic checks such as linters, type checks, and tests
- run AI review in `review-only` mode
- publish findings to build output, artifacts, or pull request comments

Recommended CI non-goals:

- silently rewriting code
- auto-committing refactors
- running broad autonomous cleanup without human review

Good CI patterns:

- non-blocking AI review report for early adoption
- blocking only on selected classes of findings after the workflow proves stable
- separate deterministic quality gates from AI review output

## Git Hooks Guidance

Git hooks can be useful, but the workflow should be split carefully.

Recommended:

- `pre-commit` or `pre-push` for deterministic checks
- optional helper commands that developers run manually before push

Use caution with AI-driven hooks:

- agent execution may be slow
- results may be non-deterministic
- automated edits at push time are hard to trust and hard to debug

Recommended policy:

- do not run `fix` mode from a push hook
- use hooks only to remind, prepare context, or run deterministic validation
- if AI is involved near push time, prefer `review-only`

## Suggested Team Rollout

### Phase 1

- enable the `review-lenses` feature in project standards
- document `review-only` and `fix`
- use manual activation in chats

### Phase 2

- add managed or custom local tool artifacts such as Codex skills or Cursor rules
- standardize prompt wording inside the team
- use `review-only` on selected PRs

### Phase 3

- integrate `review-only` into CI
- publish findings automatically
- decide whether any findings should become blocking

### Phase 4

- refine stack-specific heuristics in local rules or stack fragments
- keep `fix` manual unless the team has a very controlled automation workflow

## Starter Prompts

Use these prompts as the default language for the team.

### Review-Only

- `Run a review-lenses pass on my current changes in review-only mode. Report findings under Reuse, Quality, and Efficiency.`
- `Review this diff in review-only mode. Preserve public APIs and highlight structural gains that would come from a safe cleanup pass.`

### Fix

- `Run simplify-review in fix mode on the changed files. Apply only safe behavior-preserving cleanup.`
- `Use the review-lenses workflow in fix mode. If a change is risky, report it instead of editing.`

## Relationship To Other Quality Mechanisms

`review-lenses` should complement, not replace:

- normal human review
- deterministic linters and type checks
- tests
- architecture and error-handling rules already defined in `ai-standards`

Use it when a plain review is too vague, but a full redesign is unnecessary.
