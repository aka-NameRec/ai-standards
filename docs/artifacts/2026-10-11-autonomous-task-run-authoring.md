---
title: 'Authoring worksheet and task spec: autonomous-task-run skill'
permalink: ai-standards/artifacts/2026-10-11-autonomous-task-run-authoring
---

# Authoring worksheet and task spec: autonomous-task-run skill

Russian localized version: [2026-10-11-autonomous-task-run-authoring.ru.md](2026-10-11-autonomous-task-run-authoring.ru.md)

Task spec for issue #24, doubling as the Rule Engineering authoring worksheet
(SE-002) and the slice plan. Written before implementation starts; requirements
are the constant of the run.

## Goal

Ship the `autonomous-task-run` skill as a standards-deployed template: a
repeatable, trigger-recognizable procedure for running an approved plan
end-to-end — entry gate, slice loop with task-spec conformance checks,
immutable requirements, stop conditions, knowledge capture, merge by standard.

## Non-goals

- No eval-runner implementation (execution belongs to `ai-standards-evals`,
  issue #18).
- No changes to the normative content of `autonomy-boundaries` beyond a
  one-line pointer to the deployed skill.
- No push to any remote; no other fragments or features touched.

## Requirements (the constant of this run)

| ID | Requirement | Acceptance criterion |
|---|---|---|
| REQ-1 | Skill template exists in all four adapter forms (SKILL.md for codex/kilo, `.cursor.mdc`, `.claude.md`), frontmatter `name`/`description` carrying RU and EN trigger phrases | Files exist under `templates/autonomous-task-run/`; deployed copies appear after `sync-templates` |
| REQ-2 | Deployment registered for codex, cursor, claude, kilo, gated on the `autonomy-boundaries` feature | New registry test mirrors `test_skill_engineering_templates_registered_for_all_agents`; `uv run pytest` passes |
| REQ-3 | Skill body carries the issue #24 invariants: entry gate (approved plan; verifiable task spec with per-requirement acceptance criteria; slice-level plan checked pre-flight; repo/task context), slice-end conformance checks, drift-fix rule, requirements immutability (no add/change/reinterpret), stop conditions with a detailed stop report naming the blocked requirement, commit/push rules, knowledge capture before merge, merge by standard, completion report, non-goals | Structural pytest asserts key phrases of every normative block in the SKILL.md template |
| REQ-4 | Rules traced as `ATR-001`–`ATR-007` in `rule_map.toml`, atomic, bound to skill-source sections; prefix comment updated | `tests/test_rule_map.py` passes (sections exist, one-line behaviors, ids unique) |
| REQ-5 | Scenario contracts `ATR-001`, `ATR-002` (behavior), `TRG-003` (trigger set), each EN + RU, wired into rule references | Policy scenario tests pass; every referenced id resolves |
| REQ-6 | `autonomy-boundaries` fragment gains exactly one pointer line to the deployed skill | Self-hosted `AGENTS.md` contains the line after render; fragment diff is one line |
| REQ-7 | Knowledge capture in the same change set: decision record (+.ru), task record (+.ru), this artifact (+.ru), local-memory progress note (date-prefixed) | Files exist; `ai-sync doctor` reports no new warnings for them |
| REQ-8 | Full verification: `pytest` green, `mypy scripts/` clean, `render` idempotent, `doctor` zero errors | Commands run on the final state with results recorded in the completion report |
| REQ-9 | Release metadata prepared for 2.9.0 via `bump-version save`; CHANGELOG entry under `[Unreleased]` | `meta.toml` = `2.9.0` / `2026-10-11`, both manifest pins updated, `AGENTS.md` header v2.9.0 |
| REQ-10 | Merge into `main` by the merge-by-standard flow, feature branch deleted, no push | `main` carries the merge commit; branch gone; worktree clean; `main` ahead of `origin/main` |

## Worksheet (Rule Engineering verdicts)

| Candidate guidance | Verdict | Note |
|---|---|---|
| Entry gate with four mandatory conditions (approved plan; verifiable task spec; sliced plan checked pre-flight; repo/task context) | accepted | Maps onto `autonomy-boundaries` artifact and slice rules; refusal without the gate is observable |
| Task spec phrased as "ADR" | adapted | ai-standards names this artifact class "task spec"; ADR is a project-local form — the skill says "task spec (an ADR where the project uses that form)" |
| Slice-end conformance check against requirements | accepted | Operationalizes `reasoning-hygiene` local re-evaluation and design anchors |
| Drift fixes allowed only within requirements | accepted | Verbatim-service rule; observable via scenario |
| Requirements are an absolute constant; no add/change | accepted | Matches the Required Stop Conditions ("widening scope → stop, not a new decision") |
| Requirements also never *reinterpreted* by the agent | adapted | User's clause 4 extended with reinterpretation to close the silent-rewording loophole |
| Commits without per-commit approval | adapted | Paired with precedence wording: the instruction to run autonomously is the standing approval of the commit flow; message form still follows the standard |
| Push never without explicit approval | accepted | Reaffirms the cross-project push-hardening rule inside the procedure |
| Stop conditions with a detailed stop report | accepted | Report names the blocked requirement by its task-spec id — verifiable |
| Knowledge capture before merge; merge by standard; completion report | accepted | Mirrors the #23 run the skill abstracts |

Uniqueness: no existing rule or skill demands the same observable behavior —
`autonomy-boundaries` and `session-hygiene` state invariants and stop
conditions; this skill is the procedure that satisfies them run-by-run.
Validation forms: behavioral scenarios (ATR-001 slice loop, ATR-002 stop on
requirements change), trigger set (TRG-003), structural pytest (REQ-3).

## Slices

| Slice | Content | Verification |
|---|---|---|
| S1 | Discovery: template registry shape, adapter forms, worksheet precedent | Done pre-branch; no code change |
| S2 | Skill templates (3 files) + 4 registry entries + fragment pointer line + registry/content tests | Targeted pytest on new tests |
| S3 | `rule_map.toml` ATR rules + scenario contracts ATR-001, ATR-002, TRG-003 (EN/RU) | `pytest tests/test_rule_map.py` |
| S4 | Decision record, task record, local-memory note, CHANGELOG | `doctor` — no new warnings |
| S5 | `sync-templates` deployment, full verification, release 2.9.0, commit, merge, issue updates | REQ-8 command suite |

## Observations

- [decision] Two wording adaptations were accepted: "task spec (an ADR where
  the project uses that form)" for portability, and the standing-approval
  commit clause to keep the skill co-satisfiable with the shared
  commit-approval rule.
- [fact] The self-hosted manifest declares no agents, so adapter deployment
  is verified on a demo manifest (kilo + `autonomy-boundaries`), not in this
  repository.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- implements [[DECISION: adopt-autonomous-task-run-skill]]
- relates_to [[Spec: ai-standards-evals repository (issue #18)]]
- upstream request: aka-NameRec/ai-standards issue #24
