---
title: 'Задача 26: реализация issue 26'
permalink: ai-standards/tasks/26-implement-issue-26.ru
---

# Задача 26: реализация issue 26

Локализованная версия: [26-implement-issue-26.md](26-implement-issue-26.md)

## Статус

Реализовано на ветке `rules-change/26-implement-issue-26` по процедуре
`autonomous-task-run` (инструкция пользователя от 2026-10-12: работать
автономно). Запуск завершается финальным коммитом рабочей ветки; слияние в
`main` — которое дополнительно требует сравнения из `ai-standards-evals` по
правилу merge-gate — и отправка ждут явной инструкции человека.

## Объём работ

Все шесть принятых направлений из
[../decisions/2026-10-12-implement-issue-26.md](../decisions/2026-10-12-implement-issue-26.md):

- **D1** — `standard-code-review.procedure.md` переехал в общий
  инфраструктурный шаблон `templates/standard-code-review-procedure.reference.md`,
  разворачиваемый как `.ai-standards/references/standard-code-review-procedure.md`
  (gated на `code-review`); kilo-запись развёртывания удалена, её назначение
  добавлено в `RETIRED_TEMPLATE_DESTINATIONS`; все четыре варианта
  `standard-code-review` и оба указателя во фрагменте ссылаются на общий
  путь; регрессионный тест пришивает критерий «каждая развёрнутая копия
  ссылается на существующий файл» (`scripts/ai_sync.py`, `tests/test_ai_sync.py`).
- **D2** — исключение для автономного запуска добавлено в `core/git-workflow`
  и в пункт «Never» навыка `capture-knowledge` во всех трёх адаптерах;
  отправка остаётся без исключений.
- **D3/D4** — пункт 4 entry gate, шаги 1 и 7 и условие завершения
  `autonomous-task-run` переформулированы во всех трёх адаптерах: фиксация
  знаний следует включённым фичам проекта с отчётом о пропусках, форма ветки
  следует правилам проекта с общим значением по умолчанию;
  `[knowledge_capture] tasks_tree` задокументирован в
  `templates/project_manifest.toml`; фрагмент `knowledge-capture` и адаптеры
  `capture-knowledge` ссылаются на настраиваемый каталог задачных записей;
  `rule_map.toml` обновлён (`ATR-001`, `ATR-006`, `ATR-007` переформулированы,
  добавлен `ATR-008`), инвариантные тесты пришивают новые формулировки.
- **D5** — `fragments/tools/basic-memory.md` снимает только требования к телу
  канонической заметки и больше не содержит висячей ссылки «see Project Memory».
- **D6** — у `ai-sync sync-templates` появился `--plan` (вычисление плана
  вынесено в `_plan_agent_template`/`plan_project_templates`/
  `_plan_retired_templates`); шаг 5 процедуры обновления `update-ai-standards`
  во всех трёх адаптерах выполняет префлайт и требует подтверждения для новых
  файлов навыков и рабочих процессов; `docs/standards-update-usage.md`/`.ru.md`
  обновлены; добавлены три теста режима плана (создание без записи,
  актуальность после применения, вывод отставшего без удаления).
- CHANGELOG `[Unreleased]` дополнен записями Fixed/Changed.

Коммиты: `477ce5f` (запись решения), `3a179d8` (D1), `d85412c` (D2),
`fe72cdb` (D3/D4), `e616c48` (D5), `9f2815b` (D6) и настоящая запись.

## Проверки

- `uv run pytest`: 157 пройдено.
- `uv run mypy scripts/`: чисто.
- `uv run ai-sync render --project-root .`: идемпотентно.
- `uv run ai-sync doctor --project-root .`: ноль ошибок (существующие
  предупреждения не изменились).
- Живой смоук режима плана: `--plan` на пробном проекте перечисляет строки
  `Planned create` без записи; применение создаёт их; повторный `--plan`
  сообщает полную актуальность.
- Известный ранее долг по линту, задачей не затронут: `ruff check .` даёт
  6 ошибок в `templates/ai-infrastructure/scripts/code_index.py` и 1 `E501`
  в `tests/test_ai_sync.py`; на базовом коммите — те же.
- Не выполнялось (условие слияния, а не часть этого среза): сравнение из
  `ai-standards-evals`, требуемое правилом merge-gate для веток,
  затрагивающих `fragments/**`/`templates/**`.

## Связанные артефакты

- [../decisions/2026-10-12-implement-issue-26.md](../decisions/2026-10-12-implement-issue-26.md)
- [26-verified-user-feedback-2-8-1.md](26-verified-user-feedback-2-8-1.md)
- Исходный запрос: aka-NameRec/ai-standards issue #26

## Наблюдения

- [fact] Реализация меняла только тексты правил, таблицы развёртывания и
  скрипт синхронизации; контракты сценариев eval не переписывались, а
  eval-сравнение остаётся открытым условием слияния.
- [fact] Режим плана использует то же вычисление содержимого, что и
  применение, поэтому план и применение не могут разойтись.

## Связи

- implements [[РЕШЕНИЕ: реализация issue 26]]
- relates_to [[Задача 26: верифицированный отзыв пользователя о 2.8.1]]
- localized counterpart of [[Task 26: implement issue 26]]
