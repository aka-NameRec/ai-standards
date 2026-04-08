# AI Standards

Централизованная инфраструктура инструкций для ИИ-агентов, генерирующая проектные `AGENTS.md`.

Англоязычный оригинал находится в [README.md](/home/shtirliz/workspace/myself/ai-standards/README.md). При изменениях в английской версии эту локализацию нужно обновлять в том же наборе изменений.

## Структура

- `fragments/`: переиспользуемые фрагменты инструкций, сгруппированные по доменам.
- `templates/`: стартовые файлы, которые копируются в подключаемые проекты.
- `scripts/ai_sync.py`: консольный инструмент, который собирает и проверяет `AGENTS.md`.
- `registry.toml`: сопоставляет имена возможностей и стеков с путями к фрагментам.

## Быстрый старт

```bash
uv run python scripts/ai_sync.py init-project --project-root /path/to/project
uv run python scripts/ai_sync.py render --project-root /path/to/project
uv run python scripts/ai_sync.py check --project-root /path/to/project
```

## Конфигурация только через манифест

`ai-standards` не использует именованные профили. Каждый подключаемый проект явно объявляет свои зависимости инструкций в `ai.project.toml`.

Используются три слоя:

- `fragments`: прямые базовые правила, которые должны включаться всегда.
- `features`: опциональные возможности вроде `conport`, `design-first-collaboration`, `grace` и `review-lenses`.
- `stacks`: правила, зависящие от технологии, например `python`, `fastapi`, `postgres`, `react`, `vue` или `java-spring`.

Рекомендуемая стартовая точка для Python/FastAPI проекта со стандартными требованиями к коммуникации и архитектуре:

```toml
version = "2026.03"

fragments = [
  "core/base",
  "core/git-workflow",
  "core/architecture",
  "core/error-handling",
  "core/python",
]

features = [
  "conport",
  "design-first-collaboration",
  "grace",
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
```

Выбирайте зависимости явно. Если правило нужно только одному проекту, держите его в локальном дополнении, а не превращайте в общий фрагмент.

## Правила, специфичные для проекта

Правила, которые должны действовать только внутри одного проекта, следует хранить в репозитории самого проекта.

Рекомендуемая структура подключаемого проекта:

```text
project/
  ai.project.toml
  AGENTS.md
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
- Preserve UMA2 core constraints, design-first-collaboration, and GRACE
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

## Использование Review Lenses в проекте

`review-lenses` — это опциональная возможность для более жёсткого просмотра и упрощения недавних изменений.

Подробная методика применения, включая режимы `review-only` и `fix`, способы активации, рекомендации для CI и этапы внедрения, находится в [docs/review-lenses-usage.ru.md](/home/shtirliz/workspace/myself/ai-standards/docs/review-lenses-usage.ru.md). Англоязычный оригинал: [docs/review-lenses-usage.md](/home/shtirliz/workspace/myself/ai-standards/docs/review-lenses-usage.md).

`ai-standards` должен хранить:

- когда уместен проход упрощения по нескольким ракурсам;
- переиспользуемую модель ракурсов: `Reuse`, `Quality` и `Efficiency`;
- приоритеты при конфликте между этими ракурсами;
- требования к проверке после агрессивной очистки.

Что не стоит переносить в shared fragments без нормализации:

- внутренние детали конкретных вендоров;
- недокументированные утверждения о закрытых инструментах;
- эвристики, привязанные к конкретному фреймворку, которым место в стековых фрагментах;
- хрупкие числовые пороги, не подтверждённые на нескольких проектах.

Стартовые шаблоны для подключаемых проектов:

- [templates/review-lenses/simplify-review.SKILL.md](/home/shtirliz/workspace/myself/ai-standards/templates/review-lenses/simplify-review.SKILL.md)
- [templates/review-lenses/simplify-review.cursor.mdc](/home/shtirliz/workspace/myself/ai-standards/templates/review-lenses/simplify-review.cursor.mdc)

## Использование GRACE в проекте

`ai-standards` интегрирует GRACE как правило и руководство по активации, а не как локальную копию всей исходной методологии.

Что принадлежит `ai-standards`:

- когда должен активироваться GRACE;
- как проект объявляет, что он использует GRACE;
- как GRACE сочетается с `design-first-collaboration`, архитектурными правилами и локальными дополнениями.

Что остаётся upstream:

- навыки GRACE из [`osovv/grace-marketplace`](https://github.com/osovv/grace-marketplace)
- исходный командный процесс
- исходные XML-артефакты и шаблоны

### Условия активации GRACE

Агент должен переключаться с обычного design-first execution на GRACE flow, когда присутствует один или несколько сигналов:

- новая подсистема или крупная группа модулей
- межмодульный рефакторинг
- проектирование контрактов между сервисами или слоями
- миграция с риском совместимости или развёртывания
- задача, требующая явного плана проверки
- задача, выигрывающая от работы несколькими агентами
- плохо изученная область кодовой базы, где нужны устойчивые структурированные знания

Небольшие и локальные низкорисковые изменения могут оставаться на обычном пути без полного запуска GRACE.

### Порядок работы для разработчика

1. Добавить feature `grace` в `ai.project.toml`.
2. Выполнить сборку `AGENTS.md`, чтобы инструкции проекта явно упоминали GRACE.
3. Установить или обновить навыки GRACE из `grace-marketplace`.
4. Подготовить артефакты GRACE в проекте.
5. Использовать процессы планирования, проверки и исполнения GRACE для подходящих задач.

Рекомендуемые команды установки навыков GRACE, основанные на исходном README:

```text
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-init
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-plan
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-execute
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-multiagent-execute
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-setup-subagents
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-fix
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-refresh
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-status
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-ask
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-explainer
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-verification
$skill-installer install https://github.com/osovv/grace-marketplace/tree/main/skills/grace/grace-reviewer
```

Предлагаемый рабочий порядок:

1. `/grace-init`
2. Заполнить `docs/requirements.xml` и `docs/technology.xml`
3. `/grace-plan`
4. `/grace-verification`
5. `/grace-execute` или `/grace-multiagent-execute`

Исходный репозиторий GRACE описывает следующие основные артефакты:

- `docs/requirements.xml`
- `docs/technology.xml`
- `docs/development-plan.xml`
- `docs/verification-plan.xml`
- `docs/knowledge-graph.xml`

## Порядок работы с проектом

1. Держите переиспользуемые стандарты в этом репозитории.
2. Добавляйте `ai.project.toml` в каждый подключаемый проект.
3. Выполняйте сборку `AGENTS.md` из манифеста, когда хотите принять обновления.
4. Просматривайте изменения в подключаемом проекте перед коммитом.

## Версионирование

Фиксируйте нужную версию стандартов в `ai.project.toml`.

```toml
version = "2026.03"
```

Сборщик встраивает запрошенную версию и путь к источнику в заголовок сгенерированного файла.

## Текущие фрагменты стеков

- `python`
- `fastapi`
- `react`
- `postgres`
- `vue`
- `java-spring`
