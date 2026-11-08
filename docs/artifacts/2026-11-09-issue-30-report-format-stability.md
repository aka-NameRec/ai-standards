---
title: 'Worksheet: issue 30 report-format stability task spec'
permalink: ai-standards/artifacts/2026-11-09-issue-30-report-format-stability
---

# Worksheet: issue 30 report-format stability task spec

Russian localized version: [2026-11-09-issue-30-report-format-stability.ru.md](2026-11-09-issue-30-report-format-stability.ru.md)

Task spec and Rule Engineering worksheet for issue #30, executed
autonomously under the `autonomous-task-run` discipline. Branch
`rules-change/30-report-format-stability`; merge into `main` waits for the
user's approval; nothing is pushed without approval.

## Goal

Make the code-review report-format norms robust to model formatting habits
(observed as a provider shift for the same model id): the fenced-destination
rule must be stated in the always-loaded fragment it is anchored to, and the
Dependencies drop policy must stop conflicting with the fragment's fallback
order and the worked example.

## Non-goals

- No change to the reporting policy semantics: `Dependencies` stays dropped
  for self-contained changes (an explicit-none placeholder line stays
  forbidden — it is the padding the no-padding culture exists to prevent).
- No new scenarios and no scorer changes in `ai-standards-evals`: CR-010 and
  CR-011 contracts and their mechanical oracles already pin the invariants.
- No release, no push; merge into `main` on explicit instruction only.

## Requirements (the constant of this run)

| ID | Requirement | Acceptance criterion |
|---|---|---|
| REQ-1 | The fenced-destination invariant is stated in the fragment's `Report Shape` section (the `RVW-024` anchor): the whole report goes inside a fenced Markdown code block; plain chat Markdown is the named failure mode | `fragments/process/code-review.md` carries the sentence; `rule_map.toml` `RVW-024` behavior matches it; policy tests pass |
| REQ-2 | The fragment fallback order stops contradicting the reference: `Dependencies` is named as dropped for self-contained changes | Same file; `CR-011` contract unchanged and still verified |
| REQ-3 | The reporting reference gains the anti-example for the drop policy (a heading with a placeholder line is not dropping) and the destination rule names the whole-report-inside-the-fence requirement with the failure mode | `templates/code-review-reporting.reference.md`; deployed copy refreshes via `sync-templates` |
| REQ-4 | Behavior verified on the branch revision: CR-010 and CR-011 each run 3 times against `rules-change/30-report-format-stability`; all 6 runs PASS | Run artifacts under `ai-standards-evals: reports/issue-30/` |
| REQ-5 | Known limitation recorded: cross-provider reruns are not executable from this environment (provider selection lives in the user's kilo harness config); the user may rerun CR-010/CR-011 on the previous provider to complete the #30 matrix | Recorded in the task record and the completion report |
| REQ-6 | Knowledge capture: task record (+.ru), CHANGELOG `[Unreleased]` line, local-memory progress note | Files exist; `ai-sync doctor` adds no new warnings |

## Rule Engineering verdicts

| Candidate | Verdict | Note |
|---|---|---|
| State the fenced invariant in the fragment (RVW-024 anchor text gap) | accepted | The anchor exists but the fragment text lacked the word; a delivery invariant belongs always-loaded — the report cannot be rewrapped after the fact |
| Name plain chat Markdown as the failure mode in the fragment | accepted | Turns the invariant into an observable anti-example; minimal interpretation surface |
| Anti-example for the drop policy in the reference | accepted | Closes the interpretation gap without changing semantics: "dropping" means the heading does not appear at all; a placeholder heading is the observed non-compliant form |
| Replace drop with an explicit-none one-liner (issue #30 item 2 option) | rejected | Conflicts with the no-padding culture (`honestly empty sections state Не найдено.`) and the CR-011 forbidden outcome; the anti-example achieves robustness without a semantics change |
| Align the worked example with the drop policy (drop the section there) | rejected | The example must show the section's anatomy when it exists; the drop policy lives in the reference by design (M4/M5 placement) |

## Slices

| Slice | Content | Verification |
|---|---|---|
| S1 | Discovery: contracts CR-010/CR-011, fragment Report Shape, reporting reference, worked example, scorer oracle | Done; no code change |
| S2 | This worksheet (EN/RU) + branch | Files exist; branch created |
| S3 | Fragment + reference wording, invariant test additions | `uv run pytest`, `uv run mypy scripts/` |
| S4 | Behavioral rerun: CR-010, CR-011 × 3 each on the branch revision | 6/6 PASS in evals artifacts |
| S5 | Task record (+.ru), CHANGELOG line, local memory, completion report | `doctor` adds no new warnings |

## Observations

- [fact] `RVW-024` anchors to `Report Shape`, but the fragment text carried
  no fenced wording — the norm lived only in the deployed reference; the
  anchor-text gap is closed by REQ-1.
- [fact] The fragment's fallback order lists `Dependencies` unconditionally,
  conflicting with the reference's drop policy; the model averages the two
  signals, which is the observed CR-011 failure.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- upstream request: aka-NameRec/ai-standards issue #30
- localized counterpart of [[Рабочий лист: task spec доисследования issue 30]]
