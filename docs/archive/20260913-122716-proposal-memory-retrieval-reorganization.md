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

# 2. Основной принцип

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

# 3. Удалить ConPort из ai-standards

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

Таким образом сохраняется модель памяти, но исчезает зависимость standards от конкретного abandoned/stagnating backend.

---

# 4. Ввести feature `retrieval-routing`

## Назначение

`retrieval-routing` определяет:

- когда агенту требуется retrieval;
- какой источник знания использовать;
- в каком порядке искать;
- когда переходить к более дорогому исследованию;
- как проверять полученные результаты.

Feature должен быть **tool-neutral**.

Он не должен содержать команды API Basic Memory, Chroma или Graphify.

Конкретные features реализуют соответствующие retrieval capabilities.

## Предлагаемые core rules

### R1 — Retrieve before broad exploration

> Before broad repository exploration, determine what information is missing and query the narrowest available knowledge source capable of answering it.

### R2 — Use available capabilities

> When an enabled retrieval capability directly matches the current information need, use it before falling back to broader manual exploration.

Это важнее слабого:

> Use X when useful.

Наличие инструмента должно означать, что агент обязан учитывать его при выборе стратегии поиска.

### R3 — Route by information need

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

### R4 — Retrieval is evidence discovery

> Retrieval narrows the evidence set; it does not establish correctness or completeness by itself.

### R5 — Verify at the authoritative layer

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

### R6 — Escalate progressively

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

# 5. Переработать feature `basic-memory`

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

## 5.1 Canonical project knowledge

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

## 5.2 Local working memory

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

# 6. Правило разделения canonical и local memory

Добавить жёсткое правило:

> Never treat local working memory as canonical project documentation.

И обратное:

> Do not write temporary task state, speculative findings, or session continuation data into canonical project documentation merely to preserve agent context.

Это защищает Git от превращения в dump внутреннего состояния агента.

---

# 7. Promotion local knowledge → canonical knowledge

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

# 8. Сохранить ConPort taxonomy как ai-standards memory taxonomy

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

# 9. Тип `context`

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

# 10. Тип `decisions`

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

# 11. Тип `progress`

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

# 12. Тип `patterns`

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

# 13. Тип `investigations`

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

# 14. Тип `handoffs`

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

# 15. Добавить memory-write policy

Агенту нельзя поручать «запоминай всё полезное».

Нужны критерии записи.

## Записывать в local memory, если информация:

- понадобится в следующей сессии;
- существенно влияет на дальнейшее решение;
- дорого восстанавливается;
- является результатом исследования;
- объясняет текущий статус;
- фиксирует unresolved question/blocker;
- является подтверждённым reusable pattern проекта.

## Не записывать, если информация:

- легко получается из одного очевидного файла;
- является transient tool output;
- является подробностью reasoning;
- уже существует канонически;
- является guess без полезной роли;
- дублирует существующую memory item без изменения состояния.

Ключевое правило:

> Memory is a curated state store, not an execution log.

---

# 16. Добавить memory-read policy

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

# 17. Изменить `session-hygiene`

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

# 18. Изменить `structured-artifacts`

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

# 19. Сохранить роль Chroma практически без изменений

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

# 20. Graphify / structural code intelligence

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

# 21. Graph capability должна быть experimental

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

# 22. Capability awareness

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

# 23. Retrieval capability registry

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

# 24. Design-first integration

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

# 25. Autonomy boundaries integration

Local memory является предпосылкой, а не заменой autonomy boundaries.

Добавить связь:

> Long autonomous execution must periodically preserve externally reviewable task state at meaningful phase boundaries.

Но:

> Persisting task state does not authorize the agent to cross an existing autonomy boundary.

И:

> When execution encounters a material design choice, contradictory requirements, widening scope, or evidence invalidating the agreed design, preserve the current state and request human direction rather than recording a new decision and continuing silently.

Это особенно важно перед будущей поддержкой long-running agents.

---

# 26. Подготовка к multi-agent работе

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

# 27. Предлагаемая перегруппировка features

## До

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

## После

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

# 28. Зависимости features

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

# 29. Recommended stack после изменения

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

# 30. Предлагаемая структура knowledge tree

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

# 31. Важное уточнение Basic Memory storage model

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

# 32. Изменить deployment terminology

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

# 33. Tests, которые следует добавить

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

Сценарии вида:

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

# 34. Что не следует делать в этой итерации

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

# 35. Предлагаемая последовательность реализации

## Phase 1 — Remove ConPort

Удалить dependency и references.

## Phase 2 — Retrieval routing

Добавить общий policy feature и tests.

## Phase 3 — Local project memory

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

## Phase 4 — Integrations

Обновить:

```text
session-hygiene
structured-artifacts
agent-usage-hygiene
autonomy-boundaries
chroma
```

## Phase 5 — Graph experiment

Добавить experimental structural-code-intelligence capability и benchmark/evaluation.

## Phase 6 — Harden autonomy

После стабилизации memory/retrieval:

- evaluation harness;
- longer autonomous slices;
- explicit recovery/checkpoints.

## Phase 7 — Multi-agent

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

# 36. Ключевая архитектурная формула

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