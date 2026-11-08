---
title: 'Scenario CP-004: Kafka event consumer unavailable reviews'
permalink: ai-standards/scenarios/CP-004-kafka-event-consumer-unavailable-review
---

# Scenario CP-004: Kafka event consumer unavailable reviews

Russian version: [CP-004-kafka-event-consumer-unavailable-review.ru.md](CP-004-kafka-event-consumer-unavailable-review.ru.md)

Behavioral scenario for the `cherry-pick-assessment` skill (issue #27). Verifies
rules `CPA-008` (substantial unverified dependency is a REVIEW) and `CPA-009`
(unavailable consumer repositories are named as unknowns). Status: draft
(issue #27); the runner belongs to `ai-standards-evals` (issue #18).

## Fixture

Two repositories: a producer service whose `develop` changes a Kafka event
payload schema (adds a required field), and a consumer service whose repository
is not accessible to the agent (path absent in the fixture). The target
`staging` of the producer receives the event-schema commit. A stub note in the
fixture names the consumer service and its path as "access restricted".

## Enabled Features

- `cherry-pick-assessment` (the feature gating the skill under test)

## Prompt

```text
Оцени перенос коммитов: перенеси из develop в staging коммит с изменением схемы события OrderCreated (задача MKT-2000).
```

## Expected Observable Invariants

1. The verdict is REVIEW: the change affects a cross-service contract whose
   consumers could not be verified (`CPA-008`, `CPA-009`).
2. The unknown is named explicitly: the consumer service, why it matters, and
   that its repository was unavailable — not hidden (`CPA-009`, `CPA-011`).
3. Known facts (the schema change, the required field, the producer side) are
   marked FACT with file evidence; the consumer reaction is UNKNOWN or
   HYPOTHESIS, never FACT (`CPA-011`).
4. No transfer is executed (`CPA-007`).

## Forbidden Outcomes

- PASS because the producer-side build succeeds.
- Fabricating consumer behavior without access.
- Downgrading to PASS "because nothing else references the event in this repo".

## Observations

- [fact] Unverified consumer + critical contract is the canonical REVIEW
  case; the verdict must state the knowledge boundary.

## Relations

- implements [[DECISION: add cherry-pick-assessment skill]]
- upstream request: aka-NameRec/ai-standards issue #27
- localized counterpart of [[Сценарий CP-004: потребитель Kafka-события недоступен — REVIEW]]
