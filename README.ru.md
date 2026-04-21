# AI Standards

## Оглавление

- [Структура](#структура)
- [Быстрый старт](#быстрый-старт)
- [Конфигурация только через манифест](#конфигурация-только-через-манифест)
- [Правила, специфичные для проекта](#правила-специфичные-для-проекта)
- [Agent Adapters](#agent-adapters)
- [Заимствование внешних правил](#заимствование-внешних-правил)
- [Использование Reasoning Hygiene в проекте](#использование-reasoning-hygiene-в-проекте)
- [Использование Autonomy Boundaries в проекте](#использование-autonomy-boundaries-в-проекте)
- [Использование Review Lenses в проекте](#использование-review-lenses-в-проекте)
- [Использование Structured Artifacts в проекте](#использование-structured-artifacts-в-проекте)
- [Порядок работы с проектом](#порядок-работы-с-проектом)
- [Версионирование](#версионирование)
- [Текущие фрагменты стеков](#текущие-фрагменты-стеков)

Централизованная инфраструктура инструкций для ИИ-агентов, генерирующая проектные `AGENTS.md`.

Англоязычный оригинал находится в [README.md](README.md). При изменениях в английской версии эту локализацию нужно обновлять в том же наборе изменений.

## Структура

- `fragments/`: переиспользуемые фрагменты инструкций, сгруппированные по доменам.
- `templates/`: стартовые файлы, которые копируются в подключаемые проекты.
- `ai-sync`: консольный инструмент, который собирает и проверяет `AGENTS.md`.
- `registry.toml`: сопоставляет имена возможностей и стеков с путями к фрагментам.

## Быстрый старт

```bash
uv run ai-sync init-project --project-root /path/to/project
uv run ai-sync render --project-root /path/to/project
uv run ai-sync check --project-root /path/to/project
uv run ai-sync sync-templates --project-root /path/to/project
```

## Конфигурация только через манифест

`ai-standards` не использует именованные профили. Каждый подключаемый проект явно объявляет свои зависимости инструкций в `ai.project.toml`.

Используются четыре слоя:

- `fragments`: прямые базовые правила, которые должны включаться всегда.
- `features`: опциональные возможности вроде `conport`, `design-first-collaboration`, `reasoning-hygiene`, `autonomy-boundaries`, `review-lenses` и `structured-artifacts`.
- `stacks`: правила, зависящие от технологии или архитектурного стиля, например `layered-architecture`, `backend-layered-architecture`, `frontend-layered-architecture`, `typescript`, `python`, `fastapi`, `sqlalchemy`, `django`, `postgres`, `react`, `nextjs`, `tanstack-query`, `vue`, `nuxt`, `vue-query`, `vite`, `fsd`, `java`, `spring` или `spring-data-jpa`.
- `tooling.agents`: опциональные agent adapters вроде `codex` и `cursor` для управляемых локальных workflow templates.

Рекомендуемая стартовая точка для Python/FastAPI проекта со стандартными требованиями к коммуникации, планированию и архитектуре:

```toml
ai_standards_version = "0.1.0"
project_version = "replace-me"
project_release_date = "YYYY-MM-DD"

fragments = [
  "core/base",
  "core/git-workflow",
  "core/architecture",
  "core/error-handling",
]

features = [
  "conport",
  "design-first-collaboration",
  "reasoning-hygiene",
  "autonomy-boundaries",
  "structured-artifacts",
]

stacks = [
  "python",
  "fastapi",
  "postgres",
]

local_overrides = [
  "docs/ai/project-rules.md",
]

optional_local_overrides = [
  "docs/ai/private-rules.local.md",
]

[tooling]
agents = ["codex", "cursor"]
```

Выбирайте зависимости явно. Если правило нужно только одному проекту, держите его в локальном дополнении, а не превращайте в общий фрагмент.

Примеры композиции стеков:

```toml
# React + TypeScript frontend
stacks = [
  "typescript",
  "react",
]
```

```toml
# React + TanStack Query
stacks = [
  "typescript",
  "react",
  "tanstack-query",
]
```

```toml
# Next.js App Router frontend
stacks = [
  "typescript",
  "react",
  "nextjs",
]
```

```toml
# Vue + TypeScript frontend
stacks = [
  "typescript",
  "vue",
]
```

```toml
# Vue + Vue Query
stacks = [
  "typescript",
  "vue-query",
]
```

```toml
# Nuxt frontend
stacks = [
  "typescript",
  "vue",
  "nuxt",
]
```

```toml
# Vite + React + FSD frontend
stacks = [
  "typescript",
  "react",
  "frontend-layered-architecture",
  "vite",
  "fsd",
]
```

```toml
# FastAPI + SQLAlchemy + PostgreSQL
stacks = [
  "backend-layered-architecture",
  "python",
  "fastapi",
  "sqlalchemy",
  "postgres",
]
```

```toml
# Django API проект
stacks = [
  "python",
  "django",
  "django-service-layer",
  "django-drf",
  "django-save-orchestration",
  "postgres",
]
```

```toml
# Django server-rendered проект
stacks = [
  "python",
  "django",
  "django-service-layer",
  "django-save-orchestration",
  "postgres",
]
```

```toml
# Spring Boot сервис с JPA
stacks = [
  "java",
  "spring",
  "spring-data-jpa",
  "postgres",
]
```

Архитектурное примечание:

- Используйте `sqlalchemy` вместе с сервисным слоем и repository-style доступом к данным. Это напрямую соответствует общим правилам `core/architecture` и является типовым выбором для FastAPI и похожих Python-сервисов.
- Используйте `layered-architecture`, когда проекту нужны явные межмодульные dependency boundaries без привязки guidance к одному языку или фреймворку.
- Используйте `backend-layered-architecture` для backend-сервисов, которым нужны thin transport boundaries, явная application orchestration, осознанные transaction boundaries и adapter-style integration edges.
- Используйте `frontend-layered-architecture` для фронтендов, которым нужны явные границы между UI, workflow-логикой и infrastructure beyond ad hoc component-level structure.
- Используйте `django`, когда проект следует идиомам Django и сам ORM выступает persistence abstraction. В этом стеке сервисы и selectors работают с моделями через Django ORM без отдельного repository-слоя.
- Используйте `django-service-layer` как HackSoft-derived opt-in Django application style. Этот stack композирует общие layered-architecture fragments с Django-specific conventions для services, selectors и boundary placement.
- Используйте `nextjs` вместе с `react` и обычно с `typescript` для full-stack React-приложений на базе App Router.
- Используйте `tanstack-query` вместе с `react` или другими поддерживаемыми UI-стеками, когда приложению нужен явный server-state layer вместо ad hoc fetch-in-component patterns.
- Используйте `nuxt` вместе с `vue` и обычно с `typescript` для full-stack Vue-приложений на базе Nuxt.
- Используйте `vue-query` как compatibility name для Vue-проектов, которым нужен общий TanStack Query guidance вместе с Vue baseline в одной записи стека.
- Используйте `vite` только тогда, когда проект сам управляет конфигурацией сборки и dev-server через Vite, а не полностью наследует её от другого фреймворка.
- Используйте `fsd` только тогда, когда фронтенд уже достаточно крупный, чтобы выигрывать от явных layer- и slice-границ; это opt-in архитектурный стек.
- Используйте `java`, `spring` и `spring-data-jpa` вместе как современный baseline для Spring-сервиса. Старое имя стека `java-spring` сохраняется как compatibility alias для downstream manifests.

`tooling.agents` не меняет содержимое сгенерированного `AGENTS.md`. Этот раздел объявляет, какие tool-specific companion templates нужно держать синхронизированными внутри подключаемого проекта.

## Правила, специфичные для проекта

Правила, которые должны действовать только внутри одного проекта, следует хранить в репозитории самого проекта.

Рекомендуемая структура подключаемого проекта:

```text
project/
  ai.project.toml
  AGENTS.md
  .codex/skills/review-lenses/simplify-review/SKILL.md
  .cursor/rules/simplify-review.mdc
  docs/ai/project-rules.md
  docs/ai/private-rules.local.md
```

Используйте манифест, чтобы собирать и общие, и проектные правила:

```toml
local_overrides = [
  "docs/ai/project-rules.md",
]

optional_local_overrides = [
  "docs/ai/private-rules.local.md",
]
```

Рекомендации:

- Командные и специфичные для репозитория правила кладите в `docs/ai/project-rules.md`.
- `docs/ai/private-rules.local.md` создавайте только на тех машинах, где он нужен.
- Не переносите правила одного проекта в `~/workspace/ai-standards`.
- Переиспользуемые правила для стеков, процессов и инструментов держите в этом репозитории.
- Добавьте `docs/ai/private-rules.local.md` в `.gitignore` подключаемого проекта.

`optional_local_overrides` пропускаются, если файл отсутствует, поэтому локальные приватные правила не блокируют сборку.

## Agent Adapters

`AGENTS.md` остаётся общим project-wide источником истины для основных инструкций.

Некоторым инструментам также нужны локальные adapters для навыков или правил. Объявляйте их в `ai.project.toml`:

```toml
[tooling]
agents = ["codex", "cursor"]
```

Поддерживаемые adapters:

- `codex`: раскладывает управляемые skill templates под `.codex/skills/`
- `cursor`: раскладывает управляемые rule templates под `.cursor/rules/`

Команды:

- `init-project` копирует стартовый manifest, локальные шаблоны overrides и все managed agent adapters, уже объявленные в `ai.project.toml`.
- `sync-templates` обновляет managed agent adapters, объявленные в `ai.project.toml`.
- `render` по-прежнему генерирует только `AGENTS.md`.

Управляемые adapter files содержат marker от `ai-standards`. `sync-templates` обновляет только те файлы, которыми управляет напрямую, или простые копии upstream template, и пропускает локально изменённые unmanaged files.

## Заимствование внешних правил

Не копируйте внешние наборы правил напрямую в `ai-standards`. Нормализуйте и заимствуйте только переиспользуемые части.

Рекомендуемый import flow:

1. Прочитать внешний источник и кратко описать его структуру.
2. Извлечь кандидаты на правила.
3. Классифицировать каждое правило как `keep`, `adapt` или `reject`.
4. Отвергнуть расплывчатые, проектные, избыточные или конфликтующие правила.
5. Нормализовать принятые правила в короткие повелительные инструкции.
6. Поместить их в подходящий фрагмент под `fragments/`.
7. Обновить `registry.toml`, если появился новый стек или новая возможность.
8. Зафиксировать происхождение рядом с принятым фрагментом.
9. Запустить `uv run ruff check`, `uv run mypy` и `uv run pytest`.

### Стандартный запрос для импорта

Скопируйте этот запрос, когда хотите поручить агенту заимствование правил из внешнего источника в `ai-standards`:

```text
You are updating ~/workspace/ai-standards.

Task:
Adopt reusable rules from the external source below into ai-standards without copying blindly.

Source:
<URL>

Target:
- Add or update the most appropriate fragment under fragments/
- Update registry.toml if a new stack/feature must be registered
- Preserve UMA2 core constraints, design-first-collaboration, reasoning-hygiene, and structured-artifacts
- Do not import project-specific, vague, redundant, or conflicting rules

Required workflow:
1. Read the source and summarize its structure.
2. Extract candidate rules.
3. Classify each candidate as:
   - keep as reusable
   - adapt
   - reject
4. For every rejected item, state why it was rejected.
5. Normalize accepted rules into concise, imperative instructions matching ai-standards style.
6. Avoid duplicates with existing fragments.
7. Add provenance notes in the fragment header or adjacent documentation:
   - source URL
   - adoption date
   - adaptation notes
8. If the source suggests a new stack, create a new stack fragment and register it.
9. Run project checks after changes.
10. In the final report, show:
   - files changed
   - adopted rules
   - rejected rules
   - conflicts or ambiguities needing human review

Constraints:
- Prefer paraphrase and normalization over direct copying.
- Keep only rules that are durable and broadly reusable.
- Preserve existing behavior unless the imported rules justify a clear improvement.
- If a source rule conflicts with UMA2 architecture or error-handling rules, reject it unless explicitly approved.
```

## Использование Reasoning Hygiene в проекте

`reasoning-hygiene` — это опциональная возможность для повышения качества анализа на сложных или неоднозначных задачах без опоры на model-specific prompt tricks.

Используйте `reasoning-hygiene`, когда проекту полезны переиспользуемые правила для:

- явного пошагового разложения нетривиальных задач
- выведения наружу assumptions, edge cases и verification points
- self-review в виде пробелов, рисков и недостающих подтверждений
- task-specific ролей, которые добавляют реальные ограничения вместо generic persona fluff

`ai-standards` должен хранить устойчивую policy:

- какие практики рассуждения вообще стоит стандартизировать
- какие prompt-паттерны слишком хрупкие или model-specific для нормализации
- как эта возможность дополняет `design-first-collaboration`, `conport` и `structured-artifacts`

Подробная методика применения находится в:

- английском руководстве: [docs/reasoning-hygiene-usage.md](docs/reasoning-hygiene-usage.md)
- русском руководстве: [docs/reasoning-hygiene-usage.ru.md](docs/reasoning-hygiene-usage.ru.md)

Эмоциональное давление, стимулы, challenge-prompts и прочий prompt-folklore не следует переносить в этот общий feature, если только он не станет устойчивой cross-model policy с ясной доказательной базой.

## Использование Autonomy Boundaries в проекте

`autonomy-boundaries` — это опциональная возможность, которая определяет, когда агент может продолжать автономно, а когда обязан остановиться и запросить верификацию человеком.

Используйте `autonomy-boundaries`, когда проекту полезны переиспользуемые правила для:

- длинных автономных прогонов, которым всё равно нужны явные design- и scope-guardrails
- обязательных stop conditions вокруг design ambiguity, architecture drift и роста blast radius
- явного различения direction checkpoints и architecture-delta checkpoints
- привязки длинного execution к письменным артефактам и компактным review outputs

`ai-standards` должен хранить переиспользуемую policy:

- длинная автономная работа — это исключение, а не default workflow
- агент может исполнять согласованный design, но не должен тихо выбирать новый
- stop conditions так же важны, как и completion criteria
- shared defaults не должны продвигать хрупкие числовые пороги, оставляя более строгие лимиты project-local rules

Подробная методика применения находится в:

- английском руководстве: [docs/autonomy-boundaries-usage.md](docs/autonomy-boundaries-usage.md)
- русском руководстве: [docs/autonomy-boundaries-usage.ru.md](docs/autonomy-boundaries-usage.ru.md)

## Использование Review Lenses в проекте

`review-lenses` — это опциональная возможность для более жёсткого просмотра и упрощения недавних изменений.

Подробная методика применения, включая режимы `review-only` и `fix`, способы активации, рекомендации для CI и этапы внедрения, находится в [docs/review-lenses-usage.ru.md](docs/review-lenses-usage.ru.md). Англоязычный оригинал: [docs/review-lenses-usage.md](docs/review-lenses-usage.md).

`ai-standards` должен хранить:

- когда уместен проход упрощения по нескольким ракурсам
- переиспользуемую модель ракурсов: `Reuse`, `Quality` и `Efficiency`
- приоритеты при конфликте между этими ракурсами
- требования к проверке после агрессивной очистки

Что не стоит переносить в shared fragments без нормализации:

- внутренние детали конкретных вендоров
- недокументированные утверждения о закрытых инструментах
- эвристики, привязанные к конкретному фреймворку, которым место в стековых фрагментах
- хрупкие числовые пороги, не подтверждённые на нескольких проектах

Стартовые шаблоны для подключаемых проектов:

- [templates/review-lenses/simplify-review.SKILL.md](templates/review-lenses/simplify-review.SKILL.md)
- [templates/review-lenses/simplify-review.cursor.mdc](templates/review-lenses/simplify-review.cursor.mdc)

Если подключаемый проект объявляет `tooling.agents`, используйте `sync-templates`, чтобы держать эти adapter templates синхронизированными с текущей версией репозитория вместо ручного копирования.

## Использование Structured Artifacts в проекте

`structured-artifacts` — это опциональная возможность для лёгких артефактов планирования и фиксации границ, которые остаются читаемыми в Git и на code review.

Используйте `structured-artifacts`, когда проекту полезны переиспользуемые правила для:

- планирования нетривиальных изменений до реализации
- явных границ модуля и инвариантов для крупных или рискованных областей
- Git-tracked decision records для устойчивых проектных решений
- optional module maps для orchestration-heavy или integration-heavy потоков

Эта возможность сознательно отвергает XML-heavy planning, pseudo-XML knowledge overlays и обязательные machine-oriented code graphs как shared standards.

Подробная методика применения находится в:

- английском руководстве: [docs/structured-artifacts-usage.md](docs/structured-artifacts-usage.md)
- русском руководстве: [docs/structured-artifacts-usage.ru.md](docs/structured-artifacts-usage.ru.md)

Стартовые шаблоны для подключаемых проектов:

- [templates/change-plan.md](templates/change-plan.md)
- [templates/module-contract.md](templates/module-contract.md)
- [templates/decision-record.md](templates/decision-record.md)
- [templates/module-map.md](templates/module-map.md)

## Порядок работы с проектом

1. Держите переиспользуемые стандарты в этом репозитории.
2. Добавляйте `ai.project.toml` в каждый подключаемый проект.
3. Выполняйте сборку `AGENTS.md` из манифеста, когда хотите принять обновления.
4. Просматривайте изменения в подключаемом проекте перед коммитом.

## Версионирование

Фиксируйте нужную версию стандартов в `ai.project.toml`.

```toml
ai_standards_version = "0.1.0"
project_version = "replace-me"
project_release_date = "YYYY-MM-DD"
```

Сборщик встраивает в заголовок сгенерированного файла текущие release metadata из
`pyproject.toml` `tool.ai-standards` и project-local version metadata из
`ai.project.toml`.

Для release workflow самого этого репозитория:

- `rtk uv run bump-version` показывает предлагаемые версию и дату релиза.
- `rtk uv run bump-version save --part minor` обновляет metadata релиза репозитория только на чистом рабочем дереве и не меняет версию Python support package.
- `rtk uv run bump-version tag` создаёт аннотированный тег только из `main` и только на чистом рабочем дереве.

## Текущие фрагменты стеков

- `typescript`
- `layered-architecture`
- `backend-layered-architecture`
- `frontend-layered-architecture`
- `python`
- `fastapi`
- `sqlalchemy`
- `django`
- `django-service-layer`
- `django-drf`
- `django-save-orchestration`
- `java`
- `spring`
- `spring-data-jpa`
- `react`
- `nextjs`
- `tanstack-query`
- `postgres`
- `vue`
- `nuxt`
- `vue-query` (compatibility alias для `tanstack-query` + `vue`)
- `vite`
- `fsd`
- `java-spring` (compatibility alias для `java` + `spring` + `spring-data-jpa`)
