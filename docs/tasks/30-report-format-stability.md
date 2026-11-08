---
title: 'Task 30: report-format stability under model provider shifts'
permalink: ai-standards/tasks/30-report-format-stability
---

# Task 30: report-format stability under model provider shifts

Russian localized version: [30-report-format-stability.ru.md](30-report-format-stability.ru.md)

Investigation of issue #30 executed autonomously (autonomous-task-run
discipline) on branch `rules-change/30-report-format-stability`. Trigger: the
2.10.0 regression showed CR-010 (report not inside a fenced block) and CR-011
(Dependencies section added despite the drop policy) failing stably on the
new inference provider for the same model id, while both passed on the
released 2.9.0 pin; the branch diff provably touches no code-review policy
file.

## Root Cause

- **CR-010**: the fenced-destination norm (RVW-024) was anchored to the
  fragment's `Report Shape` section, but the fragment text carried no fenced
  wording — the rule lived only in the deployed reporting reference
  (`Destination`). Under the shifted provider the model skipped or
  de-prioritized the reference's destination point and posted plain chat
  Markdown.
- **CR-011**: two conflicting signals — the fragment's fallback order lists
  `Dependencies` unconditionally, while the reference drops it for
  self-contained changes. The model averaged them into a placeholder
  section («новые зависимости не вводятся»), which the drop policy treats as
  padding, not dropping.

## Changes

- `fragments/process/code-review.md`, `Report Shape`: the fenced invariant is
  now stated in the always-loaded fragment — the whole report (headers,
  findings, prose) lands inside a fenced Markdown code block, and plain chat
  Markdown is named as the failure mode the rule exists for.
- `fragments/process/code-review.md`, fallback order: `Dependencies` is now
  named as dropped for self-contained changes, aligning the fragment with the
  reference's section policy.
- `templates/code-review-reporting.reference.md`: the `Dependencies` policy
  gains the anti-example (a heading with a placeholder line is padding, not
  dropping); the `Destination` rule names the whole-report-inside-the-fence
  requirement with the failure mode.
- `rule_map.toml`: `RVW-024` behavior wording updated to the sharper
  invariant; `tests/test_ai_sync.py` pins all new phrases.

## Deliberate Decisions

- The drop semantics were kept, not relaxed into an explicit-none one-liner:
  the placeholder section is exactly the padding the no-padding culture
  forbids, and CR-011's forbidden outcome already names it. The anti-example
  closes the interpretation gap without a normative semantics change.
- The worked example keeps its filled `Dependencies` section: it must show
  the section's anatomy when the section exists; the drop policy lives in the
  reference by the M4/M5 placement decision.

## Verification

- `uv run pytest` — 174 passed; `uv run mypy scripts/` — clean;
  `ai-sync sync-templates` refreshed the deployed reference.
- Behavioral: CR-010 and CR-011, three runs each against this branch
  revision (kilo, glm-5.3-flash) — **6/6 PASS**
  (`ai-standards-evals: reports/issue-30/20261108-21*`): the fenced block is
  present in every report and no placeholder Dependencies section appeared
  in any run.

## Known Limitation

- Cross-provider reruns (the old provider endpoint) are not executable from
  this environment: provider selection lives in the kilo harness
  configuration. Completing the both-provider matrix of issue #30 requires a
  user-side run of CR-010/CR-011 with the previous provider pinned; the
  wording changes above are expected to hold on both, since the failure mode
  is now named in the always-loaded fragment.

## Observations

- [fact] RVW-024's anchor text gap (rule behavior described wording the
  fragment did not carry) is a concrete instance of the anchor-drift risk the
  policy tests do not cover: they check the section exists, not that the
  behavior sentence is stated there.
- [decision] Anti-example wording was chosen over a semantics change; the
  rejected option is recorded in the worksheet with its reasons.

## Relations

- relates_to [[DECISION: add cherry-pick-assessment skill]]
- relates_to [[Worksheet: issue 30 report-format stability task spec]]
- upstream request: aka-NameRec/ai-standards issue #30
- localized counterpart of [[Задача 30: устойчивость формата отчёта к смене провайдера модели]]
