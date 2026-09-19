---
title: 'План изменений: инициатива Rule Engineering (issue #17)'
permalink: ai-standards/artifacts/2026-09-19-rule-engineering-change-plan.ru-1
---

# План изменений: инициатива Rule Engineering (issue #17)

Статус: в работе. Ветка `rules-change/17-rule-engineering`.
Исходный proposal: `docs/archive/20260917-000618-proposal-rule-engineering-skill-engineering-context-architecture-evals.md`.
Принятое решение: `docs/decisions/2026-09-19-adopt-rule-engineering-initiative.ru.md`.
Базовая линия: `docs/artifacts/2026-09-19-rule-engineering-baseline.ru.md`.

## Цель

Сместить `ai-standards` с накопления инструкций на управление их жизненным
циклом и контекстом: единый процесс Rule Engineering для любого нормативного
правила независимо от источника, формальная модель размещения знания, единый
домен Skill Engineering и проверка на уровне поведения — при этом исполняемая
eval-инфраструктура остаётся отдельно, в спецификации `ai-standards-evals`
(issue #18).

## Объём

Пофазно; эта ветка доставляет только фазы 0 и 1:

- Фаза 0 (эта ветка): baseline-артефакт (замеры репозитория, текущее
  review-поведение, сценарии-кандидаты).
- Фаза 1 (эта ветка): новый feature `rule-engineering` — фрагмент
  `process/rule-engineering.md`, запись в реестре с `feature_meta` `2.5.0`,
  usage-гайды (оба языка), render-тест. Поток README `Import External Rules`
  переформулирован как частный случай Rule Engineering. Существующие правила
  массово не переписываются.
- Фаза 2 (позже): rule traceability — стабильные IDs правил только в
  source/eval metadata, поддержка связи `rule ↔ source ↔ expected behavior ↔ scenarios`.
- Фаза 3 (позже): dogfooding Rule Engineering на `standard-code-review`.
- Фаза 4 (позже): feature `context-architecture` с формальной моделью
  размещения; классификация текущего содержимого `AGENTS.md`; migration plan
  без физического переноса.
- Фаза 5 (позже): контракт формата сценариев в `docs/scenarios/`; реализация
  runner относится к #18.
- Фаза 6 (позже): домен `skill-engineering`; `skill-authoring` создаётся через
  Rule Engineering (обязательное dogfooding).
- Фаза 7 (позже): наборы сценариев activation/effect eval для skills.
- Фаза 8 (позже): минификация `AGENTS.md`, каждый перенос — через regression evals.
- Фаза 9 (позже): cross-agent матрица совместимости.

## Вне объёма

- Всё, что отнесено к issue #18: scenario runner, harness-адаптеры,
  исполнение baseline/candidate, cross-agent исполнение.
- Физическая миграция содержимого `AGENTS.md` (фаза 8) и массовая перезапись
  существующих правил (явно исключены из фазы 1).
- Разделение `skill-engineering` на отдельные skills без usage/eval данных.

## Затрагиваемые модули (фазы 0–1, эта ветка)

- `fragments/process/rule-engineering.md` (новый)
- `registry.toml` (feature-запись, `feature_meta` `2.5.0`)
- `docs/rule-engineering-usage.md` + `.ru.md` (новые)
- `docs/artifacts/2026-09-19-rule-engineering-baseline.md` + `.ru.md` (новые)
- `docs/decisions/2026-09-19-adopt-rule-engineering-initiative.md` + `.ru.md` (новые)
- `ai.project.toml` (self-hosting: включение feature)
- `AGENTS.md` (перегенерация)
- `tests/test_ai_sync.py` (render-тест + тест фрагмента)
- `README.md` / `README.ru.md` (группы features, переформулировка `Import External Rules`, секция использования)
- `CHANGELOG.md` (запись в Unreleased)

## Планируемая структура

Фрагмент несёт всегда необходимое нормативное ядро: когда применяется поток,
девять свойств качества правила, понятие interpretation surface, инженерный
поток и принципы размещения. Подробные чек-листы и разобранные примеры живут в
usage-гайдах, чтобы отрендеренная секция оставалась компактной.

## Риски

- Рост фрагмента против экономии контекста — мера: фрагмент держится около
  4 КБ; детали в usage-доках.
- Дублирование с import-потоком README — мера: секция импорта маршрутизирует
  через Rule Engineering, а не повторяет методологию.
- Версионный пин: `feature_meta` указывает на `2.5.0` и должен совпасть с
  версией следующего релиза (корректируется на `bump-version` при
  необходимости).

## Инварианты

- Существующие правила сохраняют поведение; массовой перезаписи в фазе 1 нет.
- Shared policy остаётся vendor-нейтральной; harness-специфичная механика в
  общие правила не попадает.
- Модульный контракт `ai-sync` сохраняется: изменений рендерера нет; новый
  feature — чистый контент поверх существующих входов.
- Рост `AGENTS.md` от этого изменения ограничен новой секцией и ею обоснован.

## Проверки

- `uv run pytest` (включая новые render/fragment тесты)
- `uv run mypy scripts/`
- `uv run ai-sync render --project-root .` идемпотентность (чистое рабочее
  дерево после повторного рендера)
- `uv run ai-sync doctor --project-root .` — ноль ошибок
- Числа baseline воспроизводимы (байты/строки перемеряемы)

## Итог

Заполняется после реализации, если план существенно направлял работу:
фазы 0 и 1 доставлены на этой ветке — baseline зафиксирован; feature
`rule-engineering` поставлен (фрагмент, реестр `2.5.0`, usage-гайды en/ru,
self-hosting включён, render/fragment тесты, согласование README/CHANGELOG,
import flow переформулирован как частный случай Rule Engineering). Фазы 2–9
остаются открытыми со своими будущими артефактами.