---
title: 29 — AGENTS.md progressive disclosure (reference mode)
permalink: ai-standards/tasks/29-progressive-disclosure
---

# 29 — AGENTS.md progressive disclosure (reference mode)

Russian version: [29-progressive-disclosure.ru.md](29-progressive-disclosure.ru.md)

Date: 2026-11-02 · Branch: `rules-change/29-progressive-disclosure` (commits `e73acc9`, `067eaaf`, `9db45d5`, `7849022`, `ce96721`, plus the release-prep change set this record ships in; not pushed — push requires explicit user approval)

## Trigger

The user reported that rendered `AGENTS.md` files overflow Codex's 32 KiB project-doc budget, and accepted the progressive-disclosure design discussed on 2026-11-02 (issue #29): reference-mode rendering for stacks and heavyweight features with the behavioral core kept inline. Canonical decision: [docs/decisions/2026-11-02-add-agents-md-progressive-disclosure.md](../decisions/2026-11-02-add-agents-md-progressive-disclosure.md); execution ran autonomously over [docs/artifacts/2026-11-02-reference-mode-rendering-change-plan.md](../artifacts/2026-11-02-reference-mode-rendering-change-plan.md).

## What Was Done

- **Renderer**: `reference_features` / `reference_stacks` manifest lists (names must stay ordered and be registry-capable); pointer-block assembly with the `{{REFERENCE_PATH}}` token; managed deployment of provenance-stripped fragment bodies to `.ai-standards/references/{stacks,features}/<name>.md` (multi-fragment bundles concatenate in registry order); non-fatal 32 768-byte budget warning in `render`/`update`/`check`; `Source provenance` and `Source: <url>` comments stripped from renders; byte-identical back-compat without the new keys.
- **Content**: 30 pointer blocks — 8 reference-mode features plus every stack fragment.
- **Traceability**: `RD-001`/`RD-002` in `rule_map.toml`; scenario contracts `RD-101`–`RD-108`, `RD-110`, `RD-111`, `RD-120` (EN/RU) in `docs/scenarios/`.
- **Self-hosting**: manifest switched to reference mode; rendered `AGENTS.md` 56.8K → 31.3K, inside the Codex budget without a warning; nine reference documents deployed.
- **Eval coverage (STD-CHANGE-0005 in `ai-standards-evals`)**: fixtures and scorers for the RD suite (activation oracle over kilo tool-event traces) and the RD-120 stack matrix runner; release report `reports/20261102-release-2-9-0-candidate/release-report.json` — PASS, 27 scenarios, two documented waivers.

## Verification

- `uv run pytest` 170 passed, `uv run mypy scripts/` and `uv run ruff check scripts/` clean; render idempotent; `ai-sync check` up to date; `ai-sync doctor` zero errors.
- Behavioral: RD suite 10/10 PASS; RD-120 matrix 24/24 PASS on this revision (STD-CHANGE-0005).
- Regression on this revision: CR-001..012, BM-001/002, PM-001, ATR-001 PASS; CR-010 failed once on report fencing and passed on rerun (single model variance, waived in the release report); TRG-001 12/12; TRG-003 10/11 matching the documented baseline false positive.
- ATR-002 fails on this revision AND identically on the released 2.8.1 pin (commit-on-main miss inside an otherwise correct stop-on-contradiction run) — pre-existing, waived in the release report, tracked as an `ai-standards-evals` follow-up.

## Deliberately Not Done

- No skill-based delivery for reference content (agent-dependent activation) — revisit after verifying skill activation on Codex/omp.
- No nested per-directory `AGENTS.md` output; no changes to the Codex budget or to existing skill packages.
- Merge into `main`, tag `2.9.0-2026-11-02`, and push await explicit user approval; the `ai-standards-evals` config pin update follows the released tag.

## Observations

- [fact] A reference-mode heavy order renders to 30,435 bytes and the mid order to 19,221 bytes, both under the 32,768-byte Codex budget.
- [decision] Reference files for bundle entries are single concatenated documents, not per-fragment files, so a pointer block's path is stable per ordered name.

## Relations

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- relates_to [[Module Contract: scripts/ai_sync.py]]
