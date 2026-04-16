# DECISION: allow-explicit-follow-up-commits-on-protected-branches

Russian localized version: [2026-04-16-allow-explicit-follow-up-commits-on-protected-branches.ru.md](2026-04-16-allow-explicit-follow-up-commits-on-protected-branches.ru.md)

## Status

Accepted

## Date

2026-04-16

## Context

`ai-standards` previously prohibited commits on protected branches such as `main`, `master`, `develop`, and `staging` without exception.

That default rule was useful because it reduced the chance of accidental direct commits to the main delivery branch, especially in repositories with CI/CD, release automation, or expensive rollback paths.

However, the repository also encountered an immediate follow-up case after a merge and release-version update: a small lockfile adjustment remained on `main` even though the actual architectural change and version bump had already been merged correctly. Requiring yet another branch lifecycle for a tiny, tightly coupled correction added ceremony without adding meaningful review or safety value.

## Decision

The repository keeps protected branches as no-commit-by-default targets, but allows a narrow exception.

Direct commits on `main`, `master`, `develop`, or `staging` are allowed only when all of the following are true:

- the user explicitly authorizes the protected-branch commit for the current task
- the change is a small follow-up tightly coupled to work that has just been merged or released
- the change is not new feature work, a broad refactor, or a standalone behavior change

The rule that commit message text must be approved by the user before committing remains unchanged.

## Why

- preserves the main safety rail against accidental direct commits
- reduces unnecessary branch churn for tiny post-merge or post-release corrections
- keeps the exception narrow and operational instead of turning protected branches into ordinary work branches

## Alternatives Considered

### Keep the absolute prohibition with no exception

Rejected because it creates unnecessary friction for small, clearly related follow-up corrections after a merge or release step.

### Allow direct commits whenever the user says so

Rejected because that would weaken the original protection too much and make protected branches effectively normal working branches.

## Consequences

### Benefits

- ordinary feature and refactor work still goes through branch-based workflow
- small follow-up fixes such as lockfile or versioning metadata corrections can be completed without artificial ceremony
- the exception remains explicit, auditable, and user-controlled

### Costs Or Tradeoffs

- agents must judge whether a follow-up change is genuinely small and tightly coupled
- the policy becomes slightly more nuanced than a blanket prohibition

## Affected Modules

- `fragments/core/git-workflow.md`
- `AGENTS.md`

## Invariants And Constraints

- protected branches remain no-commit-by-default
- the exception requires explicit user authorization for the current task
- the exception must stay limited to small follow-up changes tied to work that has just been merged or released
- commit message approval remains mandatory

## Verification

- the rendered `AGENTS.md` reflects the narrowed protected-branch exception
- the repository can complete the current small follow-up lockfile correction on `main` under explicit user authorization

## Related Artifacts

- [../../fragments/core/git-workflow.md](../../fragments/core/git-workflow.md)
- [../../AGENTS.md](../../AGENTS.md)
