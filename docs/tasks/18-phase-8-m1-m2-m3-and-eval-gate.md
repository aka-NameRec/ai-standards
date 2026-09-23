---
title: 18 — Phase 8: M1–M3 relocation and the release verification gate
permalink: ai-standards/tasks/18-phase-8-m1-m2-m3-and-eval-gate
---

# 18 — Phase 8: M1–M3 relocation and the release verification gate

Russian version: [18-phase-8-m1-m2-m3-and-eval-gate.ru.md](18-phase-8-m1-m2-m3-and-eval-gate.ru.md)

Date: 2026-09-23 · Branches: `rules-change/18-m1-skill-reference-procedure`,
`rules-change/18-m2-gate-reference`, `rules-change/18-m3-prose-compression`,
`rules-change/18-m3-retry` (all merged into `main` and pushed; M3 rejected
once by the eval gate and re-landed with the version-line bullet kept
verbatim)

## Trigger

Phase 8 of the Context Architecture migration plan: the three relocations
(M1–M3), each gated by a baseline-vs-candidate behavioral comparison from
`ai-standards-evals`. A move without a passing comparison is rejected.

## What Was Done

- **M1** (`34baa19`): the code-review pass procedure and the fixing policy
  moved from the always-loaded fragment into
  `templates/code-review/standard-code-review.procedure.md`, deployed by
  `ai-sync sync-templates` as the `standard-code-review` skill's
  `references/procedure.md`. The fragment keeps the reporting invariants
  (evidence, no-padding, marker semantics, report shape, trigger and scope
  routing) and slim pointers; section headings preserved for `rule_map.toml`.
- **M2** (`7e19573`): the Module Contract Discovery Gate detail (discovery
  commands, coverage criteria, reasoning constraints, index-entry shape,
  reporting contract) moved to
  `templates/module-contract-gate.procedure.md`, deployed as
  `.ai-standards/references/module-contract-gate.md` gated on the
  `module-contract-gate` feature. The fragment keeps the mandate, canonical
  sources, compressed routing, and the guarantees pinned by
  `test_module_contract_gate_fragment_keeps_its_guarantees`.
- **M3** (`293da96` rejected → `515f464` accepted): prose compression of the
  Report Shape enumerations. The first attempt dropped the version-line
  motivation and the agent omitted the `ai-standards <version>` line in
  CR-006 — the gate rejected it. The retry kept the version-line bullet
  verbatim; a guarantee test
  (`test_code_review_fragment_keeps_the_version_line_guarantee`) now pins the
  line, its fallback, and its motivation against future compressions.
- **Merge gate rule** (`b4d5b92`): a branch changing `fragments/**` or
  `templates/**` merges into `main` only with an attached eval comparison
  (baseline vs candidate, LLM judge included); merging without an ACCEPT
  verdict requires an explicit user decision.
- **Release gate** (`fedb274`): `bump-version tag --evals-report
  <release-report.json>` validates the behavioral verification report
  (kind, PASS verdict, revision match against the tag name, `main`, HEAD, or
  an explicit override) before creating the tag; documented in the Release
  Workflow (EN/RU), `AGENTS.md` re-rendered.
- `AGENTS.md`: 64,591 → 62,104 bytes across M1–M3 with all gates passed.

## Verification

- Every move gated: 9-scenario suite on the candidate branch, comparison
  against the previous accepted revision, LLM judge (GLM-5.3) over finding
  depth for CR-001/004/005/006 — see `ai-standards-evals` reports
  (`20260922-20*`, `20260923-*`). One judge calibration fix (CR-005 rubric
  falsely forbade referencing the existing `src/rows.py` module).
- Full suite: 146–147 passed on each candidate; `ai-sync render` idempotent;
  `ai-sync doctor` zero errors.
- Cross-agent (Phase 9 start): the Codex column of the matrix — 9/9 PASS on
  `ai-standards@main` (gpt-5.6-luna); recorded in the evals repository
  README and reports.

## Notes

- The M1 prerequisite "skill activation proven on two harnesses" is unmet
  (only Kilo locally, Codex added later for the matrix); the deviation is
  recorded in the M1 commit message and the eval gate ran on a single
  harness.
- `AGENTS.md` remains behavior-preserving by gate evidence, not by intent
  alone: every relocation and the compression were verified against the
  recorded scenarios.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Spec: ai-standards-evals repository (issue #18)]]
- localized counterpart of [[18 — Фаза 8: перемещения M1–M3 и релизный гейт верификации]]
