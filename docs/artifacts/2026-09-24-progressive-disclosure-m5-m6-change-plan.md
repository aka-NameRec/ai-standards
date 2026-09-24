---
title: 'Change plan: progressive disclosure stage 3 — M5 basic-memory operations and M6 compression (issue #22)'
permalink: ai-standards/artifacts/2026-09-24-progressive-disclosure-m5-m6-change-plan
---

# Change plan: progressive disclosure stage 3 — M5 basic-memory operations and M6 compression (issue #22)

Russian version: [2026-09-24-progressive-disclosure-m5-m6-change-plan.ru.md](2026-09-24-progressive-disclosure-m5-m6-change-plan.ru.md)

Change set: `STD-CHANGE-0001` (continuation) · Branches:
`rules-change/22-m4-reporting-reference` (ai-standards),
`STD-CHANGE-0001-cr010-cr012` (ai-standards-evals) · Date: 2026-09-24

## Goal

Complete issue #22: relocate the basic-memory operational detail into a
deployed reference (M5), compress the project-memory and artifact-policy
enumerations (M6), and give the basic-memory rules their first behavioral
coverage. Merge into `main` follows once the gates pass.

## Scope

- M5: new `templates/basic-memory-operations.reference.md` deployed via
  `INFRA_TEMPLATES` as `.ai-standards/references/basic-memory-operations.md`
  (feature `basic-memory`). The fragment keeps routing (layers, dedicated
  tree, canonical vs working memory, genre doctrine, MCP scoping), the sync
  triggers, a compressed note-shape rule, and the pointer; the masking
  patterns, permalink and legacy-flag detail, rename mechanics, repair-tool
  specifics, and the reindex matrix move into the reference.
- New rule prefix `BM-*` in `rule_map.toml` (the basic-memory fragment had no
  rule ids); scenario contracts `BM-001` (note shape on create, verified from
  the fixture file system) and `BM-002` (sync-hygiene trigger after VCS
  operations, verified from the answer text), EN/RU pairs.
- M6: prose compression of `fragments/tools/project-memory.md` and
  `fragments/process/structured-artifacts.md` — same content, fewer tokens;
  no relocation, no normative change.
- `ai-standards-evals`: fixture builders and scorers for BM-001/BM-002
  (no live Basic Memory server required; BM MCP use instead of a repository
  file is a forbidden outcome for BM-001).

Out of scope: the knowledge-genre doctrine stays always-loaded (per the
migration-plan classification); no release/tag in this change set.

## Risks And Invariants

- The genre-doctrine bullets are dense normative text; compressing them is
  explicitly out of M6 scope to avoid an ungauged semantics change.
- BM scenarios must not touch the user's real Basic Memory store: fixtures
  render the `basic-memory` feature for AGENTS.md content only, and the
  prompts pin file-level outcomes inside the fixture.
- The M5 gate is honest about depth: BM-001/BM-002 protect the strongest
  user-visible rules (note shape, sync triggers), which stay always-loaded in
  compressed form; the moved mechanics are covered by the regression suite
  and render guarantees — stated here so the merge gate reads truthfully.

## Session Envelope

- Non-goals: no release, no push (requires explicit user approval), no changes
  to the code-review fragment in this stage.
- Stop conditions: eval-gate regression without an in-scope fix; contradictions
  with the scenario-format contract.
- Expected artifacts: this plan (EN/RU), scenario pairs, runner changes,
  comparison reports, updated task record and CHANGELOG.

## Verification

1. `ai-standards`: pytest, render idempotency, doctor — as before.
2. `ai-standards-evals`: ruff, mypy, pytest; BM scenario smoke runs.
3. Final merge-gate comparison: baseline `2.6.0-2026-09-23` vs branch HEAD —
   CR-001..CR-012 as regression, BM-001/BM-002 as new coverage, LLM judge
   included; then merge into `main` in both repositories (local merges).
