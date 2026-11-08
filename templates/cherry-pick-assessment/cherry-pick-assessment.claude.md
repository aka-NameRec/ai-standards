---
name: cherry-pick-assessment
description: Assess cherry-pick transfer risks before execution — resolve stated selectors (task ids, merge request, source branch, range, explicit SHAs) into a confirmed ordered SHA set against a named target branch, then judge history identity, companion dependencies, cross-service compatibility, applicability, testability, and cumulative effect into a PASS / REVIEW / STOP verdict. Use when the user asks to «оцени перенос коммитов», «проверь cherry-pick до выполнения», "assess cherry-pick safety", or "check which commits to cherry-pick"; do not use for regular code review, for executing the transfer, or for approving a release.
argument-hint: [transfer to assess]
---
# Cherry-pick Assessment

Assess one specific candidate set against one specific target branch state
before any transfer happens. The outcome is an evidence-backed technical
verdict — PASS / REVIEW / STOP — not an approval of a release and not the
transfer itself.

## Purpose And Boundaries

- Only analysis of the stated transfer intent against the stated target
  state; the deliverable is a justified technical verdict with evidence and
  knowledge boundaries.
- This skill never approves release readiness and never executes the
  transfer: performing the cherry-pick, resolving conflicts into the target,
  merging, pushing, rebasing, and resetting are outside its authority
  (possible future executor skill).
- PASS admits the set to a controlled transfer only; it is never a release
  permission.

## Input: Selectors, Resolution, Confirmation

The user states what to transfer and where; the skill resolves it into an
exact ordered SHA list. The user does not have to enumerate hashes.

1. The input names the source repository and the target branch explicitly.
   If only the current checked-out branch can serve as the target, echo it
   back and treat its HEAD as part of the confirmed input.
2. Selectors — any of, possibly mixed: task ids (matched against commit
   subjects, bodies, and branch names by the project's task-id conventions),
   a merge request (its commit list from the forge; unavailable → STOP with
   the reason), a source branch (commits reachable from it and missing from
   the target, from the merge-base), a commit range (its interpretation is
   fixed and echoed), explicit SHAs, or a mix.
3. Every explicit SHA is verified before use: it must exist in the source
   history, and its subject is echoed back — protection against typos and
   hashes pasted from a different repository.
4. Candidate-set completeness: commits joined to the selected ones by the
   project's task-id conventions — fixes, revert pairs, explicit follow-ups —
   join the candidate set. Resolution may only widen the set with
   evidence-backed companions; silent truncation is forbidden. A resolved
   superset of the asked-for intent is material for the dependency and
   cumulative-effect analyses, not an error.
5. Two-phase resolution: the skill resolves the selectors, presents the
   ordered list — SHA, subject, order (topological, not narrative), target
   HEAD — and proceeds with the analysis only after the user confirms this
   list. The verdict binds to the confirmed list and the target HEAD.
6. Ambiguity discipline: a selector that resolves ambiguously — a task id
   matching unrelated commits, an ambiguous merge-base, a merge commit
   without a clear primary parent line — and is not clarified by the user is
   a STOP, not a best-guess interpretation. If the set or the target state
   cannot be established, STOP. If local references may be stale, state that
   currency could not be confirmed.

## Target State

Fix the target HEAD and, when histories diverged, the merge-base. Interpret
ranges and merge commits unambiguously; record the exact commits the
assessment ran against.

## Allowed Actions

Read Git data, sources, tasks, tests, and documentation; research
architecture and dependencies; run safe read-only checks. Trial application
happens only in an isolated throwaway tree — never in the user's working
branch — and never with unverified scripts that have side effects. When
isolation is impossible, refuse to simulate and record the limitation.

## Forbidden Actions

No recorded cherry-pick, no conflict resolution saved into the target, no
push, merge, rebase, or reset, no database schema changes, no changes to
external systems, no production approval. On STOP, do not proceed to
execution.

## Analysis A — History And Identity

Fix the actual divergence; find already-transferred or equivalent changes
(including under different SHAs), partial carries, and rollbacks. Do not
treat textual equality as unconditional functional equivalence. A merge
commit without a selected primary parent line is a STOP.

## Analysis B — Completeness And Dependencies

For each commit find affected components, related commits and tasks, new
calls, interfaces, settings, events, migrations, and build dependencies.
Establish whether mandatory companion changes exist in the target branch.
Classify dependencies as confirmed, probable, or unverified. A proven
missing mandatory dependency is a STOP; a substantial probable one is a
REVIEW. Absence of Git conflicts says nothing about completeness.

## Analysis C — Compatibility

Check affected APIs, message-broker events and their consumers, serialization
formats, database migrations, background jobs, feature flags, library
versions, configuration, and cross-service dependencies. For each risk name
the known consumers, the compatibility constraints, and the evidence
sources. A proven incompatibility is a STOP; a substantial unverified one is
a REVIEW.

## Analysis D — Applicability

Find overlapping changes, re-transfers, opposite edits, and semantic context
differences. In a safe isolated trial, record conflicts without resolving
them into the real tree. A substantive conflict is usually REVIEW; a proven
incompatibility is a STOP. A successful trial does not guarantee business
correctness.

## Analysis E — Testability

Identify existing unit, integration, and contract tests and migration checks;
name the affected business scenarios as far as the code confirms them.
Strictly separate performed, recommended, unavailable, and not-found checks.
Never invent tests and never claim full regression is unnecessary while the
impact area is not established.

## Analysis F — Cumulative Effect

Assess the whole confirmed set in its confirmed order: individually
applicable commits may contradict each other. Check cross-repository
dependencies as far as access allows; when a consumer repository is
unavailable, name the unknown explicitly.

## Verdict

- **STOP**: ambiguous transfer object (including unclarified ambiguous
  selectors); proven missing mandatory dependency; proven incompatibility;
  contradictory set; attempted authority overrun.
- **REVIEW**: substantial probable dependency; unknown consumer of a critical
  contract; substantive conflict; insufficient verification of an important
  path; critical access limitation.
- **PASS**: the set is established, mandatory directions researched, no
  blocking evidence and no substantial unresolved unknowns; analysis
  boundaries stated.
- Competing grounds resolve to the most restrictive outcome:
  STOP > REVIEW > PASS. Reason codes are allowed, e.g. `ALREADY_PRESENT`
  (a re-transfer is not needed).

## Evidence Discipline

Mark every material statement as **FACT** (exact SHA / file / line / command
result), **HYPOTHESIS** (a justified inference), or **UNKNOWN** (not
researched, and why it matters). Never present unexecuted tests as passed;
never hide unknowns; never substitute concrete evidence with abstract "there
may be risks" phrasing.

## Stopping And Validity

On STOP: stop the simulation, present the concrete reason, evidence, and the
minimal next action. On REVIEW: hand the human a clearly formulated question
and the missing checks; do not continue automatically. Any change to the
target HEAD, the confirmed set, or its order invalidates the verdict:
re-resolve and re-assess; never reuse a stale verdict.

## Mandatory Report

Verdict headline with reason codes; source repository, source refs and SHAs;
target repository, branch, and HEAD; the resolution record — which selectors
were stated and the confirmed list they resolved into; the commit list in
order; the purpose of each change; checked facts with evidence; confirmed
and probable dependencies; unknowns; performed / recommended / unavailable
checks; the concrete next action. Never state production readiness.

## Non-goals

No transfer execution, no conflict resolution into the target, no merge
request creation, no release approval, no universal analysis of all business
scenarios, no numeric risk scoring, no QA/QC/AF regulation changes.
