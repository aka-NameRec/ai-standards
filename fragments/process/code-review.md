<!--
Source provenance:
- Adopted on 2026-08-06 from a request for a natural-language "code review" trigger with a report
  shape that stays identical across runs, tools, and models. The evidence and no-padding rules were
  normalized from public AI code-review prompting guidance (OpenAI Codex, Cloudflare); only the
  durable, tool-neutral parts were kept.
- The report shape is specified once, by the worked example below. An example pins a format down
  more reliably, and far more briefly, than a list of constraints describing that format.
- The `Verification` and `Dependencies` sections, the evidence rule about reading the code rather
  than the diff, and the small-fix policy were normalized from a hand-written per-repository review
  workflow that had been in daily use alongside this feature.
- Full rationale and rejected alternatives: docs/decisions/2026-08-06-add-code-review-feature.md
-->

## Code Review
- Treat a bare, unqualified request such as "code review", "review this", "сделай ревью", or "проверь код" as a request to run this workflow. A request that already names its own scope, mode, or lens takes priority over this default.
- Review the current diff, or the files the user names; do not expand into unrelated files.
- Default to reporting. Editing is limited to the small fixes allowed by `Fixing While Reviewing` below; anything beyond that waits for an explicit request, and then applies the smallest coherent patch.

### What To Check
- Correctness first: logic errors, missed edge cases, and failure paths that ignore the `Error Handling` rules in force here.
- Then Architecture & Conventions: violations of this project's architecture rules and of any active stack fragments. Check the changed modules against their active module contracts (`MODULE_CONTRACT.md` — ownership, non-goals, invariants), against accepted records under `docs/architecture/**`, and against the module map when one exists; a violation cites the exact contract clause it breaks. A changed major module with no contract is reported as a `(no contract)` note — a gap to fill, not a defect.
- Then Reuse: code that should have reused an existing project primitive, and duplication the change introduces on its own. Two new copies added by one change satisfy "prefer existing primitives", because neither copy is an existing primitive, and are duplication all the same; so is one intent expressed two different ways in sibling files.
- Then Efficiency: avoidable cost, such as repeated queries, per-row or per-render work that could be hoisted, and client-side handling of something the server should do. Judge it against realistic data volumes and say when the cost is currently free.
- Then Quality: readability, contract stability, test coverage of edge cases, and traps that only surface in production.
- Report a notable problem that predates the diff as well, marked `(pre-existing)` so it does not read as blame for this change. Whether to fix it stays the author's call, it can be offered as a follow-up instead, and it must not expand into an unrequested audit of the surrounding code.

### What Makes A Finding Reportable
- It cites a concrete file, and a line when one is available. No location, no finding.
- It names the specific rule or requirement it violates. If nothing maps, say so instead of inventing a rule.
- It was checked against the code, not against the diff. Before writing that something duplicates `X` or reuses `Y`, open `X` and `Y`; before writing about a query pattern, a migration risk, or a uniqueness constraint, open the model and the configuration. An unverified claim is either verified or not written.
- It is detailed enough that another agent could apply the fix without asking a clarifying question.
- Prefer fewer, high-confidence findings. An honestly empty section, stated as "None found.", beats a manufactured nitpick, and a risky suggestion is reported rather than guessed at.

### Report Shape
- Read `.ai-standards/code-review-report.md` and reproduce the shape of that worked example exactly: the same sections in the same order, and the same fields on every finding. That file is the only definition of the shape; nothing here restates it.
- If the file is absent, the project has not run `ai-sync sync-templates`. Say so, and fall back to this order: `Task` (when known), `What Was Done`, `How It Was Done`, then findings under `Correctness`, `Architecture & Conventions`, `Reuse`, `Efficiency`, and `Quality`, then `Verification` and `Dependencies`, each finding written as `<marker> <file>:<line> — <what is wrong> — violates: <rule>`.
- An open finding carries a coloured marker: 🔴 blocking, 🟡 should fix, 🔵 optional. A finding you fixed switches to ✅ and gains a `→ fixed:` tail on the same line; one you deliberately left alone keeps its coloured marker and gains `→ left as-is:` instead. There is no verdict and no resolution section — scanning the markers alone must answer what is left to do.
- Always include `What Was Done` and `How It Was Done` as short prose. The first is a factual summary of what the change does, read from the diff; the second names the reuse and conventions the change got right rather than findings, because a marker has to mean outstanding work for the markers to stay scannable. Do not invent rationale the diff does not show; when the change is trivially self-describing, one sentence each is enough.
- Fill `Verification` from what was actually run, with the command and its result, and name what was not checked. A silently omitted line reads as "everything was checked"; "backend tests pass, 34 of them; migrations and the UI not checked" is a useful sentence. Never carry a result over from one repository to another, and mark as stale any result the fixes below invalidated.
- Drop `Dependencies` entirely when the change is self-contained. Keep it only when the change requires a change in another repository, and say which repository and what it needs.
- Omit the `Task` line when no tracked reference is known; never invent one, and when `core/git-workflow` is enabled take the id from the branch name that rule already parses. Emit the full link only when the tracker base URL is actually knowable — from the session, from the project's own rules, or from a `tracker_url` entry in the manifest metadata that renders into this file's header. Never guess a URL.
- Write the whole report in the language the user is chatting in, headers included; never mix languages. The 🔴 🟡 🔵 ✅ markers carry no words and stay as they are. For Russian use: `Code Review` → `Код-ревью`; `Task` → `Задача`; `What Was Done` → `Что сделано`; `How It Was Done` → `Как сделано`; `Correctness` → `Корректность`; `Architecture & Conventions` → `Архитектура и конвенции`; `Reuse` → `Переиспользование`; `Efficiency` → `Эффективность`; `Quality` → `Качество`; `Verification` → `Проверки`; `Dependencies` → `Зависимости`; `violates` → `нарушает`; `fixed:` → `исправлено:`; `left as-is:` → `оставлено как есть:`; `None found.` → `Не найдено.`; `(pre-existing)` → `(существовало ранее)`.
- When the change spans more than one repository, produce one report per repository rather than a combined one, because each report is pasted into a different pull request. Name the repository in the heading as `## Code Review — <repository>`, keep every file path relative to that repository's root, and list the siblings under `Dependencies`.
- Post the report in the chat inside a fenced Markdown code block by default; save it to a file only when asked, defaulting to `docs/ai-memory/code-review/<YYYY-MM-DD>-<topic-slug>.md` when `structured-artifacts` is enabled. Say which destination you used.
- A later "resend the report" updates it: reclassify the findings already on record against what has since been fixed — by an explicit fix pass or by an ordinary follow-up like "fix the first one" — rather than reviewing the diff again from scratch.

### Fixing While Reviewing
- Reporting stays the default. The one exception is a small fix whose safety can be established by reading alone, without running anything: make it, and record it as a ✅ finding with a `→ fixed:` tail like any other.
- Safe to fix without asking: wrong or missing translations, typos in user-facing strings and comments, a defensive tightening that cannot change behaviour on current data, a missing `.gitignore` entry for generated junk, and plain inconsistencies with the surrounding code such as the wrong import or the wrong constant.
- Report instead of fixing: anything touching migrations, lock files, dependencies, or build configuration; changes to public types and contracts other code depends on; refactors, however obviously correct, because that is the author's decision and not a defect; the state of the git index; and anything whose safety would need a test run to establish.
- Review first, then fix, then write the report, so the report describes the state after the fixes. List the fixes in the chat as well, separately from the report, so they can be reviewed on their own.

### Relationship To Review Lenses
- This workflow answers a plain "code review" request and covers correctness and convention conformance alongside cleanup. `review-lenses` keeps its own explicit activation and its narrower three-lens cleanup model, and remains the one to use in CI.
- Enabling both is not a conflict: enabling `review-lenses` does not change what a bare "code review" request does.
- The feature-gated `standard-code-review` skill packages this workflow into the standard entry point: the same passes plus the full lens set (including the surrounding-convention and clone-detector DRY rules) and the architecture-and-contract check above, in one report. Its activation phrases («стандартный code review», "standard code review") select it over the bare default.

### Normalization Rules
- Keep the report shape defined by the example above and nowhere else, so it stays identical across runs and across tools.
- Keep framework-specific review heuristics in the relevant stack fragment rather than here.
- Do not encode tool- or vendor-specific review-bot output formats; keep those in local adapters.
