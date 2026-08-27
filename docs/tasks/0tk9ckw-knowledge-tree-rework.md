---
title: 0tk9ckw — Knowledge Tree Rework and Audit
permalink: ai-standards/tasks/0tk9ckw-knowledge-tree-rework
---

# 0tk9ckw — Knowledge Tree Rework and Audit

Task: `0tk9ckw` (umbrella; subtasks 0tk6h6b, 0tk6h8x, 0tk7xg0, 0tk85o3, 0tk868q, 0tk9bdz, 0tk9ckw, 0tk9d9t, 0tk9qdl, 0tk9qeh, 0tk9qqb, 0tk9t0y, 0tk9t95) · Branch: `feature/0tk9ckw-archive-history-in-docs-tree` · 2026-08-22 — 2026-08-27

Russian version: [0tk9ckw-knowledge-tree-rework.ru.md](0tk9ckw-knowledge-tree-rework.ru.md)

## What Was Done

**Pull request line (ai-standards):** reviewed #6 (code-review feature), #7 (knowledge tree), #8 (DRY pass), #9 (report unification). #6, #8, #9 merged by the user; conflict resolutions pushed into the contributor forks through the maintainer-can-modify flag (#8: CHANGELOG additive conflict; #7: additive test conflict). A live bug found in an untracked artifact — HTML managed markers corrupting `.py`/`.toml` templates — was fixed per-format with tests and merged to `main` locally (`5de0bcb`).

**Rework direction:** pull request #7 is not taken as opened. Two decisions define the rework: [archive-history-in-docs-tree](../decisions/2026-08-24-archive-history-in-docs-tree.md) and [knowledge-store-role-separation](../decisions/2026-08-24-knowledge-store-role-separation.md). #7 was integrated into this branch (`2ab86bf`) as the base for the rework.

**Documentation:** three method documents with README links — [knowledge genres](0tk9qoy-knowledge-genres.md), [ai-sync doctor](0tk9qpd-ai-sync-doctor.md), [audit-knowledge-tree skill](0tk9qpt-audit-knowledge-tree.md) — plus the [stack overview](../architecture/2026-08-27-knowledge-stack-roles.md) and `MODULE_CONTRACT.md`.

**Audit applied (0tk9t95):** `ai-sync doctor` found 264 warnings / 0 errors; `--fix` gave 90 notes frontmatter titles (permalinks stamped by the running Basic Memory sync); the skill's judgment half added Observations/Relations to the eight session documents and renamed one Russian H1 to fix a duplicate-title collision. Remaining: 158 warnings (78 notes without observations, 80 without relations) — deferred to periodic hygiene by design, since observation synthesis is forbidden to batch.

**Archive decision implemented:** chat exports moved `temp/` → `docs/archive/`; `doctor` skips the archive when auditing notes and warns (`archive-not-excluded`) when `.bmignore` does not exclude it; `-log-` rule globs updated to `docs/**/*-log-*.md`; chroma template documents the opt-in history collection.

**Cockpit side:** `git-updater` Basic Memory path narrowed from the repository root to `docs` (registry commit `dd4be88`; adapter re-created the project entry; retrieval verified).

## Findings Left for Hygiene

- ~20 bilingual decision pairs share an identical H1 across languages; the graph identifies notes by title, so these are duplicate identifiers. Fix by localizing the Russian H1, one file at a time.
- 78 notes without observations / 80 without relations: filled in only when a person works with the document.
- `docs/ai/project-rules.md` in git-updater sits inside its indexed tree (pre-#7 scaffold); five `-log-` files remain in that tree.

## Pending

- Push of `main` (marker fix) and of this branch (needs explicit user approval); release and downstream re-render; devcats `.ai-standards/` migration unblocked by the marker fix.

## Observations

- [fact] The marker bug artifact of 2026-08-03 described a real, unfixed defect; the fix landed only on 2026-08-24, and untracked artifacts remain one `git clean` away from loss.
- [fact] Conflict resolutions can be delivered into contributor forks without force-push when the maintainer-can-modify flag is set: a merge commit updates the pull request in place.
- [fact] Basic Memory stamps permalinks during sync once a file gains frontmatter; `doctor --fix` writes titles only.

## Relations

- relates_to [[DECISION: archive-history-in-docs-tree]]
- relates_to [[DECISION: knowledge-store-role-separation]]
- relates_to [[Knowledge Stack Roles]]
- localized counterpart of [[0tk9ckw — Переработка дерева знаний и аудит]]