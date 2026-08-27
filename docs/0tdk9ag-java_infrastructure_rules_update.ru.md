---
title: 'План Изменений: Обновление Правил Java-Инфраструктуры'
permalink: ai-standards/0tdk9ag-java-infrastructure-rules-update.ru
---

# План Изменений: Обновление Правил Java-Инфраструктуры

Англоязычный оригинал: [0tdk9ag-java_infrastructure_rules_update.md](0tdk9ag-java_infrastructure_rules_update.md)

## Цель

Обновить Java и Spring guidance так, чтобы он отражал современные shared best practices и официальные рекомендации фреймворков, сохраняя при этом предсказуемость для downstream-подключения.

## Scope

- заменить комбинированный `java-spring` fragment как источник истины
- ввести отдельные stack baselines для `java`, `spring` и `spring-data-jpa`
- сохранить `java-spring` как compatibility alias в `registry.toml`
- обновить документацию репозитория и renderer tests
- зафиксировать решение в двуязычных decision records

## Не Цели

- не превращать стек в жёстко предписанный локальный architectural style
- не навязывать всем проектам один persistence или HTTP client style
- не ломать существующие downstream manifests, уже использующие `java-spring`

## Инварианты

- Java language guidance должен жить в Java-specific stack fragment
- Spring framework guidance должен быть отделён от JPA-specific persistence guidance
- downstream-проекты, использующие `java-spring`, должны продолжать рендериться без изменений манифеста
- новые правила должны опираться на устойчивый official-framework guidance, а не на project-local conventions

## Проверка

- `registry.toml` содержит `java`, `spring` и `spring-data-jpa`
- `java-spring` остаётся рендеримым как compatibility alias
- README и README.ru описывают новую композицию стеков
- renderer tests покрывают и compatibility alias, и явную новую комбинацию стеков
- проверки репозитория остаются зелёными