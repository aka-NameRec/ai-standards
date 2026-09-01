---
title: 0tko3rt — Module Contract Record Notation
permalink: ai-standards/tasks/0tko3rt-module-contract-record-notation
---

# 0tko3rt — Module Contract Record Notation

Russian version: [0tko3rt-module-contract-record-notation.ru.md](0tko3rt-module-contract-record-notation.ru.md)

Date: 2026-09-01 · Branch: `feature/0tko3rt-module-contract-notation` · User issue: [#10](https://github.com/aka-NameRec/ai-standards/issues/10)

## Trigger

User issue #10: in two different projects an agent asked to create a module contract wrote a root-level `MODULE_CONTRACT.md` instead of a record under `docs/architecture/**`, without the frontmatter `title` Basic Memory requires. Verified against the sources: the `Module Contracts` section literally prescribed `Create MODULE_CONTRACT.md only for major, risky, shared, or architecturally non-obvious modules`, the root file appeared first in the discovery gate's canonical list and in the canonical-documentation enumerations (`structured-artifacts`, `basic-memory`), and no rule named a notation or a storage place for contracts. The failure was systemic — wording, not agent behavior.

## What Was Done

- **Decision record** `docs/decisions/2026-09-01-module-contract-record-notation.md` (+ `.ru.md`): a module contract is one `YYYY-MM-DD-module-contract-<module-slug>.md` record under `docs/architecture/**` with frontmatter `title` and `type: module-contract`; one record per contract; the root-level `MODULE_CONTRACT.md` is legacy — recognized, never created. Rejected alternatives: a dedicated `docs/contracts/**`, keeping the root file as target, tags-only marking. The frontmatter type (not the file name) is the classification marker, because decision records about contracts also carry `module-contract` in the slug.
- **Fragments**: `structured-artifacts` — Module Contracts rewritten to the record form; `MODULE_CONTRACT.md` dropped from the canonical enumeration. `module-contract-gate` — records first in Canonical Source with the root file as legacy; the cheap Task Start check globs `docs/architecture -g '*module-contract*'`; the scan pattern includes `type: module-contract`. `basic-memory` — canonical enumeration updated. `code-review` — the Architecture & Conventions pass finds contracts by the record marker.
- **Templates**: `module-contract.md` carries the record frontmatter; the three `standard-code-review` adapters and the report example cite a record path; the three `capture-knowledge` adapters write records.
- **Tooling**: `ai-sync doctor` reports a root-level `MODULE_CONTRACT.md` (repository root or knowledge-tree root) as a `legacy-module-contract-location` warning; reported, never auto-fixed — a move is a rename, and renames need a decision.
- **This repository migrated to its own rule**: `docs/MODULE_CONTRACT.md` (+ `.ru.md`) moved to `docs/architecture/2026-09-01-module-contract-ai-sync.md` (+ `.ru.md`), `type: module-contract` added, permalinks kept stable.
- **Docs**: usage guides (`structured-artifacts`, `basic-memory`, `code-review`, `conport`, en+ru) updated to the record notation; CHANGELOG gained an `Unreleased` entry.

## Verification

106 tests passed (rendered Module Contracts wording, the code-review fragment/template assertions updated to `type: module-contract` and the record citation form, new doctor tests: legacy locations flagged at both roots, a proper record accepted, the legacy name still out of scope of the note-name convention); `mypy` and `ruff` clean; render idempotent; `ai-sync check` passes; `doctor` reports 0 errors and the same 168 warnings as on `main` — no new findings, none for the new or renamed files.

## Deliberately Not Done

- Historical documents untouched: `docs/tasks/**`, `docs/archive/**`, past CHANGELOG entries, and the proposal documents keep their `MODULE_CONTRACT.md` wording as history.
- No version bump: the release preparation (manifest pin, tag) is a separate step; CHANGELOG carries the `Unreleased` section.
- Downstream root `MODULE_CONTRACT.md` files are not auto-migrated — doctor points at the record home; the move stays a per-project decision.

## Context For The Next Session

- Downstream projects that adopt ai-standards receive the new wording on their next standards update; the pin upgrade is per-project.
- A doctor warning landing in a downstream project is the expected migration nudge, not a regression.

## Observations

- [fact] The root cause of issue #10 was the wording naming exactly one artifact — the root file — with no place and no notation, so literal reading won in two projects.
- [decision] A module contract is a `YYYY-MM-DD-module-contract-<module-slug>.md` record under `docs/architecture/**` with frontmatter `title` and `type: module-contract`.
- [decision] A root-level `MODULE_CONTRACT.md` is legacy: recognized and read during discovery and review, never created, reported by `doctor` as `legacy-module-contract-location`.
- [fact] The frontmatter type, not the file name, is the precise classification marker: decision records about contracts also carry `module-contract` in the slug.

## Relations

- relates_to [[DECISION: module-contract-record-notation]]
- relates_to [[DECISION: module-contract-gate-feature-placement]]
- relates_to [[Module Contract: scripts/ai_sync.py]]
- localized counterpart of [[0tko3rt — Нотация записей модульных контрактов]]
