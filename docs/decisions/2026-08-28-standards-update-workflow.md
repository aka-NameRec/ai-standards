---
title: 'DECISION: standards-update-workflow'
permalink: ai-standards/decisions/2026-08-28-standards-update-workflow
---

# DECISION: standards-update-workflow

Russian localized version: [2026-08-28-standards-update-workflow.ru.md](2026-08-28-standards-update-workflow.ru.md)

## Status

Accepted

## Date

2026-08-28

## Context

A downstream update request — «please update ai-standards to the latest version available in its repository» — was underdefined at four points. Nothing said which checkout counts as the latest source. The `ai_standards_version` pin in `ai.project.toml` was never updated by any command: on a mismatch the renderer only added a header comment and rendered the source in use anyway, so a deployment could silently move off the version it claimed to pin. New features never arrived, because the renderer takes features strictly from the manifest's `features` list — correct under the opt-in model (see the placement decision of the same date), but it meant an update announced nothing and enabled nothing. And no rule asked the agent to show what changed or to confirm what to enable, so the agent improvised.

The maintainer's requirements: the request must stay short; the latest version is the newest release of the ai-standards repository on GitHub; new features must be announced with descriptions and enabled only after explicit confirmation suited to the project's stacks; and the bootstrap case — a deployment older than the skill itself — must be discoverable from the release notes.

## Decision

The `update-ai-standards` skill defines the whole update procedure; the request stays one phrase. The skill deploys with every ai-standards deployment that declares agents in `[tooling].agents` — no feature toggle, because it maintains ai-standards itself rather than a project process.

The procedure: compare the deployed version (`ai_standards_version` pin, falling back to the rendered header) with the latest release of the maintained checkout (`standards_source` manifest metadata when present, otherwise the checkout known to the session); refresh enabled features silently; announce features whose `[feature_meta]` `since` in `registry.toml` is newer than the deployed version, one line each, with a recommendation against the project's stacks and a link to the usage guide; ask once what to enable; apply only the confirmed features, move the pin, and verify with `render`, `sync-templates`, `check`, and `doctor` before reporting.

Supporting changes: `[feature_meta]` in `registry.toml` records the release that introduced each feature, so the digest is mechanical; `ai-sync check` fails on pin drift, `render`/`update` warn, and `doctor` reports `standards-version-drift`; release notes carry bootstrap instructions so a deployment older than the skill can adopt the update by hand once.

## Why

- the prompt is the interface, the skill is the contract: a bare phrase must produce a defined procedure, the same way a bare "code review" request does
- silence is the failure mode this fixes: a pin that disagrees with the rendered source, and features the project cannot know about, both become visible instead of silent
- the confirmation step is what reconciles updates with the opt-in model — an update must never change what a project opted into, and one question per update is the minimum fatigue that guarantees it
- shipping the skill unconditionally removes the chicken-and-egg problem: the tool that maintains deployments has to be present in every deployment it maintains

## Alternatives Considered

### Reference the skill by its repository path in the prompt

Rejected. A skill is resolved in the agent's own environment after deployment; a path into the ai-standards checkout turns the prompt back into improvisation instructions that only work when that checkout happens to be reachable. The legitimate bootstrap case is covered by the release notes instead.

### Enable new features by default at update time

Rejected. It contradicts the opt-in model and the gate placement decision of the same date: an update that flips features on is exactly the silent behavior change adopters cannot see. The single confirmation question achieves minimal fatigue with explicit consent.

### Render an activation fragment into `AGENTS.md`

Rejected for now. The skill's own description carries the activator phrases, adapters already ship through `sync-templates`, and an always-on fragment would cost context in every session of every project for a procedure that runs between releases.

### Parse the CHANGELOG as the only source of new-feature discovery

Rejected as the sole mechanism. Prose parsing is brittle; `[feature_meta].since` makes the digest deterministic, and the CHANGELOG remains the prose source the skill reads for notable non-feature additions.

## Consequences

### Benefits

- one phrase updates a deployment, with a fixed procedure and a visible diff of behavior
- pin drift is impossible to miss: `check` fails, `render`/`update` warn, `doctor` reports
- new capabilities reach adopters at update time instead of requiring them to read release notes proactively

### Trade-offs

- every deployment that declares agents gains one more adapter per agent; projects that never update pay nothing beyond disk
- `feature_meta.since` values pointing at an unreleased version must be reconciled with the actual release number during `bump-version`

### Follow-ups

- promote the module-contract discovery gate as the `module-contract-gate` feature (placement accepted in the same-date decision); the update skill will then announce it to older deployments exactly as designed

## Observations

- [decision] The update-ai-standards skill deploys to every declared agent without a feature toggle, because it maintains ai-standards itself.
- [decision] New features are announced at update time from `[feature_meta].since` and enabled only after one explicit confirmation; nothing is enabled by default.
- [fact] `ai-sync check` fails while `ai_standards_version` disagrees with the standards source in use; `render` and `update` warn, and `doctor` reports `standards-version-drift`.

## Relations

- relates_to [[DECISION: module-contract-gate-feature-placement]]
