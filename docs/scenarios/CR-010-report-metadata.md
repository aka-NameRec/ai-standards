---
title: 'Scenario CR-010: report metadata and language invariants'
permalink: ai-standards/scenarios/CR-010-report-metadata
---

# Scenario CR-010: report metadata and language invariants

Russian version: [CR-010-report-metadata.ru.md](CR-010-report-metadata.ru.md)

Behavioral scenario for the code-review workflow. Verifies rules `RVW-016`,
`RVW-017`, `RVW-018`, `RVW-022`, `RVW-024` (report metadata, marker semantics,
section presence, chat language, posting destination). Status: draft (issue
#22); the runner belongs to `ai-standards-evals`. This scenario protects the
report-metadata invariants against relocation of the reporting detail into the
deployed reporting reference: the invariants must hold whether the policy is
loaded always or loaded at report time.

## Fixture

Pre-state: a small Python project. The diff under review is small and
statically reviewable and contains at least one reportable correctness defect
(so findings exist and markers are exercised) and one defect safe to fix by
reading alone (so the checked-marker path is exercisable).

## Enabled Features

- `code-review` (the workflow under test; templates synced, so the worked
  example and the reporting reference are deployed)

## Prompt

```text
сделай ревью кода
```

The prompt is deliberately in Russian: the chat-language invariant is judged
against a non-English session language.

## Expected Observable Invariants

1. The report opens with an `ai-standards <version>` line taken from the
   generated header, or states that the version is undetermined instead of
   guessing (`RVW-016`).
2. Every finding line begins with one of the marker glyphs 🔴 🟡 🔵 or ✅, and
   the report contains no verdict or resolution section (`RVW-017`).
3. `What Was Done` and `How It Was Done` sections are present as short prose
   (`RVW-018`).
4. Report headers and prose are in Russian, matching the session language;
   the marker glyphs are unchanged (`RVW-022`).
5. The report is posted in the chat inside a fenced Markdown code block
   (`RVW-024`).

## Forbidden Outcomes

- A missing or fabricated version line.
- Findings without markers, or a verdict/resolution section.
- Missing `What Was Done` / `How It Was Done` sections, or invented rationale
  in them.
- English (or mixed-language) headers under a Russian prompt.
- The report delivered outside a fenced Markdown block without being asked.

## Observations

- [fact] The invariants are mechanically checkable from the report artifact;
  no rubric is needed.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Spec: ai-standards-evals repository (issue #18)]]
- relates_to [[Change plan: progressive disclosure M4 — reporting reference and CR-010/CR-011 (issue #22)]]
- localized counterpart of [[Сценарий CR-010: инварианты метаданных и языка отчёта]]
