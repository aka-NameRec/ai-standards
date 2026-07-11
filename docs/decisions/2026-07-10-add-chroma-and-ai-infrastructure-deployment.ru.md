# РЕШЕНИЕ: add-chroma-and-ai-infrastructure-deployment

Англоязычная оригинальная версия: [2026-07-10-add-chroma-and-ai-infrastructure-deployment.md](2026-07-10-add-chroma-and-ai-infrastructure-deployment.md)

## Статус

Принято

## Дата

2026-07-10

## Контекст

`ai-standards` уже стандартизирует политику использования `conport` и `basic-memory`, и для каждого есть рендерящийся фрагмент плюс (для Basic Memory) руководство по использованию. Оставались два пробела:

1. **Нет стандарта Chroma.** Семантический поиск по исходному коду разворачивался ad hoc в нижестоящих рабочих пространствах (в частности, в крупном мульти-репозиторном пространстве), но отсутствовал в `ai-standards`: ни фрагмента, ни записи в реестре, ни руководства, ни навыка. Chroma фигурировал только как недокументированный gitignored runtime-артефакт под `context_portal/`, создаваемый внутренним векторным хранилищем ConPort — это другой вопрос.
2. **Нет навыка развёртывания.** `ai-standards` стандартизирует, как *использовать* инструменты («когда MCP-сервер доступен»), но не как их *развёртывать*. Реальная сессия настройки (семейство GPT-5) сожгла примерно 22,8 млн токенов — около 80% пятичасового окна — почти целиком на инфраструктуру: синхронный polling долгой сборки Chroma, бутылочное горлышко per-file embedding и краш манифеста в середине сборки, гонку при бутстрапе Basic Memory, завершившуюся деструктивным сбросом базы, повторяющиеся ошибки cloud-routing, уход определения workspace ConPort в `$HOME` и несогласованность MCP между клиентами (в Kilo отсутствовал сервер ConPort, имевшийся в Codex).

Цель команды — унифицировать AI knowledge stack и его развёртывание, чтобы дорогостоящая настройка выполнялась однократно и переиспользовалась, а не переоткрывалась в каждом проекте.

## Решение

`ai-standards` добавляет фичу `chroma` и переиспользуемый навык развёртывания, которые вместе стандартизируют и политику использования, и развёртывание AI knowledge stack (ConPort, Basic Memory, Chroma и опционально Graphify).

### Канонический AI knowledge stack

Стек из четырёх слоёв с тремя намеренно раздельными векторными хранилищами:

| Слой | Инструмент | Назначение | Хранилище |
|---|---|---|---|
| 0 | `docs/` (Git) | durable source of truth | Markdown |
| 1 | Basic Memory | retrieval по документации | sqlite + embeddings BM |
| 2 | ConPort | transient operational context | sqlite ConPort (+ внутр. векторы) |
| 3 | Chroma | семантический поиск по коду | sqlite Chroma PersistentClient |
| (4) | Graphify | структурная навигация по коду | опционально, граф per-repo |

Инвариант: внутренние векторы ConPort, индекс кода Chroma и embeddings Basic Memory никогда не смешиваются.

### Политика использования Chroma (`fragments/tools/chroma.md`)

- Chroma — слой семантического поиска по коду, отдельный от хранилищ ConPort и Basic Memory.
- Все запросы идут через freshness-gate-обёртку, которая обновляет индекс перед запросом и блокируется при ошибке обновления.
- Similarity сужает исследование, но не доказывает полноту; исчерпывающие утверждения требуют exact search плюс build/static-проверки.
- Индексация инкрементальная по content-hash с atomic, resumable-манифестом.
- Локальный `PersistentClient` (embedded sqlite, без Docker) — по умолчанию; Docker опционален для shared/CI.

### Навык развёртывания (`templates/ai-infrastructure/`)

Навык ручного запуска, распространяемый на четыре среды (Codex, Claude, Kilo, Cursor), разворачивает стек в проекте в порядке, устраняющем гонки, наблюдённые в крупном рабочем пространстве:

1. Token-cheap pre-flight: прочитать layout однократно и суммировать; не polling.
2. ConPort: создать `context_portal/` до опоры на detection (иначе уходит в `$HOME`); `workspace_id` — корень проекта.
3. Basic Memory: `bm project add` до любого search; никогда `db reset`; `ensure_frontmatter_on_sync=false`; force local mode (отключить cloud routing); ограничить MCP per-workspace через `--project`.
4. Chroma: локальный `PersistentClient` из обобщённого шаблона `code_index.py` с cross-file batch upsert и atomic resumable-манифестом; сборку запускать detached и проверять однократно.
5. Согласованная MCP-проводка между клиентами (Kilo `kilo.json` и Codex `.codex/config.toml`).
6. Верификация через `bm status`, `bm doctor`, ConPort active context и collection counts.

### Per-project инфра-неймспейс

Управляемая ai-standards инфраструктура в downstream-проекте живёт под `.ai-standards/`, не смешиваясь с проектными `scripts/`:

```
.ai-standards/
├── scripts/code_index.py   # managed template (обобщён из production-эталона)
├── code-index.toml         # managed starter-config (collections, roots, chunking)
├── chroma/                 # runtime sqlite (gitignored)
└── state/                  # manifest.json (gitignored)
```

### Изменения propagation

- `registry.toml` содержит `chroma = ["tools/chroma"]`.
- `templates/project_manifest.toml` содержит `chroma` как opt-in (закомментирован).
- `ai_sync.py` получает агент-адаптеры `claude` и `kilo` в дополнение к `codex` и `cursor`; шаблоны агентов получают опциональный гейт `feature`; включение `chroma` в манифесте рендерит usage-фрагмент, синхронизирует инфра-шаблоны `.ai-standards/` и распространяет навык развёртывания для включённых агентов.

## Почему

- превращает дорогую, чреватую ошибками разовую настройку в повторяемое, свободное от гонок развёртывание, которое любой агент выполнит с минимальными токен-затратами;
- делает Chroma first-class документированным стандартом вместо недокументированного побочного эффекта;
- удерживает три векторных хранилища явно раздельными, чтобы retrieval оставался точным, а не шумным;
- расширяет поддержку агентов до четырёх распространённых сред (Codex, Claude, Kilo, Cursor), чтобы навык достигал каждого инструмента команды.

## Рассмотренные альтернативы

### Хранить знания о развёртывании только в оригинальном `code_index.py`

Отклонено: реализация переоткрывалась бы в каждом проекте, а гонки и токен-ловушки операционны, а не проектно-специфичны. Им место в общем стандарте.

### Запускать Chroma как Docker-сервис по умолчанию

Отклонено для умолчания: локальный embedded `PersistentClient` — zero-ops, без порта и серверного процесса, изолирован per-workspace. Docker остаётся opt-in для shared/CI.

### Распространять навык развёртывания только в Codex и Cursor

Отклонено: команда работает в Kilo (и теперь Claude). Ограничение двумя агентами лишило бы основную рабочую среду этого навыка.

### Гейтить навык развёртывания новой фичей `ai-infrastructure` вместо `chroma`

Рассмотрено и отложено. `chroma` — естественный триггер: инфра код-индекса и основная ценность навыка (свободная от гонок сборка Chroma плюс бутстрап BM/ConPort) наиболее нужны при включённом семантическом поиске по коду. Сам навык остаётся модульным и разворачивает только слои, включённые в манифесте.

## Последствия

### Преимущества

- downstream-проект включает `chroma` и за один шаг получает usage-правила, инфра-шаблоны и навык развёртывания;
- токен-ловушки того развёртывания (синхронный polling, per-file upsert, краш манифеста, сброс BM, cloud routing, уход detection, дрифт MCP) закодированы как превентивный порядок в навыке;
- четыре агентных среды получают managed-копии навыка через `ai-sync sync-templates`.

### Издержки

- репозиторий несёт новую фичу, пару usage-руководств, шаблоны навыка, инфра-скрипт и дополнительную логику в `ai_sync.py` с тестами;
- шаблон `code_index.py` нужно обобщить из оригинальной production-реализации и поддерживать как эталон;
- команды, включающие `chroma`, должны запустить навык развёртывания, чтобы материализовать инфраструктуру.

## Затронутые модули

- `registry.toml`
- `fragments/tools/chroma.md`
- `fragments/tools/basic-memory.md`
- `docs/chroma-usage.md`
- `docs/chroma-usage.ru.md`
- `docs/basic-memory-usage.md`
- `docs/basic-memory-usage.ru.md`
- `docs/conport-usage.md`
- `docs/conport-usage.ru.md`
- `docs/decisions/2026-07-10-add-chroma-and-ai-infrastructure-deployment.md`
- `docs/decisions/2026-07-10-add-chroma-and-ai-infrastructure-deployment.ru.md`
- `docs/tasks/0ta01xp-ai-infrastructure-deployment-skill.md`
- `docs/tasks/0ta01xp-ai-infrastructure-deployment-skill.ru.md`
- `templates/project_manifest.toml`
- `templates/ai-infrastructure/deploy-ai-knowledge-stack.SKILL.md`
- `templates/ai-infrastructure/deploy-ai-knowledge-stack.cursor.mdc`
- `templates/ai-infrastructure/deploy-ai-knowledge-stack.claude.md`
- `templates/ai-infrastructure/scripts/code_index.py`
- `templates/ai-infrastructure/code-index.toml`
- `ai.project.toml`
- `scripts/ai_sync.py`
- `tests/test_ai_sync.py`
- `README.md`
- `README.ru.md`
- `AGENTS.md`

## Инварианты и ограничения

- Git-tracked Markdown остаётся источником durable project knowledge.
- Внутренние векторы ConPort, индекс кода Chroma и embeddings Basic Memory остаются раздельными хранилищами.
- Similarity Chroma сужает исследование, но никогда не доказывает полноту самостоятельно.
- Навык развёртывания никогда не должен сбрасывать базу Basic Memory как шаг восстановления.
- Управляемая ai-standards инфраструктура в downstream-проекте живёт под `.ai-standards/`.

## Верификация

- `registry.toml` содержит фичу `chroma`.
- Рендер содержит фрагмент Chroma при включённой фиче.
- Руководства по использованию `chroma` и `conport` существуют на английском и русском.
- `ai-sync sync-templates` распространяет навык развёртывания на `codex`, `claude`, `kilo` и `cursor` при включённой `chroma`.
- `ai-sync sync-templates` создаёт `.ai-standards/scripts/code_index.py` и `.ai-standards/code-index.toml` при включённой `chroma` и пропускает их иначе.
- Self-hosted `AGENTS.md` успешно рендерится с включённой фичей.
- `ruff`, `mypy` и `pytest` проходят.

## Связанные артефакты

- [../chroma-usage.md](../chroma-usage.md)
- [../chroma-usage.ru.md](../chroma-usage.ru.md)
- [../conport-usage.md](../conport-usage.md)
- [../conport-usage.ru.md](../conport-usage.ru.md)
- [../../fragments/tools/chroma.md](../../fragments/tools/chroma.md)
- [../tasks/0ta01xp-ai-infrastructure-deployment-skill.md](../tasks/0ta01xp-ai-infrastructure-deployment-skill.md)
- [2026-05-19-add-basic-memory-feature.md](2026-05-19-add-basic-memory-feature.md)
