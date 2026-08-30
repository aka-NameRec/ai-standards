---
title: 'DECISION: standards-install-and-cold-start'
permalink: ai-standards/decisions/2026-08-29-standards-install-and-cold-start
---

# DECISION: standards-install-and-cold-start

Russian localized version: [2026-08-29-standards-install-and-cold-start.ru.md](2026-08-29-standards-install-and-cold-start.ru.md)

## Status

Accepted

## Date

2026-08-29

## Context

The 2.2.0 update skill only works where it is already deployed, which leaves two scenarios undefined: installing ai-standards into a project that has no deployment at all, and upgrading a deployment older than the skill itself (the bootstrap chicken-and-egg). The maintainer wants both scenarios served by short user prompts — a URL for install, a bare phrase for updates — with the agent surveying the project, announcing new features, and enabling only what the user confirms.

Three further facts constrain the shape. First, an agent given nothing but a repository URL will improvise an install unless the prompt binds it to the standard's own procedure. Second, a digest that announces features by `since` alone announces false positives for projects that already enabled them at the current content but kept an older pin — observed live on cockpit (pin 2.1.0, 2.2.0 content, two features already enabled). Third, the standards repository must be locally present for `render`/`sync-templates` regardless of the scenario, so source acquisition is a step of every mode, not a special case.

## Decision

The `update-ai-standards` skill becomes dual-mode; the name and activators stay. **Install mode** acquires the source, surveys the project (existing `AGENTS.md` and its provenance, stacks, docs layout and language, ConPort/Basic Memory presence, CI, tracker, agent environments), proposes the feature set one line at a time with recommendations, and deploys the confirmed set through `init-project`, the filled manifest, `render`, `sync-templates`, `check`, and `doctor`. **Upgrade mode** keeps the 2.2.0 procedure with two amendments: the digest announces only features that are new **and not yet enabled** (absent from the manifest `features` list), and a bootstrap preamble runs `render` + `sync-templates` before the digest whenever the deployed skill is missing or older than the file.

The skill file is written to be followed straight from a checkout: a cold-start header states that the file is the procedure when the target project has no deployment. The canonical user prompts are published in the README ("Standard Install And Update Prompts") and in the 2.2.1 release notes verbatim; install records `standards_source` in the manifest metadata, so update prompts need no URL afterwards.

## Why

- the skill file is the only artifact guaranteed to be present in every scenario — a checkout exists in install and bootstrap cases by definition, and the deployed copy exists in steady state — so one self-sufficient file serves both without a second distribution channel
- binding the prompt to the procedure file is what turns a URL into an installation of *this* standard rather than an improvised one; the procedure file, not the URL, is the contract
- excluding already-enabled features from the digest makes the announcement truthful, which the confirmation step depends on
- recording `standards_source` at install time is what lets later prompts stay short; the source location is knowledge about the deployment, so it belongs in the deployment's manifest, and it renders into the `AGENTS.md` header for free

## Alternatives Considered

### A separate `install-ai-standards` skill

Rejected. A project without a deployment has no deployment channel, so the install skill could only ever be followed from the repository checkout — the same cold-start property the dual-mode file already provides. Two skills would duplicate the bootstrap logic and put two file paths into the canonical prompts.

### Treat a bare URL as a sufficient install prompt

Rejected as the canonical form. The URL delivers the code; without naming the procedure, the agent improvises. The repository README routes agents to the skill file, so a URL-only prompt usually works, but the release notes publish the deterministic form that names the file.

### Announce by `since` alone, regardless of the manifest

Rejected. It produces false positives for deployments whose content is current but whose pin is stale — exactly the drift situation this release cycle also tightened elsewhere.

## Consequences

### Benefits

- both maintainer scenarios work from one short prompt, published verbatim in the release notes and the README
- the digest is truthful: nothing already enabled is re-announced, nothing enabled without confirmation
- later update prompts need no URL, because the deployment carries its own source pointer

### Trade-offs

- the skill file is now longer and carries mode routing; the deployed copy costs a few more lines in every agent environment
- `standards_source` is convention, not enforcement: deployments installed before 2.2.1 lack it until an update writes it

### Follow-ups

- publish the three canonical prompts in the 2.2.1 release notes verbatim
- the update skill for deployments of 2.2.0 gains the enabled-awareness only after its first update to 2.2.1; until then, bootstrap prompts name the manifest check explicitly

## Observations

- [decision] The update skill is dual-mode (Install/Upgrade) and self-sufficient from a checkout; no separate install skill exists.
- [decision] The upgrade digest announces only features that are new and absent from the manifest `features` list.
- [fact] Install records `standards_source` in the manifest metadata, and manifest metadata renders into the `AGENTS.md` header.
- [fact] The canonical prompts are published verbatim in the README and in the 2.2.1 release notes.

## Relations

- relates_to [[DECISION: standards-update-workflow]]
- relates_to [[Module Contract: scripts/ai_sync.py]]
