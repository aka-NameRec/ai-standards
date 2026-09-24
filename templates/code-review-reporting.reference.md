# Code Review Reporting Reference

Full reporting policy for the code-review workflow. The always-loaded
`Code Review` rules carry the trigger, the scope, the finding invariants, and
the shape pointer; the deployed worked example `.ai-standards/code-review-report.md`
defines the report shape. This reference carries the reporting policy detail.
Read it when writing or revising a code-review report. If this file is absent,
the project has not run `ai-sync sync-templates`; apply the fallback named in
the always-loaded rules.

## Markers

- An open finding carries a coloured marker: 🔴 blocking, 🟡 should fix,
  🔵 optional.
- A fixed finding switches to ✅ with a `→ fixed:` tail on the same line; a
  deliberately kept finding gains `→ left as-is:` instead.
- There is no verdict and no resolution section — the markers alone must
  answer what is left to do.

## What Was Done And How It Was Done

- Always include `What Was Done` and `How It Was Done` as short prose: what
  the change does (read from the diff), and the reuse and conventions it got
  right rather than findings. A marker has to mean outstanding work for the
  markers to stay scannable.
- Do not invent rationale the diff does not show; one sentence each is enough
  when the change is trivially self-describing.

## Verification

- Fill `Verification` from what was actually run, with the command and its
  result, and name what was not checked. A silently omitted line reads as
  "everything was checked" — "backend tests pass, 34 of them; migrations and
  the UI not checked" is a useful sentence.
- Never carry a result over from one repository to another, and mark as stale
  any result the fixes invalidated.

## Dependencies

- Drop `Dependencies` when the change is self-contained; keep it only when
  another repository must change, and say which one and what it needs.

## Task Reference

- Omit `Task` when no tracked reference is known; never invent one.
- With `core/git-workflow` enabled, take the id from the branch name that rule
  already parses.
- Emit a full link only when the tracker base URL is actually knowable — from
  the session, the project's rules, or a `tracker_url` entry in the manifest
  metadata — and never guess a URL.

## Multiple Repositories

- For a change spanning several repositories, produce one report per
  repository — each lands in a different pull request.
- Name it `## Code Review — <repository>`, keep every file path relative to
  that repository's root, and list the siblings under `Dependencies`.

## Destination

- Post the report in the chat inside a fenced Markdown code block by default;
  save it to a file only when asked, defaulting to
  `docs/local/code-review/<YYYY-MM-DD>-<topic-slug>.md` when `project-memory`
  is enabled. Say which destination you used.

## Resending The Report

- A later "resend the report" updates the findings already on record against
  what has since been fixed — by an explicit fix pass or an ordinary
  follow-up like "fix the first one" — rather than reviewing the diff again
  from scratch.
