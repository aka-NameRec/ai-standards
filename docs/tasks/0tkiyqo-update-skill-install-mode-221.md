---
title: '0tkiyqo — update skill install mode and the 2.2.1 release'
permalink: ai-standards/tasks/0tkiyqo-update-skill-install-mode-221
---

# 0tkiyqo — update skill install mode and the 2.2.1 release

Russian version: [0tkiyqo-update-skill-install-mode-221.ru.md](0tkiyqo-update-skill-install-mode-221.ru.md)

Date: 2026-08-30 · Released as 2.2.1 (tag `2.2.1-2026-08-30`, GitHub release published as Latest; `main` @ `cb65813` == origin)

## Trigger

After 2.2.0 the maintainer widened the goal: ai-standards is deployed in projects that are not his, and both maintainer scenarios — installing into a project with no deployment and upgrading an older one — had to work from short prompts. Verification of the prompt wording raised the deciding questions: a bare URL delivers the code but not the procedure, so canonical prompts must name the procedure file; and a digest that announces by `since` alone produces false positives for deployments whose content is current but whose pin is stale (observed live on cockpit: pin 2.1.0, 2.2.0 content, two features already enabled).

## What Was Done

- **The `update-ai-standards` skill became dual-mode and cold-start capable** (branch `feat/0tkiyqo-skill-install-mode`, commit `6cd0f23`): an **Install mode** (acquire the source, survey the project — existing `AGENTS.md` and its provenance, stacks, docs layout and language, ConPort/Basic Memory presence, CI, tracker, agent environments — propose features one line at a time with recommendations, deploy the confirmed set through `init-project` + manifest + `render` + `sync-templates` + `check` + `doctor`); a **cold-start header** making the file executable straight from a checkout; an **Upgrade mode** with a bootstrap preamble (`render` + `sync-templates` before the digest) and an **enabled-aware digest** announcing only features new *and* absent from the manifest `features` list. The claude/cursor adapters are regenerated from the SKILL.md body, so the three templates cannot diverge.
- **`standards_source` standardized**: recorded at install time in `[metadata]`, rendered into the `AGENTS.md` header by the existing metadata channel, read by every later update — update prompts need no URL afterwards.
- **Canonical prompts published** in the README ("Standard Install And Update Prompts", en + ru) and in the 2.2.1 release notes verbatim: cold install (URL + procedure file), bare-phrase update for deployments of this release or newer, and the bootstrap update prompt for older deployments.
- **Decision record** `2026-08-29-standards-install-and-cold-start` (en + ru): one dual-mode skill over a separate install skill; URL-only prompt rejected as canonical; enabled-awareness in the digest.
- **Release 2.2.1** (commit `cb65813` after a fast-forward merge — `bump-version tag` enforces tagging from `main`; the lesson cost one failed tag attempt): `bump-version save --part patch` (2.2.1, 2026-08-30), CHANGELOG `[2.2.1]` with the Canonical Prompts section, test fixture constants bumped, tag pushed, GitHub release published with the prompts verbatim.

## Verification

104 tests passed; `mypy` strict and `ruff` clean; `ai-sync check` green; `doctor` zero errors; `gh release view` confirmed the release as Latest, targeting `main`, not a draft. Cockpit's push state was verified before attempting a push — the maintainer had already pushed `917e091` (found "Everything up-to-date").

## Deliberately Not Done

- `standards_source` stays a convention, not enforcement: deployments installed before 2.2.1 lack it until an update records it.
- No code changes to `scripts/ai_sync.py` — the whole feature is procedure text, docs, and tests; the module contract needed no amendment this time.
- Cockpit's bootstrap is not completed from here: its pin is 2.1.0 against released 2.2.1, and finishing that belongs to a live run of the bare phrase in a cockpit session.

## Context For The Next Session

- The first «обнови ai-standards» run in cockpit doubles as the first live dogfood of the 2.2.1 skill: it will detect the pin drift, announce `code-review` and `knowledge-capture` (enabled-aware), enable on confirmation, and move the pin.
- `bump-version` without arguments proposes a minor bump; patch releases need `--part patch` explicitly.
- Release operations require a clean worktree, and tagging requires `main` — merge feature branches before tagging.

## Observations

- [decision] The update skill is dual-mode (Install/Upgrade) and self-sufficient from a checkout; the canonical prompts name the procedure file, not just the repository URL.
- [fact] The upgrade digest announces only features that are new and absent from the manifest `features` list; already-enabled features are never re-announced.
- [fact] `bump-version save` requires a clean worktree and `bump-version tag` requires the `main` branch; the default version proposal is a minor bump, patch releases need `--part patch`.
- [fact] `standards_source` is recorded at install time and renders into the `AGENTS.md` header via the manifest metadata channel.

## Relations

- relates_to [[DECISION: standards-install-and-cold-start]]
- relates_to [[DECISION: standards-update-workflow]]
- relates_to [[Module Contract: scripts/ai_sync.py]]
- relates_to [[0tkhikr — ai-standards 2.2.0 release session]]
