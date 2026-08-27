<h2>Оглавление</h2>

- [Верификация и обновление правил Java и Spring для ai-standards](#верификация-и-обновление-правил-java-и-spring-для-ai-standards)
- [Обновление правил Java-инфраструктуры на ветке задачи 0tdk9ag](#обновление-правил-java-инфраструктуры-на-ветке-задачи-0tdk9ag)

## Верификация и обновление правил Java и Spring для ai-standards

**Question**

(0tdk9ag) Давай вернёмся в проект ai-standards, и продолжим обновление правил по стекам.
На очереди Java и Spring – пожалуйста, верифицируй существующие правила на соответствие их современности, стандартам, текущим рекомендациям и лучшим практикам.
Ожидаю твоих предложений по доработкам и/или переработке существующего набора правил.

**Answer**

Перехожу в `ai-standards`: сначала загружу его `AGENTS.md` и ConPort, затем найду текущие правила по Java/Spring и сверю их с актуальными рекомендациями и современными практиками.

Контекст проекта восстановлен. Сейчас читаю локальные правила `ai-standards` и вытаскиваю весь материал по Java/Spring, чтобы отделить уже хорошие практики от устаревших или слишком спорных рекомендаций.

Нашёл единый стековый фрагмент `fragments/stacks/java-spring.md`. Сейчас разберу его построчно и затем сверю спорные места с официальными источниками Spring/Java, а не с вторичными блогами.

Собрал и локальный фрагмент, и официальные источники Spring/Oracle. Следующий шаг: разложу правила на три группы — оставить как есть, уточнить формулировку, добавить как отсутствующие — и затем дам конкретное предложение по новой структуре фрагментов.

Проверил текущий `java-spring` фрагмент в `ai-standards` против актуальных официальных источников Spring и Oracle на 2026-04-16. В целом фрагмент неплохой: в нём уже есть тонкие контроллеры, DTO на HTTP-границе, constructor injection, явные транзакционные границы и осознанная работа с загрузкой связей. То есть базовый вектор современный, а не legacy.

Но в текущем виде фрагмент уже слегка отстаёт по двум направлениям: он слишком смешивает разные уровни стека, и ему не хватает нескольких правил, которые сегодня уже выглядят базовыми для Spring Boot/Spring MVC/Spring Data.

**Что оставить**
- Оставить thin controllers, сервисный слой, запрет прямой инъекции repository в controller.
- Оставить DTO на HTTP-границе и запрет на бездумное раскрытие JPA entity наружу.
- Оставить constructor injection.
- Оставить явные transaction boundaries.
- Оставить правило про deliberate loading и N+1.
- Оставить идею “не форсировать interface + impl механически”.

**Что я бы усилил или переписал**
- `Prefer constructor injection over field injection.`  
  Лучше усилить до: использовать constructor injection по умолчанию; field injection не использовать, кроме редких framework-driven edge cases и тестовых заглушек. Для современных Spring-кодовых баз это уже скорее норма, чем мягкая рекомендация.
- `Validate inputs explicitly at the boundary and model layers where the contract requires it.`  
  Формулировка слишком общая. Сейчас лучше явно закрепить Spring MVC/Spring Boot idioms: `@Valid`/`@Validated`, обработку `MethodArgumentNotValidException` и `HandlerMethodValidationException`, и не вешать class-level `@Validated` на MVC controller без причины, потому что с Spring 6.1 встроенная method validation работает иначе.
- `Raise explicit exceptions with actionable context...`  
  Для Spring REST сегодня уже стоит уточнить, что для HTTP-ошибок предпочтителен RFC 9457 через `ProblemDetail`/`ErrorResponse`, а не произвольные ad hoc JSON-ошибки.
- `Treat relationship loading deliberately; prefer lazy loading by default...`  
  Смысл верный, но формулировка неполная. Я бы явно добавил: не полагаться на lazy loading за пределами корректно очерченной transactional boundary; для read-моделей использовать projections, `@EntityGraph`, fetch-стратегии и специально сформулированные запросы.
- `Use JPQL, derived queries, or native SQL deliberately...`  
  Хорошо, но не хватает modern Spring Data акцента на projections и entity graphs. Сейчас правило выглядит как выбор синтаксиса запроса, а не как выбор подхода к чтению данных.

**Что сейчас отсутствует и стоит добавить**
- Правило про современный Java baseline.  
  Не как жёсткий lock на одну версию, а как стандарт стиля: не писать код в стиле Java 8, если проект не ограничен платформой; для новых проектов ориентироваться минимум на Java 21 idioms, а Java 25 рассматривать как текущий LTS-кандидат там, где экосистема допускает. Это уже вывод из текущего состояния платформы, а не прямое требование Spring.
- Правило про immutable configuration.  
  Для структурированной конфигурации предпочитать `@ConfigurationProperties` вместо разрозненных `@Value`; для конфигурационных моделей предпочитать immutable/constructor-bound classes или records плюс validation.
- Правило про REST error contracts.  
  Для HTTP API стандартизовать `ProblemDetail`/`ErrorResponse` и централизованный `@ControllerAdvice`.
- Правило про testing strategy.  
  Для web/data/client сценариев предпочитать test slices (`@WebMvcTest`, `@DataJpaTest`, `@RestClientTest` и т.д.), а интеграционные тесты с инфраструктурой строить через Testcontainers вместо хрупких shared env/stub zoo.
- Правило про external HTTP clients.  
  Если проект на современном Spring, для sync HTTP-клиента предпочитать `RestClient`, для reactive/streaming `WebClient`; не тащить новый код на `RestTemplate`, если нет причины совместимости.
- Правило про transaction caveats.  
  `@Transactional` прокси-основан; self-invocation и уход в новые threads/reactive boundaries требуют отдельного внимания. Это частая реальная ловушка и её стоит сделать явной.

**Главное структурное замечание**
Сейчас `java-spring` смешивает:
- Java language/style
- Spring MVC/Web API
- Spring Boot configuration/testing
- Spring Data JPA

После Python-рефакторинга в этом репозитории такая смесь уже выглядит несимметрично. Я бы рекомендовал не просто “подправить текст”, а разделить стек на более чистые фрагменты:

1. `stacks/java`
2. `stacks/spring`
3. `stacks/spring-boot`
4. `stacks/spring-data-jpa`
5. Опционально `stacks/spring-web`

Минимальный вариант без лишней дробности:
- `java`
- `spring`
- `spring-data-jpa`

Это даст более чистую композицию. Например, проект может быть `java + spring` без JPA, или `java + spring + spring-data-jpa`, не наследуя лишние REST/JPA-предписания.

**Предлагаемый rewrite в кратком виде**
Если переписывать набор правил по смыслу, я бы сделал его таким:

- Use modern Java idioms; for greenfield code, prefer Java 21+ style where the project baseline allows it.
- Keep controllers thin and limited to transport concerns.
- Validate request and configuration contracts explicitly with Bean Validation and Spring validation support.
- Use DTOs or projections for transport and read models; do not expose JPA entities as public API contracts by default.
- Prefer immutable request, response, and configuration models; use `record` where it fits the project and framework constraints.
- Use constructor injection by default; avoid field injection in application code.
- Keep business logic in services or application use cases; do not put orchestration logic into controllers or repositories.
- Define transactional boundaries explicitly at service entry points; do not rely on incidental transactional behavior.
- Remember that `@Transactional` is proxy-based; self-invocation and thread/reactive boundary changes need explicit design.
- Prefer `@ConfigurationProperties` over scattered `@Value` for structured configuration, and validate configuration at startup.
- Treat JPA fetching deliberately; keep associations lazy by default, and solve read-shape needs with projections, entity graphs, or dedicated queries.
- Use Spring Data derived queries, JPQL, or native SQL deliberately based on query shape and clarity; do not standardize on one style mechanically.
- For REST APIs, standardize error responses with `ProblemDetail`/`ErrorResponse` and centralized exception handling.
- Prefer Spring test slices for focused tests and Testcontainers for infrastructure-backed integration tests.
- For outbound HTTP, prefer `RestClient` for synchronous integrations and `WebClient` for reactive or streaming scenarios.

**Итоговая рекомендация**
Я бы не ограничивался косметическим апдейтом текущего `fragments/stacks/java-spring.md`. Более сильный вариант:
1. Разделить combined fragment на `java` + `spring` + `spring-data-jpa`.
2. Подтянуть правила под современные Spring idioms: `ProblemDetail`, `@ConfigurationProperties`, Spring 6.1 validation behavior, projections/entity graphs, Testcontainers, test slices, `RestClient`.
3. Сделать формулировки чуть менее “general enterprise” и чуть более “2026 Spring practice”.

Официальные источники, на которые я опирался:
- Spring Boot system requirements: https://docs.spring.io/spring-boot/system-requirements.html
- Spring Boot externalized configuration and `@ConfigurationProperties`: https://docs.spring.io/spring-boot/reference/features/external-config.html
- Spring MVC validation: https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-controller/ann-validation.html
- Spring MVC error responses / `ProblemDetail`: https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-ann-rest-exceptions.html
- Spring transaction management: https://docs.spring.io/spring-framework/reference/data-access/transaction.html
- Declarative transaction proxy behavior: https://docs.spring.io/spring-framework/reference/data-access/transaction/declarative/tx-decl-explained.html
- Spring Data JPA projections: https://docs.spring.io/spring-data/jpa/reference/repositories/projections.html
- Spring Data JPA `@EntityGraph` and fetch/load graphs: https://docs.spring.io/spring-data/jpa/reference/jpa/query-methods.html
- Spring Boot test slices: https://docs.spring.io/spring-boot/appendix/test-auto-configuration/slices.html
- Spring Boot Testcontainers support: https://docs.spring.io/spring-boot/reference/testing/testcontainers.html
- Oracle Java SE support roadmap: https://www.oracle.com/java/technologies/java-se-support-roadmap.html

Если хочешь, следующим сообщением я могу сразу подготовить конкретный патч для `ai-standards`: либо мягкий rewrite текущего `java-spring`, либо полноценное разбиение на несколько stack fragments по аналогии с недавним Python-рефакторингом.

## Обновление правил Java-инфраструктуры на ветке задачи 0tdk9ag

**Question**

(0tdk9rv) Полностью поддерживаю твои рекомендации.
Давай отработаем их на ветке по задаче `0tdk9ag` с темой "Обновление правил Java-итнфраструктуры".

**Answer**

Перехожу к реализации в `ai-standards`: проверю текущую ветку и состояние репозитория, затем внесу рефакторинг Java/Spring stack fragments под задачу `0tdk9ag` с темой обновления Java-инфраструктурных правил.

Сейчас репозиторий на `main`, поэтому продолжать на нём нельзя. Создам рабочую ветку под `0tdk9ag`, затем подготовлю change plan и сам рефакторинг фрагментов, чтобы изменения были симметричны недавнему Python-рефакторингу.

Картина подтверждается: `java-spring` пока оформлен как один комбинированный stack, тогда как свежие изменения в репозитории уже двигаются к более чистым baselines и opt-in fragments. Сейчас зафиксирую план и затем начну правки `registry`, фрагментов, README и рендер-тестов.

Решение по структуре определил: не буду оставлять старый монолит как источник истины. Вместо этого введу новые baselines `java`, `spring`, `spring-data-jpa`, а `java-spring` оставлю как совместимый alias в `registry.toml`, чтобы downstream manifests не ломались.

Перед правками файлов добавлю короткий change plan в `docs/`, чтобы зафиксировать scope, инварианты и совместимость. После этого внесу сам рефакторинг фрагментов и документации одним проходом.

Начинаю основной patch: добавляю новые baseline fragments, перевожу `java-spring` в alias для совместимости, обновляю README и тесты, затем зафиксирую решение отдельным decision record.

Основной рефакторинг внесён. Сейчас дочищаю следы старого `java-spring` fragment, проверяю связанные ссылки и затем прогоню полный набор проверок рендера, типов и тестов.

Нашёлся только один замечание от `ruff`: длинный assert в новом тесте. Исправляю его и повторно прогоняю проверки, чтобы закрыть задачу чисто.

Изменения уже проходят проверки. Остался последний организационный шаг: кратко синхронизирую результат в ConPort, чтобы в следующем чате контекст по Java/Spring рефакторингу восстановился без ручного разбора diff.

Работа выполнена на ветке `feature/0tdk9ag-java-infrastructure-rules-update`.

Я перевёл Java/Spring guidance на новую структуру: вместо одного монолитного `java-spring` теперь есть три baseline-фрагмента — [java.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/java.md), [spring.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/spring.md) и [spring-data-jpa.md](/home/shtirliz/workspace/myself/ai-standards/fragments/stacks/spring-data-jpa.md). Старый `java-spring` удалён как источник истины, но сохранён как совместимый alias в [registry.toml](/home/shtirliz/workspace/myself/ai-standards/registry.toml:1), так что downstream manifests не ломаются.

Дополнительно обновил [README.md](/home/shtirliz/workspace/myself/ai-standards/README.md:43) и [README.ru.md](/home/shtirliz/workspace/myself/ai-standards/README.ru.md:43), добавил change plan [0tdk9ag-java_infrastructure_rules_update.md](/home/shtirliz/workspace/myself/ai-standards/docs/0tdk9ag-java_infrastructure_rules_update.md:1) и decision record [2026-04-16-refresh-java-infrastructure-guidance.md](/home/shtirliz/workspace/myself/ai-standards/docs/decisions/2026-04-16-refresh-java-infrastructure-guidance.md:1) с русскими локализациями, а в [tests/test_ai_sync.py](/home/shtirliz/workspace/myself/ai-standards/tests/test_ai_sync.py:62) добавил проверки и для alias `java-spring`, и для явной композиции `java + spring + spring-data-jpa`.

Проверки прошли:
- `rtk uv run ruff check`
- `rtk uv run mypy`
- `rtk uv run python -m pytest -q`
- `rtk uv run python scripts/ai_sync.py render --project-root /home/shtirliz/workspace/myself/ai-standards`

Коммит не создавал. Если хочешь, следующим сообщением подготовлю commit по стандарту с текстом на утверждение.
