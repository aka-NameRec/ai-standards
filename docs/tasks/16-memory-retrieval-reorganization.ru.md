---
title: 'Задача 16: реорганизация memory и retrieval'
permalink: ai-standards/tasks/16-memory-retrieval-reorganization.ru
---

# Задача 16: реорганизация memory и retrieval

Английская версия: [16-memory-retrieval-reorganization.md](16-memory-retrieval-reorganization.md)

## Status

Реализовано на ветке `rules-change/16-memory-retrieval-reorganization` (фазы 1–5, пять коммитов). Пометка релиза 2.4.0 и миграция downstream-проектов следуют за слиянием.

## Goal

Реализовать issue #16: разделить project memory, knowledge retrieval и code retrieval/intelligence — удалить ConPort, ввести `retrieval-routing` и `project-memory`, переработать интеграции, добавить экспериментальную `structural-code-intelligence` с методологией evaluation.

## Что сделано

- Фаза 1: ConPort удалён из реестра, манифестов, фрагментов, шаблонов и живой документации; деплой-скилл переименован в `deploy-ai-retrieval-stack` (capability-based, без ConPort); защищённый маркером retire-механизм для переименованных managed-шаблонов; инструкция миграции ConPort → `docs/local` в `update-ai-standards`; запись решения с supersession-пометками у разделения ролей 2026-08-24 и обзора knowledge-stack-roles.
- Фаза 2: policy-слой `retrieval-routing` (правила R1–R6, таблица маршрутизации, разделение capability/implementation); гейт деплой-скилла переведён с `chroma` на `retrieval-routing`.
- Фаза 3: фича `project-memory` — таксономия `docs/local/**` (context, decisions, progress, patterns, investigations, handoffs), политики записи/чтения, явное продвижение; секция манифеста `[project_memory]`; ослабленный аудит `doctor` для локальной области плюс advisory `local-memory-not-gitignored`.
- Фаза 4: интеграции — `session-hygiene` (когда против что/как), `structured-artifacts` (граница `docs/local/**`), `agent-usage-hygiene` (точечный retrieval как дисциплина контекста), `autonomy-boundaries` (сохранение состояния не пересекает границ; стоп на материальных проектных выборах), `basic-memory` (два класса знания), `knowledge-capture`; группы фич и зависимости в README.
- Фаза 5: экспериментальная `structural-code-intelligence` с нейтральными к реализации правилами маршрутизации и методологией evaluation A/B/C; сознательно вне рекомендуемого стека и вне self-hosted манифеста.

## Верификация

- `uv run python scripts/ai_sync.py render/check --project-root .` — идемпотентно, чисто.
- `uv run ruff check scripts tests`, `uv run mypy` — чисто. (Полный `ruff check` по дереву всё ещё даёт 5 предсуществующих находок в `templates/ai-infrastructure/scripts/code_index.py`, воспроизведённых на `main`, задача их не трогала.)
- `uv run python -m pytest` — 127 passed (7 новых policy/retire/local-memory тестов; гейт-зависимые тесты обновлены).
- `ai-sync doctor --project-root .` — 0 ошибок.
- `rg -i conport` — совпадения только в датированной истории (`docs/decisions/**`, `docs/tasks/**`, `docs/archive/**`, `CHANGELOG.md`, `docs/artifacts/**`) и намеренных ссылках инструкций миграции в шаблонах `update-ai-standards` и `deploy-ai-retrieval-stack`.
- Поведенческие сценарии A–E сверены по сгенерированным правилам: A (продолжение вчерашней задачи — таблица маршрутизации + правила извлечения session-hygiene), B (семантический поиск — маршрутизация в Chroma + свежесть + сужение), C (известный точный класс — прямой доступ к исходникам), D (анализ влияния — правила структурного фрагмента; capability в референсном манифесте не включена by design), E (stop-and-consult — stop-condition границ автономии).

## Последующие шаги

- Слияние, релиз 2.4.0 (`bump-version`), тег (отдельные шаги по релизному workflow).
- Миграция девяти downstream-проектов с `conport` в манифестах (сам ai-standards плюс восемь локальных проектов), декомиссия их `context_portal/` после переноса данных.
- Прогон evaluation A/B/C для structural-code-intelligence до любого решения о включении (эпик #19 трекает остальное).

## Observations

- [fact] Все пять критериев готовности issue #16 покрыты: ConPort отсутствует в манифестах/сгенерированных файлах/живой документации; правила routing-политики отрендерены и покрыты policy-тестами; тесты knowledge-tree защищают `docs/local` от давления канонического аудита; сценарии A–E сверены; graph-capability экспериментальна с гейтом evaluation.
- [fact] Retire-механизм защищён маркером: managed-копии переименованных шаблонов удаляются, переписанные пользователем файлы выживают (протестировано).

## Relations

- implements issue #16
- follows [[РЕШЕНИЕ: реорганизация memory и retrieval]]
- planned by [[План изменений: реорганизация memory и retrieval (issue #16)]]
- локальная версия [[Task 16: memory and retrieval reorganization]]
