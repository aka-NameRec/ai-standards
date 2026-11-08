---
title: 'Task 27: cherry-pick-assessment skill, stage 1'
permalink: ai-standards/tasks/27-cherry-pick-assessment-skill
---

# Task 27: cherry-pick-assessment skill, stage 1

Russian localized version: [27-cherry-pick-assessment-skill.ru.md](27-cherry-pick-assessment-skill.ru.md)

Stage 1 of issue #27: ADR, Rule Engineering worksheet/task spec, the skill
itself (four adapter forms), registry and deployment wiring, rule map
entries, and behavioral scenario contracts. Branch
`feature/27-cherry-pick-assessment`; execution of the scenarios belongs to
`ai-standards-evals` (issue #18) and was deliberately not started.

## What Was Done

- **Decision record** `docs/decisions/2026-11-08-add-cherry-pick-assessment-skill.md`
  (+ `.ru.md`): a read-only pre-transfer assessment skill with a
  selector-based input model — the user states task ids / merge request /
  source branch / range / explicit SHAs; the skill resolves them into an
  ordered SHA list, includes evidence-backed companion commits, presents the
  list with the target HEAD, and proceeds only after user confirmation.
  Verdicts PASS / REVIEW / STOP with STOP > REVIEW > PASS precedence,
  FACT/HYPOTHESIS/UNKNOWN evidence discipline, validity bound to the
  confirmed set and target HEAD.
- **Worksheet/task spec** `docs/artifacts/2026-11-08-cherry-pick-assessment-authoring.md`
  (+ `.ru.md`): nine requirements with acceptance criteria, Rule Engineering
  verdicts (two accepted adaptations, two rejections), slice plan, and the
  issue-to-contract scenario map (CP-01…CP-08 → CP-001…CP-010, because the
  policy-test ID pattern is `[A-Z]{2,5}-\d{3}`).
- **Skill** `templates/cherry-pick-assessment/` in three adapter forms
  (SKILL.md for codex/kilo, `.cursor.mdc`, `.claude.md`); adapter bodies are
  byte-identical to the canonical SKILL.md body. New section "Input:
  Selectors, Resolution, Confirmation" carries the two-phase input model;
  analyses A–F, verdict rules, evidence discipline, and the mandatory report
  shape follow issue #27.
- **Placement**: feature `cherry-pick-assessment` registered in
  `registry.toml` (fragment `process/cherry-pick-assessment`) and added to
  `[reference_disclosure].features`; the self-hosted manifest enables it in
  `features` + `reference_features`, so `AGENTS.md` renders the authored
  pointer block (`.ai-standards/references/features/cherry-pick-assessment.md`
  deploys via `sync-templates` for every agent). The full fragment is not
  rendered inline — the first draft's inline render would have left
  `AGENTS.md` 160 bytes under the Codex 32 768-byte truncation budget.
- **Deployment registration** in `scripts/ai_sync.py` `AGENT_TEMPLATES` for
  codex, cursor, claude, kilo, gated on the new feature.
- **Rule map**: `CPA-001`–`CPA-012` in `rule_map.toml`, bound to
  skill-template sections; prefix comment updated.
- **Scenarios**: `CP-001`…`CP-010` behavior contracts + `TRG-004` trigger
  set, each EN + RU. CP-009 (selector resolution presents the full set
  including companions) and CP-010 (ambiguous selector without clarification
  → STOP) are new relative to the issue; the rest map the issue's CP-01…CP-08.

## Key Decisions

- Selector-based confirmed input replaces hand-enumerated SHAs (the user's
  review request); the confirmation step keeps the strict validity binding.
- Always-loaded placement follows the reference disclosure mode (decision
  2026-11-02): pointer block in `AGENTS.md` (~345 bytes delta), full
  invariant text in the deployed reference file and the skill — deterministic
  across agents without depending on per-agent skill activation.

## Verification

- `uv run pytest` — 174 passed (was 150 on `main`; new: registry
  registration, pointer-block render, fragment/feature resolution, issue
  invariant pinning, scenario policy tests).
- `uv run mypy scripts/` — clean.
- `ai-sync render` — idempotent; `AGENTS.md` grew by ~345 bytes vs `main`
  (31 683 vs 31 338), well under the budget warning threshold.
- `ai-sync doctor` — 0 errors, warning count equal to `main` (226).
- `sync-templates` smoke on a demo manifest (kilo + the feature) created
  `.agents/skills/cherry-pick-assessment/cherry-pick-assessment/SKILL.md`
  with the managed marker; demo project removed afterwards.

## What Remains

- Scenario execution in `ai-standards-evals` (issue #18) — the release gate;
  explicitly stopped before this step at the user's request.
- Issue #27 comment with the design summary and the input-model decision.
- `feature_meta` for the feature points at `2.10.0` (unreleased); adjust
  during `bump-version` if the release number differs.
- Merge into `main` only on explicit instruction; no push without approval.

## Observations

- [decision] The input model is selector-based with mandatory confirmation;
  scenario IDs follow the `[A-Z]{2,5}-\d{3}` pattern.
- [fact] The reference-mode placement keeps the always-loaded delta at ~345
  bytes; the inline first draft would have consumed nearly all remaining
  budget headroom.

## Relations

- implements [[DECISION: add cherry-pick-assessment skill]]
- relates_to [[Worksheet: cherry-pick-assessment skill authoring and task spec]]
- upstream request: aka-NameRec/ai-standards issue #27
- localized counterpart of [[Задача 27: skill cherry-pick-assessment, этап 1]]
