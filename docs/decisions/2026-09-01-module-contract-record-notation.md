---
title: 'DECISION: module-contract-record-notation'
permalink: ai-standards/decisions/2026-09-01-module-contract-record-notation
---

# DECISION: module-contract-record-notation

Russian localized version: [2026-09-01-module-contract-record-notation.ru.md](2026-09-01-module-contract-record-notation.ru.md)

## Status

Accepted

## Date

2026-09-01

## Context

User issue #10 reported the same manifestation in two different projects: an agent asked to create a module contract wrote a root-level `MODULE_CONTRACT.md` instead of a record under `docs/architecture/**`, and did so without the frontmatter `title` the Basic Memory indexing layer requires. The rules named exactly one artifact — `Create MODULE_CONTRACT.md only for major, risky, shared, or architecturally non-obvious modules` — while never naming a storage location or a notation for contracts, so the literal reading won, and the pattern repeated across projects. The root file also appeared first in the discovery gate's list of canonical sources and in the canonical-documentation enumerations, reinforcing it as the target format.

The knowledge-stack side already expects records, not root files: notes are identified by frontmatter `title`, dated artifacts follow `YYYY-MM-DD-<topic-slug>.md`, and `docs/architecture/**` is an established canonical home shared with architecture decision records. This record fixes where a module contract lives and what it looks like.

## Decision

A module contract is one record under `docs/architecture/**`:

- the file is named `YYYY-MM-DD-module-contract-<module-slug>.md` — the decision-record notation with an explicit `module-contract` label in the slug, so a directory listing shows contracts at a glance;
- the frontmatter carries `title` (the Basic Memory identifier) and `type: module-contract` (the classification marker);
- one record states one contract — ownership, non-goals, inputs, outputs, dependencies, invariants, failure boundaries, verification;
- contracts are still written only for major, risky, shared, or architecturally non-obvious modules;
- a root-level `MODULE_CONTRACT.md` is a legacy form: discovery and review still recognize and read one, but no rule creates a new one, and `ai-sync doctor` reports a legacy location as a warning.

The `type: module-contract` frontmatter field, not the file name, is the classification marker. Decision records about contracts legitimately carry `module-contract` in their slug too (for example `2026-08-28-module-contract-gate-feature-placement.md`, a decision, not a contract), so a file-name glob is only a cheap hint; the frontmatter marker is precise and feeds the schema tooling of the Basic Memory feature.

## Why

- The failure was systemic: the wording, not individual agent behavior, produced the root file in two projects, so the fix belongs in the wording.
- A record under `docs/architecture/**` puts the contract where the discovery gate already scans and where Basic Memory indexing works — the previous root file was invisible to the note conventions.
- The slug label plus the frontmatter type give both cheap discovery (name glob, content grep) and precise classification without relying on either alone.

## Alternatives Considered

### A dedicated `docs/contracts/**` directory

Rejected: it fragments the canonical locations, contradicts the shared naming rule that already covers `docs/architecture/**`, and the discovery gate and review checks would need a third place to scan.

### Keep the root `MODULE_CONTRACT.md` as the target format

Rejected: it is the manifestation issue #10 reports, and it sits outside the note conventions — no frontmatter identity, no dated notation, invisible to the record-based tooling.

### Mark contracts by tags only

Rejected as the sole marker: tags are for cross-cutting topics; a note type feeds the `infer`/`validate`/`diff` schema commands and gives discovery an exact predicate. The slug label already covers the cheap human-readable hint.

## Consequences

### Benefits

- contract records are first-class notes: titled, dated, indexed, greppable;
- discovery, review, and knowledge-capture instructions agree on one place and one notation;
- legacy files keep working — recognition stays, creation stops, doctor nudges migration.

### Trade-offs

- existing root `MODULE_CONTRACT.md` files in downstream projects remain until migrated; doctor reports them instead of fixing them, because moving a note is a rename and renames need a decision.

### Follow-ups

- this repository's own contract migrated in the same change set: `docs/architecture/2026-09-01-module-contract-ai-sync.md` (previously `docs/MODULE_CONTRACT.md`, originally recorded 2026-08-27).

## Observations

- [decision] A module contract lives as one `YYYY-MM-DD-module-contract-<module-slug>.md` record under `docs/architecture/**` with frontmatter `title` and `type: module-contract`.
- [decision] A root-level `MODULE_CONTRACT.md` is a legacy form: recognized and read, never created, reported by `ai-sync doctor` as `legacy-module-contract-location`.
- [fact] A file-name glob for `module-contract` alone misclassifies decision records about contracts; the frontmatter type is the precise marker.

## Relations

- relates_to [[DECISION: module-contract-gate-feature-placement]]
