# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Fixed

- The `code-review` fragment's default file-save destination for review reports pointed at the retired `docs/ai-memory/**` area (issue #20): now `docs/local/code-review/<YYYY-MM-DD>-<topic-slug>.md`, and the enabling feature is `project-memory` (the owner of the `docs/local/**` area), not `structured-artifacts`. Issue #12, if accepted, replaces this line again with the `temp/` flow.

## [2.5.0] — 2026-09-21

### Added

- **New feature `rule-engineering`** (user issue #17, phases 0–1; decision record `docs/decisions/2026-09-19-adopt-rule-engineering-initiative.md`): one Rule Engineering process for every normative rule regardless of source — nine quality properties (atomic, unambiguous, actionable, properly scoped, observable, unique by behavioral overlap, non-conflicting with explicit precedence, correct abstraction level, portable), the interpretation surface concept, the engineering flow from candidate knowledge to accept/adapt/reject with a mandatory validation form per rule, and context placement principles. Existing rules are not mass-rewritten; adoption is incremental.
- Baseline artifact for the initiative: `docs/artifacts/2026-09-19-rule-engineering-baseline.md` (both languages) — repository measures at release 2.4.0, current rule-related behavior, and candidate scenarios for future comparison.
- Usage guides `docs/rule-engineering-usage.md` / `.ru.md`; feature registered in `registry.toml` with `feature_meta` `2.5.0` and enabled in the self-hosted manifest.
- **Rule traceability map `rule_map.toml`** (issue #17, Phase 2; decision record `docs/decisions/2026-09-19-rule-traceability-design.md`): stable rule IDs (`RE-001`–`RE-006` seeded for the `rule-engineering` fragment) bound to fragment, section anchor, one-line expected behavior, and scenario references reserved for `ai-standards-evals` (issue #18). Policy tests in `tests/test_rule_map.py` validate IDs, anchors, and that rule IDs never render into `AGENTS.md`.
- **Phase 3 dogfooding of Rule Engineering on the code-review feature** (issue #17; artifact `docs/artifacts/2026-09-21-code-review-rule-engineering-dogfooding.md`): the fragment decomposed into 32 atomic normative behaviors mapped as `RVW-001`–`RVW-032`; the ambiguity/overlap/conflict review found no rule changes required, with three overlaps documented and explicit precedence. First behavioral scenario contracts `docs/scenarios/CR-001`–`CR-003` (both languages) are wired to the map by policy tests. A pre-existing placement issue is reported, not fixed: HTML provenance comments in fragments render into downstream `AGENTS.md`.
- **Phase 4 context architecture** (issue #17; artifact `docs/artifacts/2026-09-21-context-architecture-migration-plan.md`): new feature `context-architecture` — the seven-layer placement model, ordered placement questions with the latest-loading tie-break, and the control-plane invariant with a reduction gate (`CA-001`–`CA-005` in `rule_map.toml`). The self-hosted `AGENTS.md` is classified against the model and a migration plan records Phase 8 relocation candidates (code-review procedural body, gate details, prose compression), each gated by behavior-preserving comparisons. No physical moves in this phase.
- **Phase 5 scenario format contract** (issue #17): `docs/scenarios/scenario-format.md` / `.ru.md` defines the scenario file layout, required structure (fixture, enabled features, verbatim prompt, expected observable invariants, forbidden outcomes, optional scoring rubric), and the required behavior of a conforming runner — whose implementation stays with `ai-standards-evals` (issue #18). Policy tests enforce the mechanical half on both languages.
- **Phase 6 skill engineering** (issue #17; artifact `docs/artifacts/2026-09-21-skill-engineering-dogfooding.md`): new feature `skill-engineering` (policy base `rule-engineering`) deploying the `skill-engineering` domain skill for codex, cursor, claude, and kilo — authoring rules (`skill-authoring` as its first section), the four validation questions, and the lifecycle gates. The skill itself was authored through Rule Engineering: the public worksheet maps candidate guidance to accepted/adapted/rejected verdicts and seeds `SE-001`–`SE-009` in `rule_map.toml` (new optional `source` field for rules living in template skills). Also fixed here, disclosed: the test version pin left at `2.3.0` had broken four tests since the 2.4.0 release — the suite is fully green again.
- **Phase 7 activation and effect scenarios** (issue #17): the scenario format contract gains a second scenario kind — activation trigger sets (positive/negative/boundary cases with expected `should_trigger`) — and the required-harness-behavior list gains with-skill/without-skill ablation runs. Defined: `TRG-001` (standard-code-review triggers), `TRG-002` (skill-engineering triggers), and the behavior scenario `SK-001` (the skill-authoring justification gate), all linked to `RVW-029`/`SE-*` in `rule_map.toml` and enforced by kind-aware policy tests. Execution belongs to `ai-standards-evals` (issue #18).

### Changed

- **The README `Import External Rules` flow is restated as a special case of Rule Engineering** (both languages): the standard import prompt now routes every candidate through the Rule Engineering properties and requires a validation form per accepted rule. No renderer behavior changed.

## [2.4.0] — 2026-09-18

### Changed

- **Memory and retrieval reorganization** (user issue #16; decision record `docs/decisions/2026-09-18-memory-retrieval-reorganization.md`): the standards now separate project memory, knowledge retrieval, and code retrieval/intelligence. ConPort is removed entirely — the feature, registry entry, default manifest, fragments, templates, and living documentation — while its useful semantics (context, decisions, progress, patterns, explicit relationships, cross-session continuation) survive as tool-independent rules. Dated history keeps its mentions with supersession links on `docs/decisions/2026-08-24-knowledge-store-role-separation.md` and `docs/architecture/2026-08-27-knowledge-stack-roles.md`. Phases 6–7 (harden autonomy, multi-agent) are tracked separately in issue #19.
- **New feature `retrieval-routing`** — the tool-neutral policy layer over every retrieval capability: retrieve before broad exploration, consider enabled capabilities, route by information need (routing table: project memory / canonical documentation / Chroma / direct source / structural graph / final verification), retrieval as evidence discovery, verification at the authoritative layer, progressive escalation. The deployment-skill template gate moved from `chroma` to `retrieval-routing`.
- **New feature `project-memory`** — local cross-session working memory under `docs/local/**` (gitignored by default, configurable via `[project_memory]` `local_tree`): fixed taxonomy (`context`, `decisions`, `progress`, `patterns`, `investigations`, `handoffs`), write policy (curated state store, not an execution log), read policy (targeted queries, never whole-tree reads), and explicit promotion into canonical documentation. Works standalone; works best with `basic-memory` indexing the area — capability deliberately separated from implementation.
- **`ai-sync doctor`** audits the local-memory area with relaxed canonical rules (readability only) and reports `local-memory-not-gitignored` when the area exists without a covering `.gitignore` pattern; the repair path never touches local notes.
- **`sync-templates` retires renamed templates**: a marker-guarded mechanism (`RETIRED_TEMPLATE_DESTINATIONS`) removes deployed managed copies of templates that no longer ship and prunes emptied directories; user-rewritten files survive. Covered by tests.
- **The deployment skill is renamed `deploy-ai-retrieval-stack`** and is now capability-based: it deploys only the layers enabled in the manifest (Basic Memory, Chroma), refuses to deploy ConPort, and stops on a legacy ConPort installation. The `update-ai-standards` skill (all three adapters) carries a full ConPort → `docs/local` migration procedure: detect, export via MCP or SQLite, lay out by taxonomy, decommission only after the user confirms the migrated notes.
- **Integration fragments reworked**: `session-hygiene` says when state must be preserved (a new session retrieves the handoff, never all accumulated memory); `structured-artifacts` binds working memory to `docs/local/**` (replacing `docs/ai-memory/**`); `autonomy-boundaries` gains the stop condition for material design choices (preserve state and ask, never record a new decision and continue silently) and working-state rules (persisting state never crosses a boundary); `agent-usage-hygiene` treats targeted retrieval as context discipline; `basic-memory` names its two knowledge classes; `knowledge-capture` updates local project memory instead of mirroring to ConPort.
- **README (both languages)** groups features by concern (Knowledge and context / Engineering artifacts / Code intelligence / Execution governance) and records feature dependencies.
- **New experimental feature `structural-code-intelligence`**: retrieval over code-entity relationships (call paths, dependency paths, impact analysis), implementation-neutral (Graphify is one possible backend, no tool commands in the standards), deliberately absent from the recommended stack and the self-hosted manifest. Adoption waits for the A/B/C evaluation methodology shipped at `docs/structural-code-intelligence-evaluation.md` (both languages).
- **Policy tests** now guard the reorganization: rendered rules never mention ConPort; routing, project-memory, integration, and experimental-capability invariants are asserted; retire and relaxed-audit behavior is covered. Test fixtures no longer reference the removed feature.

## [2.3.0] — 2026-09-03

### Changed

- **Non-note data files stay out of the knowledge tree** (user issue #13): the `basic-memory` fragment and the usage guide (both languages) now state explicitly that binary and bulk-data files (images, PDFs, raw logs, CSV dumps) are indexed as notes and belong outside the tree — or, while notes cite them, behind a `.gitignore` at the knowledge-tree root (the indexer's project home) or the global `~/.basic-memory/.bmignore`. The guide documents the mask quirks (directory patterns match one path component at any depth, globs apply per component, `*` crosses `/`, no `!` negation so a whitelist is inexpressible, hidden names ignored by default), the one-time phantom-entity cleanup and reindex after masking, and that `docs/archive` is walked by the indexer until a `.bmignore` line excludes it.
- **`ai-sync doctor`** reports a new `non-note-data-file-inside-knowledge-tree` warning for every non-Markdown, non-hidden, unmasked file under the knowledge tree. The check mirrors the indexer's own matcher (`.gitignore` at the knowledge-tree root plus the global `.bmignore` beside the indexer configuration, read while the feature gate opens) so an already-masked tree stays quiet; declared overrides and the `archive/` subtree are not double-reported. Reported, never auto-fixed.
- **The `audit-knowledge-tree` skill** (all three adapters) names the new doctor finding, classifies data files, and prescribes the repair: move out of the tree or mask at the root, never delete silently, and reindex only after `ai-sync doctor` stops reporting the file.
- **Unified release versioning around `meta.toml [release]`** (user issue #11): the repository root gains `meta.toml` with a mandatory `[release]` table (`version`, `date`) as the single source of release truth; `[tool.ai-standards]` is removed from `pyproject.toml` and `[project] version` is fixed at `0.0.0` (the Python support package is no longer versioned separately). The manifest pin `ai_standards_version` becomes the single version key in the full `<version>-<date>` format, identical to the release tag name; `project_version` and `project_release_date` are retired from `ai.project.toml`, `templates/project_manifest.toml`, the renderer, and `bump-version save`. Drift checks in `render`/`update`/`check`/`doctor` compare against the full pin through one helper; the `update-ai-standards` skill reads the release from `meta.toml` and compares `[feature_meta].since` against the version part of the pin. Decision record: `docs/decisions/2026-09-01-unify-release-versioning-meta-toml.md` (supersedes the 2026-04-18 release-version separation).
- **Module contracts are records, not root files** (user issue #10): the `Module Contracts` rules now place a contract as one `YYYY-MM-DD-module-contract-<module-slug>.md` record under `docs/architecture/**` with frontmatter `title` and `type: module-contract`; a root-level `MODULE_CONTRACT.md` is a legacy form that discovery and review still recognize but never create. The `Module Contract Discovery Gate` lists the records first and keeps the root file as legacy; the canonical-documentation enumerations in `structured-artifacts` and `basic-memory` no longer name the root file; the `code-review` fragment and the `standard-code-review` templates find contracts by the record marker; the `capture-knowledge` templates write records. Decision record: `docs/decisions/2026-09-01-module-contract-record-notation.md`.
- **`ai-sync doctor`** reports a root-level `MODULE_CONTRACT.md` (repository root or knowledge-tree root) as a `legacy-module-contract-location` warning pointing at the record home; the warning is reported, never auto-fixed.
- **This repository's own contract migrated** from `docs/MODULE_CONTRACT.md` to `docs/architecture/2026-09-01-module-contract-ai-sync.md` (+ `.ru.md`), with `type: module-contract` in the frontmatter; the template `templates/module-contract.md` carries the record frontmatter.

## [2.2.1] — 2026-08-30

### Canonical Prompts

Give your agent one of these, verbatim.

Install (no deployment in the project):

```text
Install ai-standards into this project from https://github.com/aka-NameRec/ai-standards:
clone it, read templates/standards-update/update-ai-standards.SKILL.md, and run its Install
mode — survey the project, propose features with recommendations, deploy the confirmed set
after my confirmation.
```

Update (deployment of this release or newer):

```text
Update ai-standards to the latest release.
```

Update (deployment older than the skill — bootstrap):

```text
Update ai-standards in this project from https://github.com/aka-NameRec/ai-standards: clone
it, read templates/standards-update/update-ai-standards.SKILL.md, and run its Upgrade mode —
silently refresh the enabled features, announce the ones not yet in the manifest, enable the
confirmed set, and move the version pin.
```

### Changed

- **The `update-ai-standards` skill is dual-mode and cold-start capable**: an Install mode surveys a project without a deployment (existing `AGENTS.md` and its provenance, stacks, docs layout and language, ConPort/Basic Memory presence, CI, tracker, agent environments), proposes the feature set one line at a time with recommendations, and deploys the confirmed set; the file is written to be followed straight from a checkout, so a project older than the skill bootstraps from the URL alone by naming it. The upgrade digest now announces only features that are new **and not yet enabled**, and a bootstrap preamble re-deploys the procedure before announcing. Rationale: [`docs/decisions/2026-08-29-standards-install-and-cold-start.md`](docs/decisions/2026-08-29-standards-install-and-cold-start.md).
- **`standards_source` is recorded at install time**: the manifest metadata carries the repository URL the standards came from, renders into the `AGENTS.md` header, and is what lets later update prompts skip the URL.

## [2.2.0] — 2026-08-28

### Upgrade Notes

This release ships the `update-ai-standards` skill, which makes every later update a one-phrase request. To adopt it on an existing deployment:

1. Bring your ai-standards checkout to this release, then run `uv run ai-sync render --project-root <project>` and `uv run ai-sync sync-templates --project-root <project>`. The skill deploys to every declared agent in `[tooling].agents` without a feature toggle.
2. Set `ai_standards_version` in `ai.project.toml` to this release. `ai-sync check` now fails while the pin disagrees with the source in use, so a skipped step shows up as drift instead of passing silently.
3. From the next update on, the whole procedure is one request — «обнови ai-standards» / "update ai-standards": the skill refreshes enabled features, announces what is new since the pinned version, and enables only what you confirm.

### Added

- **`code-review` feature**: a bare "code review" request now runs a review against the project's assembled rules and prints a report of a fixed shape. The shape is defined once, by the worked example in `templates/code-review-report.md`, which `sync-templates` deploys to `.ai-standards/code-review-report.md` through the agent-agnostic template channel — no `tooling.agents` adapter required. Findings carry severity markers (🔴 🟡 🔵 ✅), a cited file location, and the rule they violate. Ships with bilingual usage guides and a decision record. Contributed by **tsinana** ([#6](https://github.com/aka-NameRec/ai-standards/pull/6)).
- **`Verification` and `Dependencies` sections in the code-review report**: the report states which checks actually ran, with their results, and explicitly names what was not checked, because a silently omitted line reads as a check that passed. `Dependencies` is kept only when the change requires a change in another repository. Both were normalized from a hand-written per-repository review workflow that had been in daily use alongside the feature.
- **`ai-standards` version line in the code-review report**: the report opens with `ai-standards <version>`, copied from the `Generated by ai-standards` header of the generated instructions file in force, so a report pasted into a pull request records which rule set the review ran under. The line stays as-is across languages; when the header is missing, the report states that the version is undetermined rather than guessing.
- **`standard-code-review` skill**: deploys with the `code-review` feature to the declared agents and packages the review workflow into one procedure — the `code-review` passes, the full lens set including the two extra DRY rules, and an architecture-and-contracts check that reconciles changed modules with their `MODULE_CONTRACT.md` and the records under `docs/architecture/**`. One pass, one report; `review-lenses` keeps its cleanup-and-fix role.
- **`Fixing While Reviewing` policy**: the ✅ marker previously existed without a rule saying when a fix is allowed. Fixes whose safety reading alone establishes — translations, typos, junk in `.gitignore`, local inconsistencies — are made and recorded as ✅ findings; migrations, lock files, dependencies, build configuration, public contracts, the git index, refactors, and anything needing a test run are reported and left alone.
- **`DRY` pass in the `review-lenses` feature**: duplication introduced by the reviewed change itself is now a separate pass rather than a corner of the `Reuse` lens, which by its wording ("prefer existing project primitives") never described the case where a single change adds two new copies. The pass also covers one intent expressed two different ways in sibling files, requires reading the surrounding convention before extracting a shared primitive, and calls for a clone detector once the scope grows past a diff. Propagated to the three `simplify-review` adapter templates covering all four agent environments, guarded by a test so an adapter cannot silently lose it, and documented in both usage guides. Rationale: [`docs/decisions/2026-08-21-add-dry-review-pass.md`](docs/decisions/2026-08-21-add-dry-review-pass.md).
- **`update-ai-standards` skill**: deploys with every ai-standards deployment that declares agents — no feature toggle, because the skill maintains ai-standards itself rather than a project process. One request («обнови ai-standards» / "update ai-standards") brings the deployment to the latest release: the maintained checkout is refreshed, already-enabled features re-render silently, features added since the pinned version are announced with recommendations against the project's stacks, and only the features the user confirms are enabled. Rationale: [`docs/decisions/2026-08-28-standards-update-workflow.md`](docs/decisions/2026-08-28-standards-update-workflow.md).
- **Feature discovery metadata** (`[feature_meta]` in `registry.toml`): records the release that introduced each feature, so the update skill computes what is new for a project mechanically instead of parsing changelog prose. Features that predate the changelog carry no entry and are never announced as new; entries pointing at this release must be reconciled with the actual release number during `bump-version`.
- **Pin drift is reported, not silent**: `ai-sync check` fails when `ai_standards_version` in the manifest disagrees with the standards source in use, `render` and `update` echo a warning, and `doctor` reports `standards-version-drift`. The rendered header already recorded what was actually used; now the mismatch is impossible to miss.
- **`module-contract-gate` feature**: before changing production code, the agent must complete module-contract discovery for the affected area — canonical contracts read from the repository, Basic Memory as an index only, coverage decided per touched file, re-discovery on defined triggers, and a short contract note in the implementation summary. Discovery is proportional: a cheap check that the project declares no contract artifacts completes it, and the strict rule — no edit before discovery completes — stays absolute. A registry composite that carries `structured-artifacts` with it. Promoted from the contributor draft `docs/archive/0tkgv0g-module-contract-discovery-gate.md`; placement and adjustments: [`docs/decisions/2026-08-28-module-contract-gate-feature-placement.md`](docs/decisions/2026-08-28-module-contract-gate-feature-placement.md).
- **`response-language-style` feature**: replies to the user stay in natural Russian — anglicisms with common Russian equivalents go out ("срок", not "дедлайн"; "согласование", not "апрув"), and so do slang and informal jargon. Cryptic project-local abbreviations require an immediate explanation; widely accepted ones are expanded on first mention; exact technical names are quoted verbatim in prose. Opt-in, because the style is a team's choice rather than a default. Promoted from the cockpit project-local rule of the same name; the cockpit-specific clause about carrying the rule into external projects stays in cockpit's local override.

### Changed

- **The code-review report has five finding sections instead of three**: `Reuse`, `Efficiency`, and `Quality` get their own headings rather than sharing one, while `Correctness` and `Architecture & Conventions` keep their priority positions. Findings are also now required to be checked against the code rather than against the diff, and what the change got right is named in `How It Was Done` rather than as a marked finding, so scanning the markers keeps answering what is left to do.
- **`What Was Done` and `How It Was Done` are always included in the report**: the previous rule omitted both for a standalone review with no implementation work behind it, which also dropped the praise slot — the naming of the reuse and conventions the change got right. The first section is now a factual summary of what the change does, read from the diff; invented rationale stays out, and a trivially self-describing change needs one sentence per section. The architecture pass now also reconciles changed modules with their `MODULE_CONTRACT.md` and the records under `docs/architecture/**`, citing the exact clause; a changed major module with no contract is reported as a `(no contract)` note.

## [2.1.0] — 2026-07-11

### Added

- **`chroma` feature**: a semantic code-search standard over repository source files, kept separate from ConPort operational memory and Basic Memory documentation retrieval. Includes a usage fragment (`fragments/tools/chroma.md`) and a bilingual usage guide (`docs/chroma-usage.md`).
- **AI infrastructure deployment skill** (`deploy-ai-knowledge-stack`): a manually invoked skill that deploys the whole knowledge stack (ConPort, Basic Memory, Chroma) in a race-free order, eliminating the setup traps observed in a prior production deployment (synchronous polling burn, Basic Memory bootstrap race, cloud-routing errors, ConPort workspace detection walk-up, MCP drift across clients).
- **Four agent environments**: added `claude` and `kilo` agent adapters alongside `codex` and `cursor`. The deployment skill and `simplify-review` are now propagated to all four.
- **Feature-gated templates**: `AgentTemplate` gained an optional `feature` gate. Enabling `chroma` now renders the usage fragment, materializes the code-index infrastructure under `.ai-standards/`, and propagates the deployment skill in one step.
- **`.ai-standards/` infrastructure namespace**: managed templates (`scripts/code_index.py`, `code-index.toml`) are synced under `.ai-standards/` instead of mixing with project-owned `scripts/`. `code_index.py` is generalized from a battle-tested reference implementation (cross-file batched upsert, atomic resumable manifest, freshness-gated querying).
- **Basic Memory per-workspace isolation**: a rule requiring the Basic Memory MCP server to be constrained to a single project per workspace (`--project`), so retrieval returns only the current project's artifacts.
- **ConPort usage guide** (`docs/conport-usage.md`): fills the prior gap (every other feature already had a usage guide).

### Changed since 2.0.1 (previously merged into `main`)

- **Claude Code compatibility**: `init-claude-bridge` command that creates a thin managed `CLAUDE.md` importing `AGENTS.md`. Contributed by **tsinana** ([#4](https://github.com/aka-NameRec/ai-standards/pull/4)).
- **Django rule**: keep a derived value instead of an ORM instance when only a field is needed. Contributed by **akuznetzz** ([#5](https://github.com/aka-NameRec/ai-standards/pull/5)).

### Proposals

- **Graphify integration proposal** (`0thzm41`): outlines an opt-in `graphify` feature for module-map generation and structural contract-invariant verification (not a replacement for authored contracts), with fire-and-forget deployment integration and graph-freshness methodology. To be pursued as a separate task.

### Contributors

- Sergey Shturkin ([aka-NameRec](https://github.com/aka-NameRec)) — chroma feature, deployment skill, agent adapters, Basic Memory isolation, ConPort usage guide, Graphify proposal, release.
- [tsinana](https://github.com/tsinana) — Claude Code `init-claude-bridge` compatibility (#4).
- [akuznetzz](https://github.com/akuznetzz) — Django derived-value rule (#5).

## [2.0.1] — 2026-05-27

- Canonical artifact naming defaults and ai-standards version separation.

## [2.0.0] — 2026-05-19

- Added the `basic-memory` feature and memory policy.
