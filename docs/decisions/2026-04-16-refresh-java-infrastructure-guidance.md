---
title: 'DECISION: refresh-java-infrastructure-guidance'
permalink: ai-standards/decisions/2026-04-16-refresh-java-infrastructure-guidance
---

# DECISION: refresh-java-infrastructure-guidance

Russian localized version: [2026-04-16-refresh-java-infrastructure-guidance.ru.md](2026-04-16-refresh-java-infrastructure-guidance.ru.md)

## Status

Accepted

## Date

2026-04-16

## Context

`ai-standards` had Java and Spring guidance only through one combined fragment: `fragments/stacks/java-spring.md`.

That fragment already captured several solid service-layer and JPA practices, but it mixed Java language guidance, Spring framework rules, and Spring Data JPA persistence advice into one unit. This made the stack layering less consistent than the repository's newer Python and TypeScript baselines.

The fragment also missed several durable Spring recommendations that are now standard in modern Spring Boot and Spring Framework guidance, such as centralized RFC 9457 error contracts, `@ConfigurationProperties` for structured configuration, explicit transaction caveats around proxy-based `@Transactional`, and modern testing guidance around test slices and Testcontainers-backed integration tests.

## Decision

`ai-standards` splits the former `java-spring` baseline into three stack fragments:

- `java` for language-level and platform-level Java guidance
- `spring` for framework-level Spring and Spring Boot guidance
- `spring-data-jpa` for JPA and Spring Data persistence guidance

The repository keeps `java-spring` as a compatibility alias in `registry.toml`, mapped to the new three-fragment composition, so existing downstream manifests continue to render without changes.

The new baseline keeps durable existing rules such as thin controllers, constructor injection, explicit transaction boundaries, DTO boundaries, and deliberate fetch planning, while adding newer shared guidance for:

- RFC 9457 `ProblemDetail` and `ErrorResponse` contracts for REST APIs
- `@ConfigurationProperties` for structured configuration
- explicit awareness of proxy-based `@Transactional` behavior
- modern outbound HTTP client guidance via `RestClient` and `WebClient`
- focused Spring test slices and Testcontainers-backed integration testing where infrastructure fidelity matters

## Why

- makes Java language guidance discoverable as its own reusable stack
- separates Spring framework concerns from JPA-specific persistence guidance
- aligns Java stack composition with the repository's newer baseline design
- preserves downstream compatibility by keeping `java-spring` as an alias
- refreshes the guidance toward current official Spring recommendations instead of leaving it at a narrower enterprise-service checklist

## Alternatives Considered

### Keep `java-spring` as the only fragment and only revise the bullet list

Rejected because the structural layering problem would remain: Java, Spring, and JPA guidance would still be mixed into one stack unit.

### Remove `java-spring` entirely and force downstream manifests to migrate

Rejected because the repository can preserve compatibility cheaply through a registry alias, and there is no need to create migration pressure for downstream projects yet.

### Put JPA rules into `spring.md`

Rejected because not every Spring project uses JPA, and persistence guidance should remain optional and composable.

## Consequences

### Benefits

- downstream projects can compose Java baselines more precisely
- Java guidance is easier to extend without overloading one fragment
- Spring guidance now includes more current framework recommendations
- existing `java-spring` users keep working without manifest churn

### Costs Or Tradeoffs

- the repository maintains more stack fragments and related tests
- documentation must explain both the preferred new composition and the compatibility alias
- some users may need to learn the difference between `spring` and `spring-data-jpa`

## Affected Modules

- `fragments/stacks/java.md`
- `fragments/stacks/spring.md`
- `fragments/stacks/spring-data-jpa.md`
- `fragments/stacks/java-spring.md`
- `registry.toml`
- `README.md`
- `README.ru.md`
- `tests/test_ai_sync.py`
- `docs/0tdk9ag-java_infrastructure_rules_update.md`
- `docs/0tdk9ag-java_infrastructure_rules_update.ru.md`

## Invariants And Constraints

- Java language guidance must live in a Java-specific stack fragment
- Spring framework guidance must stay separate from JPA-specific persistence guidance
- `java-spring` must remain renderable for downstream compatibility
- the shared baseline must stay framework-oriented and avoid project-local architecture dogma

## Verification

- `registry.toml` exposes `java`, `spring`, and `spring-data-jpa`
- `java-spring` still renders through the compatibility alias
- README and README.ru show the preferred explicit stack composition
- renderer tests cover both the compatibility alias and the explicit three-stack composition
- repository checks continue to pass

## Related Artifacts

- [../../fragments/stacks/java.md](../../fragments/stacks/java.md)
- [../../fragments/stacks/spring.md](../../fragments/stacks/spring.md)
- [../../fragments/stacks/spring-data-jpa.md](../../fragments/stacks/spring-data-jpa.md)
- [../../registry.toml](../../registry.toml)
- [../../README.md](../../README.md)
- [../../README.ru.md](../../README.ru.md)
- [../0tdk9ag-java_infrastructure_rules_update.md](../0tdk9ag-java_infrastructure_rules_update.md)