---
title: 'DECISION: add-typescript-stack'
permalink: ai-standards/decisions/2026-04-15-add-typescript-stack.ru
---

# DECISION: add-typescript-stack

Англоязычный оригинал: [2026-04-15-add-typescript-stack.md](2026-04-15-add-typescript-stack.md)

## Статус

Accepted

## Дата

2026-04-15

## Контекст

В `ai-standards` уже есть stack fragments для Python, FastAPI, Django, React, Vue, PostgreSQL и Java Spring, но до сих пор не было общего переиспользуемого фрагмента с базовыми правилами именно для TypeScript.

Анализ `awesome-cursorrules`, официальной документации TypeScript и рекомендаций `typescript-eslint` показал, что для общего `typescript` stack уже есть достаточно устойчивых language-level правил, но при этом нет оснований смешивать их с framework-specific conventions в одном фрагменте.

Репозиторию нужен переиспользуемый слой TypeScript, который можно явно комбинировать с `react`, `vue` или будущими стеками вроде `nestjs`, не подтягивая по умолчанию архитектурные или UI-framework-specific правила.

## Решение

`ai-standards` добавляет новый общий stack fragment `typescript`, сфокусированный на language-level и type-system guidance.

Фрагмент покрывает строгие typing defaults, типизацию на границах модулей, безопасное narrowing, точное моделирование optionality, современные правила для module boundaries и явную валидацию недоверенного ввода.

Фрагмент не включает React, Vue, Next.js, NestJS и другие framework-specific conventions, а также не предписывает архитектурные паттерны вроде repository, factory, builder или Result-type-based error handling.

## Почему

- закрывает существующий пробел между framework stacks и language-level guidance
- позволяет downstream-проектам явно комбинировать `typescript` с `react`, `vue` и будущими TS-based stacks
- сохраняет общий фрагмент пригодным и для frontend, и для backend-репозиториев
- лучше опирается на официальные рекомендации TypeScript и `typescript-eslint`, а не только на upstream prompt collections
- не импортирует style dogma и framework coupling в shared layer

## Рассмотренные альтернативы

### Оставить TypeScript guidance только внутри framework stacks

Отклонено, потому что это дублирует language rules по нескольким стекам и оставляет TypeScript-проекты без framework без переиспользуемой базы.

### Добавить TypeScript-правила через расширение `react` и `vue`

Отклонено, потому что language-level rules должны оставаться композиционными и независимыми от конкретных UI frameworks.

### Импортировать более широкие TypeScript prompt packs напрямую

Отклонено, потому что большинство upstream-наборов смешивает переиспользуемые TypeScript-правила с framework conventions, folder structures, архитектурными предпочтениями и жёсткими стилевыми догмами, которые не подходят для shared standards.

## Последствия

### Плюсы

- downstream-проекты получают единую базу для TypeScript без framework-specific правил
- TypeScript guidance теперь живёт в одном общем месте и переиспользуется последовательно
- существующие `react` и `vue` stacks могут оставаться сфокусированными на поведении framework, а не на общих TS language rules

### Минусы или цена

- downstream-проектам по-прежнему нужны дополнительные stacks или local overrides для framework- и runtime-specific TS conventions
- репозиторию нужно поддерживать ещё один stack fragment и его документирование

## Затронутые модули

- `fragments/stacks/typescript.md`
- `registry.toml`
- `README.md`
- `README.ru.md`
- `tests/test_ai_sync.py`

## Инварианты и ограничения

- общий TypeScript stack должен оставаться language-level и framework-neutral
- существующие правила `core/error-handling`, основанные на explicit exceptions, сохраняют силу
- архитектурные паттерны вроде repository layering или dependency injection не навязываются через TypeScript stack
- framework-specific TS rules остаются в релевантных stack fragments или будущих выделенных стеках

## Проверка

- `registry.toml` содержит новый stack `typescript`
- `README.md` и `README.ru.md` перечисляют `typescript` среди текущих stack fragments и показывают, как он комбинируется с другими стеками
- renderer tests покрывают манифест с новым stack `typescript`
- проверки репозитория остаются зелёными

## Связанные артефакты

- [../../fragments/stacks/typescript.md](../../fragments/stacks/typescript.md)
- [../../registry.toml](../../registry.toml)
- [../../README.md](../../README.md)
- [../../README.ru.md](../../README.ru.md)