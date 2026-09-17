---
title: Russian GitHub issues and September 2026 proposals
permalink: ai-standards/tasks/rules-change-russian-github-issues
---

# Russian GitHub issues and September 2026 proposals

Task `rules-change` (2026-09-17): three untracked September 2026 proposals in `docs/archive/` were studied and filed as GitHub issues, and a new project rule fixed the issue language.

## What was done

- Studied three proposals: memory/retrieval reorganization, Rule/Skill Engineering + Context Architecture + Standard Evals, and the `ai-standards-evals` spec.
- Filed Russian-language issues #16 (memory/retrieval reorganization), #17 (Rule Engineering / Context Architecture / Skill Engineering / Standard Evals), and #18 (`ai-standards-evals` spec); #17 and #18 are cross-linked because the evals repository implements the executable half of the Rule Engineering proposal.
- Added the "Issue Tracker Language" rule to `ai/project-rules.md` and its Russian pair to `ai/project-rules.ru.md`: issues are created exclusively in Russian, both title and description; verbatim technical names stay untranslated.
- Regenerated `AGENTS.md` with `ai-sync render`; `ai-sync check` passes.
- Commit `4b1aaba` on `main`: rule change plus the four archived `docs/archive/` files (three proposals and one discussion log).

## Observations

- [fact] The three September 2026 proposals are filed as issues #16/#17/#18 for consideration, not accepted; no direction is chosen yet, so no decision record exists for them.
- [fact] Issues #17 and #18 are tracked separately so methodology (standards) and infrastructure (the evals repository) can be accepted or rejected independently.
- [decision] GitHub issues in this repository are created exclusively in Russian, both title and description; verbatim technical names stay untranslated (rule "Issue Tracker Language" in `ai/project-rules.md`).
- [fact] The commit convention `task_id. (commit_type) message.` accepted `rules-change` as the task id for this change set.

## Relations

- localized counterpart of [[Задачи GitHub на русском и предложения сентября 2026]]