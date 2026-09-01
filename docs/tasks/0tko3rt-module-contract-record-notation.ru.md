---
title: 0tko3rt — Нотация записей модульных контрактов
permalink: ai-standards/tasks/0tko3rt-module-contract-record-notation.ru
---

# 0tko3rt — Нотация записей модульных контрактов

Английский источник истины: [0tko3rt-module-contract-record-notation.md](0tko3rt-module-contract-record-notation.md)

Дата: 2026-09-01 · Ветка: `feature/0tko3rt-module-contract-notation` · Обращение пользователя: [#10](https://github.com/aka-NameRec/ai-standards/issues/10)

## Триггер

Обращение пользователя #10: в двух разных проектах агент, попросенный создать модульный контракт, писал корневой `MODULE_CONTRACT.md` вместо записи в `docs/architecture/**` и без frontmatter `title`, который требует Basic Memory. Проверено по исходникам: секция `Module Contracts` буквально предписывала «Create MODULE_CONTRACT.md only for major, risky, shared, or architecturally non-obvious modules», корневой файл стоял первым в списке канонических источников discovery gate и в перечнях канонической документации (`structured-artifacts`, `basic-memory`), а ни одно правило не называло нотацию и место хранения контрактов. Отказ был системным — формулировки, а не поведение агентов.

## Что сделано

- **Decision record** `docs/decisions/2026-09-01-module-contract-record-notation.md` (+ `.ru.md`): модульный контракт — одна запись `YYYY-MM-DD-module-contract-<module-slug>.md` в `docs/architecture/**` с frontmatter `title` и `type: module-contract`; одна запись — один контракт; корневой `MODULE_CONTRACT.md` — legacy-форма: распознаётся, не создаётся. Отклонённые альтернативы: отдельный `docs/contracts/**`, сохранение корневого файла как целевого, маркировка только тегами. Маркер классификации — тип во frontmatter, а не имя файла: decision records о контрактах тоже несут `module-contract` в slug.
- **Фрагменты**: `structured-artifacts` — секция Module Contracts переписана на запись; `MODULE_CONTRACT.md` убран из перечня канонических артефактов. `module-contract-gate` — записи первыми в Canonical Source, корневой файл помечен legacy; дешёвая проверка в Task Start ищет `docs/architecture -g '*module-contract*'`; шаблон сканирования включает `type: module-contract`. `basic-memory` — перечень канонических артефактов обновлён. `code-review` — проход Architecture & Conventions ищет контракты по маркеру записи.
- **Шаблоны**: `module-contract.md` несёт frontmatter записи; три адаптера `standard-code-review` и пример отчёта цитируют путь записи; три адаптера `capture-knowledge` создают записи.
- **Tooling**: `ai-sync doctor` сообщает о корневом `MODULE_CONTRACT.md` (корень репозитория или корень дерева знаний) предупреждением `legacy-module-contract-location`; только сообщение, без автопереноса — перенос заметки это переименование, а переименования требуют решения.
- **Этот репозиторий перенесён на собственное правило**: `docs/MODULE_CONTRACT.md` (+ `.ru.md`) переехали в `docs/architecture/2026-09-01-module-contract-ai-sync.md` (+ `.ru.md`), добавлен `type: module-contract`, permalinks сохранены.
- **Документация**: usage-гиды (`structured-artifacts`, `basic-memory`, `code-review`, `conport`, en+ru) переведены на нотацию записей; в CHANGELOG добавлена секция `Unreleased`.

## Проверки

106 тестов пройдено (формулировка Module Contracts в рендере, обновлённые проверки фрагмента и шаблона code review на `type: module-contract` и форму цитирования записи, новые тесты doctor: legacy-размещения отмечаются в обоих корнях, корректная запись принимается, legacy-имя по-прежнему вне проверки имён); `mypy` и `ruff` чисты; рендер идемпотентен; `ai-sync check` проходит; `doctor` — 0 ошибок и те же 168 предупреждений, что на `main`, — новых находок нет, в том числе для новых и переименованных файлов.

## Намеренно не сделано

- Исторические документы не тронуты: `docs/tasks/**`, `docs/archive/**`, прошлые записи CHANGELOG и документы-предложения сохраняют формулировки с `MODULE_CONTRACT.md` как историю.
- Без подъёма версии: подготовка релиза (пин в манифесте, тег) — отдельный шаг; CHANGELOG несёт секцию `Unreleased`.
- Корневые `MODULE_CONTRACT.md` в downstream-проектах не переносятся автоматически — doctor указывает на дом записей; перенос остаётся решением каждого проекта.

## Контекст следующей сессии

- Проекты, принявшие ai-standards, получают новые формулировки при следующем обновлении стандартов; подъём пина — на каждом проекте отдельно.
- Предупреждение doctor в downstream-проекте — ожидаемый миграционный сигнал, а не регрессия.

## Observations

- [fact] Корневая причина issue #10 — формулировка, называвшая ровно один артефакт, корневой файл, без места и нотации, поэтому литеральное прочтение побеждало в двух проектах.
- [decision] Модульный контракт — запись `YYYY-MM-DD-module-contract-<module-slug>.md` в `docs/architecture/**` с frontmatter `title` и `type: module-contract`.
- [decision] Корневой `MODULE_CONTRACT.md` — legacy: распознаётся и читается при discovery и ревью, не создаётся, doctor сообщает кодом `legacy-module-contract-location`.
- [fact] Точный маркер классификации — тип во frontmatter, а не имя файла: decision records о контрактах тоже несут `module-contract` в slug.

## Relations

- relates_to [[РЕШЕНИЕ: module-contract-record-notation]]
- relates_to [[РЕШЕНИЕ: module-contract-gate-feature-placement]]
- relates_to [[Модульный контракт: scripts/ai_sync.py]]
- localized counterpart of [[0tko3rt — Module Contract Record Notation]]
