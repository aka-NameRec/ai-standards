<h2>Оглавление</h2>

- [Проверка дублирования правил между django-service-layer и django-hacksoft-style](#проверка-дублирования-правил-между-django-service-layer-и-django-hacksoft-style)
- [Есть ли у нас отдельные общие правила слоистой архитектуры](#есть-ли-у-нас-отдельные-общие-правила-слоистой-архитектуры)
- [Верификация выделения общих backend frontend правил и зависимостей фрагментов](#верификация-выделения-общих-backend-frontend-правил-и-зависимостей-фрагментов)
- [Верификация тезисов о слиянии Django фрагментов и выделении layering rules](#верификация-тезисов-о-слиянии-django-фрагментов-и-выделении-layering-rules)
- [Слияние с сохранением HackSoft framing и opt in характера подхода](#слияние-с-сохранением-hacksoft-framing-и-opt-in-характера-подхода)
- [Нужно ли оставлять django-naming отдельным стеком](#нужно-ли-оставлять-django-naming-отдельным-стеком)
- [Слияние django-naming в django-service-layer и удаление отдельного stack](#слияние-django-naming-в-django-service-layer-и-удаление-отдельного-stack)
- [Ветка коммит релиз 1.2.0 и подготовка тега для 0tdkklm](#ветка-коммит-релиз-120-и-подготовка-тега-для-0tdkklm)

## Проверка дублирования правил между django-service-layer и django-hacksoft-style

**Question**

(0tdkklm) Давай вернёмся в ai-standards.
Коллега утверждает, что правила в `fragments/stacks/django-service-layer.md` и в `fragments/stacks/django-hacksoft-style.md` частично дублируются.
Насколько это соответствует действительности?

**Answer**

Сначала найду репозиторий `ai-standards`, загружу его `AGENTS.md` и ConPort, затем сравню оба фрагмента по смысловым блокам, а не только по совпадающим словам.

Нашёл `ai-standards`. Сейчас загружу его локальные правила и контекст проекта, после этого разберу оба markdown-фрагмента по пересекающимся требованиям и по отличиям.

Контекст проекта поднят. Теперь читаю оба фрагмента целиком и раскладываю их на правила: слой сервиса, ORM/QuerySet, транзакции, селекторы, эффекты, типовые паттерны. Это покажет реальное пересечение, а не просто похожую терминологию.

Уже видно, что дублирование есть, но оно не полное: один фрагмент выглядит как конкретный operational subset, второй как opt-in стиль более высокого уровня. Доберу номера строк и сверю, где именно они повторяют одно и то же правило разной формулировкой.

Да, утверждение в целом верное.

`[fragments/stacks/django-service-layer.md](../fragments/stacks/django-service-layer.md:7)` и `[fragments/stacks/django-hacksoft-style.md](../fragments/stacks/django-hacksoft-style.md:11)` действительно частично дублируют друг друга по базовой архитектурной идее. Пересечение заметное, но не тотальное.

Что явно повторяется по смыслу:
- Тонкие entry points: `service-layer` говорит про thin views/API/Celery tasks ([строка 8](../fragments/stacks/django-service-layer.md:8)), `hacksoft-style` про thin views/API/admin/background tasks ([строка 12](../fragments/stacks/django-hacksoft-style.md:12)).
- Разделение write/read между services и selectors: [service-layer: 9-10](../fragments/stacks/django-service-layer.md:9), [hacksoft-style: 13](../fragments/stacks/django-hacksoft-style.md:13).
- Запрет бизнес-логики в serializers/forms/model save/signals/managers: [service-layer: 11](../fragments/stacks/django-service-layer.md:11), [hacksoft-style: 14](../fragments/stacks/django-hacksoft-style.md:14).
- `transaction.on_commit`: [service-layer: 22](../fragments/stacks/django-service-layer.md:22), [hacksoft-style: 20](../fragments/stacks/django-hacksoft-style.md:20).
- Layer-based testing layout: [service-layer: 25-27](../fragments/stacks/django-service-layer.md:25), [hacksoft-style: 22-23](../fragments/stacks/django-hacksoft-style.md:22).

Что не дублируется и делает фрагменты разными:
- `django-hacksoft-style` задаёт рамку применения: это opt-in architectural style, а не baseline ([строки 7-10](../fragments/stacks/django-hacksoft-style.md:7)).
- `django-hacksoft-style` добавляет boundary semantics: serializers/forms как boundary-validation/mapping tools, явная orchestration вместо signal-driven flow, reviewability границ ([17-20](../fragments/stacks/django-hacksoft-style.md:17)).
- `django-service-layer` гораздо более operational: ORM как persistence abstraction, `full_clean()` перед `save()`, keyword-only args, type annotations, `django-filter`, конкретика по Celery retry handling, и более жёсткий testing guidance ([12-27](../fragments/stacks/django-service-layer.md:12)).

Итоговая оценка:
- По intent и core rules дублирование существенное.
- По детализации и назначению фрагменты всё же не идентичны.
- Практически `django-service-layer` выглядит как конкретизированный поднабор/операционализация HackSoft-style, а `django-hacksoft-style` как meta-fragment, который объясняет, когда и зачем этот стиль вообще включать.

Если нужно дать короткий вердикт: дублирование есть примерно на уровне архитектурного ядра, но не на уровне всех правил.  
Если захотите, следующим сообщением могу предложить, как это аккуратно развести без потери смысла: например, оставить `django-hacksoft-style` как umbrella-стиль, а `django-service-layer` сократить до чисто дополнительных конвенций без повторения базовых принципов.

## Есть ли у нас отдельные общие правила слоистой архитектуры

**Question**

Хм... А такой вопрос тебе: правила для слоистой архитектуры (не применительно к Python/Django) у нас вообще отдельно сформулированы?

**Answer**

Проверю, есть ли в `ai-standards` отдельные общие фрагменты про layering вне Django/Python, и сверю это с тем, что уже зашито в базовые архитектурные правила.

Похоже, отдельного общего stack-фрагмента про layer architecture нет. Есть только короткое ядро в `core/architecture`, а дальше уже stack-specific реализации вроде Django, SQLAlchemy, Spring, FSD. Сейчас открою это ядро, чтобы ответить точно по формулировкам.

Да, но очень коротко.

Сейчас общие, не привязанные к Python/Django, правила для слоистой архитектуры у вас сформулированы только в `[fragments/core/architecture.md](../fragments/core/architecture.md:1)`. Там всего несколько базовых инвариантов:

- service layer содержит только business logic
- service layer не ходит напрямую в ORM
- service layer не вызывает напрямую внешние протоколы вроде HTTP
- доступ к БД должен быть спрятан за repository-style abstraction

Это именно общий cross-stack слой, но он довольно узкий и явно backend-oriented.

Отдельного самостоятельного общего фрагмента вида `layered-architecture`, `application-layer`, `hexagonal`, `clean-architecture` или чего-то подобного я в репозитории не вижу. Дальше layering уже раскрывается через stack-specific фрагменты:
- `[fragments/stacks/sqlalchemy.md](../fragments/stacks/sqlalchemy.md:19)` для repository/session/transaction details
- `[fragments/stacks/spring.md](../fragments/stacks/spring.md:2)` для thin controllers, services, transactional boundaries
- Django-фрагменты для service/selector style
- `[fragments/stacks/fsd.md](../fragments/stacks/fsd.md:1)` как отдельный frontend layering stack

То есть ответ такой: в общем виде правила есть, но только как минимальное ядро в `core/architecture`; полноценного отдельного vendor-neutral фрагмента про layered architecture сейчас нет. Это, кстати, хорошо объясняет, почему Django-фрагменты начали частично дублировать друг друга: общего промежуточного слоя между `core/architecture` и конкретным stack-style сейчас не хватает.

Если хочешь, следующим сообщением могу предложить конкретную декомпозицию: что вынести в новый общий `stacks/layered-application.md`, а что оставить в Django/HackSoft-specific фрагментах.

## Верификация выделения общих backend frontend правил и зависимостей фрагментов

**Question**

> Если хочешь, следующим сообщением могу предложить конкретную декомпозицию: что вынести в новый общий stacks/layered-application.md, а что оставить в Django/HackSoft-specific фрагментах.

Да, мне бы хотелось выделить правила слоистой архитектуры вообще, и отдельно – для backend и frontend.
В таком случае правила слоистой архитектуры именно для Django было бы логично разместить в `django-hacksoft-style`, поскольку именно у Hacksoft я встретил системное изложение применитьелдьно к Django.
Дополнительно, считаю важным поддержать зависимости между фрагментами. В частности, нахожу правильным, если бы рекомендации Hacksoft style guide ссылались, и приводили к включению в итоговый AGENTS.md фрагмента по слоистой архитектуре, общего для всех языков и фреймворков.
На мой взгляд, это заметно упростит проектирование наполнения `ai.project.toml`.
Пожалуйста, верифицируй эту идею.

**Answer**

Проверю две вещи: насколько предложенная декомпозиция согласуется с текущей структурой фрагментов, и поддерживает ли рендерер зависимые фрагменты из коробки или это потребует изменений в модели манифеста.

Идея в целом корректная и хорошо согласуется с текущей архитектурой `ai-standards`, но с одной важной оговоркой: поддержку зависимостей лучше сначала реализовывать не как новый механизм манифеста, а как композицию через `registry.toml`.

Почему идея выглядит сильной:

- Сейчас общий слой слишком тонкий: `[fragments/core/architecture.md](../fragments/core/architecture.md:1)` содержит только несколько backend-ориентированных инвариантов и не покрывает отдельно frontend/backend layering.
- Stack composition уже является базовой моделью репозитория. Это прямо отражено в `[registry.toml](../registry.toml:1)`, где один stack name может разворачиваться в несколько fragment ids. Пример: `java-spring = ["stacks/java", "stacks/spring", "stacks/spring-data-jpa"]` и `vue-query = ["stacks/tanstack-query", "stacks/vue"]`.
- Рендерер это уже поддерживает без дополнительных сущностей: `[scripts/ai_sync.py](../scripts/ai_sync.py:258)` разворачивает стек в список fragment ids, а `[scripts/ai_sync.py](../scripts/ai_sync.py:280)` дедуплицирует их с сохранением порядка. То есть зависимость вида “HackSoft style включает общий layering fragment” уже можно выразить существующим способом.

Главная оговорка:

- В репозитории сейчас нет first-class механизма “fragment depends on fragment”. Есть только “manifest выбирает stack/feature”, а registry разворачивает это в fragments.
- Поэтому если делать именно “`django-hacksoft-style` ссылается на и автоматически включает общий fragment”, то на сегодня это логичнее моделировать как alias-composition в `registry.toml`, а не как новые поля `depends_on` в самих markdown-фрагментах или в `ai.project.toml`.
- Иначе придётся менять формат registry/manifest и код рендера, хотя польза пока достигается уже имеющимися средствами.

По существу декомпозиции я бы верифицировал идею так:

1. Общий слой “layered architecture” стоит выделить.
2. Отдельные backend/frontend layering rules тоже стоит выделить.
3. Django-specific layering действительно логичнее держать в `django-hacksoft-style`, а не в `django-service-layer`.
4. `django-service-layer` после этого либо становится избыточным, либо должен быть ужат до узких Django operational conventions, которые не покрывает HackSoft-style.

Наиболее естественная структура выглядит так:

- `stacks/layered-architecture`
  Общие инварианты слоистости вне языка и фреймворка.
  Примеры: явные границы слоёв, зависимости направлены inward/upward only, orchestration не размазывается по boundary adapters, side effects держатся на edges, cross-layer contracts reviewable.

- `stacks/backend-layered-architecture`
  Backend-специфика.
  Примеры: transport boundary отдельно от application/service layer, persistence behind abstractions, external integrations behind adapters, transaction boundaries на use-case/service уровне, thin controllers/handlers/jobs.

- `stacks/frontend-layered-architecture`
  Frontend-специфика.
  Примеры: UI layer отдельно от state/query/domain workflows, side effects и data fetching не размазываются по случайным компонентам, container/presentational or feature boundary rules, public API у slices/modules, запрет deep imports между несоседними слоями.

- `stacks/django-hacksoft-style`
  Только Django/HackSoft-specific concretization.
  Примеры: services/selectors, serializers/forms as boundary tools, explicit anti-signal guidance, `transaction.on_commit`, test layout by layer, возможно `full_clean()` и naming rules только если это действительно HackSoft-derived и не претендует на generic backend guidance.

Как это можно выразить без нового синтаксиса манифеста:

- `django-hacksoft-style = ["stacks/layered-architecture", "stacks/backend-layered-architecture", "stacks/django-hacksoft-style"]`
- Аналогично можно будет делать `spring`, `fastapi`, `sqlalchemy` aliases, если захотите сделать layering частью рекомендованной композиции.

Что это даст:

- `ai.project.toml` станет проще: downstream-проекту достаточно выбрать `django-hacksoft-style`, а не помнить вручную весь набор layering fragments.
- Дублирование уменьшится: общие правила живут в одном месте, Django-фрагмент только конкретизирует их.
- README и composition examples станут чище, потому что появится явная иерархия: generic -> backend/frontend -> framework style.

Что я бы не рекомендовал:

- Не делать слишком абстрактный “универсальный layering fragment”, который пытается одинаково описывать и backend, и frontend, и event-driven, и MVC, и FSD. Такой слой быстро станет либо банальным, либо внутренне противоречивым.
- Не переносить в общий fragment Django-specific понятия вроде selectors, `full_clean()`, `transaction.on_commit`, serializers/forms, model `save()` и signals.
- Не вводить новый dependency DSL в `ai.project.toml`, пока registry aliases уже решают задачу.

Короткий вывод: идея правильная, архитектурно совместимая с текущим `ai-standards` и может быть реализована эволюционно без изменения формата манифеста. Самая сильная версия этой идеи: вынести `layered-architecture`, `backend-layered-architecture`, `frontend-layered-architecture`, а `django-hacksoft-style` превратить в composed stack alias плюс Django-specific fragment.

Если хочешь, следующим сообщением я могу перейти от верификации к конкретному проектному предложению: перечислить точный состав новых фрагментов и показать, как должны измениться `registry.toml`, `django-hacksoft-style.md`, `django-service-layer.md` и примеры в `README.md`/`README.ru.md`.

## Верификация тезисов о слиянии Django фрагментов и выделении layering rules

**Question**

(0tdkm07)
> с одной важной оговоркой: поддержку зависимостей лучше сначала реализовывать не как новый механизм манифеста, а как композицию через registry.toml.

Да, согласен с оговоркой. Если зависимости можно поддержать с помощью существующего операционного языка – нечего множить сущности.

> django-service-layer после этого либо становится избыточным, либо должен быть ужат до узких Django operational conventions, которые не покрывает HackSoft-style.

Мне представляется логичным вынести в django-service-layer объединение множества правил, содержащихся в нём, и в django-hacksoft-style. При этом django-hacksoft-style упразднить, но не забыть перенести оттуда комментарий со ссылкой на Hacksoft в django-service-layer.
Мотивация: django-service-layer действительно может содержать какие-то дополнительные вещи, но он, безусловно, основан на django-hacksoft-style.

> Общий слой “layered architecture” стоит выделить.
> Отдельные backend/frontend layering rules тоже стоит выделить.

С этим согласен.

(0tdkm02) Пожалуйста, верифицируй тезисы, обозначенные выше.

**Answer**

Да, эти тезисы выглядят состоятельными.

Первое: зависимость через `registry.toml`, а не через новый синтаксис манифеста, это правильное решение. Текущий рендерер уже работает именно в этой модели: stack name разворачивается в список fragment ids, порядок сохраняется, дубликаты убираются. Для вашей цели этого достаточно. Добавление отдельного механизма `depends_on` сейчас дало бы больше сложности, чем пользы.

Второе: объединить `django-hacksoft-style` в `django-service-layer` и убрать отдельный `django-hacksoft-style` тоже выглядит логично. По факту нынешний `django-hacksoft-style` почти целиком задаёт рамку того же service-and-selector подхода, а `django-service-layer` уже содержит более прикладные правила того же семейства. То есть у вас сейчас не два независимых стека, а один стек, разрезанный на “идеологический” и “операционный” слои. Если целевая модель репозитория должна быть проще для downstream-проектов, то один явный стек `django-service-layer` лучше двух почти пересекающихся.

При этом важна одна оговорка: если `django-hacksoft-style` упраздняется, его смысл нельзя просто потерять. В `django-service-layer` действительно стоит сохранить:
- provenance-комментарий со ссылкой на HackSoft styleguide
- явное указание, что это opt-in architectural style для Django-проектов, а не baseline для любого Django-кода
- boundary semantics, которые сейчас лучше выражены именно в `django-hacksoft-style`: serializers/forms как boundary tools, предпочтение explicit orchestration вместо signal-driven flows, `transaction.on_commit` для post-commit side effects

Иначе после слияния фрагмент станет просто набором практик без чёткой архитектурной рамки, а это ухудшит читаемость.

Третье: выделить общий `layered-architecture`, а также отдельные `backend-layered-architecture` и `frontend-layered-architecture`, это хорошая декомпозиция. Она решает сразу две реальные проблемы:
- сейчас `core/architecture` слишком узкий и фактически backend-centric
- Django-фрагменты вынуждены повторно проговаривать общие правила, потому что промежуточного уровня абстракции нет

Именно в такой схеме `django-service-layer` сможет стать нормальной специализацией:
- `layered-architecture` задаёт общие инварианты слоёв
- `backend-layered-architecture` уточняет transport/application/persistence/integration boundaries
- `django-service-layer` добавляет уже Django-specific concretization через services, selectors, serializers/forms, signals, `full_clean()`, `transaction.on_commit`, test layout

С практической точки зрения это ещё и упростит `ai.project.toml`. Вместо ручного перечисления общих и Django-специфичных архитектурных частей можно будет зарегистрировать `django-service-layer` как composed stack alias в `registry.toml`, например в духе:
- `django-service-layer = ["stacks/layered-architecture", "stacks/backend-layered-architecture", "stacks/django-service-layer"]`

Это соответствует уже существующему стилю репозитория, как у `java-spring` и `vue-query`.

Мой итоговый вердикт такой:
- тезис про зависимости через `registry.toml` верный
- тезис про слияние `django-hacksoft-style` в `django-service-layer` верный
- тезис про выделение общего layering и отдельных backend/frontend layering fragments верный
- архитектурно это улучшит и чистоту репозитория, и удобство downstream composition

Единственный риск: при слиянии нельзя оставить `django-service-layer` только как “сборник техник”. Нужно сохранить в нём и HackSoft-derived framing, и явное указание на opt-in характер этого подхода.

Если хочешь, следующим сообщением я могу уже оформить это как точное change proposal: какие файлы добавить, какие удалить, как переписать `registry.toml`, и что именно должно остаться в новом `django-service-layer.md`.

## Слияние с сохранением HackSoft framing и opt in характера подхода

**Question**

(0tdkm7l) Да, отлично. Давай проделаем предложенное.

> Единственный риск: при слиянии нельзя оставить django-service-layer только как “сборник техник”. Нужно сохранить в нём и HackSoft-derived framing, и явное указание на opt-in характер этого подхода.

Пожалуйста, ути это обстоятельство, я рассматриваю его как очень важное.

**Answer**

Перехожу к патчу в `ai-standards`: сначала соберу точный срез файлов, где зашиты текущие Django stack names, composition examples и тесты рендера, затем внесу связанный набор изменений одним проходом.

Картина уже ясна: нужно не просто слить два Django-фрагмента, а одновременно ввести новые общие architectural stacks, перевести `django-service-layer` в роль composed stack alias и обновить документацию и тесты под новую композицию.

Сейчас внесу сами правки: добавлю три новых architectural stack fragments, солью HackSoft framing в `django-service-layer`, удалю отдельный `django-hacksoft-style` из registry и документации, и добью это тестами рендера.

Правку делаю минимально, но связно: без нового механизма зависимостей, только через composition в `registry.toml`; при этом важный opt-in framing HackSoft останется внутри нового `django-service-layer`, а не потеряется при слиянии.

Патч внесён. Сейчас прогоню целевые проверки: найду остаточные ссылки на удалённый stack name и выполню рендер-тесты, чтобы убедиться, что composition через `registry.toml` работает как задумано.

`rtk` отработал корректно: проблема не в нём, а в отсутствии standalone `pytest` в окружении. Перехожу на рекомендуемый путь через `uv run python -m pytest` и доберу ещё быстрый рендер-чек.

Остался один точечный тестовый разнобой: ожидание в тесте осталось от старой формулировки. Исправлю его и повторю проверки.

Сделал реорганизацию в `ai-standards` так, как мы согласовали.

Главное изменение: `django-hacksoft-style` упразднён как отдельный stack, а его opt-in framing и ссылка на первоисточник HackSoft перенесены в [fragments/stacks/django-service-layer.md](../fragments/stacks/django-service-layer.md:1). При этом `django-service-layer` теперь разворачивается через `registry.toml` в общий [layered-architecture](../fragments/stacks/layered-architecture.md:1), [backend-layered-architecture](../fragments/stacks/backend-layered-architecture.md:1) и сам Django-specific фрагмент. Важное для тебя обстоятельство сохранено: `django-service-layer` по-прежнему явно помечен как opt-in architectural style, а не как Django baseline.

Отдельно добавил [frontend-layered-architecture](../fragments/stacks/frontend-layered-architecture.md:1), обновил [registry.toml](../registry.toml:1), [README.md](../README.md:1), [README.ru.md](../README.ru.md:1), а также зафиксировал решение в новых decision records: [EN](decisions/2026-04-16-extract-layered-architecture-and-merge-django-style.md) и [RU](decisions/2026-04-16-extract-layered-architecture-and-merge-django-style.ru.md). Рендер-тесты прошли: `25 passed`. Дополнительно `scripts/ai_sync.py check --project-root /home/shtirliz/workspace/myself/ai-standards` подтвердил, что текущий `AGENTS.md` в самом репозитории актуален.

Небольшая оговорка: исторические chat-export файлы и старый decision record по Python-инфраструктуре по-прежнему упоминают `django-hacksoft-style` как часть прошлой структуры. Я их сознательно не переписывал, чтобы не ломать исторический контекст.

## Нужно ли оставлять django-naming отдельным стеком

**Question**

(0tdkmo6) Ok, но вопрос тебе: `django-naming` не следует ли включить в стек `django`, а нек выделять его как отдельный стек?
Вообще, нужен ли `stacks/django-naming` отдельно?

**Answer**

Проверю сам фрагмент `django-naming`, где он используется и насколько его правила действительно тянут на отдельный opt-in stack, а не на обычную часть `django` или `django-service-layer`.

Судя по текущему содержимому, отдельно `django-naming` держать, скорее всего, не стоит.

Сейчас [fragments/stacks/django-naming.md](../fragments/stacks/django-naming.md:1) очень маленький и содержит всего три правила:
- `<entity>_<action>` для services/selectors
- `<Entity><Action>Api` для API views
- naming для test files и test classes

Из них только первое действительно жёстко связано с HackSoft-derived service/selector style. Второе уже спорнее как shared standard, потому что naming API views сильно зависит от того, использует ли проект DRF viewsets, generic views, CBV, function views, router-based naming и так далее. Третье вообще выглядит не как Django-specific stack, а как обычная локальная naming convention для тестов.

Поэтому мой вывод такой:

- В текущем виде отдельный stack `django-naming` слабоват и вряд ли оправдывает отдельную сущность в манифесте.
- Включать его в `django` целиком я бы не стал, потому что `django` у вас сейчас позиционируется как framework baseline, а naming conventions такого рода уже выглядят как opinionated style, а не baseline.
- Самое логичное место для большей части этого фрагмента сейчас — `django-service-layer`, если правило относится именно к HackSoft-style архитектуре.

Практически я бы рекомендовал так:

1. Перенести правило `<entity>_<action>` в `django-service-layer`.
2. Подумать, нужно ли вообще сохранять `<Entity><Action>Api` как shared rule.
3. Правило про `test_<name>.py` и `...Tests` либо удалить из shared stacks, либо перенести в какой-то более общий testing/naming fragment только если оно реально повторяется в нескольких проектах.
4. После этого удалить `stacks/django-naming` и убрать его из `registry.toml` и README.

Коротко:  
`django-naming` как отдельный стек, скорее всего, не нужен.  
В `django` его включать тоже не лучший вариант.  
Лучше либо распаковать полезную часть в `django-service-layer`, либо вовсе убрать этот фрагмент как слишком мелкий и слишком stylistic.

Если хочешь, я могу сразу сделать и эту следующую чистку: слить уместное из `django-naming` в `django-service-layer`, удалить отдельный stack и обновить тесты/README.

## Слияние django-naming в django-service-layer и удаление отдельного stack

**Question**

> Если хочешь, я могу сразу сделать и эту следующую чистку: слить уместное из django-naming в django-service-layer, удалить отдельный stack и обновить тесты/README.

Да, сделай пожалуйста.

**Answer**

Сделаю это как небольшую завершающую чистку: перенесу только осмысленную HackSoft-related naming convention в `django-service-layer`, удалю отдельный `django-naming` stack и синхронизирую README с registry.

Уточнение по содержанию: перенесу только `<entity>_<action>` для services/selectors. Именование API views и тестов в shared stack тащить не буду, это уже слишком style-specific и хуже композируется с нейтральным `django-drf`.

Добиваю верификацию: проверю, что `django-naming` больше не фигурирует в живой конфигурации, и снова прогоню тесты рендера.

Убрал `django-naming` как отдельный stack. Полезную часть, которая действительно связана с HackSoft-derived service/selector style, перенёс в [fragments/stacks/django-service-layer.md](../fragments/stacks/django-service-layer.md:1): теперь там есть правило про `<entity>_<action>` для services и selectors. Отдельный [django-naming.md](../fragments/stacks/django-naming.md:1) удалён, а [registry.toml](../registry.toml:1), [README.md](../README.md:1), [README.ru.md](../README.ru.md:1) и новый decision record обновлены под эту структуру.

Сознательно не переносил naming для API views и тестов: это уже слишком style-specific и хуже сочетается с нейтральным `django-drf`. Проверка прошла: `uv run python -m pytest -q tests/test_ai_sync.py` дал `25 passed`. Единственный остаток упоминаний `django-naming` теперь только в исторических логах и старых chat-export документах, которые я не переписывал.

## Ветка коммит релиз 1.2.0 и подготовка тега для 0tdkklm

**Question**

(0tdkzms) Отлично!
Теперь давай сделаем ветку по задаче `0tdkklm` с темой "Нормализация правил service layer для Django", и выполним commit для проделанных тобой изменений.
После этого сольём ветку стандартным образом, увеличим версию пакета до `1.2.0` и подготовим релиз тэгом.

**Answer**

Сначала проверю текущую git-ситуацию в `ai-standards` и загружу локальные workflow-инструкции для стандартного commit/merge, чтобы не нарушить правила веток, сообщения коммита и релизного процесса.

Сейчас репозиторий `ai-standards` находится на `main`, поэтому прямой commit туда запрещён. Создам рабочую ветку по задаче `0tdkklm`, подготовлю точные commit message для feature-изменений и для последующего version bump, и на этом шаге остановлюсь на обязательное утверждение сообщений.

Создана ветка `feat/0tdkklm-normalize-django-service-layer-rules`.

Нужны твои утверждения для двух commit message, потому что проектные правила требуют подтверждать текст перед каждым коммитом:

1. Для текущих изменений:
`0tdkklm. (refactor) normalize Django service layer rules and layered architecture stacks.`

2. Для последующего повышения версии до `1.2.0`:
`0tdkklm. (release) bump ai-standards version to 1.2.0.`

Если подтверждаешь оба текста, я сразу:
1. закоммичу текущие изменения в рабочей ветке,
2. солью ветку по стандарту в `main`,
3. оформлю отдельную release-ветку для `1.2.0`,
4. выполню `bump_version.py save --part minor`,
5. закоммичу version bump,
6. солью его в `main`,
7. подготовлю release tag стандартным способом.
