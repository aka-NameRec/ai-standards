# DECISION: refresh-python-infrastructure-guidance

Англоязычный оригинал: [2026-04-16-refresh-python-infrastructure-guidance.md](2026-04-16-refresh-python-infrastructure-guidance.md)

## Статус

Accepted

## Дата

2026-04-16

## Контекст

В `ai-standards` Python-guidance со временем разросся по нескольким слоям с размытыми границами.

Правила для Python частично жили в `fragments/core/python.md`, а частично в `fragments/stacks/python.md`, из-за чего нарушалась логика слоёв: Python-specific правила оказывались в `core`, тогда как другие language-specific правила, например для TypeScript, уже жили целиком в stack fragments.

Также требовалось доработать baseline-фрагменты для Django и FastAPI. `fragments/stacks/fastapi.md` был слишком тонким для роли общего baseline, а часть Django-guidance смешивала framework-neutral правила с project-specific architectural choices.

Наибольшая неоднозначность возникала в opt-in Django области. `django-drf.md` и `django-save-lifecycle.md` импортировали HackSoft-derived и локальные project patterns так, будто это shared defaults, хотя часть этих правил на самом деле является optional architectural conventions, а не framework baselines.

## Решение

`ai-standards` консолидирует Python-specific guidance в stack fragments и отделяет Django framework baselines от opinionated application-architecture patterns.

Репозиторий удаляет `fragments/core/python.md` и оставляет Python-guidance в `fragments/stacks/python.md` как единственный общий Python baseline.

Репозиторий расширяет `fastapi` до более полноценного framework baseline, делает `django` более нейтральным framework baseline и смягчает `django-drf`, чтобы он больше не выдавал один локальный DRF style за общий shared rule set.

Репозиторий удаляет `django-save-lifecycle` и заменяет его двумя явными opt-in fragments:

- `django-hacksoft-style` для HackSoft-derived service-and-selector architectural style
- `django-save-orchestration` для optional unified `save()` wrapper pattern, включая явное правило использовать `transaction.on_commit`, когда post-save side effects зависят от успешного commit

## Почему

- удерживает `core` сфокусированным на cross-technology engineering rules, а не на language-specific guidance
- упрощает поиск и развитие Python-guidance, потому что он живёт в одном месте
- усиливает FastAPI и Django baselines более устойчивыми official-framework правилами
- не выдаёт локальные или opinionated Django/DRF conventions за universal best practices
- сохраняет полезные architectural patterns, но делает их явными opt-in fragments вместо скрытых defaults

## Рассмотренные альтернативы

### Оставить Python-правила разделёнными между `core/python` и `stacks/python`

Отклонено, потому что это ослабляет модель слоёв и делает Python-guidance труднее для восприятия.

### Оставить `django-save-lifecycle` общим default fragment

Отклонено, потому что он смешивает полезный project-level orchestration pattern с framework-baseline rules и слишком уверенно подаёт одну локальную конвенцию как общую best practice.

### Перенести unified `save()` orchestration в `django.md`

Отклонено, потому что этот паттерн не является Django baseline. Это переиспользуемая architectural convention, которую следует подключать явно и только там, где create/update orchestration в основном симметричен.

## Последствия

### Плюсы

- Python-проекты теперь опираются на один ясный общий Python baseline
- downstream Django-проекты могут явно выбирать между нейтральными framework rules и HackSoft-derived architecture layers
- unified `save()` pattern остаётся переиспользуемым, но не навязывается каждому Django-проекту
- границы между baseline rules и opt-in architecture styles стали понятнее и в коде, и в документации

### Минусы или цена

- репозиторию нужно поддерживать больше stack fragments и связанной документации
- downstream manifests, которые использовали `django-save-lifecycle`, должны переключиться на новые явные stack names, если хотят сохранить тот же style
- командам придётся более явно решать, хотят ли они HackSoft-style layering и unified save orchestration

## Затронутые модули

- `fragments/stacks/python.md`
- `fragments/stacks/django.md`
- `fragments/stacks/fastapi.md`
- `fragments/stacks/django-drf.md`
- `fragments/stacks/django-hacksoft-style.md`
- `fragments/stacks/django-save-orchestration.md`
- `fragments/stacks/django-save-lifecycle.md`
- `registry.toml`
- `README.md`
- `README.ru.md`
- `ai.project.toml`
- `templates/project_manifest.toml`
- `tests/test_ai_sync.py`
- `AGENTS.md`

## Инварианты и ограничения

- Python-specific guidance не должен жить в `core`
- `django.md` и `django-drf.md` должны оставаться baseline-oriented и не скатываться в project-specific style dogma
- HackSoft-derived architecture rules должны быть явными opt-in fragments
- unified `save()` orchestration должен документироваться как optional convention, а не universal best practice
- зависящие от commit side effects в unified `save()` pattern должны использовать `transaction.on_commit`

## Проверка

- Python-guidance корректно рендерится без `core/python`
- `registry.toml` содержит `django-hacksoft-style` и `django-save-orchestration` и больше не содержит `django-save-lifecycle`
- `README.md` и `README.ru.md` показывают новые Django composition examples
- renderer tests покрывают обновлённый Python baseline, смягчённый DRF guidance и новые opt-in Django fragments
- проверки репозитория остаются зелёными

## Связанные артефакты

- [../../fragments/stacks/python.md](../../fragments/stacks/python.md)
- [../../fragments/stacks/django.md](../../fragments/stacks/django.md)
- [../../fragments/stacks/fastapi.md](../../fragments/stacks/fastapi.md)
- [../../fragments/stacks/django-drf.md](../../fragments/stacks/django-drf.md)
- [../../fragments/stacks/django-hacksoft-style.md](../../fragments/stacks/django-hacksoft-style.md)
- [../../fragments/stacks/django-save-orchestration.md](../../fragments/stacks/django-save-orchestration.md)
- [../../registry.toml](../../registry.toml)
- [../../README.md](../../README.md)
- [../../README.ru.md](../../README.ru.md)
