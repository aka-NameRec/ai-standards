---
title: 'DECISION: add-autonomy-boundaries-feature'
permalink: ai-standards/decisions/2026-04-18-add-autonomy-boundaries-feature.ru
---

# DECISION: add-autonomy-boundaries-feature

Англоязычный оригинал: [2026-04-18-add-autonomy-boundaries-feature.md](2026-04-18-add-autonomy-boundaries-feature.md)

## Статус

Accepted

## Дата

2026-04-18

## Контекст

`ai-standards` уже продвигал design-first collaboration, reasoning hygiene и lightweight structured artifacts, но пока не задавал переиспользуемую policy о том, когда агент обязан остановить автономное выполнение и запросить human verification.

Этот пробел особенно заметен в более длинных agentic-сессиях. Существующие правила помогали проектам фиксировать intent, boundaries и invariants, но не разделяли явно:

- checkpoint, где агенту нужно согласование человека для нового design direction
- checkpoint, где направление не изменилось, но накопленная architecture delta уже слишком велика, чтобы продолжать без review

Репозиторию был нужен общий process feature для таких stop conditions без навязывания тяжёлого workflow всем проектам по умолчанию.

## Решение

`ai-standards` добавляет `autonomy-boundaries` как opt-in process feature.

Feature определяет:

- длинную автономию как исключение, а не default workflow
- обязательные предпосылки для bounded autonomous execution
- явные stop conditions для design ambiguity, architecture drift, widening scope и non-converging verification
- чувствительные области, где autonomous design decisions запрещены без human approval
- ожидания к review artifacts в конце длинного автономного прогона

Репозиторий хранит эту policy в `process/`, а не в `core/`, чтобы downstream-проекты подключали более строгие autonomy guardrails явно.

## Почему

- даёт переиспользуемый ответ на вопрос "когда агент обязан остановиться?"
- отделяет execution autonomy от autonomous design choice
- делает review архитектурной дельты явным понятием наряду с review направления
- соответствует курсу репозитория на lightweight, Git-reviewable process rules
- избегает хрупких числовых порогов как shared defaults

## Рассмотренные альтернативы

### Расширить только `design-first-collaboration`

Отклонено, потому что одного дополнительного bullet недостаточно, чтобы ясно выразить session envelopes, sensitive areas, review outputs и политику stop conditions.

### Перенести весь policy в `core`

Отклонено, потому что не каждому downstream-проекту по умолчанию нужен одинаковый уровень autonomy governance, а репозиторий уже использует opt-in process features для более строгих workflow-правил.

### Стандартизовать обязательный файл вроде `SESSION_ENVELOPE.md`

Отклонено, потому что устойчивую ценность несёт содержание session envelope, а не единое имя файла для всех репозиториев. Проектам нужно оставить локальную гибкость в хранении этого артефакта.

## Последствия

### Плюсы

- downstream-проекты могут явно подключить понятную shared policy по автономии
- длинные автономные сессии теперь имеют явные stop conditions в shared standards
- и direction checkpoints, и architecture-delta checkpoints названы и задокументированы
- self-hosted репозиторий может применять ту же policy через собственный manifest

### Минусы или цена

- в репозитории появляется ещё один process feature и пара usage guides
- downstream-проектам придётся явно решать, нужен ли им такой уровень governance
- некоторым проектам всё равно потребуются более строгие локальные правила для числовых лимитов, operational risk или approval workflow

## Затронутые модули

- `registry.toml`
- `fragments/process/autonomy-boundaries.md`
- `fragments/process/design-first-collaboration.md`
- `fragments/process/structured-artifacts.md`
- `README.md`
- `README.ru.md`
- `ai.project.toml`
- `AGENTS.md`
- `tests/test_ai_sync.py`

## Инварианты и ограничения

- длинная автономная работа остаётся запрещённой по умолчанию
- design choice и execution должны оставаться разными вещами
- shared standards не должны продвигать хрупкие числовые пороги как универсальные defaults
- содержание session envelope важнее, чем любое конкретное имя файла
- human review должно оставаться дешевле, чем reverse-engineering скрытого прогона

## Проверка

- `registry.toml` содержит feature `autonomy-boundaries`
- рендеринг включает новый process fragment, когда feature подключён
- usage guides существуют на английском и русском
- README документирует feature на обоих языках
- self-hosted `AGENTS.md` успешно рендерится с включённым feature

## Связанные артефакты

- [../autonomy-boundaries-usage.md](../autonomy-boundaries-usage.md)
- [../autonomy-boundaries-usage.ru.md](../autonomy-boundaries-usage.ru.md)
- [../../fragments/process/autonomy-boundaries.md](../../fragments/process/autonomy-boundaries.md)
- [../../ai.project.toml](../../ai.project.toml)