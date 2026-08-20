<h2>Оглавление</h2>

- [Коммит и стандартное слияние новой документации в main](#коммит-и-стандартное-слияние-новой-документации-в-main)
- [Коммит и продолжение работы](#коммит-и-продолжение-работы)
- [Рекомендации по обновлению правил Python на основе best practices](#рекомендации-по-обновлению-правил-python-на-основе-best-practices)
- [Внести согласованные изменения в проект](#внести-согласованные-изменения-в-проект)
- [Коммит по задаче 0tdk1bp и стандартное слияние ветки](#коммит-по-задаче-0tdk1bp-и-стандартное-слияние-ветки)
- [Выполнить коммит и продолжить](#выполнить-коммит-и-продолжить)
- [Предложения по верификации и обновлению правил Django и FastAPI](#предложения-по-верификации-и-обновлению-правил-django-и-fastapi)
- [Усиление django.md и расширение fastapi.md без перехода к спорным фрагментам](#усиление-djangomd-и-расширение-fastapimd-без-перехода-к-спорным-фрагментам)
- [Перенос фундаментальных Python правил из core в stacks/python](#перенос-фундаментальных-python-правил-из-core-в-stackspython)
- [Перенести Python правила в stacks/python](#перенести-python-правила-в-stackspython)
- [Коммит по задаче 0tdk1sa для обновления Python стека и возврат к спорным правилам](#коммит-по-задаче-0tdk1sa-для-обновления-python-стека-и-возврат-к-спорным-правилам)
- [Объединение обновления Python стека и спорных правил в один коммит](#объединение-обновления-python-стека-и-спорных-правил-в-один-коммит)
- [Коммит и подробный разбор спорных решений в django-drf и django-save-lifecycle](#коммит-и-подробный-разбор-спорных-решений-в-django-drf-и-django-save-lifecycle)
- [Изменения в django-drf и верификация HackSoft подхода и unified save в Django](#изменения-в-django-drf-и-верификация-hacksoft-подхода-и-unified-save-в-django)
- [Фиксация on\_commit в правилах и выделение опциональных HackSoft и unified save фрагментов](#фиксация-on_commit-в-правилах-и-выделение-опциональных-hacksoft-и-unified-save-фрагментов)
- [Структура новых opt-in фрагментов и судьба django-save-lifecycle](#структура-новых-opt-in-фрагментов-и-судьба-django-save-lifecycle)
- [Размещение unified save как архитектурной конвенции вне базовых Django правил](#размещение-unified-save-как-архитектурной-конвенции-вне-базовых-django-правил)
- [Реализовать согласованную схему](#реализовать-согласованную-схему)

## Коммит и стандартное слияние новой документации в main

**Question**

(0tdk1bp) Привет! 🙂
Давай вернёмся в проект ai-standards, и добавим новые файлы под управление Git. там появился новый файл в `docs`.
Давай выполним commit на ветке `feature/0tdk1bp-log-tyescript_and_versioning` и сольём его в `main` по стандарту.

**Answer**

Перехожу в `ai-standards`, сначала подниму правила целевого репозитория и его ConPort, затем проверю git-статус и подготовлю commit по локальному workflow.

Использую навыки `commit-on-branch` и `merge-by-standard`: workflow подходит напрямую. Сейчас дочитаю `AGENTS.md` у `ai-standards`, загружу ConPort и проверю состояние ветки и изменений, чтобы предложить точный commit message.

Контекст восстановлен. В `ai-standards` сейчас `main` защищённая и на ней есть один неотслеживаемый файл `docs/0tdiwfc-log-typesctipt_and_versioning_support.md`, так что прямой commit делать нельзя.

План:
1. Проверить, существует ли ветка `feature/0tdk1bp-log-tyescript_and_versioning`.
2. Если нет, создать её от текущего `main`.
3. Под управление Git взять только новый файл из `docs`.
4. Показать точный commit message и дождаться вашего подтверждения.
5. После подтверждения сделать commit, затем fast-forward merge в `main` и удалить рабочую ветку, если merge пройдет без конфликтов.

Проверил содержимое нового файла: это log-документ из чата, он подпадает под исключение `docs/*-log-*` и не требует парной локализации. Сейчас уточню состояние целевой ветки и подготовлю точный commit message без лишних файлов.

Есть одно несоответствие, которое я не буду самовольно исправлять: имя ветки содержит task id `0tdk1bp`, а новый файл в `docs` содержит `0tdiwfc`. Для git-flow это не блокер, потому что вы явно задали целевую ветку, но commit message я тогда привяжу к `0tdk1bp`.

Создаю рабочую ветку от текущего `main` и возьму под staging только этот новый файл, без прочих изменений.

Ветка создана, staged только один новый файл из `docs`. Перед commit фиксирую точный текст сообщения и жду ваше подтверждение, как требует workflow репозитория.

Подготовлено к commit на ветке `feature/0tdk1bp-log-tyescript_and_versioning`: в staging только `docs/0tdiwfc-log-typesctipt_and_versioning_support.md`.

Предлагаю commit message:
```text
0tdk1bp. (docs) add typescript and versioning support chat log.
```

Если подтверждаете этот текст, я сразу сделаю commit и затем солью ветку в `main` по стандарту.

## Коммит и продолжение работы

**Question**

Да, отлично. Выполняй commit и продолжай.

**Answer**

Делаю commit с подтверждённым сообщением, затем переключусь на `main`, выполню merge и удалю рабочую ветку, если fast-forward пройдет чисто.

Commit прошёл. Проверяю получившийся commit, затем выполняю стандартное слияние в `main` и уберу рабочую ветку после merge.

Сейчас `main` локально уже был на 1 commit впереди `origin/main`; это не мешает merge, но фиксирую состояние явно. Делаю merge из рабочей ветки в локальный `main`, после чего проверю итоговый `HEAD` и удалю source branch.

Merge выполнен fast-forward. Остался финальный шаг workflow: удалить рабочую ветку и зафиксировать итоговое состояние `main`.

Commit и merge завершены по стандарту.

Создан commit `1a8e24d` с сообщением `0tdk1bp. (docs) add typescript and versioning support chat log.` Затем ветка `feature/0tdk1bp-log-tyescript_and_versioning` была слита в `main` через fast-forward и удалена. Сейчас `HEAD` на `main` указывает на `1a8e24d`.

Текущее состояние репозитория чистое, а локальный `main` находится `ahead 2` относительно `origin/main`, то есть оба локальных commit пока не опубликованы. Если нужно, следующим шагом могу запушить `main` в `origin`.

## Рекомендации по обновлению правил Python на основе best practices

**Question**

(0tdk1jk) Отлично!
Теперь смотри: ранее мы использовали репозиторий https://github.com/PatrickJS/awesome-cursorrules как источник для заимствования правил для разработки в разных стеках, но после недавнего импорта правил для TypeScript я обнаружил, что мы себя ограничивам, если рассматривам только этот источник.
Я хотел бы обновить набор правил для всех стеков, основываясь на твоих знаниях, официальной документации и рекомендациях, а также на базе лучших практик.
Цель: создать для стеком набор устоявшихся, не вызывающих сомнений правил, а также учесть лучшие практики, которые будут подталкивать агента и человека к созаднию качественных решений.

(0tdk1sa) Предлагается начать с Python.
Что бы ты мог рекомендовать в части дополнений/переработки существующих правил?

**Answer**

Сначала посмотрю текущий Python stack в `ai-standards`, чтобы рекомендации были привязаны к существующим правилам и не дублировали уже принятое.

Текущий `stacks/python.md` очень короткий, а часть Python-правил уже размазана по `core/python.md`. Добираю этот слой, чтобы отделить общие инженерные правила от действительно stack-level рекомендаций для Python.

Теперь добираю первичные источники: Python docs и PEP, чтобы рекомендации были не вкусовыми, а опирались на официальный baseline языка и стандартной библиотеки.

Я бы начал не с простого расширения текущего `Python Stack`, а с его переразделения. Сейчас в `ai-standards` Python-правила слишком тонкие на уровне stack и частично смешаны с локальными tooling-предпочтениями в `core/python.md`. Для общего стандарта это слабое место: язык, типизация, границы модулей и работа с runtime-ошибками должны жить отдельно от репозиторных предпочтений вроде `Typer`, `plumbum`, `uv run ruff`, `mypy`, `pytest`.

То, что я бы рекомендовал для Python, можно свести к трём группам: что сохранить, что перенести, и что добавить.

**Что сохранить**
- `Respect repository-local tooling and module layout.`
- `Favor explicit domain models and typed interfaces.`
- `Keep application wiring separate from business logic.`

Это хорошие, устойчивые правила. Они не спорные и хорошо переживают переход между FastAPI, Django, CLI, batch jobs и библиотеками.

**Что я бы вынес из shared Python baseline**
- `Prefer Typer for CLI entrypoints.`
- `Prefer plumbum when Python code must execute OS commands.`
- `When project tooling exists, prefer uv run ruff check, uv run mypy, and uv run pytest after code changes.`

Это уже не “Python как стек”, а локальная operational policy репозитория или семейства репозиториев. Такие вещи лучше держать либо в project-specific fragments, либо в документации по workflow, но не в универсальном `Python Stack`.

**Что я бы добавил в сам `Python Stack`**
Ниже то, что выглядит дюрабельным и опирается на официальный Python/typing baseline, а не на вкусовщину.

- Prefer explicit types at public module boundaries: exported functions, service interfaces, repositories, adapters, and shared utilities.
- For function parameters, prefer the widest interface the implementation truly supports, such as `Iterable`, `Sequence`, or `Mapping`; for return values, prefer the concrete type you actually return.
- Avoid `Any` as a convenience shortcut; use `object` when any value is accepted, and use `Any` only as an intentional escape hatch.
- Keep structured data explicit: prefer dataclasses or typed models for domain data instead of loose dictionaries passed across module boundaries.
- Parse and validate untrusted input at the application boundary before it reaches business logic.
- Prefer `pathlib.Path` over stringly-typed path handling in application code.
- Use context managers for resources with lifetimes, including files, database sessions, locks, and network clients.
- Raise exceptions with actionable context instead of returning sentinel values that hide failure.
- Keep side effects at the edges; prefer pure, testable functions for transformations and business rules.
- Prefer logging for application and library diagnostics; reserve `print` for deliberate CLI output and simple scripts.
- Prefer composition over inheritance; use inheritance only when the subtype relationship is stable and behaviorally clear.
- Use `match` when working with closed variants or tagged states, not as a blanket replacement for ordinary conditionals.
- Keep framework-specific rules in framework fragments such as Django, FastAPI, or SQLAlchemy, not in the shared Python baseline.
- For libraries and reusable packages, aim for type-complete public interfaces so published types are part of the contract.

**Почему именно это**
Это хорошо ложится на официальные источники:
- Typing best practices прямо поддерживают идею “шире на входе, конкретнее на выходе”, а также различение `object` и `Any`: [typing best practices](https://typing.python.org/en/latest/reference/best_practices.html)
- Для библиотек официальный typing guidance рекомендует типизировать именно публичный интерфейс как контракт: [typing libraries](https://typing.python.org/en/latest/guides/libraries.html)
- `dataclasses` и явные модели поддерживают ваш текущий вектор на typed interfaces и domain models: [PEP 557](https://peps.python.org/pep-0557/)
- `pathlib` даёт более устойчивую модель путей, чем строковые операции: [pathlib docs](https://docs.python.org/3/library/pathlib.html)
- `logging` как стандартный механизм диагностики предпочтительнее разрозненных `print`: [logging docs](https://docs.python.org/3/library/logging.html)
- `match` полезен, но его стоит ограничить случаями, где он действительно улучшает модель закрытых вариантов, а не просто “потому что можно”: [control flow / match](https://docs.python.org/3/tutorial/controlflow.html)
- Базовый stylistic floor по-прежнему задаёт [PEP 8](https://peps.python.org/pep-0008/)

**Что я бы отдельно пересмотрел в формулировках**
Есть несколько правил, которые стоит сделать аккуратнее, чтобы они не звучали догматично:

- Вместо `Use type hints for parameters and return values` лучше `Use type hints for public and shared module boundaries; add local annotations where they improve clarity or checker feedback.`
Причина: тотальная аннотация каждой локальной переменной как стандарт для всех Python-проектов выглядит слишком жёстко и не подтверждается как универсальная лучшая практика.

- Вместо `Prefer match over long if / elif chains when it improves readability` лучше `Use match for closed variants, tagged states, and structural patterns when it makes the decision logic clearer.`
Причина: текущая формулировка слишком широкая и провоцирует злоупотребление `match`.

- Вместо простого `Prefer dataclasses or typed models over loose dictionaries for structured data` я бы усилил: `Do not pass loose dictionaries across important module boundaries when the shape is stable and meaningful.`
Причина: тут важен именно запрет на “shape by convention”.

**Если формулировать это как целевой shape для `fragments/stacks/python.md`**
Я бы ожидал там примерно 10–14 коротких bullet’ов про:
- typed boundaries
- abstract inputs / concrete outputs
- disciplined use of `Any`
- explicit domain models
- boundary validation
- resource lifetime via context managers
- actionable exceptions
- side effects at edges
- logging vs print
- composition over inheritance
- deliberate use of `match`
- separation of generic Python rules from Django/FastAPI/SQLAlchemy rules

**Моё ключевое замечание по архитектуре стандарта**
Для Python у вас сейчас, по сути, смешаны три уровня:
- общие инженерные правила
- универсальные Python language/runtime rules
- локальные tooling conventions конкретного семейства проектов

Их лучше развести. Иначе Python stack получится либо слишком бедным, либо слишком project-specific.

Если хочешь, следующим сообщением я могу сразу предложить готовую новую редакцию `fragments/stacks/python.md` в стиле, в котором уже оформлен `typescript.md`, плюс отдельно указать, что стоит убрать или переписать в `fragments/core/python.md`.

## Внести согласованные изменения в проект

**Question**

(0tdk223) Принимается. Внеси изменения в проект.

**Answer**

Вношу это как изменение стандарта: обновлю Python stack, уберу из shared core project-specific tooling-предпочтения и затем перегенерирую `AGENTS.md`, чтобы итог совпадал с исходниками.

Смотрю, как в тестах уже проверяются stack fragments. Если есть существующий рендер-тест для Python, расширю его; если нет, добавлю точечную проверку новых формулировок без лишнего шума.

Делаю точечные правки в Python fragments и тесте рендера. После этого перегенерирую `AGENTS.md` и прогоню проверки, чтобы не оставить рассинхрон между фрагментами и итоговым артефактом.

Правки внесены. Теперь синхронизирую сгенерированный `AGENTS.md` и прогоню `ruff`, `mypy`, `pytest`, плюс `ai_sync check`, чтобы подтвердить, что новые формулировки не сломали рендер и тесты.

`pytest` и `mypy` уже зелёные; остался только `ruff` на длине одной строки в новом тесте. Исправляю это и добиваю финальную верификацию.

В `ai-standards` обновил Python-стандарт в двух слоях. В [fragments/core/python.md](/home/shtirliz/workspace/myself/ai-standards/fragments/core/python.md:1) убрал project-specific предпочтения про `Typer`, `plumbum` и конкретный verification toolchain, а сами правила сделал уже и точнее: boundary typing вместо тотальной аннотации и более аккуратное правило для `match`. В [fragments/stacks/python.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/python.md:1) добавил полноценный baseline для Python: typed public boundaries, abstract inputs / concrete outputs, disciplined `Any`, явные модели данных, boundary validation, `pathlib`, context managers, actionable exceptions, side effects at the edges, logging, composition over inheritance и отделение framework-specific правил от shared stack.

Также обновил сгенерированный [AGENTS.md](/home/shtirliz/workspace/myself/ai-standards/AGENTS.md:1) и добавил рендер-тест в [tests/test_ai_sync.py](/home/shtirliz/workspace/myself/ai-standards/tests/test_ai_sync.py:1), который фиксирует новые Python guidance в итоговом артефакте.

Проверка прошла: `rtk uv run ruff check`, `rtk uv run mypy`, `rtk uv run python -m pytest -q`, `rtk uv run python scripts/ai_sync.py check --project-root /home/shtirliz/workspace/myself/ai-standards`. Если хочешь, следующим шагом оформлю это в отдельный commit на рабочей ветке по стандарту.

## Коммит по задаче 0tdk1bp и стандартное слияние ветки

**Question**

(0tdk2du) Отлично. Думаю нам следует выполнить commit на ветке с идентификатором задачи `0tdk1bp`, после чего слить её стандартным образом.

**Answer**

Подготовлю commit по правилам `ai-standards`: проверю текущую ветку и состав изменений, затем создам рабочую ветку с task id `0tdk1bp`, зафиксирую только релевантные файлы и предложу точный commit message на утверждение.

Сейчас изменения находятся на `main`, а это защищённая ветка, поэтому сначала перенесу их на новую рабочую ветку с `0tdk1bp`. После этого покажу точный commit message для вашего утверждения.

Ветка создана: `feature/0tdk1bp-python_stack_refresh`. Изменения ограничены четырьмя ожидаемыми файлами и выглядят как единый пакет обновления Python guidance.

Предлагаю commit message:
```text
0tdk1bp. (feat) refine shared python stack guidance.
```

Если подтверждаете этот текст, я сразу сделаю commit и затем солью ветку в `main` по стандарту.

Ветка создана: `feature/0tdk1bp-python_stack_refresh`. Изменения ограничены четырьмя ожидаемыми файлами и выглядят как единый пакет обновления Python guidance.

Предлагаю commit message:
```text
0tdk1bp. (feat) refine shared python stack guidance.
```

Если подтверждаете этот текст, я сразу сделаю commit и затем солью ветку в `main` по стандарту.

## Выполнить коммит и продолжить

**Question**

Отлично. Делай commit и продолжай.

**Answer**

Делаю commit с подтверждённым сообщением, затем переключусь на `main`, выполню стандартный merge и удалю рабочую ветку после успешного fast-forward.

Commit создан. Проверяю итоговый commit, затем выполняю merge в `main` и завершаю lifecycle ветки.

Локальный `main` синхронизирован с `origin/main`, так что делаю чистый fast-forward merge из рабочей ветки. После него удалю source branch и проверю итоговый статус.

Merge завершён fast-forward. Удаляю рабочую ветку и фиксирую финальное состояние репозитория.

Commit и merge завершены по стандарту.

Создан commit `c2f202d` с сообщением `0tdk1bp. (feat) refine shared python stack guidance.` Затем ветка `feature/0tdk1bp-python_stack_refresh` была слита в `main` через fast-forward и удалена. Сейчас `HEAD` на `main` указывает на `c2f202d`.

Локальный `main` теперь `ahead 1` относительно `origin/main`, то есть этот commit ещё не опубликован. Если нужно, следующим шагом могу запушить `main` в `origin`.

## Предложения по верификации и обновлению правил Django и FastAPI

**Question**

(0tdk2in) Теперь давай аналогичным образом верифицируем и обновим правила для Django и FastAPI.
Ожидаю твоих предложений.

**Answer**

Сначала подниму текущие Django и FastAPI fragments в `ai-standards`, затем сопоставлю их с официальной документацией и устойчивыми практиками, чтобы предложения были точечными, а не абстрактными.

Добираю ещё смежные Django fragments, чтобы не предложить правила, которые уже покрыты отдельными composable-слоями вроде `django-save-lifecycle` и `django-naming`.

Сейчас оба фрагмента несимметричны по зрелости: `django.md` уже содержит полезную основу, но местами смешивает durable framework rules с локальными подходами; `fastapi.md` пока слишком тонкий и не покрывает несколько ключевых официальных практик FastAPI. Ниже мои предложения по обновлению.

**Django**
Я бы не переписывал Django-стек с нуля. Его лучше аккуратно усилить и убрать из него спорные или project-specific акценты.

Что стоит сохранить:
- следование уже существующему архитектурному паттерну внутри конкретного app/module;
- ограничения на бизнес-логику в сигналах;
- явную оптимизацию `select_related` / `prefetch_related`;
- ориентацию на DB constraints;
- security defaults как baseline.

Что я бы уточнил:
- Блок `Existing Code` правильный по духу, но его лучше сделать короче и жёстче: “не вносить новый architectural style локально, если модуль уже последователен”.
- Формулировку про `full_clean()` не стоит дублировать в общем `django.md`, потому что это уже покрывает `django-service-layer.md` и зависит от того, через какие entry points идёт запись.
- `Use django-environ or equivalent` лучше ослабить до “use environment-based configuration and never commit secrets”. Конкретная библиотека не должна становиться shared standard.
- `Use Django's cache framework ...` не стоит держать как универсальное правило. Кэширование в Django слишком зависит от сценария и инфраструктуры. Лучше перенести это в guidance/docs, а не в обязательный stack fragment.

Что я бы добавил в `django.md`:
- Prefer Django’s built-in protections and conventions unless there is a documented reason to bypass them.
- Keep model methods small and local to the model’s own invariants; move cross-aggregate orchestration out of models.
- Use database constraints and indexes deliberately for invariants and query patterns, not only application-level checks.
- Be explicit about queryset shape in request paths; do not rely on incidental lazy loading for correctness or performance.
- Use transactions deliberately around multi-step writes that must succeed or fail as one unit.
- Keep signals rare and narrowly scoped; if sender and receiver are both inside the project, prefer explicit function calls.
- Validate and normalize user input through forms, serializers, or service boundaries before it reaches deeper layers.
- Keep migrations reviewable and intentional; do not treat autogenerated migrations as correct by default.
- Prefer custom QuerySet/manager methods only for reusable query construction, not for hiding business workflows.
- In admin, forms, serializers, and views, keep framework glue thin and delegate business decisions to the chosen application layer.

Что я бы не добавлял в общий Django stack:
- жёсткое требование `factory_boy`;
- жёсткое требование `django-filter`;
- предписание конкретного API style вроде “только APIView”;
- локальные naming conventions, потому что это уже отдельный composable fragment.

Почему:
- Django docs прямо поддерживают акцент на DB optimization, constraints, security defaults и аккуратное использование signals. Особенно важны текущие официальные страницы про optimization, security и signals, где Django сам предупреждает, что explicit function call внутри проекта обычно лучше, чем custom signal.  
Источники:
- https://docs.djangoproject.com/en/6.0/topics/db/optimization/
- https://docs.djangoproject.com/en/6.0/topics/security/
- https://docs.djangoproject.com/en/5.0/topics/signals/
- https://docs.djangoproject.com/en/2.0/ref/models/instances/

**FastAPI**
Здесь, на мой взгляд, нужен уже не тюнинг, а полноценное расширение фрагмента. Текущий `fastapi.md` слишком общий и не фиксирует то, что в FastAPI реально влияет на качество решений.

Что стоит сохранить:
- thin endpoints;
- validation at the boundary;
- DI only for wiring.

Что я бы добавил в `fastapi.md` почти обязательно:
- Use `response_model` or explicit return typing for externally visible response contracts; do not leak raw ORM objects or ad hoc dictionaries by accident.
- Keep path operations thin; parse input, call the use case, map the result to the response schema.
- Use dependencies for wiring, auth, settings, sessions, and request-scoped resources; do not hide business workflows inside dependency graphs.
- Use dependencies with `yield` for resources that require deterministic cleanup, such as database sessions and clients.
- Use `lifespan` for application startup and shutdown resources; do not spread shared resource initialization across import side effects.
- Choose `def` vs `async def` based on the actual I/O model of the called code; do not mark handlers `async` by default if the stack underneath is synchronous.
- Keep Pydantic models explicit at API boundaries; use stricter validation where silent coercion would hide client or integration errors.
- Raise `HTTPException` only at the HTTP boundary; keep domain and service layers framework-agnostic.
- Use `BackgroundTasks` only for small in-process follow-up work; use a real task queue for heavy, retry-sensitive, or cross-process jobs.
- Keep security dependencies explicit and based on FastAPI’s security utilities instead of ad hoc header parsing.
- Keep OpenAPI-facing contracts stable and intentional; avoid undocumented response shapes and exception payload drift.
- Prefer one request-scoped unit of work per request; do not share mutable sessions or clients globally unless they are designed for it.

Что я бы отдельно уточнил:
- Для FastAPI полезно зафиксировать distinction между app lifecycle resources и request lifecycle resources. Это очень частый источник плохих решений.
- Я бы не тащил в shared fragment слишком SQLAlchemy-specific советы, потому что часть из них уже живёт в `sqlalchemy.md`.
- Я бы не писал “always use async” или “always use Pydantic strict mode”. Это уже будет переусложнение и начнёт конфликтовать с реальными интеграциями.

Почему:
- Официальный FastAPI tutorial прямо подчёркивает важность `response_model`, `yield` dependencies, `lifespan` и встроенных security utilities.
- Pydantic docs подтверждают, что strict validation полезна именно там, где нежелательна молчаливая coercion, но не как безусловный глобальный default для всего.
Источники:
- https://fastapi.tiangolo.com/tutorial/response-model/
- https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
- https://fastapi.tiangolo.com/advanced/events/
- https://fastapi.tiangolo.com/tutorial/background-tasks/
- https://fastapi.tiangolo.com/tutorial/security/first-steps/
- https://docs.pydantic.dev/latest/concepts/strict_mode/
- https://docs.pydantic.dev/latest/why/

**Где я вижу основную структурную проблему сейчас**
Для Django у вас уже есть composable fragments:
- `django.md`
- `django-service-layer.md`
- `django-save-lifecycle.md`
- `django-drf.md`
- `django-naming.md`

Это хорошо, но границы между ними стоит сделать жёстче:
- `django.md` должен остаться framework baseline.
- `django-service-layer.md` должен оставаться optional architectural style, а не скрытым default.
- `django-drf.md` сейчас слишком opinionated из-за `APIView` и nested serializers; я бы позже тоже его пересмотрел.
- `django-save-lifecycle.md` выглядит скорее как локальный operational pattern, чем как безусловная shared best practice.

Для FastAPI ситуация обратная: там пока baseline слишком бедный, и его надо довести хотя бы до уровня, на котором он покрывает lifecycle, dependencies, response contracts, async discipline, security boundary и background-work discipline.

**Если кратко по change intent**
Я бы предложил такой курс:
1. Усилить `django.md`, но не превращать его в копию HackSoft styleguide.
2. Существенно расширить `fastapi.md` до полноценного baseline fragment.
3. Отдельно, уже следующим шагом, решить, нужно ли смягчать `django-drf.md` и `django-save-lifecycle.md`, потому что именно там сейчас больше всего спорных локальных решений.

Если хочешь, следующим сообщением я могу сразу перевести это в конкретный patch для `ai-standards`: обновить `fragments/stacks/django.md` и `fragments/stacks/fastapi.md`, перегенерировать `AGENTS.md`, добавить тесты рендера и затем подготовить commit по стандарту.

## Усиление django.md и расширение fastapi.md без перехода к спорным фрагментам

**Question**

(0tdk33j)
> 1. Усилить django.md, но не превращать его в копию HackSoft styleguide.
> 2. Существенно расширить fastapi.md до полноценного baseline fragment.
> 3. Отдельно, уже следующим шагом, решить, нужно ли смягчать django-drf.md и django-save-lifecycle.md, потому что именно там сейчас больше всего спорных локальных решений.

Давай прямо сейчас сделаем 1 и 2, чтобы на следующем шаге полностью сфокусироваться на проблемном 3.

**Answer**

Делаю именно пункты 1 и 2: обновлю `django.md` как framework baseline без навязывания service-style, расширю `fastapi.md` до полноценного baseline, затем перегенерирую `AGENTS.md` и прогоню проверки.

Подход простой: `django.md` станет более нейтральным и опирающимся на официальный baseline Django, а `fastapi.md` получит правила про lifecycle, dependencies, response contracts, async discipline и boundary errors без привязки к конкретному ORM.

Правки внесены. Перегенерирую `AGENTS.md` и прогоню стандартный набор проверок, чтобы убедиться, что новый baseline для Django и FastAPI консистентен и тестами зафиксирован.

Проверки зелёные. Финально сверю git-статус и зафиксирую, какие файлы вошли в изменение, чтобы следующий шаг по проблемным Django fragments можно было делать отдельно и без смешивания контекста.

В `ai-standards` обновил оба baseline-фрагмента в пределах согласованного scope.

В [fragments/stacks/django.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/django.md:1) Django стал более нейтральным framework-level стандартом: убраны лишние привязки к конкретным библиотекам и спорные обязательности, добавлены более устойчивые правила про local invariants в моделях, deliberate use of constraints and indexes, explicit query shape, transactions, boundary validation, built-in protections и reviewable migrations. Это усиливает `django.md`, но не превращает его в скрытый `django-service-layer`.

В [fragments/stacks/fastapi.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/fastapi.md:1) FastAPI доведён до полноценного baseline: response contracts через `response_model`/return typing, thin path operations, disciplined dependencies, `yield` cleanup, `lifespan`, осознанный выбор `def` vs `async def`, explicit Pydantic boundary models, `HTTPException` только на HTTP-границе, ограничения для `BackgroundTasks`, явная security wiring и request-scoped unit of work. В [tests/test_ai_sync.py](/home/shtirliz/workspace/myself/ai-standards/tests/test_ai_sync.py:1) добавил рендер-тест, который фиксирует новые правила обоих стеков.

Проверка прошла: `rtk uv run ruff check`, `rtk uv run mypy`, `rtk uv run python -m pytest -q`, `rtk uv run python scripts/ai_sync.py render --project-root /home/shtirliz/workspace/myself/ai-standards`. В рабочем дереве сейчас изменены только `fragments/stacks/django.md`, `fragments/stacks/fastapi.md` и `tests/test_ai_sync.py`, так что следующим шагом можно чисто и отдельно заняться проблемным пунктом 3.

## Перенос фундаментальных Python правил из core в stacks/python

**Question**

(0tdk38z) Ok. Но меня смущает существование "куцых" правил для Python в `core`, где я ожидал бы вещей фундаментальных.
Не стоит ли перенести правила для Python из `core` в `stacks/python`? 🙄

**Answer**

Да, меня это тоже смущает. В текущей структуре `core/python.md` выглядит архитектурно слабее, чем должен.

Проблема здесь не в самих формулировках, а в слое, в который они положены. `core` у вас сейчас означает правила, которые почти не зависят от технологии проекта и должны быть уместны в широком наборе репозиториев. Python туда попадает плохо, потому что это уже выбор языка исполнения, а не общая инженерная основа. Даже “фундаментальные” Python-правила всё равно остаются language-specific.

Я бы рекомендовал следующее:
- перенести Python-specific guidance из `core/python.md` в `stacks/python.md`;
- `core/python.md` либо удалить совсем, либо свести к нулю и затем убрать его из манифестов/шаблонов;
- считать `stacks/python` единственным источником Python baseline, а `django`, `fastapi`, `sqlalchemy` уже надстраивать поверх него.

Почему это лучше:
- исчезает размытая граница между “core” и “stack”;
- все Python-правила оказываются в одном месте, и их проще развивать;
- downstream manifest становится честнее: если проект на Python, он явно подключает `python` stack, а не получает Python-специфику через якобы общий `core`;
- структура становится симметричнее с TypeScript, Java Spring и остальными стеками.

Я бы не оставлял в `core` даже “самые базовые” Python-вещи вроде type hints, dataclasses, `match` и т.д. Это всё равно не фундамент проекта вообще, а фундамент Python-проекта.

Если делать это аккуратно, то план такой:
1. Перенести содержимое `fragments/core/python.md` в `fragments/stacks/python.md`.
2. Удалить `core/python.md` из шаблонов и примеров манифеста.
3. Проверить, не опираются ли тесты и README на старую схему.
4. Перегенерировать `AGENTS.md` и обновить рендер-тесты.

С практической точки зрения я считаю это правильным следующим изменением. Если хочешь, я могу сразу внести этот рефакторинг в `ai-standards`.

## Перенести Python правила в stacks/python

**Question**

Да, проделай это пожалуйста.

**Answer**

Сделаю этот рефакторинг как структурное изменение стандарта: перенесу Python guidance целиком в `stacks/python`, уберу зависимость от `core/python` из шаблонов и тестов, затем перегенерирую `AGENTS.md` и прогоню проверки.

Смотрю, где именно в README и self-hosted manifest зашито старое подключение `core/python`, чтобы убрать его без побочных дыр в примерах и документации.

Перед правкой добираю участок тестов, который сейчас ждёт отдельную секцию `Python Preferences`, чтобы сразу перестроить ожидания под единый `Python Stack`.

Делаю структурный patch: солью содержимое `core/python` в `stacks/python`, уберу `core/python` из всех живых manifest/examples и удалю сам фрагмент, чтобы не осталось двух источников истины.

Патч применён. Сейчас добью остаточные ссылки на `core/python`, если они ещё есть в живых артефактах, затем перегенерирую `AGENTS.md` и прогоню проверки.

`render`, `ruff` и `mypy` уже зелёные. Осталось подтвердить это тестами и `ai_sync check`, чтобы зафиксировать, что удаление `core/python` не оставило скрытых зависимостей.

Сделано. Python-specific guidance теперь живёт только в `stacks/python`, а отдельный [fragments/core/python.md](/home/shtirliz/workspace/myself/ai-standards/fragments/core/python.md:1) удалён. В [fragments/stacks/python.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/python.md:1) я добавил туда бывшие core-правила про type hints, typed models и осмысленное использование `match`, так что Python baseline собран в одном месте.

Также убрал `core/python` из self-hosted manifest и шаблонов: [ai.project.toml](/home/shtirliz/workspace/myself/ai-standards/ai.project.toml:1), [templates/project_manifest.toml](/home/shtirliz/workspace/myself/ai-standards/templates/project_manifest.toml:1), [README.md](/home/shtirliz/workspace/myself/ai-standards/README.md:1) и [README.ru.md](/home/shtirliz/workspace/myself/ai-standards/README.ru.md:1). В [tests/test_ai_sync.py](/home/shtirliz/workspace/myself/ai-standards/tests/test_ai_sync.py:1) перестроил тест на unified Python stack. `AGENTS.md` перегенерирован и уже не тянет `core/python`.

Проверка прошла: `rtk uv run ruff check`, `rtk uv run mypy`, `rtk uv run python -m pytest -q`, `rtk uv run python scripts/ai_sync.py check --project-root /home/shtirliz/workspace/myself/ai-standards`.

В рабочем дереве сейчас вместе с этим изменением всё ещё лежат не закоммиченные правки по `django.md` и `fastapi.md`, которые мы сделали шагом раньше. Это нормально, но важно: если следующим действием пойдём в commit, лучше решить, коммитим ли всё одним пакетом или разделяем Python-рефакторинг структуры и Django/FastAPI baseline на два отдельных commit.

## Коммит по задаче 0tdk1sa для обновления Python стека и возврат к спорным правилам

**Question**

(0tdk3f6) Да, двай выполним commit на ветке с идентификатором задачи `0tdk1sa` и темой "Обновление Python-стека".
После выполнения commit-а я предлагаю вернуться к подсвеченному тобой ранее:
> 3. Отдельно, уже следующим шагом, решить, нужно ли смягчать django-drf.md и django-save-lifecycle.md, потому что именно там сейчас больше всего спорных локальных решений.

**Answer**

Сначала проверю текущую ветку и состав изменений, потому что в рабочем дереве сейчас смешаны два пакета: обновление Python-стека и отдельные правки baseline для Django/FastAPI. Если commit должен быть именно про Python stack, это лучше не замазывать одним сообщением.

Сейчас на `main` лежат не только изменения по Python-стеку, но и уже подготовленные правки [fragments/stacks/django.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/django.md:1) и [fragments/stacks/fastapi.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/fastapi.md:1). Если я сделаю один commit с темой “Обновление Python-стека”, сообщение будет неточным.

Нужен ваш выбор:
- делаем один commit `0tdk1sa` сразу на весь текущий пакет, включая Django/FastAPI;
- или я сначала отделяю только Python-изменения в отдельный commit `0tdk1sa`, а Django/FastAPI оставляю незакоммиченными для следующего шага.

## Объединение обновления Python стека и спорных правил в один коммит

**Question**

Да, я думаю, следует объединить это в одном commit-е поскольку наша локальная цель – обновить правила для всей инфраструктуры Python.
В эту же канву (и ветку тоже) ложится разбирательство с этим пунктом:
> 3. Отдельно, уже следующим шагом, решить, нужно ли смягчать django-drf.md и django-save-lifecycle.md, потому что именно там сейчас больше всего спорных локальных решений.

**Answer**

Тогда собираем это как единый пакет обновления Python infrastructure guidance. Сначала перенесу изменения с `main` на рабочую ветку `0tdk1sa`, затем зафиксирую точный commit message на утверждение, как требует workflow репозитория.

Ветка создана: `feature/0tdk1sa-python_infrastructure_guidance_refresh`. В commit войдёт единый пакет: унификация `python` stack, удаление `core/python`, обновление baseline для Django/FastAPI и синхронизация тестов, README и self-hosted manifest.

Предлагаю commit message:
```text
0tdk1sa. (feat) refresh python infrastructure guidance.
```

Если подтверждаете этот текст, я сразу сделаю commit и затем солью ветку в `main` по стандарту.

Ветка создана: `feature/0tdk1sa-python_infrastructure_guidance_refresh`. В commit войдёт единый пакет: унификация `python` stack, удаление `core/python`, обновление baseline для Django/FastAPI и синхронизация тестов, README и self-hosted manifest.

Предлагаю commit message:
```text
0tdk1sa. (feat) refresh python infrastructure guidance.
```

Если подтверждаете этот текст, я сразу сделаю commit и затем солью ветку в `main` по стандарту.

## Коммит и подробный разбор спорных решений в django-drf и django-save-lifecycle

**Question**

Отлично, выполни commit, и давай подробно разберём
> 3. Отдельно, уже следующим шагом, решить, нужно ли смягчать django-drf.md и django-save-lifecycle.md, потому что именно там сейчас больше всего спорных локальных решений.

Пожалуйста, обозначь спорные решения и предложения по улучшению.

**Answer**

Делаю commit с подтверждённым сообщением на рабочей ветке, затем разберу `django-drf.md` и `django-save-lifecycle.md` по пунктам: что там спорно, что выглядит локальным паттерном, и что стоит ослабить или вынести из shared standard.

Commit создан. Теперь разбираю два проблемных фрагмента отдельно от уже принятого baseline: подниму их текущий текст и сверю спорные места с Django/DRF docs, чтобы предложения были не на вкусе, а на более устойчивом основании.

Commit уже создан на рабочей ветке. Для разбора спорных мест добираю точные ссылки на строки в `django-drf.md` и `django-save-lifecycle.md`, чтобы предложения были привязаны к конкретным формулировкам, а не к общему впечатлению.

Commit выполнен на ветке `feature/0tdk1sa-python_infrastructure_guidance_refresh`.

Создан commit `a2ab754` с сообщением `0tdk1sa. (feat) refresh python infrastructure guidance.` Я его пока не сливал в `main`, потому что вы попросили сначала подробно разобрать спорный пункт 3.

**Спорные места**
На мой взгляд, самые слабые места сейчас действительно в [django-drf.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/django-drf.md:5) и [django-save-lifecycle.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/django-save-lifecycle.md:5). Проблема не в том, что эти правила “плохие”, а в том, что они слишком похожи на локальный стиль конкретной команды, а не на shared standard.

В [django-drf.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/django-drf.md:6) спорны такие пункты:
- `Prefer inheriting from DRF APIView over generic views` слишком догматично. В официальной DRF-документации и generic views, и viewsets считаются штатными абстракциями, а не “уступкой удобству”. Лучше правило формулировать как выбор наименьшей достаточной абстракции, а не как запрет generic views. Источники: https://www.django-rest-framework.org/api-guide/generic-views/ , https://www.django-rest-framework.org/api-guide/viewsets/
- `Nest InputSerializer and OutputSerializer inside the API class` это явный style choice, а не устоявшаяся best practice DRF. В DRF обычно сериализаторы объявляются как обычные классы модуля, и это нормально.
- `prefer Serializer over ModelSerializer` тоже слишком жёстко. `ModelSerializer` сам по себе не анти-паттерн; он плох только там, где прячет сложные правила или создаёт ложную связанность контракта с моделью. Источник: https://www.django-rest-framework.org/api-guide/serializers/
- `Do not reuse serializers across different APIs unless intentional` по сути верно, но формулировка слабая: почти любое переиспользование и так “intentional”. Лучше говорить о том, что сериализатор можно переиспользовать только когда контракт действительно общий, а не “похожий”.
- `delegate to the service or viewset save lifecycle` привязывает DRF-фрагмент к другому, тоже спорному фрагменту. Это лишняя сцепка между стандартами.

В [django-save-lifecycle.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/django-save-lifecycle.md:8) спорны такие пункты:
- `Use the view or viewset as the orchestration point` слишком узко. Хорошее правило здесь не про “view/viewset”, а про explicit orchestration вместо сигналов. Оркестрация может жить и в application/service layer.
- `Keep business logic functions in the services layer` уже навязывает конкретную архитектуру. Для shared fragment это слишком сильно. Это скорее optional architectural mode, а не baseline.
- Блок с base viewset и методом `save(self, serializer, additional_data=None)` в [django-save-lifecycle.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/django-save-lifecycle.md:12) выглядит как локальный framework pattern. DRF официально даёт для этого `perform_create()` и `perform_update()`, и их прямое переопределение является нормальным extension point, а не чем-то, чего нужно избегать. Источник: https://www.django-rest-framework.org/api-guide/generic-views/
- Запрет `do not override perform_create or perform_update directly` в [django-save-lifecycle.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/django-save-lifecycle.md:13) я считаю самым спорным утверждением во всём пакете. Это уже не best practice, а мнение конкретного локального паттерна.
- Аналогично, базовый `CreateView`/`UpdateView` с отдельным `save(self, form, additional_data=None)` в [django-save-lifecycle.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/django-save-lifecycle.md:20) тоже является локальным соглашением. В Django штатная точка расширения здесь обычно `form_valid()`. Источник: https://docs.djangoproject.com/en/stable/topics/class-based-views/generic-editing/
- Деление на pre-save/post-save полезно как мыслительная модель, но правило про “side effects after save” стоит уточнить: если побочный эффект зависит от успешного commit, его безопаснее планировать через `transaction.on_commit`, а не просто делать “после save”. Источник: https://docs.djangoproject.com/en/stable/topics/db/transactions/
- `additional_data` как параметр для прокидывания `created_by`/`updated_by` опять же выглядит как локальная idiom, а не общий стандарт.

**Что я бы предложил вместо этого**
Я бы не удалял оба фрагмента целиком. Я бы их смягчил и развёл по слоям.

Для `django-drf.md` я бы предложил такой вектор:
- выбирать `APIView`, generic views или viewsets по уровню необходимой абстракции и читаемости;
- держать request/response serializers явными, особенно если входной и выходной контракт различаются;
- не злоупотреблять `ModelSerializer`, но и не запрещать его;
- переиспользовать serializers только при реально общем контракте;
- валидировать вход на boundary и делегировать orchestration в выбранный application layer, не ссылаясь на конкретный `save lifecycle` fragment.

Для `django-save-lifecycle.md` я бы предложил сделать его не “единственно правильным flow”, а более нейтральным:
- explicit calls are preferred over signals for project-internal business workflows;
- keep entrypoints thin and place orchestration in a consistent application layer chosen by the project;
- use Django/DRF standard hooks such as `form_valid`, `perform_create`, `perform_update`, or a local wrapper pattern consistently within a project;
- schedule post-commit side effects with `transaction.on_commit` when correctness depends on committed data;
- reserve signals for cross-cutting events that must fire regardless of the entry point.

**Что я считаю главным архитектурным выводом**
`django-drf.md` и `django-save-lifecycle.md` сейчас оформлены как reusable stack fragments, но по содержанию это скорее:
- `django-drf.md`: opinionated API style guide;
- `django-save-lifecycle.md`: optional application-architecture pattern.

То есть они выглядят не как “общие правила Django/DRF”, а как “один из возможных способов писать Django/DRF”. Для `ai-standards` это и есть источник напряжения.

**Моё предложение по следующему изменению**
Я бы сделал так:
1. Смягчить `django-drf.md`, убрав обязательность `APIView`, nested serializers и запрет на `ModelSerializer`.
2. Переписать `django-save-lifecycle.md` из конкретного base-class pattern в более общий fragment про explicit save orchestration и standard hooks.
3. Если хочется сохранить текущий более жёсткий HackSoft-style flow, вынести его в отдельный fragment с явным названием уровня `django-opinionated-service-flow` или `django-hacksoft-style`, чтобы не маскировать локальный стиль под baseline.

Если хочешь, следующим сообщением я могу сразу перевести это в конкретный patch для этих двух файлов и подготовить новый commit уже в рамках той же ветки `0tdk1sa`.

## Изменения в django-drf и верификация HackSoft подхода и unified save в Django

**Question**

(0tdk491) Очень сильный анализ. Спасибо.
Что предлагаю в этой связи.

(0tdk49y) Все твои предложения по `django-drf.md` принимаются, изменения можно выполнить прямо сейчас, чтобы высвободить контекст предлагаю сразу сделать commit.

(0tdk4bz) Относительно `django-save-lifecycle.md` я предлагаю немного обсудить самую спорную его часть, в выработке которой я принимал непосредственное участие:
> Блок с base viewset и методом save(self, serializer, additional_data=None) в django-save-lifecycle.md (line 12) выглядит как локальный framework pattern. DRF официально даёт для этого perform_create() и perform_update(), и их прямое переопределение является нормальным extension point, а не чем-то, чего нужно избегать. Источник: https://www.django-rest-framework.org/api-guide/generic-views/
> Запрет do not override perform_create or perform_update directly в django-save-lifecycle.md (line 13) я считаю самым спорным утверждением во всём пакете. Это уже не best practice, а мнение конкретного локального паттерна.
> Аналогично, базовый CreateView/UpdateView с отдельным save(self, form, additional_data=None) в django-save-lifecycle.md (line 20) тоже является локальным соглашением. В Django штатная точка расширения здесь обычно form_valid(). Источник: https://docs.djangoproject.com/en/stable/topics/class-based-views/generic-editing/

(.0tdk4lc) Смотри, `django-save-lifecycle.md` – в сущности, надстройка над Hacksoft style guide, который, кстати, я бы предложил выделить отдельно и целиком, разумеется, без дублирования с более общими правилами по Python.
(!) Пожалуйста, верифицируй это предложение.

(.0tdk4lk) Далее, возвращаясь к спорным тезисам. Выделение метода `save`, так, как описано в правилах возникло в результате наблюдения, что операции create и update чаще всего очень похожи в части задействуемой бизнес-логики.
Соответственно, различать `create` и `update` в `save()`, ориентируясь на значение PK (`None` – значит `create`, в противном случае `update`) куда проще, чем дублировать логику оркестрации (да даже дублирование простого вызова сервисного слоя – это же шум!) в `perform_create` и `perform_update`.
(!) Пожалуйста, верифицируй эти соображения. Дальше решим, как поступить с `django-save-lifecycle.md`.

**Answer**

Сначала верифицирую два тезиса по первичным источникам: 1) стоит ли выделять HackSoft-style слой отдельно, 2) насколько defensible pattern с единым `save()` поверх `perform_create`/`perform_update` и `form_valid`. Параллельно подготовлю точечный patch для `django-drf.md`, чтобы затем можно было быстро оформить его отдельным commit.

Вношу только `django-drf.md` как отдельный шаг, без изменения `django-save-lifecycle.md`. Цель: снять наиболее жёсткие локальные предписания и оставить нейтральный DRF baseline, после чего прогоню проверки и предложу отдельный commit message для вашего утверждения.

Правка внесена. Сейчас прогоню проверки только для этого шага, а затем дам верификацию по двум вашим тезисам: про отдельный HackSoft layer и про общий `save()` как способ убрать оркестрационный шум.

Изменения по `django-drf.md` уже внесены и проверены. В рабочем дереве сейчас только [fragments/stacks/django-drf.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/django-drf.md:1) и [tests/test_ai_sync.py](/home/shtirliz/workspace/myself/ai-standards/tests/test_ai_sync.py:1). Проверка прошла: `rtk uv run ruff check`, `rtk uv run mypy`, `rtk uv run python -m pytest -q`.

Теперь по верификации ваших тезисов.

**1. Выделить HackSoft style guide отдельно и целиком**
Это предложение я считаю правильным.

Причина простая: и `django-drf.md`, и особенно `django-save-lifecycle.md` по содержанию действительно ближе к opinionated architectural style, чем к framework baseline. Это не делает их плохими. Это делает их неправильным слоем для shared default fragment. Если оформить их как отдельный opt-in слой уровня `django-hacksoft-style` или `django-opinionated-service-flow`, структура станет чище:
- `django.md` останется нейтральным baseline для Django;
- `django-drf.md` может остаться нейтральным baseline для DRF;
- HackSoft-like сервисно-ориентированный flow станет явной надстройкой, а не скрытым “как будто общим стандартом”.

Это хорошо согласуется и с самим духом DRF/Django docs: официальная документация поддерживает разные точки расширения и не продвигает один обязательный архитектурный шаблон.
Источники:
- DRF generic views: https://www.django-rest-framework.org/api-guide/generic-views/
- DRF viewsets: https://www.django-rest-framework.org/api-guide/viewsets/
- DRF serializers: https://www.django-rest-framework.org/api-guide/serializers/
- Django generic editing views: https://docs.djangoproject.com/en/stable/topics/class-based-views/generic-editing/

Итого: да, выделять такой стиль отдельно имеет смысл. Я бы это верифицировал как хорошее архитектурное направление.

**2. Логика общего `save()` поверх create/update**
Ваше обоснование технически сильное. Я не считаю его ошибочным.

Что в нём действительно хорошо:
- оно уменьшает дублирование orchestration-кода между `create` и `update`;
- оно даёт единое место для pre-save / post-save логики;
- оно делает общую ветку поведения явной, если разница между create и update действительно минимальна;
- проверка через наличие `pk` или `instance is None` в ряде CRUD-сценариев действительно практична и проще, чем зеркалить две почти одинаковые ветки в `perform_create` и `perform_update`.

То есть как локальный pattern это решение вполне defensible.

Но здесь важна граница применимости. Я бы верифицировал это так:
- как project-level convention или opinionated reusable pattern: да, это разумно;
- как shared best practice для всех Django/DRF проектов: нет, слишком сильно.

Почему я не считаю это universal best practice:
- официальные extension points в DRF для этого именно `perform_create()` и `perform_update()`, и их использование само по себе не является smell;
- в части проектов различие между create и update быстро становится существенным: разные permissions, разные invariants, разные side effects, разные audit rules;
- единый `save()` снижает шум там, где lifecycle действительно симметричен, но может скрывать важные семантические различия там, где create/update начинают расходиться;
- кастомный wrapper `save()` требует, чтобы команда приняла эту конвенцию целиком, иначе он становится ещё одним локальным слоем поверх стандартного DRF API.

То есть ваш тезис я бы уточнил так:
- это хороший способ убрать orchestration noise в проектах, где create/update mostly symmetric;
- это не основание объявлять `perform_create`/`perform_update` “неправильными” или запрещёнными.

Для plain Django CBV вывод аналогичный:
- `form_valid()` является стандартной точкой расширения;
- отдельный `save(form, additional_data=None)` может быть удобным локальным wrapper-паттерном;
- но делать его shared standard для всех Django-проектов я бы не стал.

Отдельно важное уточнение по post-save phase: если речь о побочных эффектах, зависящих от успешного commit, ваша модель “после save” должна дополняться `transaction.on_commit`, иначе логика формально “после save”, но ещё не обязательно “после commit”.
Источник:
- Django transactions / `on_commit`: https://docs.djangoproject.com/en/6.0/topics/db/transactions/

**Практический вывод**
Я бы сейчас зафиксировал такую позицию:
- `django-save-lifecycle.md` не нужно выбрасывать;
- его не стоит держать как нейтральный baseline fragment;
- его стоит либо смягчить до общего правила про explicit orchestration and standard hooks, либо выделить в отдельный явно opinionated HackSoft-derived fragment;
- pattern с единым `save()` имеет право на жизнь и выглядит инженерно оправданным, но должен быть представлен как optional project architecture choice, а не как универсальная лучшая практика.

**Commit по уже внесённым изменениям `django-drf.md`**
Предлагаю commit message:
```text
0tdk1sa. (refactor) soften django drf stack guidance.
```

Если подтверждаете, я сразу сделаю этот commit на текущей ветке. После этого можем отдельно принять решение по будущему shape для `django-save-lifecycle.md`: смягчать его или выделять в отдельный HackSoft-style fragment.

## Фиксация on_commit в правилах и выделение опциональных HackSoft и unified save фрагментов

**Question**

(0tdk55y) Сообщение commit-а подтверждаю.

(0tdk51z)
> Отдельно важное уточнение по post-save phase: если речь о побочных эффектах, зависящих от успешного commit, ваша модель “после save” должна дополняться transaction.on_commit, иначе логика формально “после save”, но ещё не обязательно “после commit”.
> Источник: Django transactions / on_commit: https://docs.djangoproject.com/en/6.0/topics/db/transactions/

Да-да, спасибо что напомнил. Полностью согла сен с тобой, что в таких случаях следует применять `transaction.on_commit`.
Но думаю, это следует всё-таки зафиксировать в правилах.

(0tdk56d) Предложи пожалуйста опциональный набор правил на базе Hacksoft style guide.

(0tdk57m)
> pattern с единым save() имеет право на жизнь и выглядит инженерно оправданным, но должен быть представлен как optional project architecture choice, а не как универсальная лучшая практика.

Совершенно согласен, предлагаю выделить этот паттен в отдельный md-файл с возможностью явного подключения.
Как тебе такая идея?

**Answer**

Сначала зафиксирую уже внесённое смягчение `django-drf.md` отдельным commit на текущей ветке, после чего предложу shape для опционального HackSoft-derived набора и отдельного фрагмента под unified `save()` pattern.

Commit создан. Проверю хеш и затем предложу конкретную структуру для опционального HackSoft-style набора и отдельного фрагмента для unified `save()` pattern.

Commit выполнен: `7b79227` с сообщением `0tdk1sa. (refactor) soften django drf stack guidance.` Рабочее дерево чистое, остаёмся на ветке `feature/0tdk1sa-python_infrastructure_guidance_refresh`.

Идею с отдельным подключаемым фрагментом для HackSoft-derived подхода я считаю правильной. Это как раз решает главную архитектурную проблему: нейтральный baseline остаётся нейтральным, а opinionated application pattern подключается явно.

Я бы предложил такую структуру.

**Что выделить отдельно**
- `stacks/django.md`: нейтральный framework baseline.
- `stacks/django-drf.md`: нейтральный DRF baseline.
- Новый фрагмент, например `stacks/django-hacksoft-style.md` или `stacks/django-service-flow.md`: opt-in набор правил, основанный на HackSoft-style архитектуре.
- Отдельный фрагмент, например `stacks/django-save-orchestration.md`: opt-in pattern для unified `save()` flow, если хотите сделать его включаемым независимо от полного HackSoft-style слоя.

Если хочется минимизировать сущности, можно объединить последние два в один фрагмент. Но мне кажется, лучше держать их раздельно:
- `django-hacksoft-style` про services/selectors/thin views;
- `django-save-orchestration` про конкретный lifecycle pattern вокруг `save()`.

**Что включить в опциональный HackSoft-derived набор**
Я бы включил туда только реально связанные правила, без дублей с `python`, `django`, `django-drf`.

Примерный состав:
- Keep views, APIs, admin actions, and tasks thin; orchestration belongs to the application layer.
- Place write workflows in services and reusable reads in selectors.
- Do not put business workflows in serializers, forms, signals, or model `save()` methods.
- Use explicit service boundaries with typed keyword-only arguments where it improves call clarity.
- Treat serializers and forms as boundary validation and mapping tools, not as the home of business rules.
- Prefer explicit orchestration over implicit signal-driven flows for project-internal behavior.
- When post-commit side effects matter, dispatch them via `transaction.on_commit`.
- Organize tests by application layer such as `tests/services/`, `tests/selectors/`, `tests/apis/`.

Это уже выглядит как coherent opt-in style, а не как случайный набор локальных привычек.

**Что включить в отдельный фрагмент про unified `save()` pattern**
Здесь я бы был очень аккуратен и явно пометил его как optional pattern, а не как default.

Примерный shape:
- When create and update orchestration are mostly symmetric, a shared `save()` wrapper may be used to avoid duplicated orchestration logic.
- In DRF, `perform_create()` and `perform_update()` may delegate to a shared local `save()` method instead of duplicating the workflow.
- In Django CBVs, `form_valid()` may delegate to a shared local `save()` method when the project adopts that pattern consistently.
- Distinguish create from update explicitly via instance state, such as `serializer.instance is None` or primary-key presence, rather than duplicating near-identical flows.
- Keep the wrapper focused on orchestration around persistence boundaries; business rules still belong in the chosen application layer.
- When post-save work depends on a successful transaction commit, use `transaction.on_commit` instead of running it immediately after persistence.
- Do not mix this wrapper pattern with competing save hooks inside the same module or app.

Это, на мой взгляд, честно отражает ваш тезис: pattern полезный, но только как осознанная локальная конвенция.

**Как я бы это назвал**
Самые удачные варианты, на мой взгляд:
- `django-hacksoft-style`
- `django-service-flow`
- `django-save-orchestration`

Из них:
- `django-hacksoft-style` честнее по происхождению;
- `django-service-flow` нейтральнее по тону;
- `django-save-orchestration` лучше для фрагмента именно про unified `save()`.

**Моё мнение по вашей идее**
Да, это хорошая идея. Более того, я считаю её архитектурно правильнее, чем пытаться дальше “усреднять” `django-save-lifecycle.md` так, чтобы он одновременно был и baseline, и opinionated pattern. Эти роли лучше развести.

Если хотите, следующим шагом я могу сразу внести это в `ai-standards`:
1. добавить новый opt-in фрагмент для HackSoft-derived подхода;
2. выделить отдельный фрагмент для unified `save()` pattern с правилом про `transaction.on_commit`;
3. упростить или переписать текущий `django-save-lifecycle.md`, чтобы он либо исчез как промежуточный слой, либо стал тонкой обвязкой вокруг новых явных фрагментов.

## Структура новых opt-in фрагментов и судьба django-save-lifecycle

**Question**

(0tdk5c3)
> Новый фрагмент, например stacks/django-hacksoft-style.md или stacks/django-service-flow.md: opt-in набор правил, основанный на HackSoft-style архитектуре.

`stacks/django-hacksoft-style.md` выглядит лучше, и в самом файле обязательно нужно разместить URL на первоисточник (Hasksoft Django style guide) .

(0tdk5eo)
> Отдельный фрагмент, например stacks/django-save-orchestration.md: opt-in pattern для unified save() flow, если хотите сделать его включаемым независимо от полного HackSoft-style слоя.

Да, лучше это импортировать отдельным фрагментом в тех проектах, где в этом паттерне видится смысл.
В комментариях в markdown-файле обязательно описать мотивацию паттерна, и когда его уместно использовать – твоё замечание:
> Почему я не считаю это universal best practice:
> 
> официальные extension points в DRF для этого именно perform_create() и perform_update(), и их использование само по себе не является smell;
> в части проектов различие между create и update быстро становится существенным: разные permissions, разные invariants, разные side effects, разные audit rules;
> единый save() снижает шум там, где lifecycle действительно симметричен, но может скрывать важные семантические различия там, где create/update начинают расходиться;
> кастомный wrapper save() требует, чтобы команда приняла эту конвенцию целиком, иначе он становится ещё одним локальным слоем поверх стандартного DRF API.

я нахожу абсолютно релевантным.

(0tdk5l8) Итого:
> 1. добавить новый opt-in фрагмент для HackSoft-derived подхода;

Принимается с учётом `0tdk5c3`.

> 2. выделить отдельный фрагмент для unified save() pattern с правилом про transaction.on_commit;

Обязательно. Наверное, это в `django.md`? Поскольку это касается именно Django ORM.

> 3. упростить или переписать текущий django-save-lifecycle.md, чтобы он либо исчез как промежуточный слой, либо стал тонкой обвязкой вокруг новых явных фрагментов.

Здесь у меня скорее вопрос: `django-save-lifecycle.md` – что от него останется после `0tdk5c3` и `0tdk5eo`?

**Answer**

Я бы не помещал unified `save()` pattern в `django.md`.

Причина простая: несмотря на связь с Django ORM, это не framework baseline, а архитектурная конвенция. В `django.md` должны оставаться вещи, которые почти всегда уместны для Django-проекта. Unified `save()` под это не подпадает. Поэтому правильнее держать его отдельным opt-in fragment, как вы и предложили.

По `0tdk5l8` я бы зафиксировал такую целевую структуру.

**Целевая схема**
- `stacks/django.md`
  Нейтральный baseline Django.
- `stacks/django-drf.md`
  Нейтральный baseline DRF.
- `stacks/django-hacksoft-style.md`
  Opt-in слой с явной ссылкой на первоисточник HackSoft Django Styleguide.
- `stacks/django-save-orchestration.md`
  Opt-in слой для unified `save()` pattern, с мотивацией, границами применимости, рисками и правилом про `transaction.on_commit`.

**Что делать с `django-save-lifecycle.md`**
После появления двух новых фрагментов я вижу только два разумных варианта.

1. Удалить `django-save-lifecycle.md` совсем.
Это мой предпочтительный вариант.
Причина: его содержимое сейчас смешивает два разных смысла:
- общий тезис “предпочитать explicit orchestration вместо signals”;
- конкретный локальный паттерн с `save()` wrapper.

После выделения `django-hacksoft-style.md` и `django-save-orchestration.md` этот файл становится промежуточным слоем без собственной ответственности.

2. Оставить `django-save-lifecycle.md` как тонкий compatibility fragment.
Это допустимо, если вы хотите мягкую миграцию для уже существующих downstream manifests.
Тогда он должен стать очень коротким и честным:
- сказать, что save-lifecycle orchestration должна быть explicit;
- не навязывать конкретный hook pattern;
- ссылаться по смыслу на `django-hacksoft-style` и `django-save-orchestration` как на более конкретные opt-in extensions.

Но такой совместимый слой имеет смысл только если у вас уже есть проекты, которые реально подключают `django-save-lifecycle` и вы не хотите ломать их manifests прямо сейчас.

**Мой ответ на ваш вопрос “что от него останется?”**
Если идти по архитектурно чистому пути, от `django-save-lifecycle.md` не должно остаться ничего. Его роль распадается на два более честных фрагмента:
- архитектурный стиль HackSoft-derived;
- отдельный opt-in паттерн unified `save()`.

Если идти по пути обратной совместимости, от него может остаться только тонкая обвязка без конкретного `save(self, serializer, additional_data=None)` recipe и без запрета на `perform_create()` / `perform_update()`.

**Как я бы сформулировал это решение**
- `django-save-lifecycle.md` больше не нужен как самостоятельный источник правил.
- Его содержимое следует разложить на:
  - `django-hacksoft-style.md`
  - `django-save-orchestration.md`
- Сам unified `save()` pattern не должен жить в `django.md`, потому что это не baseline, а explicit architectural choice.

**Практически**
Я бы следующим шагом сделал именно так:
1. Создать `fragments/stacks/django-hacksoft-style.md` с URL на первоисточник.
2. Создать `fragments/stacks/django-save-orchestration.md` с мотивацией, когда применять, когда не применять, и обязательным правилом про `transaction.on_commit`.
3. Зарегистрировать оба в `registry.toml`.
4. Удалить `django-save-lifecycle.md`.
5. Обновить `README` и тесты рендера.

Если хотите сохранить совместимость, можно вместо шага 4 сначала превратить `django-save-lifecycle.md` в deprecated compatibility fragment, а удалить его позже. Но если обратная совместимость сейчас не критична, я бы удалял сразу.

## Размещение unified save как архитектурной конвенции вне базовых Django правил

**Question**

(0tdk5v7)
> Практически
> Я бы следующим шагом сделал именно так:

Поддерживаю в полном объёме.

> Если хотите сохранить совместимость

Сейчас никакого сохранения совместимости.

(0tdk5xe) Хочу уточнить:
> Я бы не помещал unified save() pattern в django.md.
> Причина простая: несмотря на связь с Django ORM, это не framework baseline, а архитектурная конвенция. В django.md должны оставаться вещи, которые почти всегда уместны для Django-проекта. Unified save() под это не подпадает. Поэтому правильнее держать его отдельным opt-in fragment, как вы и предложили.

А куда ты считаешь уместным поместить эту архитектурную конвенцию?
Или ты находишь, что ей вообще не место в правилах?

**Answer**

Ей точно есть место в правилах. Я не считаю, что такой паттерн нужно выносить за пределы `ai-standards`.

Моя позиция только в том, что ему не место в `django.md`, потому что `django.md` должен оставаться baseline-слоем. А unified `save()` pattern:
- не является частью самого Django;
- не является общепринятой практикой для всех Django-проектов;
- имеет смысл только при определённой архитектуре и достаточно симметричном lifecycle.

То есть это не “неправильное правило”, а правило другого уровня.

**Куда его уместно поместить**
Наиболее уместное место: отдельный opt-in stack fragment, то есть именно то, что мы уже обсуждали как `stacks/django-save-orchestration.md`.

Почему именно туда:
- он относится к конкретному технологическому стеку Django/DRF;
- он описывает повторяемый architectural pattern;
- он должен подключаться только там, где команда сознательно принимает этот flow;
- он не должен навязываться всем downstream проектам по умолчанию.

Иными словами, это хороший кандидат на reusable fragment, но плохой кандидат на baseline fragment.

**Почему не в `core`**
Потому что это не кросс-технологическое правило. Оно завязано на Django/DRF lifecycle hooks, ORM-персистентность, `perform_create`, `perform_update`, `form_valid`, `transaction.on_commit`. В `core` такому правилу не место.

**Почему не в `django.md`**
Потому что `django.md` должен отвечать на вопрос “что почти всегда уместно в Django-проекте?”. Unified `save()` на этот вопрос не проходит.

**Почему не только в `django-hacksoft-style.md`**
Можно было бы включить его туда как часть HackSoft-derived стиля, но у вас есть хорошее наблюдение: сам паттерн может быть полезен и вне полного HackSoft-style слоя. Значит, лучше дать ему самостоятельный opt-in fragment, чтобы его можно было подключать независимо.

То есть правильная композиция, на мой взгляд, такая:
- `django.md` — baseline;
- `django-drf.md` — DRF baseline;
- `django-hacksoft-style.md` — opt-in архитектурный стиль;
- `django-save-orchestration.md` — opt-in lifecycle pattern.

**Как я бы описал его статус в стандарте**
Не как “best practice”, а как:
- “recommended optional pattern when create/update orchestration is mostly symmetric”;
- “project-level convention that must be adopted consistently within a module or app”;
- “not a replacement for Django/DRF standard hooks, but a wrapper strategy built on top of them”.

Это важная формулировка: паттерн не спорит с официальными hooks, а организует их использование определённым способом.

**Итог**
Да, этому паттерну место в правилах есть.
Но его место:
- не в `core`,
- не в `django.md`,
- а в отдельном явно подключаемом fragment вроде `stacks/django-save-orchestration.md`.

Если хотите, следующим шагом я могу уже без дополнительного обсуждения реализовать всю согласованную схему:
- добавить `django-hacksoft-style.md`,
- добавить `django-save-orchestration.md`,
- удалить `django-save-lifecycle.md`,
- зарегистрировать новые фрагменты,
- обновить README и тесты,
- прогнать проверки.

## Реализовать согласованную схему

**Question**

Всё верно. реализуй согласованную схе му.

**Answer**

Реализую согласованную схему целиком: добавлю два новых opt-in фрагмента, удалю `django-save-lifecycle.md`, зарегистрирую новые stack ids, обновлю README/README.ru и тесты, затем перегенерирую `AGENTS.md` и прогоню проверки.

Дальше внесу сами фрагменты и обновлю примеры стеков в README так, чтобы `django-save-lifecycle` исчез полностью, а новые opt-in слои были видимы как явный выбор.

Новые фрагменты добавлены, старый `django-save-lifecycle` удалён. Сейчас вычищу остаточные ссылки на старый id, перегенерирую `AGENTS.md` и прогоню полный набор проверок.

`rg`, `render`, `ruff`, `mypy` уже зелёные. Осталось добить `pytest` и `ai_sync check`, затем сверю итоговый diff и предложу следующий commit message.

Есть один важный сигнал: по `git diff --stat` не появились новые файлы-фрагменты, хотя они добавлены на диск. Сейчас быстро проверю статус, чтобы убедиться, что они действительно попали в рабочее дерево и не потерялись из-за фильтрации вывода.

Схема реализована.

Добавлены два новых opt-in фрагмента: [fragments/stacks/django-hacksoft-style.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/django-hacksoft-style.md:1) и [fragments/stacks/django-save-orchestration.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/django-save-orchestration.md:1). В первом есть явная ссылка на первоисточник HackSoft Django Styleguide и зафиксирован его статус как opt-in architectural style. Во втором вынесен unified `save()` pattern как отдельная подключаемая конвенция, с описанием мотивации, границ применимости, причин почему это не universal best practice, и с явным правилом про `transaction.on_commit`.

Старый [fragments/stacks/django-save-lifecycle.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/django-save-lifecycle.md:1) удалён. Также обновлены [registry.toml](/home/shtirliz/workspace/myself/ai-standards/registry.toml:1), [README.md](/home/shtirliz/workspace/myself/ai-standards/README.md:1), [README.ru.md](/home/shtirliz/workspace/myself/ai-standards/README.ru.md:1) и [tests/test_ai_sync.py](/home/shtirliz/workspace/myself/ai-standards/tests/test_ai_sync.py:1), чтобы примеры и рендер-тесты использовали новые stack ids: `django-hacksoft-style` и `django-save-orchestration`.

Проверка прошла: `rtk uv run ruff check`, `rtk uv run mypy`, `rtk uv run python -m pytest -q`, `rtk uv run python scripts/ai_sync.py check --project-root /home/shtirliz/workspace/myself/ai-standards`.

Текущее состояние рабочего дерева:
- изменены `README.md`, `README.ru.md`, `registry.toml`, `tests/test_ai_sync.py`
- удалён `fragments/stacks/django-save-lifecycle.md`
- добавлены `fragments/stacks/django-hacksoft-style.md` и `fragments/stacks/django-save-orchestration.md`

Если хотите, следующим сообщением я предложу точный commit message для этого шага и после подтверждения сразу его оформлю на текущей ветке.
