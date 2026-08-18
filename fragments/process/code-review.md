<!--
Source provenance:
- Adopted on 2026-08-06 from a request for a natural-language "code review" trigger with a report
  shape that stays identical across runs, tools, and models. The evidence and no-padding rules were
  normalized from public AI code-review prompting guidance (OpenAI Codex, Cloudflare); only the
  durable, tool-neutral parts were kept.
- The report shape is specified once, by the worked example below. An example pins a format down
  more reliably, and far more briefly, than a list of constraints describing that format.
- Full rationale and rejected alternatives: docs/decisions/2026-08-06-add-code-review-feature.md
-->

## Code Review
- Treat a bare, unqualified request such as "code review", "review this", "сделай ревью", or "проверь код" as a request to run this workflow. A request that already names its own scope, mode, or lens takes priority over this default.
- Review the current diff, or the files the user names; do not expand into unrelated files.
- Default to reporting only. Edit code only when the user explicitly asks for fixes, and then apply the smallest coherent patch.

### What To Check
- Correctness first: logic errors, missed edge cases, and failure paths that ignore the `Error Handling` rules in force here.
- Then Architecture & Conventions: violations of this project's architecture rules and of any active stack fragments.
- Then Reuse, Quality, and Efficiency: duplication that should reuse an existing project primitive, readability and contract stability, and avoidable noise.
- Report a notable problem that predates the diff as well, marked `(pre-existing)` so it does not read as blame for this change. Whether to fix it stays the author's call, it can be offered as a follow-up instead, and it must not expand into an unrequested audit of the surrounding code.

### What Makes A Finding Reportable
- It cites a concrete file, and a line when one is available. No location, no finding.
- It names the specific rule or requirement it violates. If nothing maps, say so instead of inventing a rule.
- It is detailed enough that another agent could apply the fix without asking a clarifying question.
- Prefer fewer, high-confidence findings. An honestly empty section, stated as "None found.", beats a manufactured nitpick, and a risky suggestion is reported rather than guessed at.

### Report Shape
- Read `.ai-standards/code-review-report.md` and reproduce the shape of that worked example exactly: the same sections in the same order, and the same fields on every finding. That file is the only definition of the shape; nothing here restates it.
- If the file is absent, the project has not run `ai-sync sync-templates`. Say so, and fall back to this order: `Task` (when known), `What Was Done`, `How It Was Done`, then findings under `Correctness`, `Architecture & Conventions`, and `Reuse / Quality / Efficiency`, each written as `<marker> <file>:<line> — <what is wrong> — violates: <rule>`.
- An open finding carries a coloured marker: 🔴 blocking, 🟡 should fix, 🔵 optional. A finding you fixed switches to ✅ and gains a `→ fixed:` tail on the same line; one you deliberately left alone keeps its coloured marker and gains `→ left as-is:` instead. There is no verdict and no resolution section — scanning the markers alone must answer what is left to do.
- Keep `What Was Done` and `How It Was Done` as short prose, and omit both only for a standalone review with no implementation work behind it. Omit the `Task` line when no tracked reference is known; never invent one, and when `core/git-workflow` is enabled take the id from the branch name that rule already parses. Give the full link, not the bare id, whenever the tracker base URL is knowable — from something the user said in this session, from the project's own rules, or from a `tracker_url` entry in the manifest metadata that renders into this file's header; fall back to the bare id only when it is not, and never guess a URL.
- Write the whole report in the language the user is chatting in, headers included; never mix languages. The 🔴 🟡 🔵 ✅ markers carry no words and stay as they are. For Russian use: `Code Review` → `Код-ревью`; `Task` → `Задача`; `What Was Done` → `Что сделано`; `How It Was Done` → `Как сделано`; `Correctness` → `Корректность`; `Architecture & Conventions` → `Архитектура и конвенции`; `Reuse / Quality / Efficiency` → `Переиспользование / Качество / Эффективность`; `violates` → `нарушает`; `fixed:` → `исправлено:`; `left as-is:` → `оставлено как есть:`; `None found.` → `Не найдено.`; `(pre-existing)` → `(существовало ранее)`.
- When the change spans more than one repository, produce one separate report per repository instead of a combined one, because each repository gets its own pull request and each report is pasted into a different description. Name the repository in the heading, as `## Code Review — <repository>`, and drop that suffix when only one repository is involved. Keep every file path relative to the root of the repository that report belongs to, and add one line to `How It Was Done` naming the sibling repositories, so a reviewer seeing a single pull request knows the change is part of a set.
- Post the report in the chat inside a fenced Markdown code block by default; save it to a file only when asked, defaulting to `docs/ai-memory/code-review/<YYYY-MM-DD>-<topic-slug>.md` when `structured-artifacts` is enabled. Say which destination you used.
- A later "resend the report" updates it: reclassify the findings already on record against what has since been fixed — by an explicit fix pass or by an ordinary follow-up like "fix the first one" — rather than reviewing the diff again from scratch.

### Relationship To Review Lenses
- This workflow answers a plain "code review" request and covers correctness and convention conformance alongside cleanup. `review-lenses` keeps its own explicit activation and its narrower three-lens cleanup model, and remains the one to use in CI.
- Enabling both is not a conflict: enabling `review-lenses` does not change what a bare "code review" request does.

### Normalization Rules
- Keep the report shape defined by the example above and nowhere else, so it stays identical across runs and across tools.
- Keep framework-specific review heuristics in the relevant stack fragment rather than here.
- Do not encode tool- or vendor-specific review-bot output formats; keep those in local adapters.
