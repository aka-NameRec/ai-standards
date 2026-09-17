# Предложение по развитию `ai-standards`

## 1. Цель

Следующий этап развития `ai-standards` должен сместить фокус с накопления инструкций на управление их жизненным циклом и контекстом.

`ai-standards` должен определять:

- как нормативное знание превращается в точное и проверяемое правило;
- где это правило должно находиться;
- когда оно должно загружаться;
- как агент должен обнаруживать task-specific procedures;
- как проверить, что правило или skill действительно изменяет поведение ожидаемым образом;
- как сохранять эти свойства одинаковыми для Codex, Claude, Kilo, Cursor и других harnesses.

### IMPORTANT: основной принцип

> **IMPORTANT: `ai-standards` MUST standardize how required knowledge is selected, placed, loaded, and verified, rather than maximize how much knowledge is always loaded. Keep only universally required invariants, routing rules, and mandatory gates in always-loaded instructions. Place task-specific procedures, conditional knowledge, retrievable knowledge, and deterministic mechanics in the appropriate on-demand layer. A rule or skill is complete only when its expected behavior can be verified through observable outcomes.**

Иными словами:

```text
right knowledge
      ↓
right layer
      ↓
right moment
      ↓
unambiguous instruction
      ↓
observable behavior
      ↓
verification
```

Главным результатом стандарта должен быть не максимальный объём инструкций в контексте агента, а воспроизводимое получение необходимого знания именно тогда, когда оно требуется.

---

# 2. Rule Engineering

Существующий `Import External Rules` следует обобщить из процесса импорта внешних правил в универсальный процесс **Rule Engineering**.

Сейчас `ai-standards` уже требует извлекать candidate rules, классифицировать их как `keep`, `adapt` или `reject`, отбрасывать vague/redundant/conflicting правила и нормализовать принятые правила. Это хорошая основа, но она применяется главным образом к внешним источникам.

Rule Engineering должен применяться одинаково к:

- внешним best practices;
- новым правилам, сформулированным внутри проекта;
- правилам reasoning;
- code-review rules;
- architecture rules;
- harness rules;
- содержимому skills;
- изменениям уже существующих rules.

## 2.1. Требования к правилу

Каждое нормативное правило должно проверяться по следующим свойствам:

### Atomic

Одно правило должно содержать одно нормативное требование.

Если две части предложения могут нарушаться независимо, их следует рассмотреть как два правила.

### Unambiguous

Формулировка должна минимизировать число разумных интерпретаций.

Необходимо избегать неопределённых требований вроде:

```text
Use existing abstractions where appropriate.
```

если можно установить наблюдаемый процесс:

```text
Before introducing a new abstraction, inspect the relevant scope for an
existing abstraction serving the same responsibility. Reuse it unless a
documented incompatibility prevents reuse.
```

### Actionable

Из правила должно следовать, что именно агент обязан сделать или не сделать.

### Properly scoped

Должны быть понятны условия применимости правила и границы, за которыми оно не действует.

### Observable

Должно существовать наблюдаемое состояние или поведение, по которому можно проверять соблюдение требования.

Не всякое правило можно проверить полностью автоматически, но критерий соблюдения должен быть хотя бы формулируемым.

### Unique

Правило не должно повторять существующее нормативное поведение.

При этом uniqueness следует определять не только текстуально.

Нужно проверять три уровня:

```text
lexical overlap
semantic overlap
behavioral overlap
```

Основной критерий:

> Существует ли уже правило, которое при тех же preconditions требует того же observable behavior?

### Non-conflicting

Новое правило не должно создавать несовместимое требование при тех же условиях.

Если применимы два правила, должен существовать способ одновременно выполнить оба либо должна быть явно определена precedence rule.

### Correct abstraction level

Project-specific, language-specific, framework-specific и universal process knowledge не должны смешиваться.

Правило следует помещать на самый общий уровень, на котором оно остаётся истинным.

### Portable

Shared rule не должен предполагать особенностей Codex, Claude, Kilo, Cursor или конкретной модели, если это не является целью самого правила.

Agent-specific mechanics должны находиться в adapters.

### Verifiable

Для правила должна существовать хотя бы одна из форм проверки:

```text
static validation
deterministic assertion
behavioral scenario
human rubric
cross-agent comparison
```

## 2.2. Interpretation surface

Полезно ввести рабочее понятие **interpretation surface**:

> количество существенных решений, которые агент вынужден самостоятельно додумывать между прочтением правила и его исполнением.

Низкий `interpretation surface` предпочтителен там, где требуется воспроизводимое поведение.

При этом он не должен искусственно снижаться там, где задача действительно требует contextual judgment.

---

# 3. Rule Engineering вместо только Import Flow

Существующий flow:

```text
source
↓
candidate rules
↓
keep / adapt / reject
↓
normalize
↓
place
```

следует расширить до:

```text
candidate normative knowledge
        ↓
extract candidate behaviors
        ↓
make each requirement atomic
        ↓
clarify preconditions and scope
        ↓
check interpretation ambiguity
        ↓
check lexical / semantic / behavioral overlap
        ↓
check conflicts and precedence
        ↓
select abstraction level
        ↓
select context layer
        ↓
define observable behavior
        ↓
define validation/eval
        ↓
accept / adapt / reject
```

External-rule importing после этого становится одним из способов получения candidate rules, а не самостоятельной методологией.

---

# 4. Context Architecture

После Rule Engineering нужно формализовать второй вопрос:

> **Где данное знание должно жить?**

Сегодня `AGENTS.md` остаётся shared source of truth, а adapters уже разводят Codex, Claude, Kilo и Cursor по их собственным механизмам.

Следует сделать это разделение явной частью стандарта.

## 4.1. Context placement model

Рекомендуемая модель:

| Layer | Назначение |
|---|---|
| `AGENTS.md` | universal invariants, routing, mandatory gates, precedence |
| Skill | repeatable task-specific procedure |
| Skill reference | conditional detailed knowledge, необходимое только при конкретном режиме skill |
| Retrieval | большой, изменчивый или project-specific корпус знаний |
| Script/tool | deterministic или fragile operation |
| Decision / contract / project knowledge | durable project truth |
| Adapter | mechanics конкретного harness |

### Placement questions

При добавлении нормативного знания следует последовательно определить:

```text
Needed for almost every task?
    → always-loaded rule

Repeatable procedure with recognizable trigger?
    → skill

Detailed knowledge needed only during that procedure?
    → skill reference

Large or searchable knowledge corpus?
    → retrieval

Deterministic/fragile operation?
    → script/tool

Durable project-specific fact or decision?
    → project knowledge

Agent-specific mechanics?
    → adapter
```

Таким образом, минификация `AGENTS.md` должна быть следствием Context Architecture, а не механическим разбиением большого Markdown-файла.

---

# 5. Минификация `AGENTS.md`

Цель не должна формулироваться как:

> вынести всё, что возможно.

Правильнее:

> **оставить always-loaded только то, что требуется для правильного выбора дальнейшего поведения.**

`AGENTS.md` постепенно должен стать control plane:

```text
AGENTS.md

universal invariants
routing rules
mandatory gates
precedence
discovery instructions
minimum completion requirements
```

Task-specific operational detail должен уходить в skills/references/retrieval/scripts.

Это особенно актуально для нынешнего состояния `AGENTS.md`, где рядом с core rules находятся подробные ConPort, Basic Memory, Chroma, design-first, reasoning и autonomy instructions.

Минификация должна производиться только после того, как существует безопасный механизм маршрутизации в вынесенное знание.

---

# 6. Skill Engineering

После реализации Rule Engineering следует создать единый domain **Skill Engineering**.

Не рекомендуется начинать с независимых `skill-authoring`, `skill-validation` и `skill-lifecycle`, потому что их границы пока являются гипотезой.

Предпочтительная начальная архитектура:

```text
skill-engineering/
    SKILL.md
    references/
        authoring.md
        validation.md
        evaluation.md
        lifecycle.md
        portability.md
```

Разделение на несколько skills следует делать только если реальные usage/eval data покажут независимые triggers и workflows.

## 6.1. Skill Authoring

`skill-authoring` должен быть первым практическим результатом Skill Engineering, но **сам должен быть создан по уже реализованному Rule Engineering**.

Это принципиальное требование.

При его создании каждая заимствованная идея из Anthropic, OpenAI или других источников должна пройти:

```text
candidate guidance
↓
Rule Engineering
↓
uniqueness/conflict check
↓
portability check
↓
context placement
↓
observable behavior definition
↓
accept/adapt/reject
```

Таким образом `skill-authoring` станет первым полноценным dogfooding нового Rule Engineering.

## 6.2. Базовые принципы Skill Authoring

Следует рассмотреть для нормализации следующие идеи.

### Progressive disclosure

OpenAI сейчас явно разделяет skill information на metadata, `SKILL.md` body и supporting resources; body загружается после выбора skill, а references/scripts используются по необходимости.

`ai-standards` должен закреплять сам принцип, но не зависеть от Codex-specific metadata.

### Context economy

Skill должен содержать только информацию, которая действительно меняет решения или улучшает выполнение задачи.

Не следует объяснять модели общие знания, которыми она уже устойчиво обладает.

### Degrees of freedom

Необходимый уровень детерминированности должен зависеть от риска операции:

```text
high freedom
    heuristics / contextual decision

medium freedom
    structured procedure

low freedom
    deterministic script/tool
```

### Portable core

Skill должен быть максимально agent-independent.

Agent-specific invocation/UI/hooks/tool syntax следует выносить в adapter.

---

# 7. Skill Validation и Skill Lifecycle

Валидацию skill необходимо разделить как минимум на четыре разных вопроса:

```text
Is it structurally valid?
Does it activate correctly?
Does the agent follow it?
Does it improve behavior?
```

Статический validator отвечает только на первый вопрос.

OpenAI прямо отмечает, что его validator проверяет frontmatter/naming/structure, но не доказывает качество решений skill.

## 7.1. Activation correctness

Для каждого skill должен существовать trigger eval set:

```text
positive cases
negative cases
boundary / ambiguous cases
```

Из него можно вычислять:

```text
activation recall
activation precision
false-positive rate
false-negative rate
```

Anthropic уже реализует практически именно такой подход: их `run_eval.py` запускает запрос несколько раз, фиксирует факт triggering и сравнивает фактическую trigger rate с ожидаемым `should_trigger`.

## 7.2. Behavioral correctness

Факт активации ещё не означает, что skill выполнен.

Необходимы task scenarios с проверяемыми expected invariants.

Пример для code review:

```text
fixture:
    code contains pre-existing defect
    new diff is unrelated

expected:
    reviewer MUST NOT report the old defect as introduced by the change
```

Проверяется результат, а не наличие определённой фразы.

## 7.3. Behavioral efficacy

Необходимо отличать:

```text
skill works
```

от:

```text
skill improves the agent
```

Для этого применяется baseline / ablation testing:

```text
same task + same model + same environment

A: without skill
B: with skill
```

После нескольких запусков сравнивается выполнение одних и тех же observable invariants.

## 7.4. Lifecycle

Предлагаемый lifecycle:

```text
candidate
↓
draft
↓
structurally validated
↓
activation-tested
↓
behavior-tested
↓
project-local / experimental
↓
stabilized
↓
generalized
↓
shared
↓
observed
↓
revised / deprecated
```

---

# 8. Coverage recurring behaviors, а не максимальное количество skills

Не следует вводить цель:

> для каждого правила создать skill.

Skill оправдан, если одновременно существуют:

```text
recognizable trigger
+
repeatable procedure
+
non-trivial reusable guidance
+
observable completion criteria
```

Если агент устойчиво выполняет действие на основании общего invariant и собственных базовых способностей, новый skill лишь увеличивает surface area стандарта.

Поэтому полноту следует оценивать как:

> **coverage of recurring behaviors that benefit from explicit reusable procedures**

а не как количество навыков.

---

# 9. Harness Architecture

`ai-standards` должен описывать минимальные возможности harness, необходимые для исполнения стандарта, независимо от vendor.

Например:

```text
discover rules
discover skills
load task-specific context
retrieve external/project knowledge
execute deterministic tools
capture observable execution events where available
run verification
preserve artifacts between phases
support bounded delegation when available
```

Не следует требовать одинаковой реализации этих механизмов.

Codex, Claude, Kilo и Cursor могут реализовывать их разными способами.

Shared standard определяет:

```text
required behavior
```

adapter определяет:

```text
mechanism
```

---

# 10. Standard Evals

`ai-standards` должен получить собственный regression suite.

Он должен проверять не Markdown как таковой, а поведение агента под действием standards.

## 10.1. Canonical scenarios

Нужно создать небольшой, но постепенно расширяемый корпус scenarios, например:

```text
ambiguous requirement
duplicate abstraction already exists
architecture decision exists
architecture decision absent
code review with no valid findings
pre-existing defect in review fixture
rule conflict
skill positive trigger
skill negative trigger
deterministic operation better performed by script
scope expansion requiring stop
verification unavailable
```

Каждый scenario содержит:

```text
input fixture
prompt
enabled standards/features
expected observable invariants
forbidden outcomes
optional scoring rubric
```

## 10.2. Baseline comparisons

При существенном изменении standards:

```text
baseline revision
vs
candidate revision
```

запускаются на одинаковых scenarios.

Сравнивается не буквальный текст ответа, а выполнение invariants.

---

# 11. Cross-agent portability evaluation

Portability должна быть проверяемым свойством.

Для критичных standard scenarios следует запускать минимум несколько representative harnesses:

```text
Codex
Claude
Kilo
Cursor
```

Не следует требовать идентичного текста или одинаковых внутренних действий.

Требуется сохранение нормативных инвариантов:

```text
same required decisions
same forbidden decisions
same stop conditions
same evidence requirements
same completion criteria
```

Результат cross-agent eval должен показывать divergence между harnesses.

Так можно обнаружить правило, которое хорошо интерпретирует Codex, но иначе понимает Kilo.

---

# 12. `standard-code-review` как pilot

`standard-code-review` следует использовать как первый полноценный pilot новой архитектуры.

Это удачный объект, потому что текущий code-review workflow уже содержит:

- natural-language activation;
- fixed checked dimensions;
- evidence requirements;
- prohibition on invented findings/padding;
- stable report shape;
- agent-independent behavior.

На нём можно последовательно проверить:

### Rule Engineering

Разложить review rules на atomic behaviors и проверить ambiguity/overlap/conflicts.

### Context Architecture

Определить, какие review invariants нужны always-on, а какие процедуры можно вынести в skill/references.

### Skill Engineering

Проверить activation correctness `standard-code-review`.

### Standard Evals

Сравнить качество review до и после изменения архитектуры.

После успешного pilot тот же механизм можно распространить на остальные features.

---

# 13. Последовательность реализации

## Phase 0 — Baseline

До изменения архитектуры зафиксировать текущее состояние:

- размер и composition `AGENTS.md`;
- существующие features/stacks/adapters;
- существующие skills;
- current code-review behavior;
- несколько representative scenarios для будущего сравнения.

Цель: получить baseline, относительно которого можно измерять последующие изменения.

---

## Phase 1 — Rule Engineering

Реализовать универсальный стандарт Rule Engineering.

Результаты:

- normative definition rule quality;
- ambiguity/atomicity/uniqueness/conflict criteria;
- behavioral uniqueness definition;
- abstraction-level criteria;
- portability requirement;
- observable-behavior requirement;
- обновлённый external import flow как частный случай Rule Engineering.

На этом этапе существующие правила массово не переписывать.

---

## Phase 2 — Rule traceability и validation support

Для правил, участвующих в evals, ввести стабильную связь:

```text
rule
↔
source location
↔
expected behavior
↔
eval scenarios
```

Необязательно показывать rule identifiers агенту в rendered `AGENTS.md`.

IDs могут существовать в source/eval metadata и использоваться только tooling.

Это позволит отвечать на вопрос:

> Какими тестами покрыто это правило?

---

## Phase 3 — Code Review dogfooding

Применить Rule Engineering к `standard-code-review`.

Провести:

- atomicity review;
- ambiguity review;
- duplicate/overlap analysis;
- conflict analysis;
- observable behavior mapping.

Создать первые behavioral scenarios.

Это первая проверка работоспособности Rule Engineering на реальном существующем feature.

---

## Phase 4 — Context Architecture

Определить формальные placement rules:

```text
always-loaded
skill
reference
retrieval
script/tool
project knowledge
adapter
```

После этого классифицировать существующее содержимое `AGENTS.md`.

Пока не переносить всё физически — сначала получить migration plan.

---

## Phase 5 — Minimal Eval Harness

До создания `skill-authoring` реализовать минимальную инфраструктуру eval:

```text
scenario definition
runner interface
result capture
deterministic assertions
human/LLM rubric where unavoidable
baseline/candidate comparison
adapter interface
```

Полная cross-agent автоматизация на этом этапе необязательна.

Главное — иметь способ проверить новые Rule/Skill Engineering rules.

---

## Phase 6 — Skill Engineering через Rule Engineering

Только теперь сформировать правила Skill Engineering.

Источники Anthropic/OpenAI и другие candidate sources проходят уже созданный Rule Engineering.

Именно здесь создаётся `skill-authoring`.

Следовательно:

```text
Rule Engineering
      ↓
applied to external skill-authoring guidance
      ↓
normalized candidate rules
      ↓
skill-authoring
```

Это обязательное dogfooding-требование.

После этого добавляются:

```text
validation
evaluation
lifecycle
portability
```

как references или отдельные skills — решение принимается на основании trigger/workflow analysis.

---

## Phase 7 — Skill activation/effect evals

Добавить:

```text
positive triggers
negative triggers
boundary triggers
behavior scenarios
with-skill baseline
without-skill baseline
```

Сначала для `standard-code-review` и `skill-authoring`.

---

## Phase 8 — `AGENTS.md` minification

Только после появления:

```text
Context Architecture
+
Skill Engineering
+
basic evals
```

начинать систематическое вынесение task-specific procedures.

Для каждого переноса проверять:

```text
old architecture behavior
vs
new routed architecture behavior
```

То есть уменьшение контекста не должно покупаться потерей поведения.

---

## Phase 9 — Cross-agent Standard Evals

Расширить runner adapters на доступные harnesses.

Начать формировать compatibility matrix:

```text
scenario      Codex   Claude   Kilo   Cursor
------------------------------------------------
CR-001        pass    pass     pass   pass
CR-002        pass    pass     fail   pass
SE-004        pass    n/a      pass   ...
```

Любая divergence становится предметом анализа:

```text
shared rule problem?
adapter problem?
harness limitation?
model variance?
```

---

# 14. Acceptance criteria всей инициативы

Работа может считаться успешной, когда выполняются следующие свойства:

1. Любое новое shared rule проходит один Rule Engineering flow независимо от источника.
2. Для нормативного правила можно сформулировать observable behavior.
3. Для recurring task можно обоснованно определить, нужен ли skill.
4. Для каждого skill можно проверить structural validity, activation и behavioral correctness.
5. Для важных skills можно сравнить результат with-skill и without-skill.
6. Существует формальное правило выбора между always-loaded context, skill, reference, retrieval, tool и project knowledge.
7. Уменьшение `AGENTS.md` сопровождается regression evals.
8. Shared policy не зависит от конкретного agent vendor.
9. Agent-specific differences локализуются в adapters.
10. Поведение critical workflows проверяется хотя бы на нескольких harnesses.
11. `standard-code-review` является первым подтверждённым end-to-end примером этой архитектуры.
12. `skill-authoring` сам создан и проверен посредством Rule Engineering.

---

# 15. Архитектурный результат

После реализации система должна выглядеть концептуально так:

```text
                    Rule Engineering
                          │
          ┌───────────────┼────────────────┐
          │               │                │
          ↓               ↓                ↓
  Context Architecture  Skill Engineering  Project Knowledge
          │               │                │
          └──────────┬────┴────────────┬───┘
                     ↓                 ↓
               Harness Architecture  Retrieval
                     │
                     ↓
                Standard Evals
                     │
                     ↓
           Cross-agent verification
```

`ai-standards` таким образом становится не хранилищем максимально полного набора prompts/rules, а системой управления нормативным знанием и поведением AI engineering agents.

Главный invariant:

> **Не количество инструкций определяет качество harness, а способность доставить необходимую, однозначную и проверяемую инструкцию в нужный момент и доказать, что требуемое поведение сохранилось.**