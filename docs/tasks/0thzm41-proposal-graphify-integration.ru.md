# 0thzm41 — Предложение: интеграция Graphify в ai-standards

Англоязычная оригинальная версия: [0thzm41-proposal-graphify-integration.md](0thzm41-proposal-graphify-integration.md)

> Статус: Предложение — ещё не принято. Зафиксировано для последующего design-first-прохода.

## Контекст

`ai-standards` теперь стандартизует политику использования и развёртывание для ConPort, Basic Memory и Chroma (задача `0ta01xp`). Слой структурного анализа кода — оставшийся пробел. DevCats уже использует Graphify (CLI `graphify`) для `broadleaf/backend`: `graphify update .` создаёт `graphify-out/graph.json` (~9k узлов / ~23k рёбер) и предоставляет операции `query` / `path` / `explain` над графом структуры кода.

Graphify **дескриптивен** (фиксирует, чем код структурно ЯВЛЯЕТСЯ) — это иная природа, чем **нормативный** module contract (чем код ДОЛЖЕН быть). Это различие определяет всё предложение.

## Предлагаемый объём

Добавить `graphify` как **opt-in фичу** (как `chroma`), scoped на два дополнительных применения:

1. **Генерация и валидация module-map.** `module-map.md` уже существует в `structured-artifacts` как дескриптивный артефакт для orchestration-heavy, integration-heavy, migration-prone модулей. Graphify — естественный генератор/валидатор для него.
2. **Верификация структурных инвариантов контракта.** Module contract (`MODULE_CONTRACT.md`) декларирует структурные факты (зависимости, слой, public API, запрещённые вызывающие). Graphify механически сверяет реальный граф с задекларированными фактами и сообщает дрейф. Контракт остаётся нормативным правилом; Graphify — исполнитель.

### Явные Non-Goals

- Graphify **не заменяет** авторские module contracts. Non-goals, инварианты, failure boundaries и ownership нормативны и не выводятся из структуры кода.
- Graphify **не является** фичей по умолчанию. Он нацелен на крупные, слоистые, integration-heavy кодовые базы (broadleaf-масштаб); для небольших и средних проектов это оверхед.
- Graphify **не хранит** контракты. Он хранит структурный граф, используемый для генерации карт и проверки фактов контракта.

## Интеграция в навык развёртывания (fire-and-forget)

Установка и настройка Graphify должны стать шагом навыка `deploy-ai-knowledge-stack`, чтобы пользователь действовал по схеме «выстрелил и забыл»: агент устанавливает, настраивает, собирает и далее использует граф без ручного вмешательства.

При включённой в манифесте `graphify` навык развёртывания выполняет:

1. **Установка** CLI `graphify` (через `uv tool install` / пакетный менеджер), с гейтом по фиче `graphify` и проверкой через `graphify --help` (внимание: `graphify --version` не поддерживается).
2. **Конфигурация** graph-таргетов per-repo под `.ai-standards/` (секция `graphify` в `code-index.toml` или отдельный конфиг), с объявлением, какие корни получают графы и где лежит `graphify-out/graph.json`.
3. **Сборка** начального графа для каждого объявленного таргета (detached, с checkpoint, проверка однократно — та же token-дисциплина, что у сборки Chroma; никакого синхронного polling).
4. **Проводка** запросов через ту же freshness-gate-обёртку, что обслуживает Chroma, чтобы refresh и query Graphify имели единую операционную точку входа.

Навык должен оставаться **модульным**: Graphify разворачивается только при `graphify` в features манифеста и только для объявленных таргетов.

## Методика поддержания графа в актуальном состоянии

Граф должен оставаться актуальным на тех же условиях, что Chroma и Basic Memory:

- **Freshness-gate**: каждый запрос Graphify сначала обновляет граф (`graphify update .` на корне таргета) и блокируется при ошибке обновления, поэтому запросы не идут против устаревшего графа.
- **Event-driven refresh-триггеры** (зеркало reindex Basic Memory и refresh Chroma): после `git pull`, `git merge`, `git rebase`, branch switch или крупного патча, меняющего структуру; перед структурными запросами, проверкой инвариантов контракта или blast-radius/impact-анализом.
- **Инкрементальность**: предпочитать инкрементальное обновление Graphify полному ребилду при поддержке; checkpoint per-target-состояния под `.ai-standards/state/` (atomic, resumable), чтобы прерванная сборка возобновлялась.
- **Никогда session-driven**: не перестраивать граф в каждой сессии; refresh только по health-сигналу или событию VCS/изменения структуры.
- **Структура/similarity — не полнота**: структурные результаты сужают исследование, но не доказывают полноту; исчерпывающие утверждения требуют exact search плюс build/type/static-проверки (то же правило, что для Chroma).

## Предлагаемый layout

Управляемые ai-standards артефакты Graphify живут под `.ai-standards/`, консистентно с Chroma:

```
.ai-standards/
├── scripts/
│   └── code_index.py        # расширен subcommand'ами graphify refresh/query (или sibling-скрипт)
├── graphify-out/            # per-repo graph.json (gitignored runtime или repo-local по прецеденту DevCats)
└── state/                   # per-target graph state (gitignored runtime)
```

Конфигурация graph-таргетов объявляется в существующем `.ai-standards/code-index.toml` в секции `[[graph]]` (прецедент DevCats), так что один конфиг управляет и коллекциями Chroma, и таргетами Graphify.

## Открытые дизайн-вопросы (для последующего design-first-прохода)

- Границы per-language-поддержки и как их выразить (покрытие Graphify различается по языкам).
- Живёт ли refresh/query Graphify в существующей обёртке `code_index.py` или в sibling-скрипте.
- `graphify-out/` — workspace-central (`.ai-standards/`) или repo-local (DevCats использовал repo-local `broadleaf/backend/graphify-out/`).
- Схема структурных фактов контракта: какие поля machine-checkable (`depends_on`, `layer`, `public_api`, `forbidden_callers`) и как они объявляются в `MODULE_CONTRACT.md` (блок frontmatter vs отдельный структурированный файл).
- Формат вывода верификации дрейфа инвариантов контракта (только отчёт vs падающая проверка).

## Затронутые модули (предполагаемые)

- `registry.toml` (фича `graphify`)
- `fragments/tools/graphify.md` + `docs/graphify-usage.md` (+ `.ru.md`)
- `templates/ai-infrastructure/` (расширение обёртки + секция `[[graph]]` в конфиге)
- `templates/ai-infrastructure/deploy-ai-knowledge-stack.*` (шаг развёртывания Graphify)
- `scripts/ai_sync.py` (feature-gated инфра-шаблоны, если нужны новые файлы)
- `docs/decisions/` (decision record при принятии)

## Связь с текущей работой

- Надстраивается над фундаментом `0ta01xp` (feature-gated шаблоны, неймспейс `.ai-standards/`, freshness-gate-обёртка, навык развёртывания).
- Не блокирует merge `0ta01xp`, bump версии или релиз. Выполняется как отдельная задача после ревью и релиза текущего change set.

## Следующий шаг

Открыть отдельную ветку и провести design-first-проход (change plan + decision record), разрешающий открытые дизайн-вопросы выше, до реализации.
