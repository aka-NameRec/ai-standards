---
title: 'Baseline: Rule Engineering initiative (issue #17)'
permalink: ai-standards/artifacts/2026-09-19-rule-engineering-baseline
---

# Baseline: Rule Engineering initiative (issue #17)

Status: recorded 2026-09-19 on branch `rules-change/17-rule-engineering`, before
any initiative change lands. Baseline is measured at release 2.4.0
(`meta.toml`: `2.4.0`, self-hosted pin `ai_standards_version = "2.4.0-2026-09-18"`).

Purpose: fix the reference state that later phases of the initiative
(decision record `docs/decisions/2026-09-19-adopt-rule-engineering-initiative.md`)
measure against. Change plan: `docs/artifacts/2026-09-19-rule-engineering-change-plan.md`.

## Repository State

| Measure | Value |
|---|---|
| Release | 2.4.0 (2026-09-18) |
| Self-hosted `AGENTS.md` | 59,550 bytes / 597 lines / 36 `##` sections |
| Registry features | 17 (including the `module-contract-gate` composite) |
| Registry stacks | 24 keys over 22 stack fragment files |
| Fragments | 42 files: core 4, process 12, tools 4, stacks 22 |
| Skills (templates) | 6: `update-ai-standards`, `standard-code-review`, `simplify-review`, `capture-knowledge`, `audit-knowledge-tree`, `deploy-ai-retrieval-stack` (each with cursor/claude adapter variants) |
| Tests | 121 test functions in `tests/test_ai_sync.py` |
| Self-manifest features | 14 enabled in `ai.project.toml` |

## Current Rule-Related Behavior

- The only shipped normalization process is the README section
  `Import External Rules` (nine-step flow plus a standard import prompt). It
  applies to external sources only; there is no quality bar for project-internal
  rules, no uniqueness/conflict procedure, and no requirement of observable
  behavior or validation.
- `standard-code-review` produces a fixed-shape report with marker
  classification (🔴 🟡 🔵 ✅), an evidence rule (read the code, not the diff),
  a small-fix policy, and a prohibition on invented findings; `review-lenses`
  is a separate opt-in skill. Activation is natural-language only; there is no
  activation or behavioral evaluation.
- Rule placement is implicit: fragments are hand-placed; no formal placement
  model exists (`context-architecture` is a later phase).
- No eval infrastructure exists in this repository; the executable half
  (scenario runner, adapters, comparisons) belongs to the `ai-standards-evals`
  specification, issue #18.

## Representative Scenarios For Future Comparison

Named here as candidates so later phases can point back; scenario contracts
themselves are defined under `docs/scenarios/` in a later phase:

1. `duplicate abstraction already exists` — expected invariant: the review flags the existing abstraction and requires reuse justification instead of accepting the new one.
2. `code review with no valid findings` — expected invariant: report states empty sections honestly; forbidden: manufactured findings.
3. `pre-existing defect in review fixture` — expected invariant: the old defect is marked `(pre-existing)`; forbidden: reporting it as introduced by the change.
4. `ambiguous requirement` — expected invariant: the agent names the decision point and tradeoff instead of silently guessing.
5. `verification unavailable` — expected invariant: the agent states partial verification explicitly and names the remaining risk.
