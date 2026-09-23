---
title: 18 — Фаза 8: перемещения M1–M3 и релизный гейт верификации
permalink: ai-standards/tasks/18-phase-8-m1-m2-m3-and-eval-gate-ru
---

# 18 — Фаза 8: перемещения M1–M3 и релизный гейт верификации

Английская версия: [18-phase-8-m1-m2-m3-and-eval-gate.md](18-phase-8-m1-m2-m3-and-eval-gate.md)

Дата: 2026-09-23 · Ветки: `rules-change/18-m1-skill-reference-procedure`,
`rules-change/18-m2-gate-reference`, `rules-change/18-m3-prose-compression`,
`rules-change/18-m3-retry` (все слиты в `main` и запушены; M3 один раз
отвергнут eval-гейтом и повторно внесён с дословным сохранением буллета
строки версии)

## Триггер

Фаза 8 плана миграции Context Architecture: три перемещения (M1–M3), каждое
под гейтом поведенческого сравнения baseline vs candidate из
`ai-standards-evals`. Перемещение без успешного сравнения отклоняется.

## Что сделано

- **M1** (`34baa19`): пасс-процедура code review и fixing-политика переехали
  из always-loaded фрагмента в
  `templates/code-review/standard-code-review.procedure.md`, развёртываемую
  через `ai-sync sync-templates` как `references/procedure.md` навыка
  `standard-code-review`. Фрагмент сохраняет инварианты отчёта
  (доказательность, no-padding, семантику маркеров, форму отчёта, роутинг
  триггера и scope) и компактные указатели; заголовки секций сохранены для
  `rule_map.toml`.
- **M2** (`7e19573`): деталь Module Contract Discovery Gate (команды
  discovery, критерии покрытия, ограничения reasoning, shape индексных
  записей, контракт репортинга) переехала в
  `templates/module-contract-gate.procedure.md`, развёртываемую как
  `.ai-standards/references/module-contract-gate.md` по фиче
  `module-contract-gate`. Фрагмент сохраняет мандат, канонические источники,
  сжатый роутинг и гарантии, закреплённые
  `test_module_contract_gate_fragment_keeps_its_guarantees`.
- **M3** (`293da96` отвергнут → `515f464` принят): проза-компрессия
  перечислений Report Shape. Первая попытка потеряла мотивировку строки
  версии, и агент вовсе опустил `ai-standards <version>` в CR-006 — гейт
  отверг перемещение. Повтор сохранил буллет строки версии дословно;
  гарантия-тест
  (`test_code_review_fragment_keeps_the_version_line_guarantee`) теперь
  закрепляет строку, её fallback и мотивировку против будущих компрессий.
- **Правило merge-гейта** (`b4d5b92`): ветка, изменяющая `fragments/**` или
  `templates/**`, сливается в `main` только с приложенным eval-сравнением
  (baseline vs candidate, включая LLM-судью); слияние без вердикта ACCEPT —
  только по явному решению пользователя.
- **Релизный гейт** (`fedb274`): `bump-version tag --evals-report
  <release-report.json>` проверяет отчёт поведенческой верификации (kind,
  вердикт PASS, совпадение ревизии с именем тега, `main`, HEAD или явным
  override) до создания тега; задокументировано в Release Workflow (EN/RU),
  `AGENTS.md` перерендерен.
- `AGENTS.md`: 64 591 → 62 104 байт по M1–M3, все гейты пройдены.

## Верификация

- Каждое перемещение под гейтом: набор из 9 сценариев на ветке кандидата,
  сравнение с предыдущей принятой ревизией, LLM-судья (GLM-5.3) по глубине
  находок для CR-001/004/005/006 — отчёты в `ai-standards-evals`
  (`20260922-20*`, `20260923-*`). Одна калибровка судьи: rubric CR-005
  ошибочно запрещала ссылку на существующий модуль `src/rows.py`.
- Полный набор: 146–147 passed на каждом кандидате; `ai-sync render`
  идемпотентен; `ai-sync doctor` без ошибок.
- Cross-agent (начало Phase 9): колонка Codex матрицы — 9/9 PASS на
  `ai-standards@main` (gpt-5.6-luna); зафиксировано в README и отчётах
  репозитория `ai-standards-evals`.

## Заметки

- Предпосылка M1 «активация навыка подтверждена на двух harness» не
  выполнена (локально только Kilo; Codex добавлен позже для матрицы) —
  отклонение зафиксировано в сообщении коммита M1, eval-гейт выполнен на
  одном harness.
- `AGENTS.md` сохраняет поведение по свидетельству гейтов, а не по замыслу:
  каждое перемещение и компрессия верифицированы на записанных сценариях.

## Связи

- implements [[РЕШЕНИЕ: принять инициативу Rule Engineering]]
- relates_to [[Спецификация: репозиторий ai-standards-evals (issue #18)]]
- localized counterpart of [[18 — Phase 8: M1–M3 relocation and the release verification gate]]
