# Транскрипт обсуждения: ConPort, Basic Memory, Chroma, Graphify и развитие ai-standards

**Дата:** 2026-09-13

---

## Пользователь — 2026-09-13 10:30:40

Привет! 🙂

Поправь меня, если я ошибаюсь, но у меня сложилось неприятное ощущение, что ConPort (MCP для локальной памяти между сессиями агента) прекратил развитие и поддержку.

Оцени развитие проекта, и сколько времени прошло с предыдущего обновления?

Ну и буду признателен, если ты сообщишь об аналогах ConPort – могут ли Chroma и Basic Memory заменить его?

---

## Assistant

Привет! 🙂 Твоё ощущение, к сожалению, выглядит вполне обоснованным. Я посмотрел именно текущую активность ConPort, а не только README.

**На 13 сентября 2026 года ConPort я бы классифицировал как «проект, фактически находящийся в спячке», хотя формально abandoned/deprecated он не объявлен.** Последняя версия upstream — **v0.3.13**. В release notes она датирована **31 декабря 2025 года**; после неё новых версий нет. Это значит, что с последнего реального релиза прошло **256 дней — примерно 8,4 месяца**.

Есть некоторая путаница в GitHub UI: карточка релиза показывает 29 октября, тогда как внутри changelog v0.3.13 стоит 2025-12-31. Для оценки активности я ориентировался на историю самих версий и release notes. В феврале 2026 на PyPI появился сторонний пакет-клон `iflow-mcp_greatscottymac-context-portal` той же версии 0.3.13, но это **не новая разработка ConPort**: код остался той же версии.

При этом репозиторий не архивирован, issues/PR открыты, README по-прежнему описывает проект как действующий. Поэтому говорить «официально умер» было бы неправильно. Но для проекта такого рода — MCP быстро эволюционирует, меняются FastMCP, клиенты, модели tool annotations, transports и т. п. — **восемь месяцев без релизов уже довольно серьёзный сигнал**. Особенно показательно, что последние релизы ConPort в основном состояли из dependency/security maintenance, а не из развития архитектуры памяти.

А вот **Basic Memory сейчас представляет практически противоположную картину**. В августе 2026 разработчики готовили v0.23: между 14 июня и 12 августа было **227 commits и 141 merged PR**, около 80 закрытых задач milestone; к 24 августа milestone v0.23 содержал уже 129 закрытых задач и был закрыт на 100%. В том числе развивается MCP API, indexing/persistence, embeddings, concurrency, FastMCP 4, Claude Code skills и т. д.

И вот здесь начинается самое интересное.

### ConPort, Basic Memory и Chroma — это не совсем три конкурента

Я бы нарисовал уровни примерно так:

```text
                     память агента / проекта
                              │
              ┌───────────────┴───────────────┐
              │                               │
           ConPort                       Basic Memory
       ──────────────                  ────────────────
       decisions                       Markdown notes
       progress                        observations
       patterns                        relations
       project context                 knowledge graph
       relationships                   semantic search
       semantic search                 MCP tools
              │                               │
              └──────────┬────────────────────┘
                         │
                 storage / retrieval
                         │
                      Chroma
                 ─────────────
                 embeddings
                 vectors
                 similarity search
                 metadata filtering
```

**Chroma сама по себе ConPort не заменяет.** Это примерно как спросить, может ли PostgreSQL заменить Jira. На PostgreSQL можно построить Jira — но PostgreSQL не является Jira.

Официальный Chroma MCP даёт операции над collections/documents, embeddings, metadata filters, similarity search и т. п. Он отлично решает задачу:

> «Вот миллион фрагментов информации. Найди те, которые семантически похожи на мой запрос».

Но он сам по себе не знает понятий вроде:

```text
decision
progress
system pattern
active context
product context
relationship
task
```

И не определяет жизненный цикл памяти агента. Это должен делать другой слой.

Ирония заключается ещё и в том, что **сам ConPort использует vector storage/embeddings для semantic retrieval**, то есть Chroma-подобный слой является частью его архитектуры, а не альтернативой всей архитектуре ConPort.

### А вот Basic Memory действительно может заменить ConPort

Причём для твоего сценария я сейчас склонялся бы именно к нему.

У ConPort подход такой:

```text
Agent
  │
  ▼
ConPort MCP
  │
  ├── product context
  ├── active context
  ├── decisions
  ├── progress
  ├── system patterns
  ├── custom data
  └── relations
         │
         ▼
      SQLite
     + vectors
```

А Basic Memory идёт от другого конца:

```text
Agent
  │
  ▼
Basic Memory MCP
  │
  ├── notes
  ├── observations
  ├── relations
  ├── search
  └── knowledge graph
         │
         ▼
 Markdown files
       │
       └── SQLite index / embeddings
```

То есть у ConPort **database-first structured memory**, а у Basic Memory — **document-first semantic memory**.

Basic Memory хранит первичные данные в обычных Markdown-файлах и строит из них graph: файлы становятся entities, внутри появляются observations, а relations связывают entities. SQLite используется как индекс/search layer, а не как единственный canonical storage.

Для человека, который хочет видеть и контролировать память агента, это очень существенная разница.

Например, решение может физически существовать как:

```markdown
# Catalog indexing

## Observations

- [decision] Incremental indexing uses SingleIndexRequest.
- [constraint] Full reindex causes excessive PostgreSQL I/O.
- [status] Incremental path is implemented.

## Relations

- relates_to [[Catalog Service]]
- depends_on [[Apache Solr]]
- impacts [[PostgreSQL]]
```

Это можно:

- прочитать без MCP;
- открыть в Obsidian;
- положить в Git;
- grep'нуть;
- отредактировать вручную;
- мигрировать куда угодно.

И при этом агент видит не просто файлы, а semantic graph. Именно это делает Basic Memory довольно близким **функциональным преемником ConPort**, несмотря на другую внутреннюю архитектуру.

### Но есть одно преимущество ConPort, которое Basic Memory заменяет не один-в-один

ConPort навязывает хорошую таксономию проектной памяти:

```text
Product Context
Active Context

Decisions
Progress
System Patterns
Custom Data
```

Это очень удобно для software development agent.

Basic Memory существенно более общий. Он говорит примерно:

```text
notes
observations
relations
entities
```

и дальше структуру определяешь ты.

Поэтому миграция

```text
ConPort → Basic Memory
```

не должна означать:

```text
decision #123 → какая-нибудь заметка
```

Гораздо лучше сохранить семантику:

```text
memory/
├── decisions/
│   ├── ADR-001-use-kafka.md
│   └── ADR-002-use-solr.md
│
├── architecture/
│   ├── catalog.md
│   ├── orders.md
│   └── inventory.md
│
├── progress/
│   └── catalog-indexing.md
│
├── constraints/
│   └── postgres-performance.md
│
└── concepts/
    ├── SingleIndexRequest.md
    └── Sandbox.md
```

а связи между ними дать Basic Memory построить/поддерживать через relations.

Вот тогда получается почти всё хорошее от ConPort плюс нормальный human-readable canonical storage.

### Что ещё сейчас стоит рассматривать

Есть несколько молодых проектов, которые пошли ещё дальше в сторону «agent memory», например `doobidoo/mcp-memory-service`: knowledge graph + persistent memory + MCP. Есть также `memory-mcp` от Daniel Simon — он сейчас дошёл до v12.x и имеет гораздо более сложные механизмы: event memory, reconstructive memory, relation consolidation, reflection и hybrid search.

Но я **не стал бы автоматически выбирать более sophisticated систему**. Для памяти engineering-agent'а мне нравятся свойства:

```text
простая
детерминированная
инспектируемая
версионируемая
переносимая
не привязанная к одному агенту
```

И тут Basic Memory выглядит необычно хорошо.

### Моя текущая оценка

| | ConPort | Basic Memory | Chroma |
|---|---|---|---|
| Persistent memory | ✅ | ✅ | ✅ storage |
| MCP | ✅ | ✅ | ✅ |
| Structured project memory | **✅ отлично** | ✅ можно построить | ❌ |
| Decisions/progress/patterns | **✅ native** | 🟡 моделируются | ❌ |
| Knowledge graph | ✅ | ✅ | ❌ |
| Explicit relations | ✅ | ✅ | 🟡 metadata |
| Semantic search | ✅ | ✅ | **✅ отлично** |
| Human-readable storage | ❌ SQLite | **✅ Markdown** | ❌ |
| Git-friendly | 🟡 | **✅** | ❌ |
| Obsidian-friendly | ❌ | **✅** | ❌ |
| Активность проекта сейчас | 🔴 слабая | **🟢 очень высокая** | **🟢 высокая** |
| Самостоятельная замена ConPort | — | **✅** | **❌** |

Поэтому **если сегодня начинать с нуля, ConPort я уже не выбрал бы**. Не потому, что он плох — архитектурно он мне по-прежнему нравится, — а потому что infrastructure component для долговременной памяти должен иметь достаточно живой upstream.

Для твоего случая я бы сейчас смотрел прежде всего на

**`Basic Memory + хорошо определённая схема project memory`**,

а Chroma рассматривал бы только как retrieval/vector infrastructure, если возможностей встроенного поиска Basic Memory когда-нибудь станет мало.

И тут есть ещё интересное следствие для нашего прежнего разговора об **ai-standards, design-first и retrieval**: я бы вообще перестал рассматривать такую память как «историю разговоров агента». Гораздо полезнее сделать её **слоем project knowledge**:

```text
               ai-standards
                    │
             правила / skills
                    │
                    ▼
               AI Agent
              /        \
             /          \
        source code    retrieval
                         │
                         ▼
                  Basic Memory
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
     decisions       architecture    constraints
         │               │               │
         └──────────── knowledge graph ───┘
```

То есть **ai-standards говорит агенту _как работать_, а Basic Memory сообщает _что уже известно об этом проекте_**. Это, на мой взгляд, гораздо более устойчивое разделение ответственности, чем пытаться засунуть накопленное знание в `AGENTS.md` или постоянно носить его в context window.

Если хочешь, следующим сообщением я могу сделать **практическое сравнение ConPort → Basic Memory применительно именно к нашему design-first workflow**: какие сущности ConPort чем заменить, какую структуру каталога сделать в Basic Memory и, самое важное, **что агент должен автоматически записывать в память после requirements/design/implementation/review**. Там уже можно получить вполне конкретную архитектуру для `ai-standards`.

---

## Пользователь

—
> а Chroma рассматривал бы только как retrieval/vector infrastructure, если возможностей встроенного поиска Basic Memory когда-нибудь станет мало.

Хм... Я рассматривал Chroma исключительно как инструмент векторного поиска по кодовой базе, которая может быть очень большой.
И, кстати, я думал, что правила ai-standards ангажируют агента на именно такое применение Chroma.
Это не так? 🙄

—
> То есть ai-standards говорит агенту как работать, а Basic Memory сообщает что уже известно об этом проекте. Это, на мой взгляд, гораздо более устойчивое разделение ответственности, чем пытаться засунуть накопленное знание в AGENTS.md или постоянно носить его в context window.

Да, я полностью поддерживаю.
Накопленному знанию не место в контексте, к накопленному знанию нужно обращаться, когда в этом возникает потребность – у нас одинаковое понимание?
Но нам нужно оформить это в правилах ai-standards – что предлагаешь туда добавить, убрать, изменить?

—
> следующим сообщением я могу сделать практическое сравнение ConPort → Basic Memory применительно именно к нашему design-first workflow: какие сущности ConPort чем заменить, какую структуру каталога сделать в Basic Memory и, самое важное, что агент должен автоматически записывать в память после requirements/design/implementation/review. Там уже можно получить вполне конкретную архитектуру для ai-standards.

Да, это очень интересно.
Но направление предлагаю такое: следующая версия ai-standards не должна содержать упоминаний ConPort, при этом отрабатывать flow, который обеспечит фиксацию *локальных знаний* о статусе и направлении работ в Basic Memory – суть: моя локальная работа интересна мне здесь и сейчас, и это помогает агенту решать задачу в разных сессиях, удерживая контекст. Но это ненужно в Git, если не оговорено явно: например, каталог  `docs/local`, упомянутый в `.gitignore`.
С другой стороны, если мы отказываемся от ConPort в пользу Basic Memory важно сохранить сильные черты ConPort: таксономию, structured project memory, decision/progress/patterns.
Как это оформить в правилах для Basic Memory?

— И важно не забывать наши предыдущие обсуждения развития ai-standards.
Перед "атакой" на мультиагентность и поддержку длинных сессий (нужно обезопасить их тестами и консультациями с человеком при выявлении сложностей и необходимости принятия решении), я хотел бы навести порядок с локальной памятью, и определиться с ролью Graphify – насколько он полезен агенту для работы, и не будет ли поддержание его инфраструктуры дороже результатов, которые мы можем получить от его использования.
Хочу узнать твоё мнение на этот счёт.

— Что хотел бы подчеркнуть: важно, что если в проекте используются Basic Memory и Chroma, Graphify или аналог, агент обязательно использовал их функции, когда это может помочь, чтобы эти инструменты не оказались неиспользованными возможностями при их наличии.
Достаточно ли сентенций для этого в ai-standards? Что следует добавить?

---

## Assistant

Да, понимание у нас одинаковое: **накопленное знание не должно постоянно ехать в контексте**. В контекст должны попадать только извлечённые по текущей задаче фрагменты, а каноническое/локальное знание должно жить отдельно и подтягиваться retrieval’ом по необходимости.

И я бы здесь развёл три слоя жёстче, чем раньше: **Chroma — retrieval по большой кодовой базе**, **Basic Memory — локальная рабочая память/состояние проекта между сессиями**, **Graphify — отдельный кандидат на structural/code-graph слой, ценность которого ещё надо доказать**.

Да — и тут как раз важное уточнение: **твоё исходное понимание Chroma было правильным**. В текущем `ai-standards` Chroma уже прямо определён как *semantic code-search layer over repository source files* для больших или multi-repo кодовых баз, отдельно от Basic Memory. Там же зафиксировано, что Chroma должен использоваться для semantic search по исходникам, с freshness-gate перед запросом и инкрементальным индексом.

То есть моя предыдущая формулировка про «Chroma как retrieval/vector infrastructure, если Basic Memory не хватит» была слишком широкой и в контексте твоего `ai-standards` — неудачной. **Chroma у тебя имеет самостоятельную и очень конкретную роль: retrieval по коду. Basic Memory — память/знания. Их не нужно ставить в отношение “основной/запасной”.**

Сейчас я бы зафиксировал архитектуру так:

```text
                         Agent
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
        Basic Memory     Chroma       Graphify
        ────────────     ──────       ────────
        local memory     semantic      structural
        task state       code search   code graph
        decisions        large repo    dependencies
        progress         similarity    paths/relations
        patterns
              │
              ▼
        docs/local/**
        (gitignored)
```

А Git-tracked knowledge — это четвёртый слой, отдельный от них:

```text
docs/domain/**
docs/decisions/**
docs/architecture/**
```

И вот это разделение, на мой взгляд, должно стать центральным принципом следующей версии.

## 1. Что поменять в отношении Basic Memory

Сейчас `ai-standards` в одном важном месте уже почти туда пришёл: он говорит, что canonical documentation и working memory должны быть разделены. Но само описание feature всё ещё начинается с:

> “Git-backed Markdown retrieval layer for durable knowledge across sessions”

и далее сильно акцентируется Git-tracked knowledge.

После отказа от ConPort я бы **расширил роль Basic Memory**.

Basic Memory должен обслуживать два различных класса знания:

```text
Basic Memory
│
├── Canonical project knowledge
│   ├── docs/domain/**
│   ├── docs/decisions/**
│   └── docs/architecture/**
│
└── Local working memory
    └── docs/local/**
        ├── context/
        ├── decisions/
        ├── progress/
        ├── patterns/
        └── investigations/
```

Но с принципиально разной семантикой.

**Canonical knowledge**:

```text
reviewed
durable
Git-tracked
shared with the team
source of truth
```

**Local working memory**:

```text
agent-managed
ephemeral-ish
machine/local-user specific
cross-session
not committed by default
not authoritative
```

То есть `docs/local/**` я считаю очень хорошей идеей.

Я бы прямо добавил в `.gitignore` шаблон:

```text
docs/local/
```

и правило:

> Content under `docs/local/**` is private working memory and MUST NOT be committed unless the user explicitly promotes it to canonical project documentation.

Это важно: **promotion должен быть сознательной операцией**, а не автоматическим переносом.

Например:

```text
docs/local/decisions/use-outbox-for-sync.md
```

может существовать неделю как текущее рабочее решение.

После подтверждения человеком:

```text
PROMOTE
    ↓
docs/decisions/2026-09-20-use-outbox-for-sync.md
```

И только второй файл становится project truth.

Это очень хорошо ложится на твой design-first подход.

## 2. Как сохранить сильную модель ConPort

Здесь я бы не стал заставлять Basic Memory изобретать структуру самостоятельно.

Над Basic Memory нужна **ai-standards memory taxonomy**.

Примерно такая:

```text
docs/local/
├── context/
├── decisions/
├── progress/
├── patterns/
├── investigations/
└── handoffs/
```

При этом категории — не просто каталоги, а **семантические типы памяти**.

Я бы оставил четыре сильные идеи ConPort практически без изменений:

| ConPort | Basic Memory / ai-standards |
|---|---|
| Active Context | `context` |
| Decisions | `decisions` |
| Progress | `progress` |
| System Patterns | `patterns` |

И добавил бы ещё два типа:

```text
investigations
handoffs
```

### `context`

Ответ на вопрос:

> Что сейчас происходит?

Например:

```markdown
# Catalog indexing work

- [goal] Replace full indexing with incremental indexing.
- [scope] catalog-service and search-service.
- [constraint] Production PostgreSQL I/O must not increase materially.
- [next] Inspect SingleIndexRequest publishing path.
```

### `decisions`

Ответ:

> Что мы решили и почему?

```markdown
# Incremental indexing

- [decision] Use SingleIndexRequest for sandbox promotion.
- [reason] Full indexing produces unacceptable I/O load.
- [status] provisional
```

Критически важно поле вроде:

```text
provisional
confirmed
superseded
```

Потому что local decision **не равен ADR**.

### `progress`

Ответ:

> Где мы остановились?

```markdown
- [done] Found producer of SingleIndexRequest.
- [done] Identified Kafka topic.
- [current] Trace consumer path.
- [blocked] Need clarification about production promotion semantics.
- [next] Inspect IndexRequestHandler.
```

Это, пожалуй, самая важная cross-session память.

### `patterns`

Ответ:

> Что мы выяснили об устройстве проекта, что пригодится снова?

```markdown
- [pattern] Catalog mutations are propagated asynchronously through Kafka.
- [pattern] Solr acts as the read model for catalog search.
```

Но тут нужна защита:

> A discovered pattern is local working knowledge until validated against canonical sources.

Иначе агент очень быстро построит мифологию проекта. 🙂

### `investigations`

Для временных исследований:

```text
Почему reindex грузит PostgreSQL?
Какие сервисы затрагивает sandbox promotion?
Где формируется reservation?
```

Они могут закончиться:

```text
discard
```

или породить `pattern` / `decision`.

### `handoffs`

Это compact resume point для новой сессии.

Не transcript, а именно:

```text
goal
confirmed facts
current state
open questions
next action
relevant memory links
```

Так мы фактически переносим хорошую часть ConPort в **открытый schema contract**, а не зависим от конкретного MCP.

## 3. Самое важное правило retrieval

Твою мысль я бы сделал отдельным фундаментальным правилом:

> **Stored knowledge is not conversation context. Retrieve it when relevant; do not preload it merely because it exists.**

И рядом:

> Before broad exploration, retrieve narrowly from available knowledge systems using the current task, entities, files, symbols, and decisions as search keys.

То есть flow такой:

```text
task arrives
     │
     ▼
What do I need to know?
     │
     ├── previous local state? ───────► Basic Memory
     │
     ├── code by meaning? ────────────► Chroma
     │
     ├── structural relation/path? ───► Graphify
     │
     ├── authoritative decision? ─────► Git docs
     │
     └── exact implementation? ───────► source files
```

А **не**:

```text
start session
   ↓
load everything
   ↓
150k context
   ↓
pray
```

Это хорошо согласуется и с уже существующим `agent-usage-hygiene`: текущие правила прямо требуют targeted discovery вместо broad file inspection.

# 4. Достаточно ли одной сентенции «используй инструменты, когда полезно»?

**Нет.**

Именно здесь чаще всего хорошие MCP-инструменты превращаются в музейные экспонаты.

Правило:

> Use Chroma when useful.

для агента почти эквивалентно:

> Feel free not to.

Нужна не обязанность «всегда пользоваться», а **retrieval routing policy**.

Например:

```text
When an enabled retrieval capability matches the information need,
use it before falling back to broader or more expensive exploration.
```

И дальше конкретная маршрутизация:

```text
Use Basic Memory first for:
- prior task state;
- previous decisions;
- known project patterns;
- unfinished investigations;
- cross-session handoff.

Use Chroma first for:
- semantic code discovery;
- locating implementations when exact names are unknown;
- finding analogous implementations across a large repository;
- cross-repository semantic search.

Use Graphify first for:
- dependency and call paths;
- structural relationships across modules;
- impact analysis;
- architecture questions spanning many files.
```

А затем очень важная оговорка:

```text
Retrieval narrows evidence; it does not replace verification against
canonical documentation or source code.
```

Это уже есть у Chroma в форме «similarity narrows investigation but does not prove completeness». Я бы поднял эту идею на общий уровень retrieval policy.

# 5. Я бы ввёл новый feature: `retrieval-routing`

Вот это, на мой взгляд, архитектурно чище всего.

Сейчас правила разбросаны между:

```text
basic-memory
chroma
session-hygiene
agent-usage-hygiene
```

Лучше сделать общий policy layer:

```text
retrieval-routing
```

Он **не должен знать детали API Chroma или Basic Memory**.

Он знает:

```text
which knowledge source to consult
when
in what order
what counts as evidence
when to fall back
```

А feature конкретного инструмента говорит уже **как** его использовать.

Получится:

```text
retrieval-routing
      │
      ├── Basic Memory adapter
      ├── Chroma adapter
      └── Graphify adapter
```

Это очень похоже на принцип, который у тебя уже используется с agent adapters.

И, главное, завтра Chroma можно заменить:

```text
Chroma → Qdrant
```

а Basic Memory:

```text
Basic Memory → FooMemory
```

не меняя behavioral policy агента.

# 6. Что делать с Graphify

Здесь я с твоей осторожностью согласен.

Но после того, как я посмотрел текущий Graphify, я бы его **не списывал**.

Проект сейчас позиционирует себя именно как code-intelligence graph: он строит детерминированный AST-based graph и рекомендует агенту делать scoped `graphify query "<question>"` вместо последовательного grep/read файлов. Он умеет показывать structural paths, dependencies и provenance связей; при этом для Codex/Kilo/Cursor автор сам ставит always-on guidance или hooks, чтобы агент действительно использовал граф.

И это непосредственно подтверждает твою мысль:

> мало иметь инструмент — агента нужно маршрутизировать к нему.

Graphify сам решает именно эту проблему.

Но я вижу **существенное пересечение с Chroma**.

Допустим вопрос:

> Где рассчитывается цена marketplace product?

Chroma:

```text
semantic similarity
→ вероятные файлы
```

Graphify:

```text
symbols
→ calls
→ imports
→ modules
→ path
```

Для discovery Chroma может оказаться лучше.

Для:

> Что сломается, если изменить X?

Graphify потенциально значительно полезнее.

Поэтому я бы не выбирал:

```text
Chroma OR Graphify
```

а проверял гипотезу:

```text
Chroma = semantic retrieval
Graphify = structural retrieval
```

## Но Graphify пока должен заслужить место

Особенно мне не нравится идея вводить его в core ai-standards **на вере**.

Сам Graphify публикует довольно впечатляющие benchmark'и: например, тестирует code-intelligence на ERPNext порядка миллиона LOC и сравнивает graph retrieval с другими подходами. Но benchmark принадлежит самому проекту, поэтому воспринимать его нужно как полезное свидетельство, а не независимое доказательство.

Я бы сделал маленький evaluation.

Например, взять Broadleaf и задать агенту 15–20 реальных вопросов:

```text
Where does SingleIndexRequest originate?

Which services participate in sandbox promotion?

Trace inventory reservation from REST entry point to persistence.

What code paths update Solr after a product change?

What could be affected by changing MarketplaceProduct?

Where is fulfillment order splitting implemented?
```

Три режима:

```text
A. grep/files only

B. Chroma + files

C. Chroma + Graphify + files
```

Мерить хотя бы:

```text
correctness
files opened
tool calls
tokens
elapsed work
missed dependencies
false leads
```

Если:

```text
C ≈ B
```

Graphify не нужен.

Если:

```text
C >> B
```

особенно на impact/path questions — тогда он заслужил место.

Вот это я бы сделал **до мультиагентности**. Это хороший маленький controlled experiment.

# 7. Что я предлагаю изменить прямо сейчас

Здесь я бы сделал одну достаточно цельную итерацию.

- **Полностью удалить ConPort**: feature, registry entry, docs, deployment references и упоминания в `session-hygiene`, `reasoning-hygiene`, Chroma docs.
- **Переопределить Basic Memory** из «в основном Git documentation retrieval» в `project memory + knowledge retrieval`, сохранив строгую границу canonical/local.
- Ввести **`docs/local/**` как стандартный local-working-memory tree**, `.gitignore` по умолчанию.
- Зафиксировать taxonomию: `context`, `decisions`, `progress`, `patterns`, `investigations`, `handoffs`.
- Добавить lifecycle: `capture → retrieve → update → supersede/discard → optionally promote`.
- Ввести **`retrieval-routing`** как tool-neutral behavioral feature.
- Chroma оставить ровно там, где ты его предполагал: **large-codebase semantic retrieval**.
- Graphify пока сделать **experimental feature**, а не стандартным компонентом knowledge stack.
- Перед следующей большой фазой провести Graphify evaluation.

# 8. Как это стыкуется с design-first flow

Я вижу следующий жизненный цикл.

```text
User request
     │
     ▼
RETRIEVE
 Basic Memory:
 prior context / decisions / progress

 Chroma:
 relevant implementations

 Graphify:
 structural context (if enabled/relevant)
     │
     ▼
REQUIREMENTS
     │
     ├── unresolved ambiguity
     │         ↓
     │       HUMAN
     │
     ▼
DESIGN
     │
     ├── record local decisions
     ▼
SLICE PLAN
     │
     ├── update progress
     ▼
IMPLEMENT
     │
     ├── retrieve code as needed
     ▼
TEST / EVAL
     │
     ├── failure requiring design choice
     │         ↓
     │       HUMAN
     ▼
REVIEW
     │
     ▼
UPDATE MEMORY
 context
 progress
 decisions
 patterns
     │
     ▼
PROMOTE?
   │     │
  no    yes
   │     │
local   docs/decisions
memory  docs/architecture
```

И вот тут как раз получается основа для следующего шага — **длинной автономной работы**.

Длинная сессия уже не обязана удерживать всю историю:

```text
working context
     +
retrievable memory
     +
verified artifacts
```

А когда агент упирается в то, что требует нового design choice:

```text
STOP → human consultation
```

То есть локальная память — в каком-то смысле **prerequisite для безопасной автономности**. Сначала научим агента сохранять и восстанавливать состояние без огромного context window, потом уже дадим ему длинные слайсы и субагентов.

И это очень хорошо соответствует прежнему принципу ai-standards: агент может исполнять согласованный дизайн автономно, но не должен молча выбирать новый дизайн.

## Я бы зафиксировал целевую архитектуру так

```text
                   ai-standards
                        │
               Behavioral policy
                        │
       ┌────────────────┼────────────────┐
       │                │                │
 design-first     retrieval-routing  autonomy
       │                │            boundaries
       │                │
       │        ┌───────┼────────┐
       │        │       │        │
       │       BM     Chroma  Graphify?
       │        │       │        │
       │     memory   semantic structural
       │              code      code
       │              search    graph
       │
       ▼
 canonical artifacts
 docs/domain
 docs/decisions
 docs/architecture

 local working state
 docs/local
     ├── context
     ├── decisions
     ├── progress
     ├── patterns
     ├── investigations
     └── handoffs
```

И да: **я считаю именно наведение порядка здесь правильным следующим этапом ai-standards**, раньше мультиагентности. Уже после этого последовательность выглядит естественно:

```text
1. Memory semantics
2. Retrieval routing
3. Graphify evaluation
4. Test/eval harness
5. Longer autonomous slices
6. Multi-agent orchestration
```

Пункты 4–6 тогда строятся уже не поверх «агент, у которого есть огромный чат», а поверх **агента, умеющего управлять знаниями и получать ровно тот контекст, который нужен сейчас**. Это намного более крепкое основание.

---

## Пользователь — 2026-09-13 12:13:25

Так, замечательно. Меня всё устраивает, и даже интригует.

Давай оформим твои предложения в форме предложений перегруппировки (если ты найдёшь это целесообразным) и новых правил для ai-standards.

---

## Assistant

Да. После просмотра текущего `main` я бы делал это именно как **перегруппировку**, а не просто добавлял ещё один feature. Сейчас ответственность действительно размазана: `structured-artifacts` говорит о durable knowledge и working memory, `session-hygiene` всё ещё делегирует transient context ConPort, `basic-memory` описан преимущественно как Git-backed retrieval, а `chroma` уже имеет правильную отдельную роль semantic code search.

Кроме того, ConPort сейчас остаётся и в рекомендуемом manifest, и в reasoning/session relationships, и в knowledge-stack deployment. Значит, удаление должно быть системным, а не заменой одного fragment другим.

Ниже я бы положил такой proposal в основу следующей версии.

# Предлагаемая реорганизация memory и retrieval в ai-standards

## 1. Цель изменения

Следующая итерация `ai-standards` должна разделить три разных задачи, которые не следует смешивать:

1. **Project memory** — локальное накопленное знание о текущей работе, сохраняемое между сессиями.
2. **Knowledge retrieval** — извлечение только релевантного знания тогда, когда оно требуется текущей задаче.
3. **Code retrieval / code intelligence** — поиск и анализ большой кодовой базы.

Целевая модель:

```text
                         Agent
                           │
                  Retrieval Routing
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    Basic Memory         Chroma         Graph tool
    working/project      semantic       structural
    knowledge            code search    code intelligence
          │                │                │
          ▼                ▼                ▼
       Markdown          Source           Source
       knowledge         index            graph
```

При этом Git-tracked canonical documentation остаётся отдельным источником истины:

```text
docs/domain/**
docs/decisions/**
docs/architecture/**
```

а локальная память агента по умолчанию не является частью repository history:

```text
docs/local/**
```

---

## 2. Основной принцип

Добавить общий принцип:

> **Stored knowledge is not conversation context. Retrieve it when relevant; do not preload it merely because it exists.**

В расширенной форме:

> Keep accumulated project knowledge outside the active model context by default. Retrieve only the smallest relevant subset required by the current task. Do not reload broad history merely because it is available.

Следствие:

```text
knowledge exists
      ≠
knowledge belongs in every prompt
```

Контекст должен строиться непосредственно под информационную потребность текущего шага.

---

## 3. Удалить ConPort из ai-standards

ConPort больше не должен быть частью стандартной архитектуры `ai-standards`.

Удалить:

- feature `conport`;
- registry entries;
- deployment instructions;
- упоминания ConPort в `session-hygiene`;
- упоминания ConPort в `reasoning-hygiene`;
- сравнения с ConPort в `chroma`;
- ConPort из `deploy-ai-knowledge-stack`;
- ConPort из examples/default manifests;
- документацию и templates, относящиеся только к ConPort.

Не заменять название `ConPort` механически на `Basic Memory`.

Вместо этого перенести полезные **семантические свойства** ConPort в tool-independent правила project memory:

- context;
- decisions;
- progress;
- patterns;
- explicit relationships;
- cross-session continuation.

Таким образом сохраняется модель памяти, но исчезает зависимость standards от конкретного backend.

---

## 4. Ввести feature `retrieval-routing`

### Назначение

`retrieval-routing` определяет:

- когда агенту требуется retrieval;
- какой источник знания использовать;
- в каком порядке искать;
- когда переходить к более дорогому исследованию;
- как проверять полученные результаты.

Feature должен быть **tool-neutral**.

Он не должен содержать команды API Basic Memory, Chroma или Graphify.

Конкретные features реализуют соответствующие retrieval capabilities.

### Предлагаемые core rules

#### R1 — Retrieve before broad exploration

> Before broad repository exploration, determine what information is missing and query the narrowest available knowledge source capable of answering it.

#### R2 — Use available capabilities

> When an enabled retrieval capability directly matches the current information need, use it before falling back to broader manual exploration.

Это важнее слабого:

> Use X when useful.

Наличие инструмента должно означать, что агент обязан учитывать его при выборе стратегии поиска.

#### R3 — Route by information need

> Route retrieval according to the kind of information required, not according to tool familiarity.

Рекомендуемая таблица:

| Information need | Preferred source |
|---|---|
| previous task state | Basic Memory |
| prior local decisions | Basic Memory |
| project patterns already discovered | Basic Memory |
| unresolved investigations | Basic Memory |
| canonical project decisions | Git-tracked documentation |
| semantic code discovery | Chroma |
| analogous implementations | Chroma |
| unknown implementation location | Chroma |
| exact symbol/file already known | direct source access |
| call/dependency path | structural graph tool |
| impact analysis across modules | structural graph tool |
| final verification | canonical docs/source/tests |

#### R4 — Retrieval is evidence discovery

> Retrieval narrows the evidence set; it does not establish correctness or completeness by itself.

#### R5 — Verify at the authoritative layer

> Verify retrieved claims against their authoritative source before relying on them for implementation or review when correctness matters.

For example:

```text
Basic Memory → hypothesis / remembered state
Chroma       → candidate implementation
Graph        → candidate structural relation
Git docs     → canonical decision
source code  → implementation truth
tests        → behavioral evidence
```

#### R6 — Escalate progressively

> Prefer narrow retrieval before broad retrieval, and broad retrieval before indiscriminate repository scanning.

Пример:

```text
known symbol
   ↓
direct lookup

unknown symbol but known intent
   ↓
Chroma

cross-module relationship
   ↓
Graph

still uncertain
   ↓
targeted file exploration

only then
   ↓
broader repository inspection
```

---

## 5. Переработать feature `basic-memory`

Текущее понимание:

```text
Basic Memory
≈ Git-backed Markdown retrieval
```

Предлагаемое понимание:

```text
Basic Memory
= Markdown-backed project knowledge and working-memory retrieval
```

Basic Memory должен обслуживать **два разных класса знания**, не смешивая их.

### 5.1 Canonical project knowledge

```text
docs/domain/**
docs/decisions/**
docs/architecture/**
```

Свойства:

- Git-tracked;
- reviewed;
- team-visible;
- durable;
- authoritative в пределах declared semantics.

### 5.2 Local working memory

```text
docs/local/**
```

Свойства:

- cross-session;
- agent-managed;
- user-local;
- mutable;
- not authoritative;
- not committed by default;
- может содержать provisional conclusions;
- может быть удалена без изменения project history.

По умолчанию:

```gitignore
docs/local/
```

---

## 6. Правило разделения canonical и local memory

Добавить жёсткое правило:

> Never treat local working memory as canonical project documentation.

И обратное:

> Do not write temporary task state, speculative findings, or session continuation data into canonical project documentation merely to preserve agent context.

Это защищает Git от превращения в dump внутреннего состояния агента.

---

## 7. Promotion local knowledge → canonical knowledge

Добавить явный lifecycle:

```text
capture
   ↓
retrieve/update
   ↓
validate
   ↓
 ┌──────────────┐
 │              │
discard       retain local
                │
                ▼
             promote?
              │   │
             no  yes
                  │
                  ▼
             canonical docs
```

Правило:

> Promotion from local working memory to canonical project documentation is an explicit semantic operation, not an automatic synchronization step.

И:

> Promote local knowledge only when it has become durable project knowledge and the user or project workflow permits the corresponding canonical artifact to be created or updated.

Например:

```text
docs/local/decisions/catalog-indexing.md

        validation + approval

                ↓

docs/decisions/2026-09-13-incremental-catalog-indexing.md
```

Local decision может быть provisional.

Canonical decision — уже project decision.

---

## 8. Сохранить ConPort taxonomy как ai-standards memory taxonomy

Basic Memory не должен сам определять, что считается важной памятью разработки.

Это обязанность `ai-standards`.

Предлагаемая структура:

```text
docs/local/
├── context/
├── decisions/
├── progress/
├── patterns/
├── investigations/
└── handoffs/
```

Физическое разбиение на каталоги может быть configurable, но **семантические категории должны быть стандартными**.

---

## 9. Тип `context`

Назначение:

> What are we currently trying to accomplish?

Сохранять:

- current goal;
- current scope;
- important constraints;
- accepted direction;
- current phase;
- relevant artifacts;
- immediate next step.

Не сохранять:

- transcript;
- весь reasoning;
- все просмотренные файлы;
- временные детали, которые легко восстановить.

Пример:

```markdown
# Catalog indexing

- [goal] Replace production full indexing with incremental indexing.
- [scope] catalog-service and search-service.
- [constraint] Do not increase production PostgreSQL I/O materially.
- [phase] implementation discovery.
- [next] Trace SingleIndexRequest consumer path.
```

---

## 10. Тип `decisions`

Назначение:

> What has been decided locally, and why?

Минимальная семантика:

```text
decision
reason
status
scope
```

Статусы:

```text
provisional
confirmed
superseded
rejected
```

Правило:

> Record a local decision when it materially constrains subsequent work and would otherwise need to be reconstructed in a later session.

Не записывать каждое микрорешение.

Особенно важно:

> A local `confirmed` decision means confirmed for the current work context; it does not automatically become a canonical ADR.

---

## 11. Тип `progress`

Назначение:

> Where did the work stop?

Это ключевая cross-session память.

Предлагаемая семантика:

```text
done
current
blocked
next
```

Пример:

```markdown
# Catalog indexing progress

- [done] Located SingleIndexRequest producer.
- [done] Identified Kafka topic.
- [current] Trace index consumer.
- [blocked] Production promotion semantics remain unclear.
- [next] Inspect IndexRequestHandler.
```

Правило:

> Update progress at meaningful phase boundaries and before ending work that is expected to continue in another session.

---

## 12. Тип `patterns`

Назначение:

> What reusable property of the project has been discovered?

Пример:

```markdown
- [pattern] Catalog mutations propagate asynchronously through Kafka.
- [pattern] Solr is the catalog search read model.
```

Защитное правило:

> Treat discovered patterns as working knowledge until validated against source code or canonical documentation.

И:

> Update or supersede a pattern when contrary evidence is found; do not accumulate contradictory memories without recording their relationship.

---

## 13. Тип `investigations`

Назначение:

> What question is being investigated and what evidence has been found?

Использовать для исследований, которые ещё не стали решением или pattern.

Например:

```text
Why does full reindex overload PostgreSQL?
Which service owns sandbox promotion?
Where is inventory reservation finalized?
```

Investigation должен иметь lifecycle:

```text
open
resolved
abandoned
```

Результат investigation может:

- исчезнуть;
- породить pattern;
- породить decision;
- потребовать human consultation.

---

## 14. Тип `handoffs`

Не использовать handoff как ещё один transcript.

Handoff — **resume point**.

Он должен содержать только:

```text
goal
confirmed state
current state
open questions
next action
relevant artifacts/memory links
```

Правило:

> A handoff must be sufficient to resume the task without replaying the previous conversation, but compact enough to inspect before loading additional context.

---

## 15. Добавить memory-write policy

Агенту нельзя поручать «запоминай всё полезное».

Нужны критерии записи.

### Записывать в local memory, если информация:

- понадобится в следующей сессии;
- существенно влияет на дальнейшее решение;
- дорого восстанавливается;
- является результатом исследования;
- объясняет текущий статус;
- фиксирует unresolved question/blocker;
- является подтверждённым reusable pattern проекта.

### Не записывать, если информация:

- легко получается из одного очевидного файла;
- является transient tool output;
- является подробностью reasoning;
- уже существует канонически;
- является guess без полезной роли;
- дублирует существующую memory item без изменения состояния.

Ключевое правило:

> Memory is a curated state store, not an execution log.

---

## 16. Добавить memory-read policy

На старте задачи агент не должен загружать всю memory tree.

Вместо этого:

> Query local memory using the current goal, relevant entities, modules, concepts, decisions, and task identifiers.

Для продолжения предыдущей работы:

```text
1. retrieve relevant context
2. retrieve current progress
3. retrieve relevant decisions
4. retrieve patterns only as needed
5. open linked investigations if they affect the current step
```

Не:

```text
read docs/local/**
```

---

## 17. Изменить `session-hygiene`

Удалить dependency на ConPort.

`session-hygiene` должен отвечать за:

- context drift;
- phase transitions;
- handoff;
- fresh-session decisions.

Но сохранение рабочего состояния должно происходить через абстрактную project-memory capability.

Предлагаемые правила:

> Before a deliberate session handoff, preserve the minimum durable working state required to resume the task.

> A new session should retrieve the relevant handoff and working-memory items rather than reconstructing state from conversation history.

> Do not reload all accumulated memory at session start.

И важное разделение:

```text
session-hygiene
     │
     │ says WHEN state must be preserved/reloaded
     ▼
project-memory/basic-memory
     │
     │ says WHAT and HOW
     ▼
local knowledge
```

---

## 18. Изменить `structured-artifacts`

Сейчас этот feature частично смешивает canonical artifacts и agent working memory.

Предлагается оставить ему:

```text
change plans
module contracts
decision records
architecture records
module maps
canonical structured artifacts
```

и вывести local operational memory в `basic-memory`.

Новая граница:

```text
structured-artifacts
        =
reviewable project artifacts

basic-memory
        =
retrievable project knowledge
+ local working memory
```

При этом Basic Memory может индексировать canonical structured artifacts.

---

## 19. Сохранить роль Chroma практически без изменений

Chroma уже имеет правильную ответственность:

> semantic code-search layer over repository source files.

Не превращать Chroma в general memory backend.

Предлагаемый routing contract:

> Use Chroma when the implementation is not known by exact location but can be described semantically.

Типичные случаи:

- find where a business operation is implemented;
- find analogous implementations;
- locate code by behavior rather than symbol;
- search across large repositories;
- search across multiple repositories.

Сохранить:

- freshness gate;
- incremental indexing;
- resumability;
- verification against source;
- правило, что similarity не доказывает completeness.

Убрать из документации Chroma только привязку к ConPort.

---

## 20. Graphify / structural code intelligence

Пока не включать Graphify в обязательный default knowledge stack.

Ввести концептуальную capability:

```text
structural-code-intelligence
```

а Graphify рассматривать как один возможный backend.

Назначение capability:

- call paths;
- dependency paths;
- module relationships;
- impact analysis;
- architecture traversal;
- structural navigation большой кодовой базы.

Routing rule:

> Prefer structural code intelligence when the question is primarily about relationships between known or discoverable code entities rather than semantic similarity.

Примеры:

```text
"What calls this?"
"What depends on this module?"
"Which path connects endpoint X to persistence Y?"
"What can be affected by changing class Z?"
```

---

## 21. Graph capability должна быть experimental

До её включения в recommended stack выполнить evaluation.

Сравнить:

```text
A. source tools only
B. Chroma + source tools
C. Chroma + structural graph + source tools
```

На реальных engineering tasks.

Оценивать:

- correctness;
- missed dependencies;
- false leads;
- number of source files opened;
- tool calls;
- token/context consumption;
- operational complexity;
- index maintenance cost;
- stale-index failures.

Решение о Graphify принимать по правилу:

> Adopt structural graph infrastructure only if its measured improvement on relevant engineering tasks justifies its deployment and maintenance cost.

---

## 22. Capability awareness

Это отдельное важное правило.

Если capability включена, агент не должен забывать о её существовании.

Добавить:

> At the start of non-trivial discovery, identify which enabled retrieval capabilities match the task before choosing an exploration strategy.

Но не заставлять агента бессмысленно вызвать каждый MCP.

Неправильно:

```text
always query Basic Memory
always query Chroma
always query Graphify
```

Правильно:

```text
identify information need
        ↓
identify matching enabled capability
        ↓
use it when it can materially narrow the search
```

---

## 23. Retrieval capability registry

Полезно добавить декларативную модель capabilities.

Например концептуально:

```toml
[retrieval]
project_memory = "basic-memory"
semantic_code = "chroma"
structural_code = "graphify"
```

Не обязательно вводить именно такой TOML сейчас.

Но standards должны различать **capability** и **implementation**:

```text
project-memory      → Basic Memory
semantic-code       → Chroma
structural-code     → Graphify
```

Это позволит в дальнейшем заменить backend:

```text
Chroma → Qdrant/custom index
Graphify → another graph engine
Basic Memory → another Markdown memory system
```

без переписывания behavioral rules.

---

## 24. Design-first integration

Memory должна поддерживать существующий design-first flow, а не создавать второй workflow.

Предлагаемый flow:

```text
TASK
  │
  ▼
RETRIEVE RELEVANT EXISTING KNOWLEDGE
  │
  ▼
REQUIREMENTS
  │
  ├── ambiguity requiring decision
  │             ↓
  │           HUMAN
  ▼
DESIGN
  │
  ├── record material local decisions
  ▼
SLICE PLAN
  │
  ├── initialize/update progress
  ▼
IMPLEMENT
  │
  ├── Chroma / graph retrieval as needed
  ▼
VERIFY
  │
  ├── tests / source / canonical artifacts
  │
  ├── unexpected design choice
  │             ↓
  │           HUMAN
  ▼
REVIEW
  │
  ▼
UPDATE LOCAL MEMORY
  │
  ├── progress
  ├── patterns
  ├── decisions
  └── unresolved investigations
  │
  ▼
PROMOTE DURABLE KNOWLEDGE?
      │           │
      no         yes
      │           │
    local    canonical docs
```

---

## 25. Autonomy boundaries integration

Local memory является предпосылкой, а не заменой autonomy boundaries.

Добавить связь:

> Long autonomous execution must periodically preserve externally reviewable task state at meaningful phase boundaries.

Но:

> Persisting task state does not authorize the agent to cross an existing autonomy boundary.

И:

> When execution encounters a material design choice, contradictory requirements, widening scope, or evidence invalidating the agreed design, preserve the current state and request human direction rather than recording a new decision and continuing silently.

Это особенно важно перед будущей поддержкой long-running agents.

---

## 26. Подготовка к multi-agent работе

На этой итерации не вводить multi-agent orchestration.

Но память уже должна иметь semantics, которые позволят это сделать позже:

```text
facts
decisions
progress
handoffs
ownership/provenance
```

Особенно важно:

> Shared memory must not turn one agent's hypothesis into another agent's established fact.

Поэтому observation желательно иметь provenance/status.

Минимально:

```text
type
status
source
updated
```

Полноценную multi-agent consistency model оставить следующей фазе.

---

## 27. Предлагаемая перегруппировка features

### До

```text
structured-artifacts
session-hygiene
basic-memory
chroma
conport
agent-usage-hygiene
autonomy-boundaries
```

с частично пересекающимися обязанностями.

### После

```text
Knowledge and context
├── retrieval-routing
├── basic-memory
├── session-hygiene
└── agent-usage-hygiene

Engineering artifacts
├── structured-artifacts
└── module-contract-gate

Code intelligence
├── chroma
└── structural-code-intelligence [experimental]

Execution governance
├── design-first-collaboration
├── autonomy-boundaries
├── reasoning-hygiene
├── code-review
└── review-lenses
```

`retrieval-routing` становится связующим policy-layer.

---

## 28. Зависимости features

Я бы зафиксировал следующие отношения:

```text
basic-memory
    └── requires/recommends retrieval-routing

chroma
    └── requires/recommends retrieval-routing

structural-code-intelligence
    └── requires retrieval-routing

session-hygiene
    └── integrates with project-memory when available

structured-artifacts
    └── may be indexed by basic-memory

module-contract-gate
    └── canonical source remains repository artifacts
        Basic Memory may only locate them

autonomy-boundaries
    └── integrates with working-state persistence
```

При этом `retrieval-routing` должен нормально работать даже если установлен только один retrieval backend.

---

## 29. Recommended stack после изменения

Для крупного проекта:

```toml
features = [
    "design-first-collaboration",
    "reasoning-hygiene",
    "autonomy-boundaries",

    "structured-artifacts",
    "module-contract-gate",

    "retrieval-routing",
    "basic-memory",
    "chroma",

    "session-hygiene",
    "agent-usage-hygiene",

    "code-review",
]
```

Graph capability пока:

```toml
# experimental
"structural-code-intelligence"
```

только после осознанного включения.

---

## 30. Предлагаемая структура knowledge tree

```text
docs/
├── domain/                 # canonical problem-space knowledge
├── decisions/              # canonical decisions
├── architecture/           # canonical solution-space knowledge
│
└── local/                  # local cross-session working memory
    ├── context/
    ├── decisions/
    ├── progress/
    ├── patterns/
    ├── investigations/
    └── handoffs/
```

`.gitignore`:

```gitignore
/docs/local/
```

Если конкретный проект сознательно хочет versioned/shared working memory, он может переопределить это локально.

Default остаётся private/local.

---

## 31. Важное уточнение Basic Memory storage model

`docs/local/**` следует рассматривать не как обязательную реализацию всей внутренней базы Basic Memory, а как **стандартную human-readable surface project working memory**.

Standards должны определять семантику.

Backend может дополнительно иметь:

- SQLite index;
- embeddings;
- graph edges;
- metadata;
- internal caches.

Эти детали не являются canonical knowledge.

---

## 32. Изменить deployment terminology

Вместо:

```text
deploy-ai-knowledge-stack
```

в смысле фиксированного:

```text
ConPort + Basic Memory + Chroma
```

перейти к capability-based deployment.

Например:

```text
deploy-ai-retrieval-stack
```

который разворачивает только объявленные capabilities.

Пример:

```text
Basic Memory
Chroma
```

а позднее:

```text
Basic Memory
Chroma
Graphify
```

без изменения общей семантики standards.

---

## 33. Tests, которые следует добавить

Новые правила нужно защитить не только документацией.

Минимальный набор policy tests:

### Manifest/render tests

Проверить:

- отсутствие ConPort;
- правильный порядок fragments;
- dependencies `retrieval-routing`;
- optional graph capability.

### Generated AGENTS tests

Проверить наличие правил:

```text
stored knowledge != active context
enabled retrieval capability must be considered
retrieval does not replace verification
local memory != canonical knowledge
promotion is explicit
```

### Knowledge-tree tests

Проверить:

- canonical tree rules не применяются механически к `docs/local`;
- `doctor` не пытается превратить progress/handoff в canonical dated note;
- local memory не смешивается с canonical artifacts.

### Behavioral scenarios

**Scenario A**

> Continue yesterday's unfinished catalog indexing task.

Ожидается:

```text
Basic Memory → retrieve handoff/progress/context
```

а не broad repo scan.

**Scenario B**

> Find code implementing product price resolution.

Ожидается:

```text
Chroma → candidates → source verification
```

**Scenario C**

> Change a known exact class.

Ожидается:

```text
direct source inspection
```

а не ceremonial Chroma query.

**Scenario D**

> What modules can be affected by this change?

При enabled graph capability:

```text
structural retrieval → source verification
```

**Scenario E**

Agent discovers a new architectural decision is required.

Ожидается:

```text
record current state
STOP
consult human
```

а не:

```text
create local decision
continue implementation
```

---

## 34. Что не следует делать в этой итерации

Не добавлять пока:

- autonomous multi-agent orchestration;
- automatic delegation;
- shared multi-agent memory conflict resolution;
- mandatory long-running agents;
- automatic ADR promotion;
- automatic pattern → canonical knowledge promotion;
- Graphify как mandatory dependency;
- embeddings для всего repository knowledge без доказанной необходимости.

Цель этой итерации:

> **Сначала сделать состояние агента явным, извлекаемым, компактным и проверяемым.**

После этого безопаснее развивать autonomous execution.

---

## 35. Предлагаемая последовательность реализации

### Phase 1 — Remove ConPort

Удалить dependency и references.

### Phase 2 — Retrieval routing

Добавить общий policy feature и tests.

### Phase 3 — Local project memory

Расширить Basic Memory:

```text
context
decisions
progress
patterns
investigations
handoffs
```

и `docs/local`.

### Phase 4 — Integrations

Обновить:

```text
session-hygiene
structured-artifacts
agent-usage-hygiene
autonomy-boundaries
chroma
```

### Phase 5 — Graph experiment

Добавить experimental structural-code-intelligence capability и benchmark/evaluation.

### Phase 6 — Harden autonomy

После стабилизации memory/retrieval:

- evaluation harness;
- longer autonomous slices;
- explicit recovery/checkpoints.

### Phase 7 — Multi-agent

Только после того, как single-agent workflow умеет надёжно:

```text
retrieve
work
verify
persist state
resume
stop on design ambiguity
```

---

## 36. Ключевая архитектурная формула

В результате `ai-standards` должен разделять:

```text
AGENTS.md / rules
        ↓
HOW the agent works


canonical docs
        ↓
WHAT the project has established


Basic Memory / docs/local
        ↓
WHAT the agent already learned
and WHERE work currently stands


Chroma
        ↓
WHERE relevant code may be


Structural graph
        ↓
HOW code entities are connected


source + tests
        ↓
WHAT is actually true
```

И поверх всего этого:

```text
retrieval-routing
        ↓
WHAT should be consulted now
```

Это и должно стать основой следующего поколения knowledge/context management в `ai-standards`.

---

В этой схеме мне особенно нравится одно свойство: **Basic Memory, Chroma и будущий Graphify перестают быть тремя “MCP, которые мы установили” и становятся реализациями трёх разных capabilities**. Тогда правило «пользуйся доступными возможностями» можно сделать достаточно сильным, не заставляя агента ритуально вызывать все инструменты на каждом запросе.

Я бы ещё внёс одно небольшое изменение относительно моего прошлого предложения: **`retrieval-routing` стоит сделать самостоятельным feature уже сейчас**, а не распределять routing между Basic Memory/Chroma. Именно он в будущем позволит подключить Graphify или заменить конкретный backend без изменения design-first workflow.

И порядок работы я бы действительно выбрал: **ConPort removal → retrieval-routing → local Basic Memory taxonomy → интеграция с session/autonomy → Graphify evaluation**. Только после этого — длинные автономные сессии и multi-agent. Текущий `autonomy-boundaries` уже содержит подходящую основу: агент может исполнять согласованный дизайн, но не должен молча выбирать новый; значит, memory можно встроить туда как механизм сохранения состояния перед обязательной консультацией с человеком, а не как способ эту границу обойти.

---

## Пользователь — 2026-09-13 12:28:45

Всё отлично, я готовлюсь передать это в реализацию.
Но мне нужен ещё полный транскрипт этого обсуждения – сделай пожалуйста markdown-файл для загрузки.
