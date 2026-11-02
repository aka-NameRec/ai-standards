---
title: '29 — AGENTS.md: progressive disclosure (reference-режим)'
permalink: ai-standards/tasks/29-progressive-disclosure.ru
---

# 29 — AGENTS.md: progressive disclosure (reference-режим)

Английская версия: [29-progressive-disclosure.md](29-progressive-disclosure.md)

Дата: 2026-11-02 · Ветка: `rules-change/29-progressive-disclosure` (коммиты `e73acc9`, `067eaaf`, `9db45d5`, `7849022`, `ce96721` плюс релизный набор изменений, в котором поставляется эта запись; не отправлена — push требует явного одобрения пользователя)

## Триггер

Пользователь сообщил, что отрендеренные `AGENTS.md` превышают бюджет Codex в 32 KiB на проектные доки, и принял дизайн progressive disclosure, обсуждённый 2026-11-02 (issue #29): reference-режим рендеринга для стеков и тяжёлых фич с инлайн-поведенческим ядром. Каноническое решение: [docs/decisions/2026-11-02-add-agents-md-progressive-disclosure.ru.md](../decisions/2026-11-02-add-agents-md-progressive-disclosure.ru.md); исполнение шло автономно по [docs/artifacts/2026-11-02-reference-mode-rendering-change-plan.ru.md](../artifacts/2026-11-02-reference-mode-rendering-change-plan.ru.md).

## Что сделано

- **Рендерер**: списки `reference_features` / `reference_stacks` в манифесте (имена должны оставаться заказанными и быть capability-списку реестра); сборка pointer-блоков с токеном `{{REFERENCE_PATH}}`; управляемый деплой очищенных от provenance тел фрагментов в `.ai-standards/references/{stacks,features}/<name>.md` (мультифрагментные наборы конкатенируются в порядке реестра); нефатальное предупреждение о бюджете 32 768 байт в `render`/`update`/`check`; вырезка комментариев `Source provenance` и `Source: <url>` из рендера; байт-идентичная обратная совместимость без новых ключей.
- **Контент**: 30 pointer-блоков — 8 reference-фич и все стековые фрагменты.
- **Трассируемость**: `RD-001`/`RD-002` в `rule_map.toml`; контракты сценариев `RD-101`–`RD-108`, `RD-110`, `RD-111`, `RD-120` (EN/RU) в `docs/scenarios/`.
- **Саморазвертывание**: манифест переключён на reference-режим; отрендеренный `AGENTS.md` 56.8K → 31.3K, внутри бюджета Codex без предупреждения; девять reference-документов развёрнуты.
- **Eval-покрытие (STD-CHANGE-0005 в `ai-standards-evals`)**: фикстуры и скореры для RD-сюита (оракул активации по трассировке tool-событий kilo) и раннер матрицы RD-120; релизный отчёт `reports/20261102-release-2-9-0-candidate/release-report.json` — PASS, 27 сценариев, два задокументированных исключения.

## Проверки

- `uv run pytest` 170 passed, `uv run mypy scripts/` и `uv run ruff check scripts/` чистые; рендер идемпотентен; `ai-sync check` актуален; `ai-sync doctor` без ошибок.
- Поведенческие: RD-сюит 10/10 PASS; матрица RD-120 24/24 PASS на этой ревизии (STD-CHANGE-0005).
- Регресс на этой ревизии: CR-001..012, BM-001/002, PM-001, ATR-001 PASS; CR-010 упал один раз на форме отчёта и прошёл на повторе (единичная вариативность модели, waived в релизном отчёте); TRG-001 12/12; TRG-003 10/11 — совпадение с задокументированным базовой линией false positive.
- ATR-002 падает на этой ревизии И идентично на выпущенном пине 2.8.1 (промах «коммит в main» внутри в остальном корректной остановки на противоречии) — pre-existing, waived в релизном отчёте, отслеживается как follow-up в `ai-standards-evals`.

## Намеренно не сделано

- Никакой поставки reference-контента через скиллы (зависящая от агента активация) — вернуться после верификации активации скиллов на Codex/omp.
- Никаких вложенных per-directory `AGENTS.md`; никаких изменений бюджета Codex или существующих skill-пакетов.
- Слияние в `main`, тег `2.9.0-2026-11-02` и push ждут явного одобрения пользователя; обновление пина в `ai-standards-evals` следует за выпущенным тегом.

## Наблюдения

- [fact] Тяжёлый reference-заказ рендерится в 30 435 байт, средний — в 19 221 байт, оба под бюджетом Codex в 32 768 байт.
- [decision] Reference-файлы наборов — единые конкатенированные документы, а не пофрагментные файлы: путь в pointer-блоке стабилен по заказанному имени.

## Связи

- implements [[DECISION: add-agents-md-progressive-disclosure]]
- relates_to [[Модульный контракт: scripts/ai_sync.py]]
