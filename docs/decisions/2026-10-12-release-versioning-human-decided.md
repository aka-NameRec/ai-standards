---
title: 'DECISION: release-versioning-human-decided'
permalink: ai-standards/decisions/2026-10-12-release-versioning-human-decided
---

# DECISION: release-versioning-human-decided

Russian localized version: [2026-10-12-release-versioning-human-decided.ru.md](2026-10-12-release-versioning-human-decided.ru.md)

## Status

Accepted

## Date

2026-10-12

## Context

During tasks #23 and #24 the repository version was bumped per task:
`bump-version save` ran inside each change set (2.8.0 for #23, 2.9.0 for
#24), although no release was being cut. The user caught this after the #24
merge: the version increases only when a release is performed; the release
moment is a human decision; a release may bundle several tasks. Both bumps
were reverted to 2.7.0, and the next releases (2.8.0, then 2.8.1) were cut
explicitly on the user's order.

## Decision

1. `bump-version save` runs only as part of a release cut explicitly ordered
   by the user — never inside a feature task, however complete.
2. Between releases, finished work accumulates under the CHANGELOG's
   `[Unreleased]` section; no version-numbered section is created per task.
3. At the release moment the version is chosen once, per SemVer over the
   accumulated changes since the previous release, and the CHANGELOG's
   pending entries are grouped under the release section.
4. The release flow stays: `bump-version save` → release-prep commit on
   `main` → push → `bump-version tag` → GitHub release.

## Why

- A version number is a promise about a shipped state; incrementing it per
  task invents release states that do not exist.
- Bundling is a release right: several tasks (#23, #24) shipped together in
  2.8.0, which per-task bumps would have mislabeled.
- The release moment reflects review and packaging readiness — knowledge the
  maintainer holds, not the agent.

## Alternatives Considered

### Per-task version bumps (the rejected behavior)

Rejected: produced an unreleased 2.9.0 and would mislabel bundled releases;
each bump also rewrites manifest pins and re-renders `AGENTS.md`, implying a
shipped state.

### Fully automated releases on merge to `main`

Rejected: the merge into `main` is itself human-ordered (see the
`autonomous-task-run` landing rule); automating the release would stack one
human gate on another mechanically.

## Consequences

### Benefits

- One version increment per actual release, SemVer-clean over bundled tasks.
- `[Unreleased]` becomes the single staging area; release notes are cut from
  it directly.

### Trade-offs

- Long-lived `[Unreleased]` sections need occasional hygiene (restored
  2.6.0–2.8.1 sections in the same session) so shipped entries do not linger
  unattributed.

## Observations

- [decision] The version increases only when a release is cut; the release
  moment is a human decision; a release may bundle several tasks.
- [fact] The per-task bumps of tasks #23 (2.8.0) and #24 (2.9.0) were
  reverted before 2.8.0 was properly released; the revert and the changelog
  history hygiene are recorded in task 25's record.

## Relations

- relates_to [[Task 25: autonomous-task-run skill]]
- relates_to [[DECISION: local-memory-date-prefix-naming]]
