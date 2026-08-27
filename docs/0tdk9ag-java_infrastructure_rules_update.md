---
title: 'Change Plan: Java Infrastructure Rules Update'
permalink: ai-standards/0tdk9ag-java-infrastructure-rules-update
---

# Change Plan: Java Infrastructure Rules Update

Russian localized version: [0tdk9ag-java_infrastructure_rules_update.ru.md](0tdk9ag-java_infrastructure_rules_update.ru.md)

## Goal

Refresh the Java and Spring guidance so it reflects current shared best practices and official framework recommendations, while keeping downstream adoption predictable.

## Scope

- replace the combined `java-spring` fragment as the source of truth
- introduce separate stack baselines for `java`, `spring`, and `spring-data-jpa`
- keep `java-spring` as a compatibility alias in `registry.toml`
- update repository documentation and renderer tests
- record the decision in bilingual decision records

## Non-Goals

- do not turn the stack into a prescriptive local architecture style
- do not force one persistence or HTTP client style on every project
- do not break existing downstream manifests that already use `java-spring`

## Invariants

- Java language guidance should live in a Java-specific stack fragment
- Spring framework guidance should stay separate from JPA-specific persistence guidance
- downstream projects using `java-spring` must continue to render without manifest changes
- new rules should prefer durable official-framework guidance over project-local conventions

## Verification

- `registry.toml` exposes `java`, `spring`, and `spring-data-jpa`
- `java-spring` remains renderable as a compatibility alias
- README and README.ru describe the new stack composition
- renderer tests cover both the compatibility alias and the explicit new stack combination
- repository checks remain green