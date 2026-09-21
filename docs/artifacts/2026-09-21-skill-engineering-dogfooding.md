---
title: 'Dogfooding: skill-engineering authored through Rule Engineering (issue #17)'
permalink: ai-standards/artifacts/2026-09-21-skill-engineering-dogfooding
---

# Dogfooding: skill-engineering authored through Rule Engineering (issue #17)

Status: complete (2026-09-21, branch `rules-change/17-rule-engineering`).
Phase 6 of the change plan: the `skill-engineering` domain skill created with
its own authoring content (`skill-authoring`) passing through the Rule
Engineering flow — the mandatory dogfooding requirement.

## Method

Each candidate idea (external skill-authoring practice, per the proposal's
named sources, plus this repository's own deployment experience) went through
the flow: candidate behavior → atomicity → interpretation surface →
uniqueness against existing rules (`rule_map.toml`) → portability → placement
→ observable behavior → verdict. Accepted ideas are the skill's numbered
authoring rules, mapped as `SE-001`–`SE-009`.

## Worksheet

| # | Candidate guidance (source) | RE check | Verdict |
|---|---|---|---|
| 1 | Progressive disclosure: metadata → body → supporting resources (OpenAI/Anthropic practice) | Portable as a principle; "reference files" is deployment-specific | **Adapt** — principle accepted (SE-004); physical `references/` split deferred until the template model supports it; today reference sections |
| 2 | Context economy: only what changes decisions (Anthropic) | Atomic, unique (no existing rule states it), observable as token spend vs behavior change | **Accept** (SE-004) |
| 3 | Description field carries activation phrases | Adapted: requires positive AND negative trigger phrases, giving activation testing its target set | **Adapt** (SE-003) |
| 4 | Degrees of freedom matched to risk (proposal §6.2) | Unique — generalizes the script/tool layer rule; observable as variance of execution | **Accept** (SE-005) |
| 5 | Portable core; agent mechanics in adapters (proposal §6.2) | Overlap check against `RE-*` portability rule: different object (skill bodies vs shared rules) — no behavioral duplicate | **Accept** (SE-006) |
| 6 | Self-containment: restated rules, no pointers into standards internals (this repo's own practice from task 0tkgosq) | Unique at skill level; observable: no dead references in deployments | **Accept** (SE-006) |
| 7 | Observable completion criteria (proposal §8) | Accept; joins SE-001's justification set | **Accept** (SE-007) |
| 8 | "A static validator validates skills" (Anthropic validator note) | Ambiguous as stated → split: four independent questions; validator answers only the first | **Adapt** (SE-008) |
| 9 | Trigger eval sets with `should_trigger` (Anthropic `run_eval.py`) | The machinery is harness-specific; the behavioral requirement is portable | **Adapt** — requirement in SE-008; machinery rejected here, belongs to `ai-standards-evals` (#18) |
| 10 | Lifecycle stages candidate → … → deprecated (proposal §7.4) | Accept with the gate rule: advance only when the corresponding question is answered | **Accept** (SE-009) |
| 11 | "Every rule deserves a skill" | **Reject** — violates the justification set (SE-001); coverage of recurring behaviors, not skill count |
| 12 | Separate `skill-authoring` / `skill-validation` / `skill-lifecycle` skills up front | **Reject** — boundaries are a hypothesis; one domain until usage data shows independent triggers |

## Structural Decisions

- **One domain skill**, `skill-engineering`, with authoring as its first
  section — `skill-authoring` exists as content, not as a separate skill,
  per worksheet verdicts 11–12.
- **Placement**: the skill is loaded only when authoring/editing/validating
  skills (Context Architecture: repeatable procedure with a recognizable
  trigger). The standards' always-loaded layer gains nothing; the feature
  `skill-engineering` gates deployment and reuses `rule-engineering` as its
  policy base.
- **Registry extension**: rules may now live in template skills —
  `rule_map.toml` gained the optional `source` field (repo-root-relative
  path with extension) beside `fragment`.
- **Deployment**: three adapter files registered for codex, cursor, claude,
  and kilo; the feature gates deployment like every other skill.

## Uniqueness And Conflict Review

- `SE-004` (progressive disclosure + economy) vs `CA-002` placement
  questions: different decisions — CA decides the layer once; SE-004 governs
  content layout inside a skill. No behavioral overlap.
- `SE-006` portability vs `RE-002` portability property: different objects
  (skill bodies vs shared rules); no conflict.
- No conflicts found; the skill references no rendered rules and adds no
  always-loaded content.

## Verification

- `uv run pytest`: **141 passed, 0 failed** — the full suite is green for the
  first time since the 2.4.0 release (see the note below).
- The constant fix: `tests/test_ai_sync.py` pinned `CURRENT_AI_STANDARDS_VERSION = "2.3.0"`, which broke four tests at the 2.4.0 release; the pin is corrected to the actual release (`2.4.0-2026-09-18`) in this change set — a pre-existing defect fixed, disclosed here because it rides this commit.
- `uv run ruff check`, `uv run mypy scripts/` clean; `ai-sync doctor` zero errors.
- Policy tests cover the `SE-*` map entries via the new `source` resolution.

## Relations

See `## Relations` in the localized pair; canonical links: the adoption
decision and the scenario format contract.
