---
title: Scenario Format Contract
permalink: ai-standards/scenarios/scenario-format
---

# Scenario Format Contract

Russian localized version: [scenario-format.ru.md](scenario-format.ru.md)

This contract defines the structure of behavioral scenario files under
`docs/scenarios/` and the required behavior of any runner that executes them
(issue #17, Phase 5). Scenarios verify that the standards produce observable
behavior, not that Markdown matches prose. Execution machinery — runners,
harness adapters, result storage, compatibility matrices — belongs to the
`ai-standards-evals` specification (issue #18); this contract is the
standards-side interface it consumes.

## File Layout

- One scenario per pair of files: `<ID>-<slug>.md` (English) and
  `<ID>-<slug>.ru.md` (Russian localized pair), where `ID` matches
  `<PREFIX>-<NNN>` (for example `CR-001`). The prefix groups scenarios by the
  feature they exercise (`CR-*` for code review).
- Scenario IDs are stable: an ID is never reused for a different scenario.
- Every rule reference uses an ID from `rule_map.toml` in backticks; the
  policy tests verify that every referenced ID exists.

## Required Structure

1. Frontmatter with `title` and `permalink`; the title repeats as the `# H1`.
2. An intro paragraph naming the feature area, starting `Behavioral scenario
   …` (EN) / `Поведенческий сценарий …` (RU), with a `Verifies rules …` list
   of the rule IDs the scenario targets, and a status line (`draft` until the
   format is finalized and the scenario has run at least once).
3. `## Fixture` — the declarative pre-state and the diff (or input) under
   test, described concretely enough for a runner to construct it.
4. `## Enabled Features` — the standards features rendered during execution.
5. `## Prompt` — the verbatim prompt in a fenced code block.
6. `## Expected Observable Invariants` — numbered invariants, each annotated
   with the rule IDs it enforces. Invariants judge the outcome, never the
   wording.
7. `## Forbidden Outcomes` — enumerable failure modes.
8. `## Scoring Rubric` — optional; only where an invariant cannot be decided
   mechanically.
9. `## Observations` and `## Relations` per the knowledge-tree note rules.

The Russian pair mirrors the structure with localized headings (`Фикстура`,
`Включённые features`, `Ожидаемые наблюдаемые инварианты`, `Запрещённые
исходы`, `Наблюдения`, `Связи`); the `## Prompt` heading stays English in both.

## Policy Tests

`tests/test_rule_map.py` enforces the mechanical half: file naming and ID
uniqueness, localized pairs, required headings in both languages, a fenced
prompt block, and resolution of every rule and scenario reference between
`rule_map.toml` and this directory.

## Required Harness Behavior

A conforming runner (specified in #18, implemented in `ai-standards-evals`)
must:

1. construct the fixture deterministically from the scenario's declarative
   description;
2. execute the verbatim prompt through a harness adapter with the enabled
   features rendered;
3. capture the outcome artifact (the report or answer, plus execution events
   where the harness provides them);
4. evaluate every expected invariant and every forbidden outcome, mechanically
   where possible and by the scoring rubric where unavoidable;
5. report per-scenario verdicts and support the cross-harness compatibility
   matrix;
6. support baseline versus candidate comparisons of standards revisions on
   identical scenarios.

Divergence between harnesses on the same scenario is a finding to analyze —
shared rule problem, adapter problem, harness limitation, or model variance.

## Observations

- [fact] Invariants judge outcomes, never wording: the same scenario must pass on any harness that reaches the same decisions.
- [fact] The runner contract is required behavior only; its implementation is deliberately out of this repository's scope.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Migration plan: context architecture classification (issue #17)]]
- localized counterpart of [[Контракт формата сценариев]]
