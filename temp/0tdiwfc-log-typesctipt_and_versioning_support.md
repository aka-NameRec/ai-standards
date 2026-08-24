<h2>Оглавление</h2>

- [Адаптация правил для TypeScript из awesome-cursorrules](#адаптация-правил-для-typescript-из-awesome-cursorrules)
- [Дополнения к правилам TypeScript по официальным рекомендациям и лучшим практикам](#дополнения-к-правилам-typescript-по-официальным-рекомендациям-и-лучшим-практикам)
- [Форматирование правил TypeScript в keep adapt reject для decision note](#форматирование-правил-typescript-в-keep-adapt-reject-для-decision-note)
- [Import TypeScript Stack Into ai-standards](#import-typescript-stack-into-ai-standards)
- [Внесение правил TypeScript в проект с обновлением ConPort и decision](#внесение-правил-typescript-в-проект-с-обновлением-conport-и-decision)
- [Коммит и стандартное слияние ветки с поддержкой TypeScript](#коммит-и-стандартное-слияние-ветки-с-поддержкой-typescript)
- [Подтверждение коммита и продолжение работы](#подтверждение-коммита-и-продолжение-работы)
- [Синхронизация локального состояния с origin через pull](#синхронизация-локального-состояния-с-origin-через-pull)
- [Верификация предложений по версионности и flow bump\_version](#верификация-предложений-по-версионности-и-flow-bump_version)
- [Уточнение требований к bump\_version и локальной release политике ai-standards](#уточнение-требований-к-bump_version-и-локальной-release-политике-ai-standards)
- [Проверка release правил main и структуры версий перед изменениями](#проверка-release-правил-main-и-структуры-версий-перед-изменениями)
- [Внесение изменений по версионности в ветке feature 0tdj06b package\_versioning](#внесение-изменений-по-версионности-в-ветке-feature-0tdj06b-package_versioning)
- [Коммит ветки и обсуждение release skill для ai-standards](#коммит-ветки-и-обсуждение-release-skill-для-ai-standards)
- [Подтверждённый коммит и стандартное слияние ветки](#подтверждённый-коммит-и-стандартное-слияние-ветки)


## Адаптация правил для TypeScript из awesome-cursorrules

**Question**

(0tdiwfc) Пожалуйста, перейди в репозиторий ai-standards.
Нам нужно его дополнить правилами для TypeScript.
Пожалуйста, изучи https://github.com/PatrickJS/awesome-cursorrules на предмет адаптации правил для этого языка.
Жду от тебя предложений по адаптации.

**Answer**

Перехожу в `ai-standards`, загружу его локальные инструкции и контекст проекта, затем отдельно посмотрю актуальное содержимое `awesome-cursorrules` для TypeScript и соберу предложения по адаптации.

Нашёл целевой репозиторий. Сейчас прочитаю его `AGENTS.md`, проверю структуру и загружу ConPort именно для `ai-standards`, чтобы опираться на его правила, а не на контекст `cockpit`.

Контекст `ai-standards` восстановлен. Дальше смотрю, как в репозитории устроены существующие stack-фрагменты и какие именно TypeScript-правила есть в `awesome-cursorrules`, чтобы предложить не копирование, а нормализованную адаптацию под текущую архитектуру.

В `awesome-cursorrules` по TypeScript много разрозненных файлов, и качество у них неоднородное: часть правил полезна как сырьё, часть слишком vendor-specific или просто пустые заготовки. Сейчас добираю локальный контекст в `ai-standards`, чтобы предложения сразу ложились в его формат `stack fragment + registry + docs`, а не были списком абстракций.

Собираю точечные источники из самого репозитория-источника, чтобы предложения были привязаны к конкретным upstream-файлам, а не к общему README. После этого дам нормализованную схему: что имеет смысл взять в общий `typescript` stack, что оставить в `react`/`vue`, а что сразу отфильтровать.

Сигнал из upstream уже понятен: самый полезный TypeScript-материал там не в “TypeScript-only” файлах, а размазан между `rules-new/typescript.mdc`, `typescript-code-convention`, `javascript-typescript-code-quality`, а также framework-специфичными наборами вроде NestJS и React. Это подтверждает, что в `ai-standards` разумнее делать базовый `typescript` stack и поверх него дополнять `react`, `vue`, а при необходимости потом отдельный `nestjs`, а не пытаться собрать всё в один монолитный фрагмент.

Изучил `awesome-cursorrules` и локальную структуру `ai-standards`. Из этого сырья TypeScript имеет смысл добавлять не как “свалку правил под всё подряд”, а как отдельный базовый stack-фрагмент `typescript`, который покрывает именно язык и типовую дисциплину. Framework-специфику лучше оставлять в существующих или будущих фрагментах вроде [react.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/react.md:1), [vue.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/vue.md:1) и, если понадобится позже, отдельного `nestjs`.

**Что я бы предложил принять в `typescript` stack**

Основа должна быть короткой и дюрабельной:

- Prefer `strict` TypeScript configuration and keep type errors actionable instead of weakening the compiler.
- Avoid `any`; use `unknown`, narrowing, and explicit domain types where the shape is not yet proven.
- Add explicit types at module boundaries: public function return types, exported contracts, shared utilities, and external API adapters.
- Keep local types close to usage; extract shared types only when they are reused across module boundaries.
- Prefer discriminated unions, utility types, and type guards over ad hoc assertions.
- Prefer `const`, `readonly`, and immutable updates when they improve correctness and reduce incidental mutation.
- Use descriptive names; boolean values should read as predicates such as `is`, `has`, or `can`.
- Avoid broad type assertions and non-null assertions unless the invariant is already established nearby.
- Model validation and parsing explicitly at the boundary where untrusted input enters the system.
- Keep framework-specific patterns out of the shared TypeScript fragment.

Это хорошо ложится в текущую философию `ai-standards`: короткие, переносимые, language-level правила без жёсткой привязки к React/Nest/Next/Vite.

**Что стоит адаптировать, а не переносить как есть**

В upstream есть полезные идеи, но в сыром виде их нельзя тащить напрямую:

- `Prefer interfaces over types for object definitions`  
  Лучше смягчить до: `Use interfaces or type aliases deliberately based on the shape and extension needs.`  
  Абсолютное правило про `interface > type` давно спорное.
- `Use explicit return types for public functions`  
  Это стоит оставить именно для публичных и shared boundary-функций, а не для каждой локальной стрелки.
- `Use async/await over Promises`  
  Лучше формулировать как предпочтение для читаемости в многошаговых async-flow, а не как догму.
- `Implement proper error handling with custom error types`  
  Можно оставить идею явных ошибок, но не вводить обязательный “custom error type everywhere”.
- `Use early returns`, `DRY`, `minimal code changes`  
  Эти правила уже частично покрыты `core/base` и текущей философией репозитория, так что их лучше не дублировать в `typescript`, а только не противоречить им.

**Что я бы сразу отверг**

Эти вещи либо слишком догматичны, либо конфликтуют с текущими правилами репозитория:

- `Use Result types for operations that can fail`  
  Это конфликтует с текущим [error-handling.md](/home/shtirliz/workspace/myself/ai-standards/fragments/core/error-handling.md:1), где базовая стратегия построена вокруг exceptions с actionable context.
- `Implement the Repository pattern for data access`  
  Для общего TypeScript stack это слишком архитектурно и слишком бэкенд-специфично.
- `Use the Builder pattern`, `Factory pattern`, `dependency injection`  
  Это не language-level правила, а опциональные архитектурные паттерны.
- `Always declare the type of each variable`  
  Плохое правило для TypeScript: ломает читаемость и игнорирует силу inference.
- `Use JSDoc to document public classes and methods`  
  Слишком Java-like и не универсально полезно для всех TS-проектов.
- `One export per file`  
  Слишком жёстко, особенно для UI, schema/type modules и utility aggregates.
- `Use React.FC`  
  Это уже не выглядит как хорошая современная общая рекомендация.
- `Use barrel exports (index.ts)`  
  Не как общее правило. В части проектов это помогает, в части размывает границы и ухудшает tree-shaking/debuggability.
- `Prefix interfaces for React props with Props`  
  Это должно жить в `react`, а не в `typescript`.

**Как я бы встроил это в `ai-standards`**

Минимальная и чистая адаптация:

1. Добавить новый фрагмент `fragments/stacks/typescript.md`.
2. Зарегистрировать его в [registry.toml](/home/shtirliz/workspace/myself/ai-standards/registry.toml:1) как `typescript`.
3. Не раздувать текущий `react`-фрагмент, а при использовании `react + typescript` подключать оба стека.
4. В [README.md](/home/shtirliz/workspace/myself/ai-standards/README.md:1) и `README.ru.md` добавить `typescript` в список доступных stack fragments.
5. Добавить тест рендера в [tests/test_ai_sync.py](/home/shtirliz/workspace/myself/ai-standards/tests/test_ai_sync.py:1), как уже сделано для `java-spring`, `vue` и feature-фрагментов.

**Рекомендованный черновик самого фрагмента**

```md
<!-- Source: https://github.com/PatrickJS/awesome-cursorrules/tree/main -->
<!-- Imported: 2026-04-15 -->
<!-- Adaptation: normalized for UMA2, reduced to durable TypeScript guidance, and stripped of framework-specific and overly prescriptive style rules -->

## TypeScript Stack
- Prefer strict TypeScript configuration and keep compiler guarantees strong instead of weakening types to silence errors.
- Avoid `any`; use `unknown`, narrowing, and explicit domain types where the value shape is not yet proven.
- Add explicit types at public and shared module boundaries, including exported functions, shared utilities, and external adapters.
- Keep local types close to where they are used; extract shared types only when they cross module boundaries or are reused.
- Prefer discriminated unions, utility types, and type guards over broad assertions and duplicated shape logic.
- Prefer `const`, `readonly`, and immutable updates when they improve correctness and make state changes easier to reason about.
- Use descriptive names; boolean values should read as predicates such as `is`, `has`, or `can`.
- Avoid non-null assertions and unchecked type assertions unless the invariant is established nearby and obvious from the code.
- Validate and parse untrusted input explicitly at the application boundary before it flows into domain logic.
- Keep framework-specific conventions in the relevant stack fragments rather than in the shared TypeScript rules.
```

**На какие upstream-источники я опирался**

- Общий индекс и перечень TypeScript-related rules: https://github.com/PatrickJS/awesome-cursorrules
- Базовый `rules-new/typescript.mdc`: https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules-new/typescript.mdc
- Общие JS/TS code-quality rules: https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules/javascript-typescript-code-quality-cursorrules-pro/general-coding-principles.mdc
- Minimal-change rule: https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules/javascript-typescript-code-quality-cursorrules-pro/minimal-code-changes-rule.mdc
- Early-return rule: https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules/javascript-typescript-code-quality-cursorrules-pro/coding-guidelines---early-returns-and-conditionals.mdc
- Более жёсткий TypeScript/NestJS набор, откуда видно, что часть правил слишком догматична для shared stack: https://raw.githubusercontent.com/PatrickJS/awesome-cursorrules/main/rules/typescript-nestjs-best-practices-cursorrules-promp/typescript-general-guidelines.mdc

Если хочешь, следующим сообщением могу сразу сделать из этого полноценный импорт в `ai-standards`: добавить `fragments/stacks/typescript.md`, обновить `registry.toml`, README и тесты.

## Дополнения к правилам TypeScript по официальным рекомендациям и лучшим практикам

**Question**

(0tdizds) Хочу попросить тебя предложить дополнения к предложенному тобой выше для TypeScript (что я полностью поддерживаю)  на основе известных тебе официальных рекомендаций и лучших практик, не ограничиваясь репозиторием, на который я сослался.

**Answer**

Добираю это уже не от `awesome-cursorrules`, а от первичных источников: TypeScript Handbook и `typescript-eslint`, чтобы предложить именно те дополнения, которые выглядят дюрабельными для общего stack-фрагмента, а не локальными стилевыми вкусами.

Я бы дополнил предложенный ранее `typescript` stack ещё несколькими правилами, но разделил бы их на две группы: действительно общие language-level правила, которые стоит включить в сам фрагмент, и tooling-правила, которые лучше оформить как рекомендации в документации, а не как жёсткие инструкции в `AGENTS.md`.

**Что стоит добавить прямо в `typescript` stack**

Из официальных рекомендаций TypeScript и `typescript-eslint` я бы добавил вот это:

- Prefer `strict` mode and avoid selectively disabling its safety guarantees unless the repository has a documented reason.  
  Основание: `noImplicitAny`, `useUnknownInCatchVariables` и другие safety flags являются частью строгой конфигурации TypeScript.  
  Источники:  
  https://www.typescriptlang.org/tsconfig/noImplicitAny.html  
  https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-4.html

- Prefer `unknown` over `any` for values whose runtime shape is not yet proven, especially at external boundaries and in caught errors.  
  Это усиливает уже предложенное правило про отказ от `any`, но делает его практически полезным.  
  Источники:  
  https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-4.html  
  https://typescript-eslint.io/blog/avoiding-anys

- Narrow values explicitly with type guards and control-flow checks before using them as specific domain types.  
  Это хорошо согласуется с официальной моделью narrowing в TypeScript и делает правило про `unknown` завершённым.  
  Источник:  
  https://www.typescriptlang.org/docs/handbook/2/narrowing.html

- Use the `satisfies` operator when you need to validate an object shape without losing useful inference.  
  Это одна из самых практичных современных рекомендаций, и она реально полезна как shared standard.  
  Источник:  
  https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html

- Use `import type` and `export type` for type-only module boundaries when the project relies on modern ESM-style tooling.  
  Это помогает держать module semantics явными и хорошо ложится на современные TS-проекты.  
  Источник:  
  https://www.typescriptlang.org/tsconfig/verbatimModuleSyntax.html

- Treat optional properties precisely; do not use `prop?: T` when the real contract is `prop: T | undefined`, and vice versa.  
  Это важное уточнение для model contracts, DTO и config objects.  
  Источник:  
  https://www.typescriptlang.org/tsconfig/exactOptionalPropertyTypes.html

- Treat indexed access as potentially absent unless the contract proves the key exists.  
  Это можно выразить как language-level правило без жёсткой привязки к одному `tsconfig` flag, но оно вдохновлено `noUncheckedIndexedAccess`.  
  Источник:  
  https://www.typescriptlang.org/tsconfig/noUncheckedIndexedAccess.html

- Use `override` explicitly in class hierarchies so inheritance changes fail loudly instead of drifting silently.  
  Это полезное правило, но только если проект вообще использует inheritance.  
  Источник:  
  https://www.typescriptlang.org/tsconfig/noImplicitOverride.html

**Что я бы рекомендовал, но не включал в сам stack как жёсткое правило**

Эти вещи лучше оформлять как tooling guidance в README или в отдельной usage-документации:

- Prefer typed linting configs from `typescript-eslint`, such as `recommended-type-checked`, when the repository can afford the performance cost.  
  Это уже не язык, а настройка lint pipeline.  
  Источники:  
  https://typescript-eslint.io/users/configs  
  https://typescript-eslint.io/blog/announcing-typescript-eslint-v6

- Do not force explicit annotations everywhere; prefer compiler strictness and inference, adding annotations where they improve module boundaries, readability, or error messages.  
  Это важно как контрбаланс против плохого правила “типизируй всё руками”.  
  Источник:  
  https://typescript-eslint.io/rules/typedef

- Prefer banning unsafe escape hatches in linting rather than relying only on `noImplicitAny`.  
  Например, `no-explicit-any` и ограничения на `@ts-ignore`.  
  Источники:  
  https://typescript-eslint.io/blog/avoiding-anys  
  https://typescript-eslint.io/rules/no-explicit-any/

- Avoid redundant ESLint rules that duplicate TypeScript checks.  
  Это полезная operational recommendation, но не правило код-стиля.  
  Источники:  
  https://typescript-eslint.io/troubleshooting/faqs/eslint/  
  https://typescript-eslint.io/troubleshooting/typed-linting/performance/

**Что это даёт именно для `ai-standards`**

Если держать фрагмент компактным, я бы расширил твой предыдущий черновик до такого вида:

```md
## TypeScript Stack
- Prefer strict TypeScript configuration and keep compiler guarantees strong instead of weakening types to silence errors.
- Avoid `any`; use `unknown`, narrowing, and explicit domain types where the value shape is not yet proven.
- Add explicit types at public and shared module boundaries, including exported functions, shared utilities, and external adapters.
- Keep local types close to where they are used; extract shared types only when they cross module boundaries or are reused.
- Prefer discriminated unions, utility types, and type guards over broad assertions and duplicated shape logic.
- Use `satisfies` when you need to verify object shape without losing useful inference.
- Prefer `const`, `readonly`, and immutable updates when they improve correctness and make state changes easier to reason about.
- Use descriptive names; boolean values should read as predicates such as `is`, `has`, or `can`.
- Avoid non-null assertions and unchecked type assertions unless the invariant is established nearby and obvious from the code.
- Treat optional properties and indexed access precisely; model absence explicitly instead of relying on loose object semantics.
- Use type-only imports and exports deliberately when the project tooling supports modern TypeScript module semantics.
- Use explicit `override` in inheritance-based code so base-class changes fail loudly.
- Validate and parse untrusted input explicitly at the application boundary before it flows into domain logic.
- Keep framework-specific conventions in the relevant stack fragments rather than in the shared TypeScript rules.
```

**Что я бы не добавлял даже с опорой на “best practices”**

Я бы по-прежнему не включал в shared `typescript` fragment такие популярные, но слишком спорные или context-bound вещи:

- `Prefer interfaces over types`
- `Always annotate every variable`
- `Use barrel exports`
- `One export per file`
- `Use Result types for failures`
- `Use JSDoc for all public APIs`
- `Use React.FC`

Они либо не поддерживаются как универсальная официальная рекомендация, либо слишком зависят от стека и локального стиля команды.

Источники:
- TypeScript Handbook: https://www.typescriptlang.org/docs/handbook/2/narrowing.html
- TypeScript 4.4 release notes: https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-4.html
- TypeScript 4.9 release notes (`satisfies`): https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html
- `noImplicitAny`: https://www.typescriptlang.org/tsconfig/noImplicitAny.html
- `noUncheckedIndexedAccess`: https://www.typescriptlang.org/tsconfig/noUncheckedIndexedAccess.html
- `exactOptionalPropertyTypes`: https://www.typescriptlang.org/tsconfig/exactOptionalPropertyTypes.html
- `noImplicitOverride`: https://www.typescriptlang.org/tsconfig/noImplicitOverride.html
- `verbatimModuleSyntax`: https://www.typescriptlang.org/tsconfig/verbatimModuleSyntax.html
- `typescript-eslint` shared configs: https://typescript-eslint.io/users/configs
- `typescript-eslint` on avoiding `any`: https://typescript-eslint.io/blog/avoiding-anys
- `typedef` guidance against over-annotation: https://typescript-eslint.io/rules/typedef

Если хочешь, следующим шагом я могу сделать ещё более полезную вещь: разложить это на `keep / adapt / reject` именно в формате будущего decision/import note для `ai-standards`, чтобы это уже можно было почти без доработки вносить в репозиторий.

## Форматирование правил TypeScript в keep adapt reject для decision note

**Question**

(0tdizkf)
> следующим шагом я могу сделать ещё более полезную вещь: разложить это на keep / adapt / reject именно в формате будущего decision/import note для ai-standards, чтобы это уже можно было почти без доработки вносить в репозиторий.

Да, сделай пожалуйста.

**Answer**

Собираю это в пригодный для репозитория import note: отдельно источник, proposed `keep / adapt / reject`, конфликты с текущими core-правилами и итоговую рекомендуемую форму `typescript` stack.

Ниже черновик в формате import note / decision support для `ai-standards`. Я держал его в логике существующих импортов: источник, классификация, конфликты, итоговая рекомендация по составу фрагмента.

**Draft Import Note**

## Import TypeScript Stack Into ai-standards

**Date:** 2026-04-15

### Goal

Add a reusable `typescript` stack fragment to `ai-standards` based on durable TypeScript language guidance rather than framework-specific conventions.

The fragment should:

- cover TypeScript language and type-system practices that remain useful across repositories
- avoid duplicating existing `core/*` rules
- avoid importing React, Vue, Next.js, NestJS, or other framework-specific conventions into the shared TypeScript layer
- stay compatible with existing UMA2 constraints, especially error handling, architecture, and minimal-change discipline

### Sources Reviewed

#### Source 1: `awesome-cursorrules` TypeScript-related rules

Representative upstream files reviewed:

- `rules-new/typescript.mdc`
- `rules/typescript-code-convention-cursorrules-prompt-file/general-typescript-rule.mdc`
- `rules/javascript-typescript-code-quality-cursorrules-pro/*`
- `rules/typescript-nestjs-best-practices-cursorrules-promp/typescript-general-guidelines.mdc`
- several React/Vue/NestJS TypeScript rule sets as context for separation boundaries

Source repository:

- https://github.com/PatrickJS/awesome-cursorrules

#### Source 2: Official TypeScript documentation

Primary official references reviewed:

- Narrowing
  https://www.typescriptlang.org/docs/handbook/2/narrowing.html
- TypeScript 4.4 release notes
  https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-4.html
- TypeScript 4.9 release notes (`satisfies`)
  https://www.typescriptlang.org/docs/handbook/release-notes/typescript-4-9.html
- `noImplicitAny`
  https://www.typescriptlang.org/tsconfig/noImplicitAny.html
- `noUncheckedIndexedAccess`
  https://www.typescriptlang.org/tsconfig/noUncheckedIndexedAccess.html
- `exactOptionalPropertyTypes`
  https://www.typescriptlang.org/tsconfig/exactOptionalPropertyTypes.html
- `noImplicitOverride`
  https://www.typescriptlang.org/tsconfig/noImplicitOverride.html
- `verbatimModuleSyntax`
  https://www.typescriptlang.org/tsconfig/verbatimModuleSyntax.html

#### Source 3: `typescript-eslint` best-practice guidance

Primary official references reviewed:

- Shared configs
  https://typescript-eslint.io/users/configs
- Avoiding `any`
  https://typescript-eslint.io/blog/avoiding-anys
- `typedef`
  https://typescript-eslint.io/rules/typedef
- `no-explicit-any`
  https://typescript-eslint.io/rules/no-explicit-any/

### Proposed Scope Of The New Stack

The new `typescript` stack should cover only:

- strong typing and type-safety defaults
- module-boundary typing discipline
- explicit narrowing and validation at trust boundaries
- modern TypeScript features that improve correctness without over-prescribing code style

It should not cover:

- React component structure
- Vue component conventions
- Next.js routing/data fetching
- NestJS module/service/controller layout
- package manager, formatter, bundler, or test-runner choices
- broad architecture patterns such as repository, builder, or factory patterns

### Classification

### Accepted As Reusable (`KEEP` / `ADAPT`)

#### 1. Strong compiler safety defaults

**Candidate idea**

- Use strict TypeScript configuration
- Enable strict mode
- Avoid weakening the compiler to silence errors

**Decision**

- `keep`

**Reason**

This is durable, language-level, and broadly reusable across TS projects.

**Normalized rule**

- Prefer strict TypeScript configuration and keep compiler guarantees strong instead of weakening types to silence errors.

---

#### 2. Avoid `any`

**Candidate idea**

- Avoid using `any`
- Prefer `unknown` for unknown values

**Decision**

- `adapt`

**Reason**

The useful rule is not just “avoid `any`”, but “use `unknown` plus narrowing where the runtime shape is not yet proven”.

**Normalized rule**

- Avoid `any`; use `unknown`, narrowing, and explicit domain types where the value shape is not yet proven.

---

#### 3. Narrow values before treating them as domain types

**Candidate idea**

- Use type guards for runtime type checking
- Implement proper null checking
- Narrow unknown values

**Decision**

- `keep`

**Reason**

This matches official TypeScript guidance directly and complements the `unknown` rule.

**Normalized rule**

- Narrow values explicitly with type guards and control-flow checks before using them as specific domain types.

---

#### 4. Explicit typing at module boundaries

**Candidate idea**

- Use explicit return types for public functions
- Create necessary types
- Add explicit types where helpful

**Decision**

- `adapt`

**Reason**

The broad “type everything” wording is too rigid. The durable version is boundary-focused typing, not annotation of every local variable.

**Normalized rule**

- Add explicit types at public and shared module boundaries, including exported functions, shared utilities, and external adapters.

---

#### 5. Keep local types close, extract shared types deliberately

**Candidate idea**

- Keep type definitions close to where they’re used
- Export shared types from dedicated files
- Place shared types in a `types` directory

**Decision**

- `adapt`

**Reason**

The “always use a `types/` directory” prescription is too project-specific. The durable part is locality first, extraction only when reuse or boundaries justify it.

**Normalized rule**

- Keep local types close to where they are used; extract shared types only when they cross module boundaries or are reused.

---

#### 6. Prefer discriminated unions, utility types, and precise modeling

**Candidate idea**

- Leverage TypeScript utility types
- Use unions and mapped types
- Use discriminated unions for type safety

**Decision**

- `keep`

**Reason**

These are core strengths of TypeScript and broadly applicable.

**Normalized rule**

- Prefer discriminated unions, utility types, and type guards over broad assertions and duplicated shape logic.

---

#### 7. Use `satisfies` where it preserves inference

**Candidate idea**

- Validate object shape while preserving useful inference

**Decision**

- `keep`

**Reason**

This is a modern, official TypeScript best practice with strong practical value.

**Normalized rule**

- Use `satisfies` when you need to verify object shape without losing useful inference.

---

#### 8. Prefer immutability-oriented defaults when useful

**Candidate idea**

- Use readonly for immutable properties
- Prefer const over let
- Prefer immutability for data

**Decision**

- `adapt`

**Reason**

The durable rule is not “make everything immutable”, but “prefer immutability when it improves correctness and reasoning”.

**Normalized rule**

- Prefer `const`, `readonly`, and immutable updates when they improve correctness and make state changes easier to reason about.

---

#### 9. Boolean naming as predicates

**Candidate idea**

- Use descriptive names with auxiliary verbs
- Use verbs for boolean variables such as `isLoading`, `hasError`, `canDelete`

**Decision**

- `keep`

**Reason**

This is widely applicable and improves readability without locking the project into a style niche.

**Normalized rule**

- Use descriptive names; boolean values should read as predicates such as `is`, `has`, or `can`.

---

#### 10. Avoid unchecked assertions

**Candidate idea**

- Avoid type assertions unless necessary
- Handle nullability properly

**Decision**

- `adapt`

**Reason**

The important reusable guidance is to keep assertions rare and local to already-proven invariants.

**Normalized rule**

- Avoid non-null assertions and unchecked type assertions unless the invariant is established nearby and obvious from the code.

---

#### 11. Model optionality and absence precisely

**Candidate idea**

- Implement proper null checking
- Treat optional properties carefully
- Handle indexed lookups safely

**Decision**

- `adapt`

**Reason**

This is best expressed as a modeling rule rather than as mandatory `tsconfig` flags for every repository.

**Normalized rule**

- Treat optional properties and indexed access precisely; model absence explicitly instead of relying on loose object semantics.

---

#### 12. Use type-only imports and exports deliberately

**Candidate idea**

- Separate value-level and type-level module concerns

**Decision**

- `keep`

**Reason**

This is a durable modern TypeScript practice, especially for ESM-aware toolchains.

**Normalized rule**

- Use type-only imports and exports deliberately when the project tooling supports modern TypeScript module semantics.

---

#### 13. Use explicit `override` in inheritance-based code

**Candidate idea**

- Fail loudly when inherited members drift

**Decision**

- `keep`

**Reason**

Useful, language-level, and non-invasive when a project uses classes and inheritance.

**Normalized rule**

- Use explicit `override` in inheritance-based code so base-class changes fail loudly.

---

#### 14. Validate untrusted input at boundaries

**Candidate idea**

- Parse external input explicitly before it enters core logic

**Decision**

- `keep`

**Reason**

This aligns with TypeScript’s compile-time-only guarantees and complements existing error-handling expectations.

**Normalized rule**

- Validate and parse untrusted input explicitly at the application boundary before it flows into domain logic.

---

#### 15. Keep framework-specific conventions out of shared TypeScript rules

**Candidate idea**

- Do not mix React, Vue, Next.js, or NestJS rules into the base TS layer

**Decision**

- `keep`

**Reason**

This is necessary to keep the fragment reusable and consistent with current `ai-standards` stack separation.

**Normalized rule**

- Keep framework-specific conventions in the relevant stack fragments rather than in the shared TypeScript rules.

### Rejected (`REJECT`)

#### A. “Prefer interfaces over types”

**Reason for rejection**

This is a long-running style preference, not a durable universal best practice. Official TypeScript guidance does not support enforcing this as a shared rule across projects.

---

#### B. “Always declare the type of each variable and function”

**Reason for rejection**

Over-annotation fights TypeScript inference, creates noise, and is not recommended as a universal practice. Shared rules should prefer explicit boundary types, not blanket annotation.

---

#### C. “Use barrel exports (`index.ts`) for organizing exports”

**Reason for rejection**

Barrels are context-dependent. They help some codebases and hurt clarity, dependency boundaries, or bundling in others. Not suitable as a universal stack rule.

---

#### D. “One export per file”

**Reason for rejection**

Too rigid for shared TS guidance. It is not language-specific best practice and becomes counterproductive in utility, type, and UI modules.

---

#### E. “Use JSDoc for public classes and methods”

**Reason for rejection**

This is too documentation-style-specific for a shared stack rule. Some teams benefit from it; others rely on types, naming, tests, and selective docs.

---

#### F. “Use Result types for operations that can fail”

**Reason for rejection**

Conflicts with existing `core/error-handling.md`, which standardizes explicit exceptions with actionable context rather than Result-style error signaling.

---

#### G. “Implement the Repository pattern for data access”

**Reason for rejection**

Too architectural and not specific to TypeScript as a language. Also inappropriate for a shared TS layer because persistence strategy belongs in stack- or architecture-specific guidance.

---

#### H. “Use the Builder pattern / Factory pattern / dependency injection”

**Reason for rejection**

These are optional architectural patterns, not durable TypeScript language rules.

---

#### I. “Use React.FC”

**Reason for rejection**

React-specific and no longer a strong default recommendation. If React rules are needed, they belong in the React stack.

---

#### J. “Use a fixed folder structure such as `src/components`, `src/hooks`, `src/pages`, `src/types`, `src/utils`”

**Reason for rejection**

Project- and framework-specific. Not appropriate for a generic TypeScript fragment.

### Existing Rule Interactions

### Alignment With `core/base.md`

Strong alignment:

- descriptive naming
- small focused functions
- avoiding duplication
- minimal and coherent changes

The TypeScript stack should not repeat those core rules; it should only add TS-specific precision.

### Alignment With `core/error-handling.md`

Compatible additions:

- validate and parse untrusted input explicitly
- avoid unsafe assertions
- preserve strong typing at boundaries

Conflict to reject:

- Result-type-first failure handling

The shared TS fragment should remain exception-compatible with the existing core rule set.

### Alignment With `core/architecture.md`

The new `typescript` fragment should stay architecture-neutral.

It should not prescribe:

- repository pattern
- dependency injection
- service/controller/module structures

Those belong in framework- or architecture-specific fragments such as a future `nestjs` stack if needed.

### Relationship To Existing Frontend Stacks

#### `react`

The new `typescript` stack should complement `react`, not replace or expand it.

Keep in `react`:

- component API design
- prop ownership
- presentational vs domain logic
- design-system preservation

Do not move TS language rules into `react` unless they are React-specific.

#### `vue`

The current `vue` fragment already includes one TS-related rule:

- explicit TypeScript types for props, emits, composables, and store contracts

That remains valid. The new `typescript` stack should provide the baseline language discipline, while `vue` retains Vue-specific TS guidance.

### Recommended Final Fragment

```md
<!-- Source: https://github.com/PatrickJS/awesome-cursorrules/tree/main -->
<!-- Additional references: official TypeScript docs and typescript-eslint guidance -->
<!-- Imported: 2026-04-15 -->
<!-- Adaptation: normalized for UMA2, reduced to durable TypeScript guidance, and stripped of framework-specific and overly prescriptive style rules -->

## TypeScript Stack
- Prefer strict TypeScript configuration and keep compiler guarantees strong instead of weakening types to silence errors.
- Avoid `any`; use `unknown`, narrowing, and explicit domain types where the value shape is not yet proven.
- Add explicit types at public and shared module boundaries, including exported functions, shared utilities, and external adapters.
- Keep local types close to where they are used; extract shared types only when they cross module boundaries or are reused.
- Prefer discriminated unions, utility types, and type guards over broad assertions and duplicated shape logic.
- Use `satisfies` when you need to verify object shape without losing useful inference.
- Prefer `const`, `readonly`, and immutable updates when they improve correctness and make state changes easier to reason about.
- Use descriptive names; boolean values should read as predicates such as `is`, `has`, or `can`.
- Avoid non-null assertions and unchecked type assertions unless the invariant is established nearby and obvious from the code.
- Treat optional properties and indexed access precisely; model absence explicitly instead of relying on loose object semantics.
- Use type-only imports and exports deliberately when the project tooling supports modern TypeScript module semantics.
- Use explicit `override` in inheritance-based code so base-class changes fail loudly.
- Validate and parse untrusted input explicitly at the application boundary before it flows into domain logic.
- Keep framework-specific conventions in the relevant stack fragments rather than in the shared TypeScript rules.
```

### Recommended Repository Changes

If this import is approved, the corresponding repo changes should be:

1. Add `fragments/stacks/typescript.md`.
2. Register `typescript = ["stacks/typescript"]` in `registry.toml`.
3. Update `README.md` and `README.ru.md` to list `typescript` among available stacks and show example composition with `react` or `vue`.
4. Add a render test in `tests/test_ai_sync.py` that confirms `typescript` renders correctly.
5. Optionally add a short bilingual usage note only if the repository wants per-stack documentation beyond README coverage.

### Final Recommendation

Adopt a new shared `typescript` stack fragment.

The strongest reusable value is:

- strict typing defaults
- explicit boundary modeling
- safe narrowing
- modern TS features for correctness
- separation of language rules from framework rules

Do not adopt:

- framework conventions
- rigid style dogma
- architecture patterns disguised as language rules
- Result-based error handling
- anti-inference annotation habits

Если хочешь, следующим шагом я уже переведу это в конкретный patch для `ai-standards`: добавлю сам `typescript` fragment, запись в `registry.toml`, правки `README`/`README.ru.md` и тест.

## Внесение правил TypeScript в проект с обновлением ConPort и decision

**Question**

(0tdizmx) Да, я думаю, следует уже внести изменения в проект, согласно твоим рекомендациям.

(0tdiznu) Прошу тебя также обновить ConPort знаниями, полученными в этом чате.

(0tdizok) Дополнительно, полагаю, нужна статья в decisions

**Answer**

Вношу это как полноценный импорт: добавлю `typescript` stack fragment, зарегистрирую его, обновлю README и тесты, затем оформлю decision record в `docs/decisions` с русской парой и синхронизирую ConPort по результату.

Нашёл существующий формат decision records и точки в README. Сейчас внесу сам stack, затем синхронно обновлю англоязычную и русскую документацию и оформлю отдельное решение про добавление `typescript` как базового language-level stack.

Начинаю правки файлов. Сначала добавлю новый `fragments/stacks/typescript.md` и регистрацию в `registry.toml`, затем обновлю README и decision record, после чего добью тест рендера.

Основные правки внесены. Сейчас прогоню проверки репозитория и рендер-чек, после чего запишу итог в ConPort как принятое решение, прогресс и активный контекст.

`ruff`, `mypy` и `ai_sync check` прошли. `rtk uv run pytest -q` упал не из-за `rtk`, а потому что в окружении нет отдельного исполняемого `pytest`; добиваю это корректным путём через `uv run python -m pytest -q`.

В проект внесены изменения по согласованной схеме. Добавлен новый stack fragment [fragments/stacks/typescript.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/typescript.md:1) с language-level правилами для TypeScript, а в [registry.toml](/home/shtirliz/workspace/myself/ai-standards/registry.toml:8) зарегистрирован новый stack `typescript`.

Документация тоже синхронизирована. В [README.md](/home/shtirliz/workspace/myself/ai-standards/README.md:42) и [README.ru.md](/home/shtirliz/workspace/myself/ai-standards/README.ru.md:42) `typescript` добавлен в перечень stack fragments и в примеры композиции с `react` и `vue`; в `docs/decisions` создано решение [2026-04-15-add-typescript-stack.md](/home/shtirliz/workspace/myself/ai-standards/docs/decisions/2026-04-15-add-typescript-stack.md:1) и его русская пара [2026-04-15-add-typescript-stack.ru.md](/home/shtirliz/workspace/myself/ai-standards/docs/decisions/2026-04-15-add-typescript-stack.ru.md:1). В тестах добавлено покрытие рендера нового stack в [tests/test_ai_sync.py](/home/shtirliz/workspace/myself/ai-standards/tests/test_ai_sync.py:87).

Проверка выполнена: `rtk uv run ruff check`, `rtk uv run mypy`, `rtk uv run python -m pytest -q`, `rtk uv run python scripts/ai_sync.py check --project-root /home/shtirliz/workspace/myself/ai-standards` прошли успешно. ConPort обновлён: записаны решение, progress entry и active context по добавлению `typescript` stack.

## Коммит и стандартное слияние ветки с поддержкой TypeScript

**Question**

(0tdizyy) Отлично. Думаю, пора сделать commit на ветке `feature/0tdizzp-tyescript_support`, после чего слить его стандартным образом.

**Answer**

Использую навыки `commit-on-branch` и затем `merge-by-standard`: сначала проверю текущую ветку и правила skill, подготовлю безопасный коммит в `feature/0tdizzp-tyescript_support`, после этого выполню стандартное слияние.

Сейчас вы на `main`, и по правилам прямой коммит туда делать нельзя. Переключусь на новую рабочую ветку `feature/0tdizzp-tyescript_support`, затем предложу точный текст commit message на утверждение перед коммитом.

Предлагаю commit message в требуемом формате:

`0tdizzp. (feat) add shared typescript stack fragment and decision record.`

Если подтверждаешь этот текст, я сразу выполню коммит и затем солью ветку стандартным образом.

## Подтверждение коммита и продолжение работы

**Question**

Отлично. Выполни commit пожалуйста, и продолжай.

**Answer**

Коммит выполняю с утверждённым текстом, затем переключусь на `main`, солью `feature/0tdizzp-tyescript_support` стандартным образом и удалю рабочую ветку после успешного merge.

Коммит создан на рабочей ветке. Проверяю итоговый хеш и выполняю merge в `main`; если fast-forward возможен, сделаю его и затем удалю feature-ветку.

Коммит выполнен на ветке `feature/0tdizzp-tyescript_support`, затем ветка стандартно слита fast-forward в `main` и удалена.

Итоговый коммит: `a402d15`  
Subject: `0tdizzp. (feat) add shared typescript stack fragment and decision record.`

Источник merge: `feature/0tdizzp-tyescript_support`  
Цель merge: `main`  
Feature-ветка удалена после слияния.

Рабочее дерево чистое. Текущее состояние `main`: локальная ветка `ahead 1, behind 2` относительно `origin/main`, то есть ваш коммит влит локально, но в удалённой ветке ещё есть два чужих коммита, которых нет локально.

## Синхронизация локального состояния с origin через pull

**Question**

Давай выполним pull, чтобы обеспечить синхронизацию локального состояния и origin.

**Answer**

Проверю расхождение `main` с `origin/main`, чтобы выбрать безопасную стратегию синхронизации. Если там просто линейное расхождение, сделаю `pull --rebase`, чтобы не добавлять лишний merge-коммит.

Расхождение линейное: локально один ваш коммит поверх `72688ee`, а на `origin/main` есть один новый чужой коммит `e9c06cc`. Сейчас сделаю `pull --rebase`, чтобы поставить ваш коммит поверх актуального `origin/main` без merge-коммита.

`pull` выполнен через rebase, синхронизация с `origin/main` прошла без конфликтов.

Текущее состояние:
- локальный `main` чистый
- `origin/main` подтянут
- ваш коммит переписан поверх нового удалённого коммита и теперь имеет хеш `a202754`

Сейчас ветка в состоянии `ahead 1`, то есть остаётся только выполнить `push`, если вы хотите синхронизировать и удалённый репозиторий.

## Верификация предложений по версионности и flow bump_version

**Question**

(0tdj06b) Теперь я хотел попросить тебя поддержать версионность проекта.

(0tdj0wg) Версию и дату релиза предлагается хранить в `pyproject.toml` в соответствующих полях `version` и `release_date`.

(0tdj1n3) Аналогичные поля, думаю, следует предусмотреть для "локальной" версии в `ai.project.toml`.

(0tdj0ym) При генерации AGENTS.md версия и дата релиза должны отражаться в этом файле из `pyproject.toml` и `ai.standards.toml`, отражая состояние на момент формирования AGENTS.md – думаю, это следует отразить в скрипте.

(0tdj1rj) Предлагается создать простое приложение `bump_version.py`, которое при запуске без параметров выводит предлагаемое изменение версии (изменяется вторая цифра "1.0" 🠊 "1.1") и дата релиза выставляется в текущую.

(.0tdj24y) Параметр `--version` позволяет явно задать версию, `--release_date` – дату релиза.

(.0tdj255) При запуске с ключом `-s`/`--save` обновляется `pyproject.toml` и создаётся тэг с именем `version-release_date` из `pyproject.toml`.
Имя созданного тэга следует выводить на консоль.
Указанные действия (изменения в `pyproject.tml` и создание тэга) следует выполнять только в случае, если рабочее дерево чистое, т.е. нет незакоммиченых изменений.

(0tdj28x) Полагаю, что требования по версионности следует отразить в правилах (или, лучше в навыках?) проекта `ai-standards`

(0tdj27z) Пожалуйста, верифицируй мои предложения по версионности.

**Answer**

Проверю текущую структуру `pyproject.toml`, `ai.project.toml`, рендер `AGENTS.md` и CLI в `scripts/ai_sync.py`, чтобы верифицировать предложения не абстрактно, а на совместимость с уже существующей архитектурой репозитория.

Уже видно важное расхождение терминов: сейчас `ai.project.toml.version` означает версию набора стандартов, а не локальную версию проекта. Это нужно аккуратно развести, иначе предложение в текущем виде ломает существующую семантику манифеста и рендера. Дочитаю рендер-хедер и шаблон манифеста, потом дам точную верификацию по пунктам с предложением корректной схемы.

В целом направление правильное, но в текущем виде есть два важных места, которые я бы скорректировал, чтобы не сломать существующую архитектуру и не войти в конфликт со спецификацией `pyproject.toml`.

**Итог верификации**

Поддерживаю:
- хранить версию релиза `ai-standards` централизованно
- хранить дату релиза рядом с ней
- добавить локальную версию для self-hosted `ai.project.toml`
- отражать обе версии в сгенерированном `AGENTS.md`
- сделать отдельный `bump_version.py`
- разрешать запись и создание тега только на чистом рабочем дереве

Считаю, что нужно изменить:
- `release_date` не стоит класть в `[project]` внутри `pyproject.toml`
- в `ai.project.toml` нельзя использовать поле `version` для локальной версии проекта, потому что сейчас оно уже означает версию набора стандартов, который рендерится в `AGENTS.md`

**Ключевая проблема 1: `release_date` в `[project]`**

По спецификации `pyproject.toml` таблица `[project]` содержит стандартизованные поля core metadata, а произвольная конфигурация инструментов должна жить в `[tool.*]`. Это прямо описано в спецификации PyPA: `[build-system]`, `[project]`, `[tool]`, а tool-specific данные размещаются в `[tool]`.  
Источник: https://packaging.python.org/en/latest/specifications/pyproject-toml/

Поэтому я бы предложил не так:

```toml
[project]
version = "0.1.0"
release_date = "2026-04-15"
```

а так:

```toml
[project]
name = "ai-standards"
version = "0.1.0"

[tool.ai-standards]
release_date = "2026-04-15"
```

Это технически чище и не конфликтует с PEP 621.  
Источник по `version` в `[project]`: https://packaging.python.org/en/latest/specifications/pyproject-toml/#version  
Источник по `[tool]`: https://packaging.python.org/en/latest/specifications/pyproject-toml/

**Ключевая проблема 2: `ai.project.toml.version` уже занято**

Сейчас в репозитории `ai.project.toml` использует:

```toml
version = "2026.03"
```

и это значение уже участвует в рендере заголовка `AGENTS.md`:

```python
f"<!-- Generated from ai-standards@{manifest.version}. Do not edit manually. -->"
```

То есть это не “локальная версия проекта”, а версия набора стандартов или manifest version.

Если просто переиспользовать `version` под локальную версию, получится семантическая путаница и слом текущей модели.

**Рекомендованная схема для `ai.project.toml`**

Я бы разделил понятия явно:

```toml
standards_version = "2026.03"
project_version = "0.1.0"
project_release_date = "2026-04-15"
```

Либо более компактно:

```toml
version = "2026.03"              # оставить как legacy/current semantics
local_version = "0.1.0"
local_release_date = "2026-04-15"
```

Но первый вариант лучше, потому что он самодокументируемый.

Если важна обратная совместимость, то можно сделать так:
- `version` временно продолжает означать `standards_version`
- скрипт начинает поддерживать новый `standards_version`
- `version` принимается как legacy alias
- README и шаблон переводятся на `standards_version`

**Как это должно отражаться в `AGENTS.md`**

Здесь идея правильная. Я бы выводил не одну строку, а 3-4 явных метаданных, чтобы было видно оба слоя версии:

```md
<!-- Generated by ai-standards package v0.1.0 -->
<!-- ai-standards release date: 2026-04-15 -->
<!-- Standards manifest version: 2026.03 -->
<!-- Project local version: 0.1.0 -->
<!-- Project local release date: 2026-04-15 -->
```

Это лучше текущей строки `Generated from ai-standards@2026.03`, потому что:
- разделяет версию Python-пакета/репозитория и версию подключённого стандарта
- показывает локальное self-hosted состояние проекта
- убирает неоднозначность

Если хочется сохранить старый маркер ради совместимости тестов и проверок, можно оставить его как одну из строк, но расширить заголовок.

**По `bump_version.py`**

Идея хорошая, но я бы уточнил несколько вещей.

Поддерживаю:
- запуск без параметров показывает proposed next version и дату
- `--version` задаёт версию явно
- `--release-date` задаёт дату явно
- `--save` пишет файл и создаёт тег
- всё mutating-only при clean worktree

Но я бы скорректировал детали.

1. Лучше использовать `--release-date` как основной CLI-аргумент.
   Внутреннее TOML-поле может остаться `release_date`, но CLI лучше делать в kebab-case.
   Можно поддержать и alias `--release_date`.

2. Нужно чётко определить схему bump.
   Сейчас в `pyproject.toml` версия `0.1.0`, а вы описали пример `1.0 -> 1.1`.
   Это две разные схемы.

   Я рекомендую придерживаться PEP 440-совместимого трёхсегментного формата:
   - `0.1.0 -> 0.2.0` для default minor bump
   - patch не трогать явно без отдельной опции
   - при желании позже добавить `--part major|minor|patch`

3. Перед созданием тега нужно проверять, что тег ещё не существует.

4. Тег лучше делать annotated, а не lightweight.
   Например:
   - имя: `0.2.0-2026-04-15`
   - сообщение: `Release 0.2.0 (2026-04-15)`

5. Скрипт не должен автоматически коммитить.
   Обновить файлы и создать тег на clean tree достаточно. Коммит и push лучше оставлять отдельным шагом.

6. При `--save` нужно проверять именно отсутствие любых незакоммиченных изменений:
   - staged
   - unstaged
   - untracked

**Какой минимальный контракт я бы утвердил для скрипта**

- Без аргументов:
  - читает `pyproject.toml`
  - читает `[tool.ai-standards].release_date`
  - печатает текущую версию, предложенную новую версию и дату релиза “today”
  - ничего не меняет

- С `--save`:
  - сначала проверяет clean worktree
  - обновляет `pyproject.toml`
  - создаёт annotated tag
  - печатает имя тега

- С `--version` и `--release-date`:
  - использует их вместо автоматически рассчитанных значений

**Нужно ли это отражать в rules или skills**

Я бы не выносил это в shared fragment `ai-standards` как общий стандарт прямо сейчас. Это пока выглядит как локальный release workflow самого репозитория `ai-standards`, а не как доказанно reusable cross-project policy.

Рекомендую так:

- В проектные правила `ai-standards` добавить короткое локальное правило.
  Например в `docs/ai/project-rules.md`:
  - release metadata for this repository lives in `pyproject.toml` and `[tool.ai-standards]`
  - use `scripts/bump_version.py` for release version updates
  - mutate release metadata only on a clean worktree

- Если вы ожидаете, что агент будет часто выполнять этот workflow, тогда имеет смысл отдельный skill, например `bump-release`.
  Но skill оправдан только если вы реально хотите повторяемый агентный сценарий с проверками, тегом и валидацией.

То есть:
- как policy: локальные project rules
- как automation: скрипт
- как agent workflow: skill, но опционально

**Моя рекомендуемая целевая модель**

`pyproject.toml`:
```toml
[project]
name = "ai-standards"
version = "0.1.0"

[tool.ai-standards]
release_date = "2026-04-15"
```

`ai.project.toml`:
```toml
standards_version = "2026.03"
project_version = "0.1.0"
project_release_date = "2026-04-15"
```

`AGENTS.md` header:
```md
<!-- Generated by ai-standards package v0.1.0 -->
<!-- ai-standards release date: 2026-04-15 -->
<!-- Standards manifest version: 2026.03 -->
<!-- Project local version: 0.1.0 -->
<!-- Project local release date: 2026-04-15 -->
```

**Вывод**

Ваши предложения в целом хорошие и реализуемые, но я бы утвердил их в такой скорректированной форме:

- `pyproject.toml`:
  - `project.version` оставить
  - `release_date` перенести в `[tool.ai-standards]`
- `ai.project.toml`:
  - не переиспользовать `version` под локальную версию
  - ввести отдельные поля `standards_version` и `project_version`, плюс дату
- `AGENTS.md`:
  - показывать обе версии и обе даты явно
- `bump_version.py`:
  - делать default minor bump в PEP 440-совместимой схеме
  - изменять файлы и создавать тег только на clean tree
  - не коммитить автоматически
- правила:
  - зафиксировать это как project-specific workflow в `ai-standards`
  - skill добавлять только если хотите часто запускать этот сценарий через агента

Источники:
- PyPA `pyproject.toml` specification: https://packaging.python.org/en/latest/specifications/pyproject-toml/
- `version` in `[project]`: https://packaging.python.org/en/latest/specifications/pyproject-toml/#version

Если хочешь, следующим шагом я могу уже перейти от верификации к конкретному change plan и сразу реализовать эту схему в репозитории.

## Уточнение требований к bump_version и локальной release политике ai-standards

**Question**

(0tdj3fd)
> а так:
> 
> [project]
> name = "ai-standards"
> version = "0.1.0"
> 
> [tool.ai-standards]
> release_date = "2026-04-15"

Да, принимается.

> Я бы разделил понятия явно:
> 
> standards_version = "2026.03"
> project_version = "0.1.0"
> project_release_date = "2026-04-15"

Этот вариант выглядит предпочтительнее: "явное лучше неявного" ⓒ.

> Но я бы скорректировал детали.
> 
> Лучше использовать --release-date как основной CLI-аргумент.
> Внутреннее TOML-поле может остаться release_date, но CLI лучше делать в kebab-case.

Да, так лучше.

> 0.1.0 -> 0.2.0 для default minor bump
> patch не трогать явно без отдельной опции
> при желании позже добавить --part major|minor|patch

Согласен. `--part` предлагаю поддержать прямо сейчас.

> Тег лучше делать annotated, а не lightweight.
> Например:
> 
> имя: 0.2.0-2026-04-15
> сообщение: Release 0.2.0 (2026-04-15)

Да, отличная мысль.

> Скрипт не должен автоматически коммитить.
> Обновить файлы и создать тег на clean tree достаточно. Коммит и push лучше оставлять отдельным шагом.

Отлично, что подсветил. В требованиях я это упустил.
Да, ты прав. Commit-ить ненужно.
Но тогда и тэг создавать прежддевременно.

(0tdj4ay)
Давай персмотрим требования к bump_version так.

(.0tdj4kj) Запуск без параметров – так, как договорились выше.

(.0tdj4kp) Команда `save` с параметрами `--release-date` и `--version`.

(.0tdj4lv) Команда `tag` – берёт версию и release_date из `pyproject.toml` и формирует тэг с аннотацией.
Но проверяет, что нен незакоммиченых изменений, и что текущая ветка `main`.

(.0tdj4oz) Commit же должен выполнять сам пользователь, возможно, через агента.

(0tdj4qw)
> Нужно ли это отражать в rules или skills
> Я бы не выносил это в shared fragment ai-standards как общий стандарт прямо сейчас. Это пока выглядит как локальный release workflow самого репозитория ai-standards, а не как доказанно reusable cross-project policy.

Нет-нет! Ты понял меня не правильно: речь шла об уникальных правилах проекта ai-standards, которые ни в коем случае не должны распространяться за его рамки.
Эти правила (или лучше skill для prompt-ов вида "Увеличь версию проекта до 1.2.0 и выполни commit.") определяют flow, который ведёт к релизу.

(0tdj4uf) Пожалуйста, верифицируй мои предложения с учётом тезисов, обозанченных выше.

**Answer**

С учётом уточнений схема стала существенно чище. В таком виде я её в целом поддерживаю.

**Что теперь выглядит корректно**

1. `pyproject.toml`
   Оставить `project.version` в `[project]` и хранить `release_date` в `[tool.ai-standards]` — это правильное решение.
   Оно не конфликтует со спецификацией `pyproject.toml` и отделяет packaging metadata от локальной tool-конфигурации.

   Рекомендованный вид:
   ```toml
   [project]
   name = "ai-standards"
   version = "0.1.0"

   [tool.ai-standards]
   release_date = "2026-04-15"
   ```

2. `ai.project.toml`
   Ввести:
   ```toml
   standards_version = "2026.03"
   project_version = "0.1.0"
   project_release_date = "2026-04-15"
   ```
   Это лучше, чем перегружать `version`, потому что сейчас в проекте это поле уже используется как версия набора стандартов для рендера `AGENTS.md`.

3. `bump_version.py`
   Разделение на команды `save` и `tag` — правильное.
   После твоего уточнения flow стал логичным:
   - `preview` по умолчанию, без изменений
   - `save` только обновляет файлы
   - `tag` только создаёт тег
   - commit остаётся отдельным пользовательским действием

   Это гораздо безопаснее, чем сцеплять обновление версии, commit и tag в один полуавтоматический шаг.

**Что я считаю хорошим и поддерживаю без оговорок**

- Без аргументов скрипт показывает текущую версию, предлагаемую новую версию и дату релиза “today”.
- Поддержка `--part major|minor|patch` прямо сейчас — хорошая идея.
- `--version` и `--release-date` должны переопределять автоматический расчёт.
- `save` не должен делать commit.
- `tag` должен брать версию и дату из `pyproject.toml`.
- Тег должен быть annotated.
- Перед `tag` нужно проверять:
  - чистое рабочее дерево
  - текущую ветку `main`
  - отсутствие уже существующего тега с тем же именем

**Где я бы добавил ещё одно уточнение**

Для `save` я бы рекомендовал тоже требовать чистое рабочее дерево.

Причина простая: изменение version metadata — это очень чувствительная операция, и если разрешить `save` на грязном дереве, получится неоднозначность:
- какие именно изменения относятся к bump
- можно ли потом безопасно commit-ить только версию
- не окажется ли release metadata смешана с несвязанной работой

То есть я бы предложил такой контракт:

- `bump_version.py`
  - без команды: только preview, можно запускать всегда
- `bump_version.py save ...`
  - требует clean worktree
  - обновляет `pyproject.toml`
  - при необходимости обновляет `ai.project.toml`
  - ничего не коммитит
  - тег не создаёт
- `bump_version.py tag`
  - требует clean worktree
  - требует branch `main`
  - читает версию и дату из `pyproject.toml`
  - создаёт annotated tag
  - печатает имя тега

Это даст очень предсказуемый release flow.

**По поводу branch `main` для `tag`**

Поддерживаю. Для этого репозитория это выглядит разумным локальным правилом проекта.

Но я бы рекомендовал зафиксировать это именно как repository-specific release rule, а не как абстрактное инженерное правило. То есть:
- в коде `bump_version.py` это можно жёстко проверять
- в docs/project rules это нужно явно описать
- в shared fragments это выносить не надо

**Как это должно отражаться в `AGENTS.md`**

Да, рендер это должен учитывать. И тут я бы рекомендовал не смешивать всё в одну строку.

Лучше так:

```md
<!-- Generated by ai-standards package v0.2.0 -->
<!-- ai-standards release date: 2026-04-15 -->
<!-- Standards manifest version: 2026.03 -->
<!-- Project local version: 0.2.0 -->
<!-- Project local release date: 2026-04-15 -->
```

Здесь важно:
- `package version` берётся из `pyproject.toml`
- `ai-standards release date` берётся из `[tool.ai-standards].release_date`
- `standards version` берётся из `ai.project.toml.standards_version`
- `project local version` и `project local release date` — из `ai.project.toml`

Это соответствует твоей цели: `AGENTS.md` должен отражать состояние на момент генерации.

**По поводу правил проекта или skill**

После твоего уточнения полностью согласен: это именно локальная release-политика репозитория `ai-standards`.

Я бы рекомендовал оба слоя:

1. Локальные project rules
   В `docs/ai/project-rules.md` зафиксировать:
   - version metadata lives in `pyproject.toml` and `ai.project.toml`
   - use `scripts/bump_version.py` for release preparation
   - `save` and `tag` require a clean working tree
   - `tag` is allowed only from `main`

2. Skill
   Это уже действительно полезно, если ты хочешь поддержать команды вроде:
   - “Увеличь версию проекта до 1.2.0 и подготовь изменения”
   - “Сохрани новый release metadata и оформи commit”
   - “Создай релизный тег”

   Такой skill должен:
   - сначала запускать preview
   - потом `save`
   - commit делать только после явного утверждения пользователя
   - `tag` делать отдельным шагом, когда рабочее дерево чистое и ветка `main`

То есть:
- policy живёт в project rules
- automation живёт в script
- agent workflow живёт в skill

Это хорошее разделение ответственности.

**Финальная верификация по пунктам**

Поддерживаю:
- `[tool.ai-standards].release_date` в `pyproject.toml`
- `standards_version`, `project_version`, `project_release_date` в `ai.project.toml`
- default preview mode
- `save` как отдельную команду
- `tag` как отдельную команду
- `--part major|minor|patch`
- `--release-date` в kebab-case
- annotated tags
- commit как отдельное действие пользователя/агента
- локальные project rules и, опционально, отдельный skill

Рекомендую дополнительно:
- требовать clean worktree не только для `tag`, но и для `save`
- проверять существование тега перед созданием
- явно описать source of truth для каждого поля версии
- оставить обратную совместимость в `ai_sync.py`, если будет переходный этап от `version` к `standards_version`

Если идти дальше, я бы уже не делал ещё один раунд абстрактной верификации. Следующий разумный шаг — это change plan и реализация:
- обновить схему TOML
- доработать `ai_sync.py`
- добавить `scripts/bump_version.py`
- покрыть тестами
- обновить project rules
- при желании добавить skill под release flow.

## Проверка release правил main и структуры версий перед изменениями

**Question**

(0tdj7yt)
> Причина простая: изменение version metadata — это очень чувствительная операция, и если разрешить save на грязном дереве, получится неоднозначность:

Ok, принимается.

> По поводу branch main для tag
> ... ... ...
> Но я бы рекомендовал зафиксировать это именно как repository-specific release rule, а не как абстрактное инженерное правило. То есть:
> 
> в коде bump_version.py это можно жёстко проверять
> в docs/project rules это нужно явно описать
> в shared fragments это выносить не надо

Согласен. Давай так и сделаем.

> <!-- Generated by ai-standards package v0.2.0 release date: 2026-04-15 -->

Лучше в одну строку.

> <!-- Standards manifest version: 2026.03 -->

Есть ли рациональные основания разделять версию пакета и веросию содержащихся в нём правил?
Основное назначение пакета как раз в правилах. Всё остальное - элемента инфраструктуры, изменения в которых тянут, максимум, на patch-уровень.

> По поводу правил проекта или skill
> После твоего уточнения полностью согласен: это именно локальная release-политика репозитория ai-standards.
> Я бы рекомендовал оба слоя:

Полностью поддерживаю. И локальные project rules, и Skill для проекта нужно сделать.

(0tdjc61) Пожалуйста, верифицируй тезисы выше, ответь на вопросы и, думаю, можно вносить изменения.

**Answer**

Подтверждаю предложенные уточнения. В таком виде схема стала достаточно непротиворечивой, и после ответа на вопрос про версии уже можно переходить к реализации.

По `save` только на чистом дереве: да, это правильное ужесточение. Оно делает release metadata атомарным изменением, а не побочным эффектом среди прочих правок.

По `tag` только с `main`: тоже поддерживаю. Это хорошее локальное правило именно для `ai-standards`, и его действительно лучше зафиксировать в трёх местах:
- в `scripts/bump_version.py` как жёсткую проверку
- в `docs/ai/project-rules.md` как project-specific policy
- в отдельном skill как agent workflow

По заголовку `AGENTS.md`: объединить версию пакета и дату релиза в одну строку разумно. Я бы делал так:

```md
<!-- Generated by ai-standards package v0.2.0 release date: 2026-04-15 -->
```

Это компактно и читаемо.

Теперь к главному вопросу: нужно ли разделять версию пакета и версию правил.

Мой ответ: в вашем случае, скорее всего, нет. Рациональные основания для разделения существуют, но для `ai-standards` они не выглядят обязательными.

Когда разделение имеет смысл:
- если package можно выпускать из-за инфраструктурных изменений без изменения самих стандартов
- если набор правил живёт своей независимой cadence, а CLI и шаблоны своей
- если downstream-проектам важно зафиксировать именно semantic version набора правил отдельно от версии инструмента

Но у вас сейчас модель другая:
- основной смысл репозитория действительно в правилах
- CLI, рендер, шаблоны и тесты обслуживают эти правила
- инфраструктурные изменения, не влияющие на содержание правил, действительно тянут максимум на patch
- лишняя ось версионирования добавит когнитивную нагрузку и усложнит `ai.project.toml`, `README`, рендер и release flow

Поэтому я бы рекомендовал не разделять package version и standards version.

То есть вместо:
- `project.version` для пакета
- `ai.project.toml.standards_version` для правил

лучше использовать одну общую версию релиза `ai-standards` как продукта.

Тогда схема упрощается.

`pyproject.toml`:
```toml
[project]
name = "ai-standards"
version = "0.2.0"

[tool.ai-standards]
release_date = "2026-04-15"
```

`ai.project.toml`:
```toml
ai_standards_version = "0.2.0"
project_version = "0.2.0"
project_release_date = "2026-04-15"
```

Но поскольку сам `ai.project.toml` относится к self-hosted репозиторию `ai-standards`, здесь можно упростить ещё сильнее и не дублировать одну и ту же версию дважды без необходимости.

Практически я бы предложил такой вариант:

`ai.project.toml`:
```toml
ai_standards_version = "0.2.0"
project_release_date = "2026-04-15"
```

или, если локальная версия self-hosted проекта всё же должна явно храниться отдельно:

```toml
ai_standards_version = "0.2.0"
project_version = "0.2.0"
project_release_date = "2026-04-15"
```

Но если это один и тот же self-hosted репозиторий, `project_version` и `ai_standards_version` почти наверняка будут всегда совпадать. Поэтому я бы не плодил дубли без острой причины.

Моя рекомендация здесь такая:
- для общего случая downstream-проектов версия стандартов нужна
- для самого `ai-standards` как self-hosted репозитория локальная project version может быть равна версии `ai-standards`
- если вы не планируете независимое расхождение, не стоит поддерживать две разные версии как обязательные

Соответственно заголовок `AGENTS.md` я бы делал так:

```md
<!-- Generated by ai-standards package v0.2.0 release date: 2026-04-15 -->
<!-- Project manifest version: 0.2.0 -->
<!-- Project local release date: 2026-04-15 -->
```

Или ещё проще, если для self-hosted случая хотите минимализм:

```md
<!-- Generated by ai-standards v0.2.0 release date: 2026-04-15 -->
<!-- Project version: 0.2.0 release date: 2026-04-15 -->
```

То есть:
- одну строку для релиза `ai-standards`
- одну строку для локального project state
- без отдельной “версии правил” как третьей оси

Итоговая верификация:

Поддерживаю:
- `release_date` в `[tool.ai-standards]`
- `save` только на clean worktree
- `tag` только на clean worktree и только на `main`
- `tag` как отдельную команду
- одну строку для version + release date в заголовке
- project rules + отдельный skill для release flow

На вопрос о разделении версии пакета и версии правил:
- теоретически это возможно
- практически для `ai-standards` сейчас не выглядит оправданным
- рекомендую держать одну release version `ai-standards`, а не две независимые версии

Можно переходить к изменениям. Я бы реализовывал в таком порядке:
1. обновить схему `pyproject.toml` и `ai.project.toml`
2. доработать `scripts/ai_sync.py` и рендер заголовка
3. добавить `scripts/bump_version.py`
4. обновить `docs/ai/project-rules.md`
5. добавить skill под release flow
6. покрыть всё тестами

Если хочешь, я сразу начну реализацию по этой упрощённой схеме без разделения package version и standards version.

## Внесение изменений по версионности в ветке feature 0tdj06b package_versioning

**Question**

(0tdjca5) Да, полностью одобряю твои предложения и план.
Внеси пожалуйста изменения в проект на ветке `feature/0tdj06b-package_versioning`.

**Answer**

Перехожу на ветку `feature/0tdj06b-package_versioning`, затем соберу точный объём правок: схема `pyproject.toml` и `ai.project.toml`, рендер `AGENTS.md`, новый `bump_version.py`, локальные project rules и отдельный skill под release flow.

План такой:
1. Перевести конфиги на новую схему версий: `pyproject.toml` + `[tool.ai-standards].release_date`, а в `ai.project.toml` и шаблоне манифеста — явные поля `ai_standards_version`, `project_version`, `project_release_date`.
2. Доработать `scripts/ai_sync.py`, чтобы заголовок `AGENTS.md` включал релизные метаданные в согласованном формате и поддерживал новую схему манифеста.
3. Добавить `scripts/bump_version.py` с командами preview/save/tag и полными проверками git-состояния.
4. Обновить README, локальные project rules и добавить project-local skill под release flow, затем прогнать проверки и синхронизировать ConPort.

Схема прояснилась: делаю новую явную модель полей с обратной совместимостью для старого `version` в манифесте, чтобы не ломать текущих потребителей, а release flow оформляю как локальную политику `ai-standards` плюс отдельный project-local skill. Следом вношу конфиги и код.

Дорабатываю кодовую основу: сначала переведу `ai_sync.py` на новую схему метаданных и совместимость со старым `version`, потом добавлю `bump_version.py`, чтобы не расползалась семантика по нескольким файлам.

У тестов много однотипных манифестов, поэтому делаю не ручную россыпь мелких правок, а один bulk-rewrite по новой схеме полей, а затем поверх него добью точечные изменения в ассертах и новые кейсы.

Нашёл архитектурный узел: `bump_version.py` должен уметь тестироваться на временном репозитории, а `ai_sync.py` сейчас жёстко привязан к текущему repo root. Ослабляю эту связку через явный `repo_root` override, чтобы и release script, и тесты оставались честными.

Перехожу к репозиторным артефактам: обновляю README и project rules под новый release flow, затем добавляю decision record и локальный skill, чтобы политика, automation и agent workflow были согласованы между собой.

Код готов по смыслу, сейчас привожу его к repo-style: убираю лишнее, сокращаю длинные строки и готовлю к прогону `ruff`/`mypy`/`pytest` до генерации обновлённого `AGENTS.md`.

Перехожу к верификации. Сначала прогоняю `ruff` и `mypy`, чтобы быстро поймать синтаксис и типы, потом `pytest`, и в конце пересоберу root `AGENTS.md` уже на новой схеме метаданных.

Mypy ругается не на логику, а на stubs Typer. Упрощаю CLI-обвязку без потери поведения: без аргументов скрипт сам показывает preview, а `save` и `tag` остаются обычными Typer-командами.

Код и тесты зелёные. Теперь пересобираю root `AGENTS.md` по новой схеме и прогоняю `ai_sync check`, чтобы зафиксировать уже не только код, но и self-hosted результат рендера.

Все изменения на месте, включая self-hosted `AGENTS.md`. Осталось синхронизировать ConPort: зафиксирую решение по release-versioning workflow, прогресс по внедрению и активный контекст с новым `bump_version.py`, локальными правилами и skill.

В проект внесена новая схема versioning и локальный release flow для `ai-standards`.

Основные изменения:
- В [pyproject.toml](/home/shtirliz/workspace/myself/ai-standards/pyproject.toml:1) `project.version` оставлен source of truth для версии пакета, а дата релиза перенесена в `[tool.ai-standards].release_date`.
- В [ai.project.toml](/home/shtirliz/workspace/myself/ai-standards/ai.project.toml:1) и [templates/project_manifest.toml](/home/shtirliz/workspace/myself/ai-standards/templates/project_manifest.toml:1) введены явные поля `ai_standards_version`, `project_version`, `project_release_date`; в `ai_sync.py` оставлена обратная совместимость со старым `version` как fallback.
- В [scripts/ai_sync.py](/home/shtirliz/workspace/myself/ai-standards/scripts/ai_sync.py:1) обновлён заголовок `AGENTS.md`: теперь он отражает release metadata из `pyproject.toml` и project-local metadata из манифеста. Root [AGENTS.md](/home/shtirliz/workspace/myself/ai-standards/AGENTS.md:1) пересобран.
- Добавлен [scripts/bump_version.py](/home/shtirliz/workspace/myself/ai-standards/scripts/bump_version.py:1) с flow:
  - без аргументов показывает preview
  - `save` обновляет release metadata только на чистом worktree
  - `tag` создаёт annotated tag только на чистом worktree и только из `main`
- Обновлены [README.md](/home/shtirliz/workspace/myself/ai-standards/README.md:40), [README.ru.md](/home/shtirliz/workspace/myself/ai-standards/README.ru.md:40), [docs/ai/project-rules.md](/home/shtirliz/workspace/myself/ai-standards/docs/ai/project-rules.md:1), [docs/ai/project-rules.ru.md](/home/shtirliz/workspace/myself/ai-standards/docs/ai/project-rules.ru.md:1).
- Добавлен decision record [docs/decisions/2026-04-15-add-release-versioning-workflow.md](/home/shtirliz/workspace/myself/ai-standards/docs/decisions/2026-04-15-add-release-versioning-workflow.md:1) и русская пара, а также project-local skill [release-versioning](/home/shtirliz/workspace/myself/ai-standards/.codex/skills/release-versioning/SKILL.md:1).

Покрытие и проверка:
- [tests/test_ai_sync.py](/home/shtirliz/workspace/myself/ai-standards/tests/test_ai_sync.py:1) обновлён под новую схему и legacy-совместимость.
- Добавлен [tests/test_bump_version.py](/home/shtirliz/workspace/myself/ai-standards/tests/test_bump_version.py:1) для `save`/`tag` flow.
- Прогнано успешно: `rtk uv run ruff check`, `rtk uv run mypy`, `rtk uv run python -m pytest -q`, `rtk uv run python scripts/ai_sync.py render --project-root /home/shtirliz/workspace/myself/ai-standards`, `rtk uv run python scripts/ai_sync.py check --project-root /home/shtirliz/workspace/myself/ai-standards`.

ConPort тоже обновлён: записаны решение, прогресс и активный контекст по release-versioning workflow. Если хочешь, следующим шагом могу оформить commit на ветке `feature/0tdj06b-package_versioning`.

## Коммит ветки и обсуждение release skill для ai-standards

**Question**

(0tdjzwv)
> следующим шагом могу оформить commit на ветке feature/0tdj06b-package_versioning.

Да, выполни commit, но хотел уточнить у тебя, как насчёт skill, который мы обсуждали выше:
> Skill
> Это уже действительно полезно, если ты хочешь поддержать команды вроде:
> 
> “Увеличь версию проекта до 1.2.0 и подготовь изменения”
> “Сохрани новый release metadata и оформи commit”
> “Создай релизный тег”
> Такой skill должен:
> 
> сначала запускать preview
> потом save
> commit делать только после явного утверждения пользователя
> tag делать отдельным шагом, когда рабочее дерево чистое и ветка main

**Answer**

Проверю текущее состояние ветки и покажу точный статус skill, который уже добавлен. Затем предложу commit message на утверждение, потому что по правилам репозитория коммит можно делать только после явного подтверждения текста сообщения.

Да, этот skill уже добавлен, и по сути он соответствует обсуждённому workflow.

Сейчас в [.codex/skills/release-versioning/SKILL.md](/home/shtirliz/workspace/myself/ai-standards/.codex/skills/release-versioning/SKILL.md:1) зафиксировано именно это:
- сначала preview через `scripts/bump_version.py`
- затем `save` с проверкой чистого worktree
- commit только после явного утверждения пользователем
- `tag` отдельным шагом
- `tag` только из `main` и только на чистом worktree

То есть это не просто “подсказка про versioning”, а уже локальный skill для `ai-standards`, который ведёт агента по нужному release flow. Если захочешь, позже его можно ещё усилить примерами типовых пользовательских запросов, но функционально база уже есть.

Для текущих изменений предлагаю commit message:

`0tdj06b. (feat) add repository-local release versioning workflow.`

Если подтверждаешь этот текст, я сразу выполню commit на `feature/0tdj06b-package_versioning`.

## Подтверждённый коммит и стандартное слияние ветки

**Question**

Да, отлично! 🙂
Сообщение commit-а подтверждаю, выполни commit и слей ветку стандартным образом.

**Answer**

Выполняю commit с утверждённым сообщением, затем солью `feature/0tdj06b-package_versioning` в `main` стандартным образом и удалю рабочую ветку после успешного merge.

Коммит создан на feature-ветке. Проверяю итоговый хеш и затем выполняю стандартный merge в `main`; если fast-forward доступен, использую его и после этого удалю source branch.

Коммит выполнен и ветка слита стандартным образом.

Итог:
- commit: `f6171e0`
- subject: `0tdj06b. (feat) add repository-local release versioning workflow.`

Merge:
- source: `feature/0tdj06b-package_versioning`
- target: `main`
- стратегия: fast-forward
- feature-ветка удалена после слияния

Текущее состояние:
- рабочее дерево чистое
- текущая ветка: `main`
- локальный `main` в состоянии `ahead 1` относительно `origin/main`

По skill: он уже добавлен и влит в `main` в виде [release-versioning](/home/shtirliz/workspace/myself/ai-standards/.codex/skills/release-versioning/SKILL.md:1). Он покрывает именно тот flow, который мы обсуждали: preview → save → commit по явному одобрению → tag отдельным шагом.
