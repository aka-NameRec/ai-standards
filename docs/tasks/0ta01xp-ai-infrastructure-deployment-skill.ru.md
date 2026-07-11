# 0ta01xp — Навык развёртывания AI-инфраструктуры и стандарт Chroma

Англоязычная оригинальная версия: [0ta01xp-ai-infrastructure-deployment-skill.md](0ta01xp-ai-infrastructure-deployment-skill.md)

## Цель

Добавить в `ai-standards` фичу `chroma` и переиспользуемый навык развёртывания, чтобы AI knowledge stack (ConPort, Basic Memory, Chroma, опционально Graphify) был стандартизирован и по политике использования, и по развёртыванию. Устранить переоткрытие дорогой, чреватой гонками настройки в каждом проекте.

## Объём

### В области

- usage-фрагмент `chroma` и двуязычное руководство по использованию.
- Запись `chroma` в реестре и opt-in запись в манифесте.
- Навык развёртывания, распространяемый на четыре среды (Codex, Claude, Kilo, Cursor), с гейтом по фиче `chroma`.
- Инфра-шаблоны `.ai-standards/`: обобщённые `code_index.py` и `code-index.toml`, синхронизируемые при включённой `chroma`.
- Агент-адаптеры `claude` и `kilo` в `ai_sync.py`; опциональный гейт `feature` на шаблонах агентов.
- Распространение `simplify-review` на `claude` и `kilo` для консистентности.
- Правило per-workspace изоляции Basic Memory (`--project`) во фрагменте и руководстве `basic-memory`.
- Двуязычное руководство `conport-usage` (заполнение существующего пробела).
- Self-hosted манифест включает `chroma`; перегенерированный `AGENTS.md`.
- Двуязычная decision record, task spec, обновления README и тесты.

### Вне области

- Развёртывание Chroma через Docker по умолчанию (по умолчанию локальный `PersistentClient`; Docker остаётся задокументированной опцией).
- Обобщение Graphify (упоминается в навыке как опциональное, здесь не шаблонизируется).
- Миграция существующих downstream-рабочих пространств (DevCats, cockpit) на новый layout — отдельная follow-up-задача.
- Коммиты, bump версии и release-tagging — выполняются по release-workflow после ревью.

## Затронутые модули

- `registry.toml`
- `fragments/tools/chroma.md`
- `fragments/tools/basic-memory.md`
- `docs/chroma-usage.md` (+ `.ru.md`)
- `docs/basic-memory-usage.md` (+ `.ru.md`)
- `docs/conport-usage.md` (+ `.ru.md`)
- `templates/project_manifest.toml`
- `templates/ai-infrastructure/` (варианты навыка, `scripts/code_index.py`, `code-index.toml`)
- `ai.project.toml`
- `scripts/ai_sync.py`
- `tests/test_ai_sync.py`
- `README.md` (+ `.ru.md`)
- `AGENTS.md` (перегенерированный)

## Предлагаемая структура

- `AgentTemplate` получает `feature: str | None = None`; шаблоны с фичей синхронизируются только при включённой фиче.
- Новый кортеж `INFRA_TEMPLATES` агент-независимых шаблонов (с гейтом по фиче), синхронизируемых вместе с шаблонами агентов.
- `sync_project_templates` расширяется: гейтит шаблоны агентов по фиче и синхронизирует `INFRA_TEMPLATES`.
- Исходники навыка развёртывания лежат в `templates/ai-infrastructure/`; шаблон `code_index.py` обобщён из эталона DevCats (пути под `.ai-standards/`, cross-file батчинг, atomic resumable-манифест).

## Порядок работ

1. Decision record + task spec (design-first артефакты).
2. Фрагмент Chroma + двуязычное руководство; проводка реестра и манифеста.
3. Правило изоляции Basic Memory + секция в руководстве; руководство ConPort.
4. Навык развёртывания (три исходных варианта) + шаблоны `code_index.py` + `code-index.toml`.
5. Изменения `ai_sync.py` (адаптеры claude/kilo, гейт фичи, INFRA_TEMPLATES) + тесты.
6. Включить `chroma` в self-hosted манифесте; перегенерировать `AGENTS.md`.
7. Обновления README; прогон `render`/`check`/`ruff`/`mypy`/`pytest`.

## Риски

- Обобщение `code_index.py` без живого рабочего пространства для полной сборки Chroma — смягчение: сохранить доказанный алгоритм DevCats нетронутым, абстрагировать только пути/конфиг.
- Добавление гейта `feature` может изменить порядок результатов `sync_project_templates` и сломать существующие точные утверждения в тестах — смягчение: гейтить только новые шаблоны (существующий `simplify-review` остаётся без гейта), так что манифесты без `chroma` не затрагиваются.
- Различия frontmatter четырёх сред — смягчение: один общий `SKILL.md` для codex+kilo, плюс варианты cursor и claude.

## Инварианты

- Существующие тесты для манифестов без `chroma` проходят без изменений.
- `simplify-review` продолжает синхронизироваться для `codex` и `cursor` ровно как прежде.
- Git-tracked Markdown остаётся источником истины; три векторных хранилища остаются раздельными.

## Критерии приёмки

- [ ] Фича `chroma` рендерит секцию Chroma в `AGENTS.md`.
- [ ] Руководства `chroma-usage` и `conport-usage` существуют на EN и RU.
- [ ] `sync-templates` распространяет навык развёртывания на все четыре среды при включённой `chroma`.
- [ ] `sync-templates` создаёт `.ai-standards/scripts/code_index.py` и `.ai-standards/code-index.toml` при включённой `chroma` и пропускает их иначе.
- [ ] `claude` и `kilo` — принимаемые агенты; неподдерживаемые агенты по-прежнему вызывают `SyncError`.
- [ ] `render`, `check`, `ruff`, `mypy`, `pytest` проходят.

## Верификация

- Автоматизированная: `pytest`, `ruff`, `mypy`, `ai-sync check`.
- Ручная: проверка рендеренной секции Chroma в `AGENTS.md`; проверка вывода dry-run `sync-templates` во временном проекте.
- Наблюдаемость: записи decision + progress в ConPort; этот task spec и decision record.

## Результат

- Доставлена фича `chroma` (фрагмент + двуязычное руководство), проводка реестра и манифеста, и feature-gated навык развёртывания, распространяемый на четыре среды (Codex, Claude, Kilo, Cursor).
- Добавлены агент-адаптеры `claude` и `kilo`; `AgentTemplate` получил опциональный гейт `feature`; `INFRA_TEMPLATES` материализует `.ai-standards/scripts/code_index.py` и `.ai-standards/code-index.toml` при включённой `chroma`.
- `code_index.py` обобщён из эталона DevCats (только Chroma, пути под `.ai-standards/`, cross-file batch upsert, atomic resumable-манифест).
- Расширен `basic-memory` правилом per-workspace изоляции `--project`; добавлено двуязычное руководство `conport-usage`.
- Верификация: `render`/`check` проходят, `AGENTS.md` содержит секции Chroma и изоляции Basic Memory; `ruff`, `mypy` и `pytest` (45 тестов, +4 новых) проходят.
- Отклонение: `simplify-review` добавлен для `kilo` (переиспользует существующий SKILL.md-источник), но отложен для `claude` (потребовал бы отдельного command-источника); отмечено как follow-up.
- Follow-up: коммит на рабочей ветке (утверждение сообщения ожидается), bump версии и release-tagging по release-workflow, миграция DevCats/cockpit на новый layout.
