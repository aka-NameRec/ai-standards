---
title: Knowledge Stack Roles
permalink: ai-standards/architecture/2026-08-27-knowledge-stack-roles
---

# Knowledge Stack Roles

Russian localized version: [2026-08-27-knowledge-stack-roles.ru.md](2026-08-27-knowledge-stack-roles.ru.md)

Descriptive overview of the knowledge stack around a project. The argument for this shape is [2026-08-24-knowledge-store-role-separation.md](../decisions/2026-08-24-knowledge-store-role-separation.md); the archive-specific part is [2026-08-24-archive-history-in-docs-tree.md](../decisions/2026-08-24-archive-history-in-docs-tree.md).

## Layers

| Layer | Role | Canonical? |
|---|---|---|
| git | project files and full history | yes — everything else is a projection |
| ai-standards | rule delivery: manifest → rendered `AGENTS.md`; `sync-templates` deploys skills and infrastructure; `doctor` audits wiring | rules are canonical here |
| cockpit `projects_registry.toml` | multi-project source of truth: locations, Basic Memory opt-in, indexed paths | yes, for project wiring |
| Basic Memory adapter (cockpit) | deterministic projection of the registry into `~/.basic-memory/config.json`; the only writer of that file | no — projection |
| Basic Memory | graph retrieval over the living knowledge tree (`docs/**` minus archive); notes identified by frontmatter `title`; `memory://` via permalinks | no — projection of the tree |
| Chroma | vector retrieval: code collections per explicit roots; a history collection over `docs/archive` | no — projection |
| ConPort | operational memory: active context, progress, handoffs | no — transient |

## Boundary Invariants

- Files in git are canonical; every index rebuilds from them.
- The agent writes the frontmatter `title`; the indexer stamps the `permalink`. A note that needs no repair carries `title` matching its `# H1` and closes with `## Observations` and `## Relations`.
- The archive leaves the Basic Memory graph through one conventional `.bmignore` line (`archive/`), verified by `ai-sync doctor`; it enters Chroma through one collection declaration.
- Code collections declare explicit roots that do not cover `docs/archive`; a root of `"."` would mix history into the code index.
- The registry is the only writer of the Basic Memory global config; `doctor` reads that config and never writes it.

## Retrieval Contract

- Routine work queries the living graph (Basic Memory) and code collections; archive material never surfaces unprompted.
- Explicit history research queries the history collection by name.
- Wiki-links resolve inside the living tree; references into the archive use relative Markdown links, which work in git and in readers.

## Observations

- [fact] git is the only canonical layer; Basic Memory, Chroma, ConPort, and the rendered `AGENTS.md` are projections rebuildable from files.
- [fact] The registry-to-config pipeline is single-writer: the cockpit adapter writes `~/.basic-memory/config.json`, and `ai-sync doctor` only reads it.
- [fact] The archive crosses the Basic Memory boundary through `.bmignore` and the Chroma boundary through a collection declaration, each one line and each verified differently.

## Relations

- relates_to [[DECISION: knowledge-store-role-separation]]
- relates_to [[DECISION: archive-history-in-docs-tree]]
- localized counterpart of [[Роли стека знаний]]