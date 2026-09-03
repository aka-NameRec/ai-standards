---
title: 0tkrpep — Non-Note Data Files Out Of The Knowledge Tree
permalink: ai-standards/tasks/0tkrpep-non-note-data-files-doctor-check
---

# 0tkrpep — Non-Note Data Files Out Of The Knowledge Tree

Russian version: [0tkrpep-non-note-data-files-doctor-check.ru.md](0tkrpep-non-note-data-files-doctor-check.ru.md)

Date: 2026-09-03 · Branch: `feat/0tkrpep-non-note-files-doctor-check` · User issue: [#13](https://github.com/aka-NameRec/ai-standards/issues/13)

## Trigger

User issue #13: a devcats project accumulated 37 phantom entities (7 PNG screenshots, 23 CSV dumps, 4 raw logs, 1 PDF, 2 TXT samples) in `docs/artifacts/**` of an indexed knowledge tree, and a 152K chat-export note alone cost 276 chunks / ~88s of CPU embedding time per reindex. The `basic-memory` fragment said "generated output belongs outside the tree" but never named binary and bulk-data files, and never mentioned the mask mechanism Basic Memory actually ships. The planning sessions (`0tkrne0`–`0tkrpc0`) verified the issue's claims against the Basic Memory 0.23.2 sources, rejected a hard index-blocking gate as infeasible, and fixed the policy recorded in `docs/decisions/2026-09-03-non-note-data-file-doctor-policy.md`.

## What Was Done

- **Decision record** `docs/decisions/2026-09-03-non-note-data-file-doctor-policy.md` (+ `.ru.md`): a universal non-Markdown detector plus indexer-honoured masks instead of a format deny-list; WARNING severity with an agent-side reindex gate instead of an ERROR exit-code gate; upstream `!` negation out of scope. Rejected alternatives: ERROR gate, blocking at initiation, upstream-PR-first, `docs/archive` as a data home.
- **Tooling** `scripts/ai_sync.py`: doctor reports `non-note-data-file-inside-knowledge-tree` (WARNING, never auto-fixed) for any non-Markdown, non-hidden, unmasked file under the knowledge tree; `_matches_indexer_mask` mirrors `basic_memory.ignore_utils.should_ignore_path` semantics (directory patterns match one path component at any depth, globs apply per component, `*` crosses `/`, `!` is inert); masks come from the `.gitignore` at the knowledge-tree root always and the global `.bmignore` beside the indexer configuration under the feature gate; declared overrides and `archive/` are not double-reported.
- **Fragment** `tools/basic-memory` (+ rendered `AGENTS.md`): a new bullet — binary and bulk-data files are indexed as notes; store them outside the tree or mask them via the knowledge-tree `.gitignore` or the global `.bmignore`; no `!` exceptions; reindex only after `ai-sync doctor` stops reporting them.
- **Docs** `docs/basic-memory-usage.md` (+ `.ru.md`): the Knowledge Tree Boundaries section names binary and bulk data as the same trap, states where the `.gitignore` lives (the indexer's project home, typically `docs/`, not the repository root), documents the mask quirks, the phantom-entity cleanup and one-time reindex after masking, and that `docs/archive` is walked until masked; the Reindexing Policy gates every explicit reindex on a clean doctor run.
- **Templates** `audit-knowledge-tree` (all three adapters): the doctor enumeration names the new finding, the classification adds a Data file row, and the repair order prescribes move-out-or-mask, never silent deletion.
- **CHANGELOG**: three `Unreleased` entries (guidance, doctor finding, skill).

## Verification

116 tests passed (10 new: data file flagged as WARNING, markdown-only tree quiet, hidden entries skipped, `.gitignore` masks at any depth, global `.bmignore` beside the indexer config, `archive/` skipped, no double reporting for overrides, `!` negation inert, blanket mask holds, findings never auto-fixed); `uv run mypy scripts/` and `uv run ruff check scripts tests` clean; render idempotent; `ai-sync doctor --project-root .` reports 0 errors with no new-code findings on this repository's own tree (the pre-existing hygiene warnings unchanged); CLI smoke test: a PNG under `docs/` is flagged, after `docs/.gitignore` with `*.png` the tree is quiet.

## Deliberately Not Done

- No version bump: release preparation (`bump-version`, `meta.toml [release]` pin, tag) is a separate step; CHANGELOG carries `Unreleased`.
- No auto-fix for the new finding: moving data files needs a judgement call, per the module contract's non-goals.
- No upstream Basic Memory changes: the `!`-negation PR was assessed (realistic, medium complexity, walker pruning semantics are the hard part) and deferred; the shipped approach does not depend on it.
- Push not performed: awaiting explicit approval.

## Context For The Next Session

- Downstream projects receive the fragment and skill updates on their next standards update; existing masked trees stay quiet, unmasked junk starts being reported as warnings.
- If the upstream negation PR ever lands, re-sync `_matches_indexer_mask` with the new `should_ignore_path` semantics before adopting masks with `!`.
- Release prep TODO: `bump-version` preview/save and the release tag per the Release Workflow.

## Observations

- [fact] The detection set is closed without enumerating formats: any non-note file under the tree is either masked (not indexed) or reported by the non-Markdown detector.
- [fact] Basic Memory walks `docs/archive` until a `.bmignore` line (`archive/`) excludes it, so the archive is not a default escape hatch for data files.
- [decision] The doctor finding is a WARNING plus an agent-side reindex gate; the blocking intent lives in the fragment, the Reindexing Policy, and the audit skill, not in the exit code.
- [decision] Upstream `!`-negation support was deferred; the local matcher mirrors `should_ignore_path` and must follow any upstream semantic change.

## Relations

- relates_to [[DECISION: non-note-data-file-doctor-policy]]
- relates_to [[ai-sync doctor: Deterministic Knowledge-Tree Audit]]
- relates_to [[Module Contract: scripts/ai_sync.py]]
- localized counterpart of [[0tkrpep — Не-заметочные файлы вне дерева знаний]]
