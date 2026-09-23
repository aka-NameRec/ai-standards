---
title: 18 — Eval scenario contracts for ai-standards-evals
permalink: ai-standards/tasks/18-eval-scenario-contracts
---

# 18 — Eval scenario contracts for ai-standards-evals

Russian version: [18-eval-scenario-contracts.ru.md](18-eval-scenario-contracts.ru.md)

Date: 2026-09-22 · Branch: `rules-change/18-eval-scenario-contracts` (commit `c6eda51`; pushed after user approval)

## Trigger

Issue [#18](https://github.com/aka-NameRec/ai-standards/issues/18) moves the
executable verification into the `ai-standards-evals` repository. The scenario
contracts, however, are normative knowledge and belong here: the eval
specification's scenario IDs collided with the contracts that had already been
recorded in `docs/scenarios/` (see the reconciliation comment on the issue),
so the six new scenarios were renumbered and recorded canonically.

## What Was Done

- Six behavioral scenario contracts recorded under `docs/scenarios/` (EN +
  `.ru.md` pairs), bound to `rule_map.toml`: **CR-004** (real correctness
  defect), **CR-005** (new internal duplication without a prior helper — the
  DRY vs Reuse discriminator), **CR-006** (architecture decision violation,
  ADR-004), **CR-007** (apparent violation disproved by the full code),
  **CR-008** (verification unavailable in the environment), **CR-009**
  (missing error-path test). Scenario numbering: CR-001–CR-003 and TRG-001
  were already taken, so the new contracts took CR-004–CR-009.
- `rule_map.toml`: scenario bindings added to `RVW-004`, `RVW-005`, `RVW-006`,
  `RVW-008`, `RVW-011`, `RVW-012`, `RVW-014`, `RVW-019`.

## Verification

- `uv run pytest tests/test_rule_map.py`: 9 passed; full suite: 141 passed.
- `uv run ai-sync render --project-root .` idempotent; rule IDs stay out of
  the rendered `AGENTS.md`.
- The contracts are consumed by `ai-standards-evals` (fixtures, fixtures
  runners, LLM judge rubrics) — all six scenarios pass on the current
  `main` with both mechanical and judge scoring.

## Notes

- The judge rubrics for the finding-depth scoring live in the evals
  repository (`scorers/rubrics/`), calibrated against these fixtures.
- The eval-side record of the same session lives in the evals repository's
  git history and README; this repository holds the normative contracts only.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Spec: ai-standards-evals repository (issue #18)]]
- localized counterpart of [[Задача 18: контракты сценариев для ai-standards-evals]]
