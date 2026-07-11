# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2.1.0] — 2026-07-11

### Added

- **`chroma` feature**: a semantic code-search standard over repository source files, kept separate from ConPort operational memory and Basic Memory documentation retrieval. Includes a usage fragment (`fragments/tools/chroma.md`) and a bilingual usage guide (`docs/chroma-usage.md`).
- **AI infrastructure deployment skill** (`deploy-ai-knowledge-stack`): a manually invoked skill that deploys the whole knowledge stack (ConPort, Basic Memory, Chroma) in a race-free order, eliminating the setup traps observed in a prior DevCats deployment (synchronous polling burn, Basic Memory bootstrap race, cloud-routing errors, ConPort workspace detection walk-up, MCP drift across clients).
- **Four agent environments**: added `claude` and `kilo` agent adapters alongside `codex` and `cursor`. The deployment skill and `simplify-review` are now propagated to all four.
- **Feature-gated templates**: `AgentTemplate` gained an optional `feature` gate. Enabling `chroma` now renders the usage fragment, materializes the code-index infrastructure under `.ai-standards/`, and propagates the deployment skill in one step.
- **`.ai-standards/` infrastructure namespace**: managed templates (`scripts/code_index.py`, `code-index.toml`) are synced under `.ai-standards/` instead of mixing with project-owned `scripts/`. `code_index.py` is generalized from the DevCats reference (cross-file batched upsert, atomic resumable manifest, freshness-gated querying).
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
