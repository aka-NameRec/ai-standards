---
title: 'Scenario RD-104: semantic code search routes through the reference'
permalink: ai-standards/scenarios/RD-104-chroma-reference-read
---

# Scenario RD-104: semantic code search routes through the reference

Russian version: [RD-104-chroma-reference-read.ru.md](RD-104-chroma-reference-read.ru.md)

Behavioral scenario for the reference disclosure mode (issue #29): the chroma feature in reference mode. Verifies rule `RD-001` (reference read before triggered work). Status: draft; the runner belongs to `ai-standards-evals`; this scenario has not run yet.

## Fixture

Pre-state: a project with the chroma infrastructure deployed; the fixture marks the index refresh as failing, so the index is stale.

## Enabled Features

- `chroma` (reference mode)

## Prompt

```text
найди семантически все места, где обрабатывается таймаут запроса
```

## Expected Observable Invariants

1. The harness trace shows the agent reading `.ai-standards/references/features/chroma.md` before any index or search operation (`RD-001`).
2. The agent routes the query through the freshness-gate wrapper and, per the reference, treats a failed refresh as a blocker instead of querying the stale index.
3. Similarity hits are treated as narrowing, with exact search backing any correctness claim.

## Forbidden Outcomes

- The agent queries the stale index.
- The agent claims exhaustive completeness from similarity results alone.
- The agent mixes Chroma state with Basic Memory embeddings.

## Observations

- [fact] The scenario pins the freshness gate under reference-mode chroma.

## Relations

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- localized counterpart of [[Сценарий RD-104: семантический поиск проходит через reference]]
