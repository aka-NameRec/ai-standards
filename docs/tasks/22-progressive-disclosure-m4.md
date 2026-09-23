---
title: '22 — Progressive disclosure M4: reporting reference, CR-010–CR-012, eval gate'
permalink: ai-standards/tasks/22-progressive-disclosure-m4
---

# 22 — Progressive disclosure M4: reporting reference, CR-010–CR-012, eval gate

Russian version: [22-progressive-disclosure-m4.ru.md](22-progressive-disclosure-m4.ru.md)

Date: 2026-09-23 · Branch: `rules-change/22-m4-reporting-reference`
(ai-standards) + `STD-CHANGE-0001-cr010-cr012` (ai-standards-evals)

## Trigger

Issue #22: continue the context-architecture placement work after Phase 8
(M1–M3) by moving the code-review reporting-policy detail out of the
always-loaded fragment, with behavioral verification first. Change set
`STD-CHANGE-0001` per the cross-repo flow.

## What Was Done

- Scenario contracts `CR-010`–`CR-012` (EN/RU) bound to `RVW-015`–`RVW-018`,
  `RVW-022`, `RVW-024`, `RVW-030` in `rule_map.toml`; CR-010 closes the
  scenario gap behind the report-metadata rules that the rejected M3 attempt
  showed to be load-bearing, CR-011 pins reporting-reference routing, CR-012
  pins the template-absence fallback that no earlier scenario observed.
- New template `templates/code-review-reporting.reference.md` deployed via
  `INFRA_TEMPLATES` as `.ai-standards/references/code-review-reporting.md`
  (feature `code-review`); the fragment keeps trigger, scope, finding
  invariants, shape pointer, fallback order, the verbatim version-line
  invariant, and the chat-language rule; the full Russian localization legend
  moved into the worked example; a minimal section legend returned to the
  fallback bullet after the eval gate caught the regression (below).
- `ai-standards-evals`: fixture builders (CR-010/011 sync templates,
  CR-012 never does), scenario scorers, dataset snapshot, coverage 15/52 →
  rules bound 21/52; runner fixes (matrix-layout discovery, scope exemption
  for missing-coverage findings on test paths, outcome-based pre-existing
  mark, fuzzy fallback matcher for CR-012).

## Verification

- `ai-standards`: 148 tests pass; `ai-sync render` idempotent; `ai-sync doctor`
  zero errors. `ai-standards-evals`: ruff, mypy, pytest green.
- Eval gate: the first candidate epoch FAILED — fallback-path reports degraded
  into mixed-language forms without the always-loaded legend (the M3 lesson
  recurring in a new spot). Fixed by returning a minimal legend (~230 bytes);
  the rejected epoch is archived.
- Final comparison (baseline `2.6.0-2026-09-23` vs candidate, 2 epochs each,
  LLM judge GLM-5.3): machine verdict ACCEPT, no downgrades (CR-009 baseline
  MIXED → candidate PASS; CR-010 candidate MIXED from posting-form variance);
  judge 15/15 pass. Report:
  `ai-standards-evals/reports/20260923-std-change-0001-comparison.md`.
- Measured: `Code Review` section 7,781 → 5,835 bytes; self-hosted
  `AGENTS.md` 61,888 → 60,034 bytes.

## Notes

- Push and merge into `main` intentionally not performed: push requires
  explicit user approval, and the merge gate requires this comparison to be
  attached to the merge — both await the user's decision.
- M5 (Basic Memory Usage) and M6 (Project Memory, artifact-policy
  enumerations) remain the follow-up gated moves; M5 needs at least one
  behavioral scenario of its own for the gate to be meaningful.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Change plan: progressive disclosure M4 — reporting reference and CR-010/CR-011 (issue #22)]]
- relates_to [[18 — Phase 8: M1–M3 relocation and the release verification gate]]
- localized counterpart of [[22 — Прогрессивное раскрытие M4: reporting reference, CR-010–CR-012, eval-гейт]]
