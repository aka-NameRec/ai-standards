---
title: 'План изменений: реорганизация memory и retrieval (issue #16)'
permalink: ai-standards/artifacts/2026-09-18-memory-retrieval-reorganization-change-plan.ru
---

# План изменений: реорганизация memory и retrieval (issue #16)

Статус: в работе. Ветка `rules-change/16-memory-retrieval-reorganization`.
Принятые решения и точки верификации: этот план плюс итоги обсуждения в issue #16.

## Цель

Разделить три задачи, которые стандарты сейчас смешивают, — project memory,
knowledge retrieval и code retrieval/intelligence, — удалив ConPort, введя
инструментально-нейтральный policy-слой `retrieval-routing` и дав локальной
межсессионной рабочей памяти стандартный дом (`docs/local/**`) с фиксированной
таксономией.

Исходный proposal: `docs/archive/20260913-122716-proposal-memory-retrieval-reorganization.md`.
Продолжение-эпик (фазы 6–7): issue #19.

## Объём

- В объёме (фазы 1–5, один релиз 2.4.0, одна ветка):
  - Фаза 1: удалить фичу `conport` и все живые упоминания; переименовать
    `deploy-ai-knowledge-stack` в `deploy-ai-retrieval-stack` (гейт остаётся
    `chroma` до фазы 2); добавить retire-механизм для переименованных
    managed-шаблонов; добавить инструкцию миграции ConPort → `docs/local`
    в `update-ai-standards`.
  - Фаза 2: новая фича `retrieval-routing` (правила R1–R6, capability
    awareness, разделение capability/implementation); перевод гейта
    деплой-скилла на `retrieval-routing`; policy-тесты.
  - Фаза 3: новая фича `project-memory` (таксономия `docs/local/**`:
    context, decisions, progress, patterns, investigations, handoffs;
    политика записи/чтения; явное продвижение); ослабленный аудит `doctor`
    для зоны local memory; ключ манифеста `local_memory_tree`.
  - Фаза 4: интеграции — `session-hygiene` (WHEN против WHAT/HOW),
    `structured-artifacts` (только reviewable-артефакты), `agent-usage-hygiene`,
    `autonomy-boundaries`, `chroma`, `knowledge-capture`.
  - Фаза 5: экспериментальная фича `structural-code-intelligence` плюс
    артефакт-методология evaluation A/B/C. Без развёрточной инфраструктуры.
- Вне объёма: фазы 6–7 (issue #19), развёртывание Graphify, любое
  автоматическое продвижение local memory, multi-agent-семантика за пределами
  минимальных полей provenance.

## Затрагиваемые модули

- `scripts/ai_sync.py` (реестр шаблонов, retire-механизм, зона local memory в doctor)
- `fragments/**` (удаление conport; добавление retrieval-routing,
  project-memory, structural-code-intelligence; переработка интеграций)
- `registry.toml`, `templates/project_manifest.toml`, `ai.project.toml`
- `templates/ai-infrastructure/**` (переработка и переименование деплой-скилла)
- `templates/knowledge-capture/**`, `templates/standards-update/**` (формулировки без ConPort, шаг миграции)
- `tests/test_ai_sync.py`, `tests/test_bump_version.py`
- `README.md` / `README.ru.md`, usage-документация под `docs/` (только живые упоминания)
- Новая запись решения + supersession-пометки у решения 2026-08-24 о разделении ролей и у обзора knowledge-stack-roles

## Предлагаемая структура

- Граф фич после изменения:
  `retrieval-routing` — связующий policy-слой;
  `basic-memory` — слой retrieval над Markdown (canonical + local);
  `project-memory` — инструментально-независимая таксономия и жизненный цикл
  локальной памяти; `chroma` — семантический поиск по коду;
  `structural-code-intelligence` — экспериментальная graph-capability.
- `project-memory` сознательно отделена от `basic-memory`: возможность не
  должна зависеть от одного способа её поддержки (лучше всего работает с
  basic-memory, но не требует его).
- Деплой-скилл становится capability-based: разворачивает только слои,
  включённые в манифест.

## Порядок работ

1. Фаза 1 (эта ветка): удаление ConPort; переработка и переименование
   деплой-скилла; retire-механизм; инструкция миграции; запись решения.
2. Фаза 2: фрагмент `retrieval-routing` + реестр + смена гейта + тесты.
3. Фаза 3: фрагмент `project-memory` + изменения doctor + тесты.
4. Фаза 4: фрагменты интеграций + usage-документация.
5. Фаза 5: экспериментальный фрагмент + артефакт evaluation; релиз 2.4.0
   (`bump-version`), закрытие #16, затем миграция downstream-проектов.

## Риски

- Удаление `conport` ломает `render` для downstream-манифестов, где фича ещё
  названа (`SyncError` на неизвестную фичу). Смягчение: инструкция миграции в
  `update-ai-standards`; все девять локальных проектов мигрированы до анонса
  релиза.
- Переименованные шаблоны оставляют осиротевшие копии в проектах. Смягчение:
  retire-механизм удаляет managed-копии по маркеру; пользовательские файлы без
  маркера не трогаются.
- `doctor` применяет правила канонических заметок ко всем `.md` дерева;
  local memory утонула бы в предупреждениях. Смягчение: ослабленный аудит
  зоны local memory (фаза 3).

## Инварианты

- Живая документация, фрагменты, манифесты и шаблоны не содержат упоминаний
  ConPort; датированная история (`docs/decisions/**`, `docs/tasks/**`,
  `docs/archive/**`, `CHANGELOG.md`) сохраняет их с явными supersession-ссылками
  там, где запись описывает текущее состояние.
- Рендер остаётся идемпотентным; неизвестные фичи/агенты по-прежнему
  отвергаются при загрузке; определение managed-файлов остаётся маркерным;
  поведение `--fix` не меняется.
- Локальная рабочая память никогда не считается канонической документацией;
  продвижение остаётся явной операцией.
- Один релиз: промежуточное состояние без замены `conport` не выпускается.

## Критерии готовности

- [ ] `rg -i conport` по репозиторию находит только датированную историю
      (`docs/decisions/**`, `docs/tasks/**`, `docs/archive/**`, `CHANGELOG.md`).
- [ ] Сгенерированный `AGENTS.md` не содержит раздела ConPort; это защищает
      policy-тест.
- [ ] Retire-механизм покрыт тестом: managed-копии переименованных шаблонов
      удаляются, нетронутые пользовательские файлы выживают.
- [ ] Инструкция миграции присутствует во всех трёх вариантах шаблона
      `update-ai-standards` (формулировки EN; шаблоны не локализуются).
- [ ] Критерии готовности фаз 2–5 из issue #16 (правила routing, таксономия,
      ослабленный doctor, интеграции, экспериментальная capability) покрыты
      тестами.
- [ ] Релиз 2.4.0 помечен тегом; downstream-проекты мигрированы.

## Верификация

- Автоматическая: `uv run python scripts/ai_sync.py render/check --project-root .`,
  `uv run ruff check`, `uv run mypy`, `uv run python -m pytest`.
- Ручная: аудит `rg -i conport`; поведенческие сценарии A–E на этом
  репозитории как референсной конфигурации в конце итерации.

## Итог

-Доставлено пятью фазовыми коммитами на `rules-change/16-memory-retrieval-reorganization`: ConPort удалён (с инструкцией миграции и защищённым маркером retire-механизмом); добавлен policy-слой `retrieval-routing` и стал гейтом деплой-скилла; добавлена `project-memory` с таксономией `docs/local/**` и ослабленным аудитом doctor; переработаны интеграции (session-hygiene, structured-artifacts, agent-usage-hygiene, autonomy-boundaries, basic-memory, knowledge-capture) плюс группы фич в README; добавлена экспериментальная `structural-code-intelligence` с методологией evaluation A/B/C.
- Верификация: 127 тестов прошло, render/check идемпотентны, ruff (scripts, tests) и mypy чисты, doctor 0 ошибок, `rg -i conport` ограничен датированной историей и намеренными ссылками миграции, поведенческие сценарии A–E сверены по сгенерированным правилам.
- Отклонения: существенных нет. Порядок и объём фаз по плану выдержаны; гейт деплой-скилла переключён в фазе 2 ровно как запланировано.
- Последующие шаги: пометка релиза 2.4.0; миграция девяти downstream-проектов; прогон structural evaluation до любого решения о включении (эпик #19).

## Observations

- [fact] Итерация разделяет project memory, knowledge retrieval и code intelligence на отдельные фичи; порядок фаз следует issue #16, фазы 6–7 отслеживаются в issue #19.

## Relations

- relates_to [[РЕШЕНИЕ: реорганизация memory и retrieval]]
- relates_to [[Роли стека знаний]]
