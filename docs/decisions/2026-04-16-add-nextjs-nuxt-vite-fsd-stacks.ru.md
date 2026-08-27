---
title: 'DECISION: add-nextjs-nuxt-vite-fsd-stacks'
permalink: ai-standards/decisions/2026-04-16-add-nextjs-nuxt-vite-fsd-stacks.ru
---

# DECISION: add-nextjs-nuxt-vite-fsd-stacks

Англоязычный оригинал: [2026-04-16-add-nextjs-nuxt-vite-fsd-stacks.md](2026-04-16-add-nextjs-nuxt-vite-fsd-stacks.md)

## Статус

Accepted

## Дата

2026-04-16

## Контекст

В `ai-standards` уже были baseline stack fragments для `react`, `vue` и `typescript`, но пока не было явного разделения между:

- React и Vue как базовыми UI framework layers
- Next.js и Nuxt как full-stack framework environments со своими server/rendering rules
- Vite как отдельно управляемым build/dev-server environment
- Feature-Sliced Design как opt-in архитектурной дисциплиной для более крупных фронтендов

Из-за этого downstream-проекты не могли точно выразить типовые современные комбинации. Проект мог запросить `react` или `vue`, но не было общего shared layer для App Router boundaries, Nuxt server routes, работы с Vite env/config или для slice/public-API constraints в Feature-Sliced Design.

Сверка с текущей официальной документацией Next.js, Nuxt, Vite и Feature-Sliced Design показала, что для каждого из этих направлений уже есть достаточно durable-guidance, чтобы оправдать отдельные composable stacks:

- Next.js: App Router, Server Components по умолчанию, server/client boundaries, явная работа с caching, route-level loading/error states и выбор между Server Actions и route handlers.
- Nuxt: SSR-friendly data composables, Nitro server boundaries, runtime config handling, route rules и hydration-safe client-only code.
- Vite: `import.meta.env`, согласованность aliases, осознанное использование plugins и фокус на build-specific, а не application-specific configuration.
- FSD: layer hierarchy, slice isolation, public APIs, purpose-based segmentation и явный запрет превращать `shared` в dumping ground для несвязанного кода.

## Решение

`ai-standards` добавляет четыре новых stack fragments: `nextjs`, `nuxt`, `vite` и `fsd`.

Эти стеки намеренно сделаны композиционными:

- `nextjs` дополняет `react` и обычно `typescript`
- `nuxt` дополняет `vue` и обычно `typescript`
- `vite` дополняет frontend-stacks только тогда, когда репозиторий сам владеет Vite-конфигурацией
- `fsd` остаётся opt-in architecture stack, который можно комбинировать с React- или Vue-проектами, когда это оправдано сложностью

Репозиторий также обновляет `registry.toml`, `README.md`, `README.ru.md` и renderer tests, чтобы покрыть новые stack names и примеры композиции.

## Почему

- разделяет UI-framework guidance и guidance, относящийся к full-stack frameworks и tooling
- позволяет downstream manifests точнее описывать современные frontend setups
- сохраняет фрагменты `react` и `vue` сфокусированными на поведении framework, а не на platform-specific concerns
- даёт переиспользуемое место для FSD-правил, не навязывая эту архитектуру всем frontend-проектам

## Рассмотренные альтернативы

### Расширить `react` и `vue` правилами для Next.js, Nuxt, Vite и FSD

Отклонено, потому что эти concerns зависят от среды выполнения и архитектурного выбора и должны оставаться композиционными.

### Добавить только `nextjs` и `nuxt`

Отклонено, потому что для Vite и FSD тоже уже достаточно durable-guidance, чтобы оправдать общие переиспользуемые фрагменты, а downstream-проекты часто нуждаются в них независимо от Next.js или Nuxt.

### Оставить FSD только как project-local guidance

Отклонено, потому что правила import hierarchy, public API и layering constraints уже достаточно устойчивы, чтобы переиспользоваться в нескольких frontend-репозиториях там, где команды сознательно выбирают эту архитектуру.

## Последствия

### Плюсы

- downstream-проекты могут явно собирать `typescript` + `react` + `nextjs`, `typescript` + `vue` + `nuxt` или `vite` + `fsd`
- shared frontend rules теперь отражают различие между framework, platform, tooling и architecture
- в репозитории появляется более чистая база для будущих стеков вроде `tanstack-query`, `storybook` или framework-specific testing stacks, если они понадобятся

### Минусы или цена

- увеличение числа stack fragments повышает стоимость поддержки
- некоторые проекты могут начать чрезмерно компоновать стеки, если манифесты не останутся дисциплинированными
- `fsd` намеренно остаётся high-level и не кодирует каждую naming-convention или folder-template из community starter kits

## Затронутые модули

- `fragments/stacks/nextjs.md`
- `fragments/stacks/nuxt.md`
- `fragments/stacks/vite.md`
- `fragments/stacks/fsd.md`
- `registry.toml`
- `README.md`
- `README.ru.md`
- `tests/test_ai_sync.py`

## Инварианты и ограничения

- `react` и `vue` остаются framework-level, а не platform-level fragments
- `nextjs`, `nuxt` и `vite` остаются сфокусированными на durable environment behavior, а не на transient version trivia
- `fsd` остаётся opt-in и architecture-oriented; он не должен незаметно превратиться в обязательный frontend baseline
- общие TypeScript-правила по-прежнему остаются в shared fragment `typescript`

## Проверка

- renderer tests покрывают манифесты с `nextjs`, `nuxt`, `vite` и `fsd`
- `registry.toml` перечисляет новые stacks
- `README.md` и `README.ru.md` документируют новые stack names и guidance по композиции

## Связанные артефакты

- [../../fragments/stacks/nextjs.md](../../fragments/stacks/nextjs.md)
- [../../fragments/stacks/nuxt.md](../../fragments/stacks/nuxt.md)
- [../../fragments/stacks/vite.md](../../fragments/stacks/vite.md)
- [../../fragments/stacks/fsd.md](../../fragments/stacks/fsd.md)
- [../../registry.toml](../../registry.toml)
- [../../README.md](../../README.md)
- [../../README.ru.md](../../README.ru.md)