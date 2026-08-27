---
title: 'DECISION: refresh-java-infrastructure-guidance'
permalink: ai-standards/decisions/2026-04-16-refresh-java-infrastructure-guidance.ru
---

# DECISION: refresh-java-infrastructure-guidance

Англоязычный оригинал: [2026-04-16-refresh-java-infrastructure-guidance.md](2026-04-16-refresh-java-infrastructure-guidance.md)

## Статус

Accepted

## Дата

2026-04-16

## Контекст

В `ai-standards` Java и Spring guidance существовал только через один комбинированный fragment: `fragments/stacks/java-spring.md`.

Этот fragment уже содержал несколько сильных service-layer и JPA практик, но смешивал Java language guidance, Spring framework rules и Spring Data JPA persistence advice в одном блоке. Из-за этого layering стеков был менее консистентным, чем в более свежих baselines для Python и TypeScript.

Фрагменту также не хватало ряда устойчивых Spring-рекомендаций, которые сегодня выглядят стандартными для modern Spring Boot и Spring Framework guidance: централизованные RFC 9457 error contracts, `@ConfigurationProperties` для структурированной конфигурации, явное правило про proxy-based `@Transactional` и современный testing guidance вокруг test slices и Testcontainers-backed integration tests.

## Решение

`ai-standards` разделяет прежний `java-spring` baseline на три stack fragments:

- `java` для language-level и platform-level Java guidance
- `spring` для framework-level Spring и Spring Boot guidance
- `spring-data-jpa` для JPA и Spring Data persistence guidance

Репозиторий сохраняет `java-spring` как compatibility alias в `registry.toml`, отображая его на новую композицию из трёх fragments, чтобы существующие downstream manifests продолжали рендериться без изменений.

Новый baseline сохраняет устойчивые существующие правила, такие как thin controllers, constructor injection, явные transaction boundaries, DTO boundaries и deliberate fetch planning, и одновременно добавляет более современный shared guidance для:

- RFC 9457 `ProblemDetail` и `ErrorResponse` contracts для REST API
- `@ConfigurationProperties` для структурированной конфигурации
- явного учёта proxy-based поведения `@Transactional`
- современного guidance по outbound HTTP clients через `RestClient` и `WebClient`
- focused Spring test slices и Testcontainers-backed integration testing там, где важна близость инфраструктуры к реальности

## Почему

- делает Java language guidance обнаружимым как отдельный переиспользуемый stack
- отделяет Spring framework concerns от JPA-specific persistence guidance
- выравнивает композицию Java-стеков с более новым baseline design репозитория
- сохраняет downstream compatibility через alias `java-spring`
- обновляет guidance в сторону актуальных official Spring recommendations вместо более узкого enterprise-service checklist

## Рассмотренные альтернативы

### Оставить `java-spring` единственным fragment и только переписать список правил

Отклонено, потому что структурная проблема layering осталась бы: Java, Spring и JPA guidance по-прежнему были бы смешаны в одном stack unit.

### Полностью удалить `java-spring` и заставить downstream manifests мигрировать

Отклонено, потому что репозиторий может дёшево сохранить compatibility через registry alias, и сейчас нет причин создавать лишнее migration pressure для downstream-проектов.

### Перенести JPA-правила в `spring.md`

Отклонено, потому что не каждый Spring-проект использует JPA, и persistence guidance должен оставаться optional и composable.

## Последствия

### Плюсы

- downstream-проекты могут точнее собирать Java baselines
- Java-guidance стало проще расширять без перегрузки одного fragment
- Spring-guidance теперь включает более современные framework recommendations
- существующие пользователи `java-spring` продолжают работать без churn в манифестах

### Минусы или цена

- репозиторию нужно поддерживать больше stack fragments и связанных тестов
- документация должна объяснять и предпочтительную новую композицию, и compatibility alias
- части пользователей придётся понять разницу между `spring` и `spring-data-jpa`

## Затронутые модули

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

## Инварианты и ограничения

- Java language guidance должен жить в Java-specific stack fragment
- Spring framework guidance должен быть отделён от JPA-specific persistence guidance
- `java-spring` должен оставаться рендеримым ради downstream compatibility
- shared baseline должен оставаться framework-oriented и не скатываться в project-local architecture dogma

## Проверка

- `registry.toml` содержит `java`, `spring` и `spring-data-jpa`
- `java-spring` продолжает рендериться через compatibility alias
- README и README.ru показывают предпочтительную явную композицию стеков
- renderer tests покрывают и compatibility alias, и явную композицию из трёх stack fragments
- проверки репозитория остаются зелёными

## Связанные артефакты

- [../../fragments/stacks/java.md](../../fragments/stacks/java.md)
- [../../fragments/stacks/spring.md](../../fragments/stacks/spring.md)
- [../../fragments/stacks/spring-data-jpa.md](../../fragments/stacks/spring-data-jpa.md)
- [../../registry.toml](../../registry.toml)
- [../../README.md](../../README.md)
- [../../README.ru.md](../../README.ru.md)
- [../0tdk9ag-java_infrastructure_rules_update.md](../0tdk9ag-java_infrastructure_rules_update.md)