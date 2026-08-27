---
title: 'DECISION: extract-layered-architecture-and-merge-django-style'
permalink: ai-standards/decisions/2026-04-16-extract-layered-architecture-and-merge-django-style.ru
---

# DECISION: extract-layered-architecture-and-merge-django-style

Русская локализованная версия. Англоязычный оригинал: [2026-04-16-extract-layered-architecture-and-merge-django-style.md](2026-04-16-extract-layered-architecture-and-merge-django-style.md)

## Статус

Принято

## Дата

2026-04-16

## Контекст

В `ai-standards` уже существовал небольшой cross-stack фрагмент `core/architecture` и несколько stack-specific архитектурных фрагментов, но отсутствовали переиспользуемые stack fragments именно для слоистой архитектуры.

Этот пробел создавал две проблемы:

- downstream manifests приходилось описывать layered architecture косвенно или вручную перечислять пересекающиеся stack names
- HackSoft-derived opt-in guidance для Django была разделена между `django-hacksoft-style` и `django-service-layer`, хотя оба стека описывали одно и то же семейство service-and-selector архитектуры на разном уровне детализации

Репозиторий при этом уже опирался на stack composition через aliases в `registry.toml`, как видно по существующим compatibility aliases `java-spring` и `vue-query`.

## Решение

Репозиторий вводит три переиспользуемых архитектурных стека:

- `layered-architecture`
- `backend-layered-architecture`
- `frontend-layered-architecture`

Репозиторий сливает прежний `django-hacksoft-style` в `django-service-layer` и удаляет отдельный фрагмент и stack name `django-hacksoft-style`.
Дополнительно репозиторий удаляет отдельный stack `django-naming` и оставляет внутри `django-service-layer` только то naming rule, которое естественно относится к HackSoft-derived service-and-selector style.

`django-service-layer` остаётся явным opt-in architectural style и сохраняет внутри самого фрагмента ссылку на первоисточник HackSoft и соответствующее framing.

Зависимость стека выражается через уже существующую композицию в `registry.toml`, а не через новый механизм зависимостей фрагментов или манифеста. Теперь `django-service-layer` разворачивается в:

- `stacks/layered-architecture`
- `stacks/backend-layered-architecture`
- `stacks/django-service-layer`

## Почему

- даёт слоистой архитектуре переиспользуемый cross-stack vocabulary без переноса этих правил в `core`
- позволяет держать backend- и frontend-layering guidance достаточно раздельными и логически цельными
- упрощает композицию downstream `ai.project.toml` для Django-проектов
- убирает раздвоение, при котором один Django architectural style имел два пересекающихся stack names
- убирает лишний Django stack, полезное правило которого уже принадлежало тому же архитектурному стилю
- сохраняет важное opt-in и HackSoft-derived framing вместо размывания его внутри generic Django guidance

## Рассмотренные альтернативы

### Добавить отдельный dependency mechanism в `ai.project.toml`

Отклонено, потому что композиция через `registry.toml` уже выражает зависимости стеков с меньшей сложностью.

### Оставить и `django-hacksoft-style`, и `django-service-layer`

Отклонено, потому что пересечение между ними достаточно велико, чтобы делать downstream composition шумной, а различие между именами неочевидным для большинства пользователей.

### Перенести layered architecture rules в `core/architecture`

Отклонено, потому что backend-specific и frontend-specific guidance сделают `core` менее сфокусированным и менее переиспользуемым.

## Последствия

### Плюсы

- downstream projects могут явно подключать общие правила слоистой архитектуры
- Django-проекты получают один более ясный opt-in stack для HackSoft-derived service-and-selector style
- репозиторий использует одну консистентную модель композиции на базе stack aliases в `registry.toml`

### Издержки и компромиссы

- репозиторий поддерживает больше явных архитектурных фрагментов
- downstream manifests, которые ссылались на `django-hacksoft-style`, должны переключиться на `django-service-layer`
- downstream manifests, которые ссылались на `django-naming`, должны убрать этот stack entry
- некоторые старые decision records и chat logs останутся историческими снимками прежнего нейминга

## Затронутые модули

- `fragments/stacks/layered-architecture.md`
- `fragments/stacks/backend-layered-architecture.md`
- `fragments/stacks/frontend-layered-architecture.md`
- `fragments/stacks/django-service-layer.md`
- `fragments/stacks/django-hacksoft-style.md`
- `fragments/stacks/django-naming.md`
- `registry.toml`
- `README.md`
- `README.ru.md`
- `tests/test_ai_sync.py`

## Инварианты и ограничения

- `django-service-layer` должен оставаться opt-in architectural style, а не Django baseline
- ссылка на источник HackSoft и provenance должны оставаться видимыми в `django-service-layer`
- зависимости стеков должны и дальше выражаться через композицию в `registry.toml`, а не через новый manifest DSL
- общее layered architecture guidance должно оставаться отделённым от backend-specific и frontend-specific concretization

## Проверка

- `registry.toml` содержит новые stack names для layered architecture
- `registry.toml` больше не содержит `django-hacksoft-style`
- `registry.toml` больше не содержит `django-naming`
- `django-service-layer` рендерит вместе общую layered architecture, backend layering и Django-specific service-layer guidance
- `README.md` и `README.ru.md` документируют новые stack names и обновлённую Django composition
- renderer tests покрывают новую композицию

## Связанные артефакты

- [../../fragments/stacks/layered-architecture.md](../../fragments/stacks/layered-architecture.md)
- [../../fragments/stacks/backend-layered-architecture.md](../../fragments/stacks/backend-layered-architecture.md)
- [../../fragments/stacks/frontend-layered-architecture.md](../../fragments/stacks/frontend-layered-architecture.md)
- [../../fragments/stacks/django-service-layer.md](../../fragments/stacks/django-service-layer.md)
- [../../registry.toml](../../registry.toml)
- [../../README.md](../../README.md)
- [../../README.ru.md](../../README.ru.md)