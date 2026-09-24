---
title: 'Scenario BM-001: note shape on create'
permalink: ai-standards/scenarios/BM-001-note-shape
---

# Scenario BM-001: note shape on create

Russian version: [BM-001-note-shape.ru.md](BM-001-note-shape.ru.md)

Behavioral scenario for the basic-memory feature. Verifies rule `BM-001`
(notes are written so they need no repair). Status: draft (issue #22, stage
3); the runner belongs to `ai-standards-evals`. The outcome is verified from
the fixture file system; no live Basic Memory server is required, and writing
through an external memory store instead of a repository file is a forbidden
outcome.

## Fixture

Pre-state: a small project with the `basic-memory` feature enabled; `docs/decisions/`
exists and holds one pre-existing decision record in the canonical shape;
templates synced, so `.ai-standards/references/basic-memory-operations.md`
exists.

## Enabled Features

- `basic-memory` (the feature under test)

## Prompt

```text
Зафиксируй решение в docs/decisions: внутренние сервисы переходят с REST на gRPC. Создай файл заметки в репозитории по стандарту проекта.
```

## Expected Observable Invariants

1. A new Markdown file exists directly under `docs/decisions/` with the dated
   name `YYYY-MM-DD-<topic-slug>.md` (`BM-001`).
2. The file carries a frontmatter `title` in Russian, and the `# ` heading
   repeats that title (`BM-001`).
3. The note body closes with `## Observations` and `## Relations` sections,
   and `## Observations` carries at least one substantive observation
   (`BM-001`).

## Forbidden Outcomes

- A note written through an external memory store instead of a repository
  file under `docs/decisions/`.
- An undated or slug-less file name for the decision record.
- A missing or non-Russian frontmatter title, a heading that does not repeat
  it, or missing `## Observations` / `## Relations`.

## Observations

- [fact] The invariants are checked from the fixture file system; the runner
  needs no Basic Memory server.

## Relations

- implements [[DECISION: adopt the Rule Engineering initiative]]
- relates_to [[Spec: ai-standards-evals repository (issue #18)]]
- relates_to [[Change plan: progressive disclosure stage 3 — M5 basic-memory operations and M6 compression (issue #22)]]
- localized counterpart of [[Сценарий BM-001: форма заметки при создании]]
