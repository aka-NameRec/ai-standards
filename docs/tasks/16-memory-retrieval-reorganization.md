---
title: 'Task 16: memory and retrieval reorganization'
permalink: ai-standards/tasks/16-memory-retrieval-reorganization
---

# Task 16: memory and retrieval reorganization

Russian localized version: [16-memory-retrieval-reorganization.ru.md](16-memory-retrieval-reorganization.ru.md)

## Status

Implemented on branch `rules-change/16-memory-retrieval-reorganization` (phases 1–5, five commits). Release 2.4.0 tagging and downstream project migration follow the merge.

## Goal

Implement issue #16: separate project memory, knowledge retrieval, and code retrieval/intelligence — remove ConPort, introduce `retrieval-routing` and `project-memory`, rework integrations, add experimental `structural-code-intelligence` with an evaluation methodology.

## What Was Delivered

- Phase 1: ConPort removed from the registry, manifests, fragments, templates, and living documentation; deployment skill renamed to `deploy-ai-retrieval-stack` (capability-based, ConPort-free); marker-guarded retire mechanism for renamed managed templates; ConPort → `docs/local` migration instructions in `update-ai-standards`; decision record with supersession notes on the 2026-08-24 role separation and the knowledge-stack-roles overview.
- Phase 2: `retrieval-routing` policy layer (R1–R6 rules, routing table, capability/implementation split); deployment-skill gate moved from `chroma` to `retrieval-routing`.
- Phase 3: `project-memory` feature — `docs/local/**` taxonomy (context, decisions, progress, patterns, investigations, handoffs), write/read policies, explicit promotion; `[project_memory]` manifest section; relaxed `doctor` audit for the local area plus `local-memory-not-gitignored` advisory.
- Phase 4: integrations — `session-hygiene` (when vs what/how), `structured-artifacts` (`docs/local/**` boundary), `agent-usage-hygiene` (targeted retrieval as context discipline), `autonomy-boundaries` (state persistence never crosses a boundary; stop on material design choices), `basic-memory` (two knowledge classes), `knowledge-capture`; README feature groups and dependencies.
- Phase 5: experimental `structural-code-intelligence` with implementation-neutral routing rules and the A/B/C evaluation methodology; deliberately absent from the recommended stack and from the self-hosted manifest.

## Verification

- `uv run python scripts/ai_sync.py render/check --project-root .` — idempotent, clean.
- `uv run ruff check scripts tests`, `uv run mypy` — clean. (`ruff check` over the whole tree still reports 5 pre-existing findings in `templates/ai-infrastructure/scripts/code_index.py`, reproduced on `main`, untouched by this task.)
- `uv run python -m pytest` — 127 passed (7 new policy/retire/local-memory tests; gate-dependent tests updated).
- `ai-sync doctor --project-root .` — 0 errors.
- `rg -i conport` — matches only dated history (`docs/decisions/**`, `docs/tasks/**`, `docs/archive/**`, `CHANGELOG.md`, `docs/artifacts/**`) and intentional migration-instruction references in the `update-ai-standards` and `deploy-ai-retrieval-stack` templates.
- Behavioral scenarios A–E verified against the rendered rules: A (continue yesterday's task — routing table + session-hygiene retrieval rules), B (semantic code search — Chroma routing + freshness + narrowing), C (known exact class — direct source access), D (impact analysis — structural fragment rules; capability not enabled in the reference manifest by design), E (stop-and-consult — autonomy-boundaries stop condition).

## Follow-Ups

- Merge, release 2.4.0 (`bump-version`), tag (separate steps per the release workflow).
- Migrate the nine downstream projects with `conport` in their manifests (ai-standards itself plus eight local projects), decommission their `context_portal/` after data migration.
- Run the structural-code-intelligence A/B/C evaluation before any adoption decision (epic #19 tracks the rest).

## Observations

- [fact] All five issue #16 acceptance criteria are covered: ConPort absent from manifests/generated files/living docs; routing policy rules rendered and policy-tested; knowledge-tree tests protect `docs/local` from canonical-audit pressure; scenarios A–E verified; graph capability experimental with an evaluation gate.
- [fact] The retire mechanism is marker-guarded: managed copies of renamed templates are removed, user-rewritten files survive (tested).

## Relations

- implements issue #16
- follows [[DECISION: memory and retrieval reorganization]]
- planned by [[Change plan: memory and retrieval reorganization (issue #16)]]
- localized counterpart of [[Задача 16: реорганизация memory и retrieval]]
