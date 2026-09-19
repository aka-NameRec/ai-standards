---
title: 17 — Инициатива Rule Engineering, фазы 0–1
permalink: ai-standards/tasks/17-rule-engineering-phase-0-1.ru-1
---

# 17 — Инициатива Rule Engineering, фазы 0–1

Английская версия: [17-rule-engineering-phase-0-1.md](17-rule-engineering-phase-0-1.md)

Дата: 2026-09-19 · Ветка: `rules-change/17-rule-engineering` (коммит `ecb80ca`, не отправлен; push требует явного согласия пользователя)

## Триггер

Пользователь принял issue #17 2026-09-19: направление инициативы, разделение
объёма #17/#18 (методология в этом репозитории, исполняемая eval-инфраструктура
в спецификации `ai-standards-evals`) и `docs/scenarios/` как будущий дом
контрактов сценариев. Принятое решение:
[docs/decisions/2026-09-19-adopt-rule-engineering-initiative.ru.md](../decisions/2026-09-19-adopt-rule-engineering-initiative.ru.md).

## Что сделано

- **Фаза 0**: baseline-артефакт `docs/artifacts/2026-09-19-rule-engineering-baseline.ru.md` — замеры репозитория на релизе 2.4.0 (`AGENTS.md` 59 550 байт / 597 строк / 36 секций, 17 features, 42 фрагмента, 6 skills), текущее поведение, связанное с правилами, и пять сценариев-кандидатов для будущего сравнения.
- **Фаза 1**: новый feature `rule-engineering` — фрагмент `process/rule-engineering.md` (девять свойств качества правила, понятие interpretation surface, двенадцатишаговый инженерный поток с обязательной формой валидации, принципы размещения; 3 954 байта); запись в `registry.toml` с `feature_meta` `2.5.0`; self-hosting включён в `ai.project.toml`; `AGENTS.md` перегенерирован; usage-гайды на обоих языках; README (оба языка) — оглавление, перечисление features, группа «Управление исполнением», секция «Использование Rule Engineering в проекте», поток `Заимствование внешних правил` переформулирован как частный случай Rule Engineering с обновлённым стандартным import prompt; CHANGELOG `[Unreleased]`; два теста (render + фрагмент).
- Фиксация знаний: эта task-запись и обновление локального контекста.

## Проверки

- `uv run pytest`: 125 прошли; 4 падения существовали на `main` до этого изменения (проверено через stash: `test_render_contains_expected_markers`, `test_legacy_manifest_version_key_still_renders`, `test_init_project_seeds_current_ai_standards_version`, `test_check_fails_when_manifest_pin_drifts_from_the_source` хардкодят баннер релиза `v2.3.0` и сломались на релизе 2.4.0).
- `uv run ruff check` и `uv run mypy scripts/` чисты по изменённым файлам; рендер идемпотентен; `ai-sync doctor` — ноль ошибок (184 предупреждения существующего класса `note-without-*`).
- Рост `AGENTS.md` ровно равен новой секции: 59 550 → 63 530 байт.

## Намеренно не сделано

- Никакой массовой перезаписи существующих правил — ограничение фазы 1 принятого решения.
- Четыре существовавших ранее падения тестов и пять существовавших ранее замечаний ruff в `templates/ai-infrastructure/scripts/code_index.py` зафиксированы, но не исправлены — отдельная забота.
- Фазы 2–9 инициативы остаются открытыми, каждая за собственным фрагментом change plan.

## Контекст для следующей сессии

- Дальше фаза 2: rule traceability — стабильные IDs правил только в source/eval metadata (никогда в рендеренном `AGENTS.md`), связь `rule ↔ source ↔ expected behavior ↔ eval scenarios`. Прежде чем класть IDs во frontmatter фрагментов, проверить, как рендерер обрабатывает frontmatter фрагментов.
- `feature_meta` `2.5.0` должен совпасть с версией следующего релиза (скорректировать на `bump-version` при необходимости).
- Запись фиксации знаний для этой сессии — второй коммит в той же ветке, ожидает согласования текста.

## Наблюдения

- [fact] Feature `rule-engineering` добавляет ровно одну секцию рендера размером 3 980 байт в `AGENTS.md` включившего проекта.
- [fact] Четыре теста в `tests/test_ai_sync.py` хардкодят версию баннера релиза и падают на `main` с релиза 2.4.0; к этому изменению они отношения не имеют.
- [decision] Внешний импорт правил — частный случай Rule Engineering: поток импорта в README проводит каждого кандидата через инженерный поток и требует форму валидации на каждое принятое правило.

## Связи

- implements [[РЕШЕНИЕ: принять инициативу Rule Engineering]]
- relates_to [[Базовая линия: инициатива Rule Engineering (issue #17)]]
- relates_to [[План изменений: инициатива Rule Engineering (issue #17)]]
- localized counterpart of [[17 — Rule Engineering initiative, phases 0–1]]