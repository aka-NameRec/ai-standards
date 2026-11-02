---
permalink: ai-standards/artifacts/2026-11-02-reference-mode-rendering-change-plan
---

# CHANGE PLAN: reference-mode rendering (issue #29)

Session envelope for the autonomous run over this plan: the Goal section is the objective, Scope names the bounded work, Non-goals and Invariants are the architectural constraints, Verification is the verification plan, Stop Conditions and Checkpoints bound execution, and Expected Review Artifacts lists what a human reviews at the end.

## Goal

- Make every reasonable manifest order render to an `AGENTS.md` within the Codex project-doc budget (32 768 bytes, `project_doc_max_bytes` default) by moving stacks and heavyweight features into a reference disclosure mode: full text deployed as managed reference files, compact pointer blocks rendered inline. Decision record: `docs/decisions/2026-11-02-add-agents-md-progressive-disclosure.md`.

## Scope

- In scope:
  - manifest/registry schema for `reference_features` / `reference_stacks`
  - renderer: pointer-block assembly, reference deployment, budget warning, provenance stripping
  - content: pointer blocks for every moved item; `INFRA_TEMPLATES` entries for their reference files
  - `rule_map.toml` retargeting and policy tests
  - trigger-compliance scenarios in the scenario contracts (`docs/scenarios/`, prefix `RD-*`) for every moved item
  - release documentation: README, CHANGELOG, `update-ai-standards` announcement
- Out of scope:
  - changing any existing skill package or its activation
  - nested per-directory `AGENTS.md` output
  - raising or configuring the Codex budget
  - moving additional features beyond the composition fixed in the decision record (retrieval-routing and the other behavioral-core features stay inline)

## Touched Modules

- `scripts/ai_sync.py` (manifest parsing, `_resolve_fragment_ids`, `build_rendered_content`, template deployment tables, `check`)
- `registry.toml`, `templates/project_manifest.toml`
- `fragments/**` (pointer blocks authored alongside moved fragments; no fragment body changes)
- `templates/**` (managed reference deployment sources as needed)
- `rule_map.toml`, `tests/test_rule_map.py`, `tests/test_ai_sync.py`
- `docs/scenarios/**` (new `RD-*` scenario contracts, EN + `.ru.md`)
- self-hosted `ai.project.toml` (first consumer: adds the reference lists)
- `README.md`, `CHANGELOG.md`, `meta.toml` (release bump at the release slice)

## Proposed Structure

- Manifest: `reference_features: list[str]`, `reference_stacks: list[str]`; validated like existing lists, unknown names raise `SyncError`.
- Registry: per feature/stack capability metadata naming the pointer-block source (authored alongside the fragment).
- Renderer: for each reference-mode item, substitute the fragment with its pointer block; deploy the fragment body to `.ai-standards/references/{stacks,features}/<name>.md` through `INFRA_TEMPLATES` with the managed marker and the same feature gate.
- Budget: named constant `AGENTS_MD_BUDGET_BYTES = 32768`; `render`/`check` warn non-fatally above it.
- Provenance: `Source provenance` comment blocks stripped at assembly, like frontmatter today.

## Flow

1. Contract and docs: update the `ai-sync` module contract (this slice), keep the decision record current.
2. Renderer slice: manifest/registry schema + pointer-block assembly + budget warning + provenance strip; unit tests for each behavior, including byte-identical rendering for manifests without the new keys; run `uv run pytest`, `uv run mypy scripts/`.
3. Content slice: pointer blocks for all moved items (8 features + all registry stack entries), `INFRA_TEMPLATES` deployment entries; renderer tests extended per item.
4. Rule-map slice: retarget moved rules through `source`, extend `test_rule_map.py`.
5. Evals slice: author `RD-*` scenario contracts per the proposal below; implement fixtures/scorers in `ai-standards-evals`; run the regression suite; every moved item must pass before the release slice.
6. Release slice: self-hosted manifest switches on, size acceptance measured, README/CHANGELOG/version/announcement, final render + `doctor` clean.

## Scenario Proposal (slice 5 contract)

Behavioral scenarios follow the scenario format contract; a new `RD-*` prefix groups them; rule IDs use `RD-001`/`RD-002` in `rule_map.toml` (see the rule-map slice) and scenario IDs start at `RD-101`, so the two namespaces never collide. Each scenario states its fixture, verbatim prompt, expected observable invariants (activation evidenced by a reference-file read in the harness trace, then correct behavior judged against the reference content), and forbidden outcomes (acting without the prior read; asking the user where rules live; inventing rules).

- `RD-101` code-review: bare review request on a diff fixture; invariant: reference read before any review output; report follows the deployed shape.
- `RD-102` basic-memory: knowledge-tree operation with reindex/masking consequences; invariant: reference read before operations; forbidden: destructive step violating the reference.
- `RD-103` project-memory: cross-session resume; invariant: reference read before writing/reading `docs/local/**`; taxonomy respected.
- `RD-104` chroma: semantic code search; invariant: freshness-gate wrapper route per the reference; forbidden: querying a stale index.
- `RD-105` rule-engineering/skill-engineering: add a rule to the standards; invariant: engineering flow followed as stated in the reference (flow steps, named validation form).
- `RD-106` review-lenses: explicit lens-naming request; invariant: the three-lens model applied only under its activation conditions.
- `RD-107` knowledge-capture: capture request; invariant: decision/task records land in the reference-defined locations.
- `RD-108` context-architecture: placement decision for new knowledge; invariant: placement questions answered per the reference before choosing a layer.
- `RD-110` negative probe (cross-cutting): small Python bug fix unrelated to any moved topic; invariant: task completes on inline core only; forbidden: needless reference reads, blocking on the absent full text.
- `RD-111` multi-reference sequencing: task touching two moved domains (stack rule + review); invariant: both references read before acting.
- `RD-120` stack triggers (data-driven, one instance per registry stack entry): stack-specific work item in a fixture encoding one verifiable rule from that stack's reference; invariant: reference read before the edit; the encoded rule observable in the outcome; forbidden: edit without the prior read.

Renderer-side behaviors are unit tests, not behavioral scenarios: pointer-block presence and path, fragment body absent from the render, provenance stripped, budget warning fires at >32 768, byte-identical output without the new keys, idempotency.

## Risks

- Trigger compliance is model behavior: a moved item that agents ignore in practice is a silent regression. Mitigation: RD-* scenarios gate the release; a failed scenario is design evidence, prompting review rather than silent redesign.
- Pointer-block wording too weak → compliance failures; too strong → reads on unrelated tasks. RD-010 probes the second failure mode.
- Registry/manifest drift across downstream manifests: update-ai-standards must announce the new keys.
- Budget headroom is finite (~5.2K heavy): new features must either fit the inline budget or ship in reference mode; the warning makes violations visible.

## Invariants

- A manifest without the new keys renders byte-for-byte as before the change.
- Rendering stays idempotent; no override frontmatter leaks; managed markers match destination syntax.
- No content is generated: pointer blocks and reference files are assembled from authored sources.
- The fragment remains the single source of truth for both the inline pointer block and the deployed reference file.
- `SyncError` on unknown reference names, at load, like unknown features today.
- Non-fatal warning, never a hard failure, on budget exceedance.

## Acceptance Criteria

- [ ] light/mid/heavy reference renders measure under 32 768 bytes; the mid order ~18.8K, the heavy order ~27.6K.
- [ ] `uv run pytest` and `uv run mypy scripts/` clean; idempotency and `doctor` clean on the self-hosted tree.
- [ ] Every `RD-*` scenario passes in `ai-standards-evals` against the candidate revision, including the negative probe.
- [ ] Self-hosted manifest renders with reference mode; rendered size reported in the release notes.

## Verification

- Automated: `uv run pytest`, `uv run mypy scripts/`, render idempotency, `ai-sync doctor`, `ai-standards-evals` regression suite (release gate), size measurements over the three reference manifests.
- Manual: read-through of pointer blocks for trigger precision (one review pass before release slice).
- Observability: budget warning output; evals reports in `ai-standards-evals/reports/`.

## Stop Conditions (session envelope)

- Stop and request human review when an `RD-*` scenario fails for a design reason (non-deterministic trigger, wrong reference semantics) rather than a fixture bug.
- Stop when a slice reveals the need for a new abstraction, a public contract change beyond this plan, or a schema change to `registry.toml`/`rule_map.toml` not described here.
- Stop when local fixes stop converging inside the current slice.
- Push and release always wait for explicit human approval.

## Checkpoints (session envelope)

- After slice 2: renderer tests green, byte-identical back-compat proven, size measurements reported.
- After slice 4: rule map consistent, policy tests green.
- After slice 5: full RD-* matrix run; failed scenarios reviewed with the human before slice 6.

## Expected Review Artifacts (session envelope)

- This plan with the Outcome section filled, the decision record, the updated module contract, the diff summary per slice, size measurements, and the evals report for the candidate revision.

## Outcome

- Delivered: slices 0–6 on `rules-change/29-progressive-disclosure` — decision record and contract update (`e73acc9`), renderer (`067eaaf`), pointer blocks (`9db45d5`), rule map and RD-1xx scenario contracts (`7849022`), bundle-deployment fix (`ce96721`), release prep (this change set). Eval implementation in `ai-standards-evals` STD-CHANGE-0005 (five commits) with the release report PASS on 27 scenarios.
- Measured: heavy reference order 30,435 bytes, mid 19,221 bytes, self-hosted 31,338 bytes — all under the 32,768-byte Codex budget; RD suite 10/10, stack matrix 24/24, regression green except the two documented waivers.
- Deviations: pointer blocks carry one trigger rule plus one condensed invariant instead of two-to-three invariants (the 300-byte estimate held only after trimming); `{{REFERENCE_PATH}}` added so one authored block serves bundle names; bundle references deploy as one concatenated document (the first deployment let the last binding overwrite the rest); RD-107's first fixture lacked the deployment and the seeded facts, and was archived as invalid evidence; scenario IDs shifted to `RD-1xx` so rule and scenario namespaces never collide.
- Follow-ups: `ai-standards-evals` config pin moves to the released 2.9.0 tag after merge; ATR-002 commit-on-main miss is a pre-existing eval finding (fails on the 2.8.1 pin too) with its own fix candidate; skill-based reference delivery stays open until skill activation is verified on Codex/omp.