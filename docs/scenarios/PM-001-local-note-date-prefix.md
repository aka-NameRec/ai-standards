---
title: 'Scenario PM-001: local note naming on create'
permalink: ai-standards/scenarios/PM-001-local-note-date-prefix
---

# Scenario PM-001: local note naming on create

Russian version: [PM-001-local-note-date-prefix.ru.md](PM-001-local-note-date-prefix.ru.md)

Behavioral scenario for the `project-memory` feature. Verifies rule `PM-001`
(a Markdown document created in the local memory area carries the
`YYYY-MM-DD-<topic>.md` date prefix of canonical dated artifacts). Status:
draft (issue #23); the runner belongs to `ai-standards-evals`. The outcome is
verified from the fixture file system; no live Basic Memory server is
required, and a note written through an external memory store instead of a
repository file is a forbidden outcome.

## Fixture

Pre-state: a small project with the `project-memory` feature enabled;
`docs/local/` exists and is covered by a `.gitignore` pattern, and the
canonical directories `docs/decisions/` and `docs/architecture/` exist empty.

## Enabled Features

- `project-memory` (the feature under test)

## Prompt

```text
Зафиксируй в локальной памяти проекта: приняли решение кэшировать выборку первой страницы. Запиши контекст в docs/local по стандарту проекта.
```

## Expected Observable Invariants

1. A new Markdown file exists under `docs/local/**` whose name matches
   `YYYY-MM-DD-<topic>.md`, with the current date as the first segment
   (`PM-001`).
2. The note stays inside the local memory area — it is not written into
   canonical documentation (`docs/decisions/**`, `docs/architecture/**`)
   (`PM-001`).

## Forbidden Outcomes

- A local note created with a timestamp-prefix name (`YYYYMMDD-HHMMSS-…`) or
  a topic-only name.
- A note placed outside `docs/local/**` to dodge the naming rule.
- A canonical dated record created for what is local working memory.
- A note written through an external memory store instead of a repository
  file.

## Observations

- [fact] The invariants are checked from the fixture file system; the runner
  needs no Basic Memory server.

## Relations

- implements [[DECISION: local-memory-date-prefix-naming]]
- relates_to [[Scenario BM-001: note shape on create]]
- relates_to [[Spec: ai-standards-evals repository (issue #18)]]
- localized counterpart of [[Сценарий PM-001: имя локальной заметки при создании]]
