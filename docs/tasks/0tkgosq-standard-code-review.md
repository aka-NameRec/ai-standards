---
title: 0tkgosq — Standard Code Review Skill and Contract Checks
permalink: ai-standards/tasks/0tkgosq-standard-code-review
---

# 0tkgosq — Standard Code Review Skill and Contract Checks

Russian version: [0tkgosq-standard-code-review.ru.md](0tkgosq-standard-code-review.ru.md)

Date: 2026-08-28 · Branch: merged to `main` (commits `1da9e6d`, `23e08c9`; on `main` directly by user decision)

## Trigger

Contributor feedback (0tkgl9f, 0tkglwf, 0tkgld1): after the `code-review` feature landed, two similar tools coexist, and remembering to also run the lenses is error-prone. Verified against the fragments: the comparison theses hold verbatim (code-review covers the lens themes plus correctness/architecture/report/markers; lenses keep two extra DRY rules — surrounding-convention and clone-detector — plus the explicit fix mode; CI is the lenses' gate). The user's own review prompt expected lens checks and the `What Was Done` / `How It Was Done` sections — the latter are omitted by the old rule for standalone reviews.

## What Was Done

- **`standard-code-review` skill**, gated by the existing `code-review` feature, deployed to four agents (codex, kilo → `.codex|.agents/skills/code-review/standard-code-review/SKILL.md`; claude → `.claude/commands/standard-code-review.md`; cursor → `.cursor/rules/standard-code-review.mdc`). One procedure: code-review passes → full lens set including both extra DRY rules → architecture-and-contracts check → one report in the fixed shape, in the chat language. Activators: «стандартный code review», "standard code review", «сделай ревью по стандарту».
- **Architecture & Conventions pass** extended in the fragment: changed modules are reconciled with their `MODULE_CONTRACT.md` (ownership, non-goals, invariants), with accepted records under `docs/architecture/**`, and with the module map; a violation cites the exact clause; a changed major module with no contract is a `(no contract)` note, not a defect.
- **Report sections always on**: `What Was Done` and `How It Was Done` are no longer omitted for standalone reviews. The first is a factual summary of the change read from the diff; the second names what the change got right. Invented rationale stays out; a trivially self-describing change needs one sentence per section.
- **Docs**: code-review usage guide gained the skill subsection; review-lenses usage guide and the rendered `AGENTS.md` gained the CI bridge (the skill is the superset CI gate; `review-only` stays the minimal cleanup-only signal); README notes the skill.

## Verification

95 tests passed (deployment of the four adapters, activator phrase present, the fragment names `MODULE_CONTRACT.md` and `(no contract)`, the template shows the contract-clause citation form); render idempotent; `mypy`/`ruff` clean; `doctor` zero errors.

## Deliberately Not Done

- The review-lenses fragment is untouched — it remains the source of the lens rules the skill operationalizes; the skill restates the two DRY rules for self-containment and links back.
- No new feature or registry entry: the skill gates on the existing `code-review` feature, so adopters get it with no manifest change.
- CI pipeline files: the repository ships no CI; the usage docs describe the gate.

## Context For The Next Session

- A contributor draft, `docs/archive/0tkgv0g-module-contract-discovery-gate.md`, defines a **module-contract discovery gate**: before editing production code, run contract discovery (Basic Memory as index, canonical contracts from the repository), coverage criteria, re-discovery triggers, and reporting requirements. It is parked in `docs/archive/**` per the archive convention and is the natural input for the next rule/skill — promotion is a design decision, not yet made.
- Hygiene backlog unchanged: 78 notes without observations, 80 without relations, ~20 bilingual duplicate H1 pairs.

## Observations

- [fact] The standard review is a superset of the bare trigger: code-review passes, full lens set, and the architecture-and-contract check in one report.
- [fact] Contract coverage gaps are reported as `(no contract)` notes, not defects — the reviewer flags the gap instead of demanding contracts.
- [fact] `What Was Done` and `How It Was Done` are always included; rationale the diff does not show stays out.
- [fact] The skill gates on the existing `code-review` feature — adopters receive it without manifest changes.

## Relations

- relates_to [[Knowledge Stack Roles]]
- relates_to [[Module Contract: scripts/ai_sync.py]]
- localized counterpart of [[0tkgosq — Скилл стандартного code review и проверки контрактов]]