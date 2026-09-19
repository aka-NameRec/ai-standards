---
title: 17 — Rule Engineering initiative, phases 0–1
permalink: ai-standards/tasks/17-rule-engineering-phase-0-1
---

# 17 — Rule Engineering initiative, phases 0–1

Russian version: [17-rule-engineering-phase-0-1.ru.md](17-rule-engineering-phase-0-1.ru.md)

Date: 2026-09-19 · Branch: `rules-change/17-rule-engineering` (commit `ecb80ca`, not pushed; push requires explicit user approval)

## Trigger

The user accepted issue #17 on 2026-09-19: the initiative direction, the
#17/#18 scope split (methodology in this repository, executable eval
infrastructure in the `ai-standards-evals` specification), and `docs/scenarios/`
as the future home of scenario contracts. Accepted decision:
[docs/decisions/2026-09-19-adopt-rule-engineering-initiative.md](../decisions/2026-09-19-adopt-rule-engineering-initiative.md).

## What Was Done

- **Phase 0**: baseline artifact `docs/artifacts/2026-09-19-rule-engineering-baseline.md` (both languages) — repository measures at release 2.4.0 (`AGENTS.md` 59,550 bytes / 597 lines / 36 sections, 17 features, 42 fragments, 6 skills), current rule-related behavior, and five candidate scenarios for future comparison.
- **Phase 1**: new feature `rule-engineering` — fragment `process/rule-engineering.md` (nine rule quality properties, the interpretation surface concept, the twelve-step engineering flow with a mandatory validation form, context placement principles; 3,954 bytes); `registry.toml` entry with `feature_meta` `2.5.0`; self-hosting enabled in `ai.project.toml`; `AGENTS.md` re-rendered; usage guides in both languages; README (both languages) — TOC, feature enumeration, the Execution governance group, the `Using Rule Engineering In a Project` section, and the `Import External Rules` flow restated as a Rule Engineering special case with the standard import prompt updated; CHANGELOG `[Unreleased]`; two tests (render + fragment).
- Knowledge capture: this task record and the local context update.

## Verification

- `uv run pytest`: 125 passed; 4 failures are pre-existing on `main` (verified by stashing this change: `test_render_contains_expected_markers`, `test_legacy_manifest_version_key_still_renders`, `test_init_project_seeds_current_ai_standards_version`, `test_check_fails_when_manifest_pin_drifts_from_the_source` hardcode the `v2.3.0` release banner and broke at the 2.4.0 release).
- `uv run ruff check` and `uv run mypy scripts/` clean on changed files; render idempotent; `ai-sync doctor` zero errors (184 warnings of the pre-existing `note-without-*` class).
- `AGENTS.md` growth is exactly the new section: 59,550 → 63,530 bytes.

## Deliberately Not Done

- No mass rewrite of existing rules — the Phase 1 constraint of the accepted decision.
- The four pre-existing test failures and the five pre-existing ruff findings in `templates/ai-infrastructure/scripts/code_index.py` are reported, not fixed — separate concern.
- Phases 2–9 of the initiative remain open, each behind its own change plan slice.

## Context For The Next Session

- Phase 2 next: rule traceability — stable rule IDs in source/eval metadata only (never in rendered `AGENTS.md`), the `rule ↔ source ↔ expected behavior ↔ eval scenarios` link. Before placing IDs into fragment frontmatter, check how the renderer treats fragment frontmatter.
- `feature_meta` `2.5.0` must match the version the next release actually receives (adjust at `bump-version` if needed).
- The capture record for this session is a second commit on the same branch, pending message approval.

## Observations

- [fact] The `rule-engineering` feature adds exactly one rendered section of 3,980 bytes to an enabling project's `AGENTS.md`.
- [fact] Four tests in `tests/test_ai_sync.py` hardcode the release banner version and fail on `main` since the 2.4.0 release; they are unrelated to this change.
- [decision] External rule importing is a special case of Rule Engineering: the README import flow routes every candidate through the engineering flow and requires a validation form per accepted rule.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Baseline: Rule Engineering initiative (issue #17)]]
- relates_to [[Change plan: Rule Engineering initiative (issue #17)]]
- localized counterpart of [[17 — Инициатива Rule Engineering, фазы 0–1]]
