---
name: standard-code-review
description: Run the project's standard code review in one pass — the code-review workflow plus the full review-lens set (including the surrounding-convention and clone-detector DRY rules) plus architecture and module-contract checks, reported in the fixed report shape. Use when the user asks for «стандартный code review», "standard code review", or says «сделай ревью по стандарту».
argument-hint: [scope or diff reference]
---
# Standard Code Review

One pass, one report. This skill packages the `code-review` workflow (its rules are rendered into `AGENTS.md`) together with the full review-lens set and the architecture-and-contract check. The bare "code review" trigger already runs the base workflow; this skill is its superset.

## Procedure

1. **Collect the scope.** The current diff, or the files the user names. Do not expand into unrelated files.
2. **Run the `code-review` passes** exactly as the rendered rules in `AGENTS.md` define them: Correctness, then Architecture & Conventions, then Reuse, Efficiency, Quality; evidence read from the code, not the diff; findings cite file, line, and the violated rule.
3. **Run the full lens set** on the same surface:
   - Reuse and Efficiency lenses, with the DRY rules in their full form — including the two that plain reviews usually skip: check how the surrounding code solves the same problem before extracting a shared primitive (deleting a wrapper is often the right fix), and run a clone detector over module- or package-sized surfaces, triaging its output.
   - Quality lens: readability, contract stability, edge-case test coverage, production-only traps.
4. **Check architecture and contracts.** For every changed module: find its module-contract record (a `docs/architecture/**` record marked `type: module-contract` in the frontmatter; a root-level `MODULE_CONTRACT.md` is a legacy form still worth reading — ownership, non-goals, invariants), the accepted decision records under `docs/architecture/**`, and the module map when one exists. A violation cites the exact clause. A changed major module with no contract is reported as a `(no contract)` note — a gap, not a defect.
5. **Apply the small-fix policy** from the rendered rules: safe-by-reading fixes are made and recorded as ✅; refactors, migrations, contracts, and anything needing a test run are reported.
6. **Produce one report** in the shape of `.ai-standards/code-review-report.md`, in the user's chat language, with `What Was Done` and `How It Was Done` always included. Lens findings go into the same report under their sections — the review produces one output, not two.

## Never

- Never split the result into a "review report" and a separate "lens report".
- Never invent rationale the diff does not show, and never add observations the documents do not state.
- Never commit or push without the user's explicit approval of the message.
- Never treat the built-in review command of the host tool as a substitute for this procedure when the user asked for the standard review.

## Report

State the scope, the passes that ran, the report location (chat by default), and anything the user still owes — for example, sources to confirm or contracts missing for changed modules.
