---
title: 'DECISION: add-tanstack-query-stack'
permalink: ai-standards/decisions/2026-04-16-add-tanstack-query-stack.ru
---

# DECISION: add-tanstack-query-stack

Англоязычный оригинал: [2026-04-16-add-tanstack-query-stack.md](2026-04-16-add-tanstack-query-stack.md)

## Статус

Accepted

## Дата

2026-04-16

## Контекст

`ai-standards` уже начал разделять frontend baselines по уровням: framework baselines вроде `react` и `vue`, full-stack runtimes вроде `nextjs` и `nuxt`, а также tooling- и architecture-stacks вроде `vite` и `fsd`.

При этом всё ещё не хватало общего переиспользуемого слоя для server-state и cache synchronization в приложениях, которые используют TanStack Query вместо ad hoc fetch-and-state patterns.

Официальные рекомендации TanStack Query уже содержат достаточно durable, cross-framework practices, чтобы оправдать отдельный shared stack:

- TanStack Query управляет server state, а не всеми формами local UI state
- для предсказуемого caching важны stable query keys и централизованные query-client boundaries
- mutation flows должны явно revalidate, update или reconcile затронутые cache entries
- optimistic updates полезны, но должны оставаться явными и обратимыми
- SSR prefetching, dehydration и hydration должны жить на application boundaries

Во Vue-проектах при этом по-прежнему широко используется имя `vue-query`, хотя поддерживаемый пакет и основная guidance живут под брендом TanStack Query.

## Решение

`ai-standards` добавляет общий stack fragment `tanstack-query` и compatibility alias `vue-query`.

Фрагмент `tanstack-query` остаётся framework-neutral и сфокусирован на server-state boundaries, дисциплине query keys, mutation invalidation, optimistic updates, hydration boundaries и централизованном владении query client.

Имя стека `vue-query` реализовано как registry alias для `tanstack-query` плюс `vue`, чтобы downstream Vue-manifests могли использовать привычное имя без появления второго почти дублирующегося фрагмента.

## Почему

- добавляет переиспользуемый server-state baseline, который чисто компонуется с `react`, `vue`, `nextjs` или `nuxt`
- сохраняет TanStack Query rules в одном общем месте вместо дублирования по framework stacks
- поддерживает распространённое имя `vue-query`, не увеличивая дублируемую поверхность поддержки

## Рассмотренные альтернативы

### Вшить TanStack Query rules напрямую в `react` и `vue`

Отклонено, потому что TanStack Query опционален и должен оставаться composable, а не превращаться в неявное framework guidance.

### Добавить отдельные fragments `tanstack-query` и `vue-query`

Отклонено, потому что durable guidance в основном общая, а Vue-specific behavior уже покрывается фрагментом `vue` и runtime-фрагментами вроде `nuxt`.

### Оставить TanStack Query guidance только в project-local overrides

Отклонено, потому что правила про query keys, invalidation и hydration достаточно устойчивы и повторяются в нескольких репозиториях.

## Последствия

### Плюсы

- downstream-проекты могут явно объявлять `typescript` + `react` + `tanstack-query`
- Vue-проекты могут использовать привычное имя `vue-query`, не теряя benefits shared stack composition
- общий набор frontend guidance теперь покрывает и типовой server-state layer

### Минусы или цена

- командам всё равно понадобятся local rules для domain-specific query factories, caching lifetimes и деталей error UX
- alias-подход означает, что `vue-query` остаётся naming convenience, а не independently evolving stack

## Затронутые модули

- `fragments/stacks/tanstack-query.md`
- `registry.toml`
- `README.md`
- `README.ru.md`
- `tests/test_ai_sync.py`

## Инварианты и ограничения

- `tanstack-query` остаётся framework-neutral и server-state-oriented
- Vue-specific component и composable behavior остаются в `vue` и `nuxt`
- `vue-query` остаётся compatibility alias, а не отдельным source fragment

## Проверка

- renderer tests покрывают `tanstack-query` вместе с React
- renderer tests покрывают композицию через alias `vue-query`
- `registry.toml`, `README.md` и `README.ru.md` документируют новый stack name и alias

## Связанные артефакты

- [../../fragments/stacks/tanstack-query.md](../../fragments/stacks/tanstack-query.md)
- [../../registry.toml](../../registry.toml)
- [../../README.md](../../README.md)
- [../../README.ru.md](../../README.ru.md)