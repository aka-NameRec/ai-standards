---
title: 'Change plan: progressive disclosure M4 — reporting reference and CR-010/CR-011 (issue #22)'
permalink: ai-standards/artifacts/2026-09-23-progressive-disclosure-m4-change-plan
---

# Change plan: progressive disclosure M4 — reporting reference and CR-010/CR-011 (issue #22)

Russian version: [2026-09-23-progressive-disclosure-m4-change-plan.ru.md](2026-09-23-progressive-disclosure-m4-change-plan.ru.md)

Change set: `STD-CHANGE-0001` · Branch: `rules-change/22-m4-reporting-reference` · Date: 2026-09-23

## Goal

Apply the context-architecture placement model to the `code-review` Report Shape
detail: keep the trigger, scope, finding invariants, and shape pointer
always-loaded; move the reporting policy detail into a deployed feature
reference. Behavioral verification comes first: CR-010 and CR-011 cover the
invariants that the rejected M3 attempt showed to be load-bearing.

## Scope

- `docs/scenarios/CR-010-report-metadata.md` (+ `.ru.md`) — new behavior
  scenario contract.
- `docs/scenarios/CR-011-reporting-reference.md` (+ `.ru.md`) — new behavior
  scenario contract with two fixture variants (reference present / absent).
- `rule_map.toml` — attach scenario ids to the report rules
  (RVW-016–RVW-018 and marker/task rules where they map).
- `templates/code-review-reporting.reference.md` — new; deployed via
  `INFRA_TEMPLATES` to `.ai-standards/references/code-review-reporting.md`,
  feature-gated on `code-review`.
- `templates/code-review-report.md` — gains a localization legend (Russian
  header names) so the mapping lives where the agent reads it.
- `fragments/process/code-review.md` — Report Shape section compressed to:
  shape pointer, read-the-reference instruction, fallback order, version-line
  invariant (kept verbatim per the M3 lesson), language rule.
- `tests/test_ai_sync.py` — updated guarantees and deployment assertions.
- `ai-standards-evals` — fixtures, datasets, scoring, and runs for CR-010/CR-011
  (separate repository, same change set id).

Out of scope: core invariants, routing sections (light prose compression only,
later), stacks, renderer logic beyond the new `INFRA_TEMPLATES` entry, M5/M6
(follow-up gated moves).

## Intended Structure

Always-loaded (fragment): trigger, scope, passes pointer, finding reportability,
small-fix boundary, shape pointer + fallback order, version line + fallback +
motivation, chat-language rule, relationships, normalization rules.
Reference (deployed, read at report time): full marker semantics, section
policies (`What Was Done`, `How It Was Done`, `Verification`, `Dependencies`,
`Task`), multi-repository reports, destination, resending.

## Risks And Invariants

- M3 precedent: dropping the version-line motivation from always-loaded content
  stopped the agent emitting the line. The line, its fallback, and its
  motivation therefore stay in the fragment verbatim; only the section-policy
  detail moves. `test_code_review_fragment_keeps_the_version_line_guarantee`
  is preserved.
- The reference must be hooked into the base workflow (the fragment's report
  step), not only into the `standard-code-review` skill — bare "code review"
  runs never invoke the skill.
- Scoring determinism: CR-010 invariants are mechanically checkable (version
  line, markers, section presence, header language); CR-011 reference-present
  adds one distinctive, mechanically checkable requirement.

## Session Envelope

- Non-goals: no normative semantics change — the same behavior must result,
  loaded later instead of loaded always; no merges to `main` from this branch.
- Constraints: merge gate (eval comparison attached), push approval hardening
  (local commits only), documentation language pairs updated in the same
  change set.
- Stop conditions: eval comparison showing an unexplained behavioral regression
  (reject or re-plan, per the M3 precedent); contradictions with the
  scenario-format contract.
- Expected review artifacts: change plan (this file, EN/RU), scenario pairs,
  updated tests, eval run reports in `ai-standards-evals/reports/`, task record.

## Verification

1. `uv run pytest` (ai-standards) — including updated policy tests.
2. `uv run ai-sync render --project-root .` idempotent; `ai-sync doctor` zero errors.
3. `ai-standards-evals`: `uv run ruff check .`, `uv run mypy`, `uv run pytest`.
4. Baseline vs candidate comparison on the scenario suite (existing CR-001–009
   plus CR-010/CR-011), LLM judge included, reports stored under
   `ai-standards-evals/reports/`. Merge gate: no unexplained regressions.

## Outcome (recorded after implementation)

- The first candidate epoch failed the eval gate: without the localization
  legend always-loaded, fallback-path reports (no templates, Russian ambient
  context) degraded into mixed-language forms — the same failure class as the
  rejected M3 attempt. Re-planned within the approved design: the fragment's
  fallback bullet keeps a minimal Russian section legend (~230 bytes), the
  full policy stays in the reference.
- Final comparison (2 epochs per revision, LLM judge included): ACCEPT, no
  downgrades; CR-010 CR variance only (fenced-posting form). Reports:
  `ai-standards-evals/reports/20260923-std-change-0001-comparison.md`; the
  rejected epoch is archived under `reports/archive-std-change-0001-epoch1/`.
- Measured: `Code Review` section 7,781 → 5,835 bytes; self-hosted
  `AGENTS.md` 61,888 → 60,034 bytes. M5 remains the larger win.
- Scorer calibrations made honestly in `ai-standards-evals` and recorded in
  its README: missing-coverage findings on test paths do not count as scope
  violations; the pre-existing mark is judged as an outcome, not exact
  wording; the CR-012 fallback matcher judges order and presence, not
  headings; `collect_runs`/`discover_runs` cover matrix layouts.
