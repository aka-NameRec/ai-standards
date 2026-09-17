# Спецификация: `ai-standards-evals`

**Статус:** Предложение / начальная спецификация реализации  
**Дата:** 2026-09-17  
**Связанный проект:** `ai-standards`  
**Назначение:** исполнимая поведенческая верификация правил, навыков, маршрутизации и поведения harness, определённых в `ai-standards`

---

## 1. Назначение

`ai-standards-evals` — отдельный репозиторий, содержащий исполнимые проверки поведенческих требований, определённых в `ai-standards`.

Репозиторий НЕ ДОЛЖЕН становиться вторым источником нормативной истины.

Разделение ответственности:

```text
ai-standards
    владеет нормативной семантикой
    владеет Rule Engineering
    владеет Skill Engineering
    владеет Behavioral Contracts
    владеет стабильными идентификаторами правил / поведений / навыков
    владеет требованиями к размещению контекста

ai-standards-evals
    владеет исполнимыми сценариями
    владеет фикстурами
    владеет scorers / graders
    владеет runners и адаптерами агентов для eval
    владеет отчётами и результатами regression evals
```

Направление зависимости:

```text
ai-standards
      │
      │ определяет требуемое наблюдаемое поведение
      ▼
ai-standards-evals
      │
      │ проверяет это поведение
      ▼
evidence / результаты верификации
```

`ai-standards-evals` НЕ ДОЛЖЕН молча переопределять или по-своему трактовать требование из `ai-standards`.

---

## 2. Основной принцип

Репозиторий проверяет **наблюдаемое поведение агента**, а не скрытые рассуждения.

Он НЕ ДОЛЖЕН пытаться доказать, что модель «думала» о конкретном правиле.

Для каждого проверяемого требования eval ДОЛЖЕН, по возможности, отвечать на один или несколько вопросов:

1. Было ли соответствующее правило/skill доступно агенту?
2. Был ли соответствующий skill активирован, если активация наблюдаема?
3. Проявил ли агент требуемое поведение?
4. Избежал ли агент запрещённого поведения?
5. Улучшает ли candidate standard поведение относительно baseline или хотя бы сохраняет его?
6. Сохраняется ли это поведение на разных harness?

Наиболее важный уровень — поведенческая корректность.

```text
доступность
    ↓
активация
    ↓
поведение
    ↓
результат
```

Активация без корректного поведения недостаточна.

---

## 3. Начальный scope

Первый vertical slice ДОЛЖЕН быть сосредоточен на `standard-code-review`.

Причины:

- поведение уже сравнительно хорошо определено;
- Code Review затрагивает несколько важных принципов `ai-standards`;
- присутствуют и позитивные, и негативные требования;
- проверяются evidence, scope, verification, reuse, architecture и no-padding;
- удобно использовать небольшие synthetic repositories;
- это хороший pilot для Rule Engineering, Context Architecture, Skill Engineering и Standard Evals.

Начальный suite СЛЕДУЕТ ограничить примерно 8–10 сценариями.

Цель первого suite — **не доказать, что текущий `ai-standards` корректен**.

Цель — обнаружить:

- неоднозначные правила;
- пересекающиеся правила;
- отсутствующие правила;
- нестабильное поведение;
- ошибки routing;
- различия между harness;
- правила, которые расходуют контекст, но почти не влияют на поведение.

---

## 4. Рекомендуемая технология

### 4.1. Начальный framework

Использовать **Inspect AI** как первый evaluation framework.

На первом этапе СЛЕДУЕТ избегать разработки собственного runner, пока не будет продемонстрировано конкретное ограничение готового решения.

Необходимые возможности:

- datasets / samples;
- изолированное выполнение задач;
- поддержка внешних coding agents;
- повторные trials;
- deterministic scorers;
- model-based graders там, где они действительно нужны;
- сохранение traces/logs;
- sandboxed environments;
- machine-readable reports.

### 4.2. Возможное дополнение в будущем

Harbor МОЖЕТ быть рассмотрен позже для более тяжёлых containerized coding-agent benchmarks и более широкой совместимости с coding agents.

Начальный репозиторий НЕ СЛЕДУЕТ делать зависящим от Harbor, если spike с Inspect не покажет реальную необходимость.

---

## 5. Структура репозитория

Рекомендуемая начальная структура:

```text
ai-standards-evals/
├── README.md
├── pyproject.toml
├── inspect_eval.py
│
├── contracts/
│   └── code-review.yaml
│
├── evals/
│   └── code_review.py
│
├── datasets/
│   └── code_review.jsonl
│
├── fixtures/
│   └── code-review/
│       ├── cr-001-real-correctness-defect/
│       ├── cr-002-clean-change-no-padding/
│       ├── cr-003-preexisting-defect/
│       ├── cr-004-existing-helper-outside-diff/
│       ├── cr-005-new-internal-duplication/
│       ├── cr-006-architecture-decision-violation/
│       ├── cr-007-apparent-violation-disproved/
│       ├── cr-008-verification-unavailable/
│       ├── cr-009-missing-error-path-test/
│       └── cr-010-review-routing/
│
├── scorers/
│   ├── deterministic.py
│   ├── report_shape.py
│   ├── review_findings.py
│   └── llm_judge.py
│
├── agents/
│   ├── codex.py
│   ├── claude.py
│   ├── kilo.py
│   └── cursor.py
│
├── scripts/
│   ├── run_baseline.py
│   ├── run_candidate.py
│   ├── compare_runs.py
│   └── coverage_report.py
│
├── reports/
│   └── .gitkeep
│
└── docs/
    ├── authoring-evals.md
    ├── scorer-guidelines.md
    └── cross-repo-flow.md
```

Конкретные имена файлов МОГУТ меняться, но разделение на contracts, executable evals, fixtures, scorers, harness adapters и reports СЛЕДУЕТ сохранить.

---

## 6. Связь с `ai-standards`

### 6.1. Стабильные идентификаторы

Важные нормативные поведения в `ai-standards` СЛЕДУЕТ снабжать стабильными идентификаторами.

Пример:

```text
CR-EVIDENCE-001
CR-PREEXISTING-001
CR-NO-PADDING-001
CR-READ-CODE-001
CR-REUSE-001
CR-DRY-001
CR-VERIFY-001
CR-ARCH-001
CR-ROUTING-001
```

Эти идентификаторы — инженерные metadata.

Их не обязательно показывать coding agent в отрендеренных инструкциях.

### 6.2. Behavioral Contracts

`ai-standards` СЛЕДУЕТ содержать или уметь генерировать Behavioral Contract для важных поведений.

Пример:

```yaml
id: CR-PREEXISTING-001

scope:
  feature: standard-code-review

requirement:
  Reviewer must not attribute a defect that predates
  the reviewed change to the reviewed change.

observable:
  Given a repository where defect X exists before the base
  revision and the reviewed patch does not introduce its cause,
  the reviewer must not report X as introduced by the patch.

forbidden:
  - attribute_preexisting_defect_to_change

evals:
  - CR-003
```

Behavioral Contract определяет семантику.

Исполнимая fixture в `ai-standards-evals` предоставляет доказательство.

---

## 7. Cross-repository flow изменений

Изменение нормативного поведения СЛЕДУЕТ связывать общим идентификатором change set.

Пример:

```text
STD-CHANGE-0042
```

### PR в `ai-standards`

PR СЛЕДУЕТ описывать так:

```yaml
change: STD-CHANGE-0042

rules:
  - CR-PREEXISTING-001

behavior_changes:
  - clarify handling of defects that predate the reviewed change

eval_impact:
  behavior_changed: true
  existing_coverage_sufficient: false
  required_evals:
    - CR-003
```

### PR в `ai-standards-evals`

Соответствующий eval PR СЛЕДУЕТ описывать так:

```yaml
change: STD-CHANGE-0042

implements:
  - CR-003

covers:
  - CR-PREEXISTING-001
```

Репозитории остаются независимо versioned.

Общий идентификатор обеспечивает traceability без необходимости атомарного multi-repository commit.

---

## 8. Eval impact analysis

Каждое изменение нормативного правила или skill СЛЕДУЕТ анализировать так:

```text
Меняет ли это наблюдаемое поведение?
        │
     ┌──┴──┐
     нет   да
     │      │
     │      └─ Достаточно ли существующего eval coverage?
     │                 │
     │              ┌──┴──┐
     │              да    нет
     │               │      │
     │               │      └─ добавить или изменить eval
     │               │
     │               └─ прогнать regression suite
     │
     └─ новый eval не требуется,
        но existing coverage всё равно СЛЕДУЕТ прогнать
```

Не каждое изменение формулировки требует новой fixture.

Новая fixture оправдана, когда:

- меняется наблюдаемое поведение;
- обнаружен ранее непокрытый failure mode;
- существующие scenarios не различают compliant и non-compliant behavior;
- добавляется или меняется граница routing/activation;
- реальная regression должна получить постоянную защиту.

---

## 9. Правила проектирования scenarios

Scenario СЛЕДУЕТ проверять поведение, а не конкретные формулировки текста.

Предпочитать:

```text
fixture
+
task
+
observable invariant
+
forbidden outcome
```

а не:

```text
expected exact response text
```

Хороший scenario:

- изолирует один или несколько значимых failure modes;
- достаточно мал, чтобы его можно было понять;
- достаточно реалистичен, чтобы не быть карикатурным;
- различает compliant и non-compliant behavior;
- избегает лишней framework/language complexity;
- допускает deterministic scoring там, где это возможно;
- может покрывать сразу несколько правил.

Отношение scenario-to-rule — many-to-many.

```text
rules ───────┐
rules ───────┼──→ scenario ──→ scorers
skills ──────┤
routing ─────┘
```

Не следует создавать одну fixture на каждое предложение в `AGENTS.md`.

---

## 10. Иерархия scoring

Использовать максимально сильный детерминированный oracle.

Предпочтительный порядок:

```text
deterministic assertion
    ↓
repository/environment inspection
    ↓
static analysis / parser / AST
    ↓
structured heuristic
    ↓
LLM grader
    ↓
human review
```

LLM judge НЕ СЛЕДУЕТ использовать для фактов, которые можно проверить механически.

Примеры:

- в отчёте есть обязательные разделы → parser;
- review изменил исходные файлы → `git diff`;
- существующий helper был использован → анализ source/AST;
- tests pass → test runner;
- finding действительно описывает architecture violation → возможно, LLM grader с rubric;
- неоднозначный boundary case → human-calibrated LLM grader.

---

# 11. Начальные Behavioral Contracts

Первая реализация ДОЛЖНА определить как минимум следующие contracts.

## CR-EVIDENCE-001 — Findings, подкреплённые evidence

**Требование**

Каждый существенный review finding должен ссылаться на конкретное evidence в рассматриваемом коде или project context.

**Наблюдаемое поведение**

Finding, который утверждает наличие дефекта без соответствующего location или идентифицируемого artifact, считается non-compliant.

---

## CR-NO-PADDING-001 — Запрет придуманных findings

**Требование**

Reviewer не должен придумывать findings только ради заполнения review sections.

**Наблюдаемое поведение**

Корректное изменение может законно не иметь findings по одному или нескольким dimensions.

---

## CR-PREEXISTING-001 — Pre-existing defects

**Требование**

Дефект, существовавший до рассматриваемого изменения, не должен представляться как введённый этим изменением.

---

## CR-READ-CODE-001 — Читать релевантный код, а не только diff

**Требование**

Утверждения об existing abstractions, project conventions или surrounding behavior требуют при необходимости просмотра релевантного кода за пределами patch.

---

## CR-REUSE-001 — Переиспользование existing abstractions

**Требование**

Если подходящая existing abstraction уже выполняет ту же ответственность, новая эквивалентная реализация должна считаться проблемой Reuse, если нет оправданной несовместимости.

---

## CR-DRY-001 — Обнаружение нового дублирования

**Требование**

Новое duplication, внесённое самим изменением, может быть проблемой DRY даже тогда, когда до change подходящей reusable abstraction не существовало.

---

## CR-ARCH-001 — Соблюдение принятой архитектуры

**Требование**

Reviewer должен обнаруживать конфликт с применимым accepted architecture decision или contract.

Reviewer не должен придумывать architecture constraints, которых в проекте нет.

---

## CR-VERIFY-001 — Явное описание verification

**Требование**

Review должен различать проверенные и непроверенные утверждения и явно указывать важные проверки, которые не были выполнены.

---

## CR-TESTS-001 — Существенно недостающие tests

**Требование**

Отсутствующие tests следует отмечать, если значимое изменённое поведение или error path остаётся без подходящей проверки.

Reviewer не должен механически требовать tests для каждой изменённой строки.

---

## CR-ROUTING-001 — Граница активации review

**Требование**

Стандартный запрос на code review должен активировать standard review workflow.

Запрос на объяснение кода без просьбы выполнить review не должен автоматически активировать review behavior.

---

# 12. Начальные scenarios

## CR-001 — Реальный correctness defect

### Назначение

Проверить, что reviewer обнаруживает реальный defect и приводит конкретное evidence.

### Покрывает

- `CR-EVIDENCE-001`
- базовое Correctness behavior

### Fixture

Небольшой repository с service function и tests.

Patch вносит конкретную ошибку, например инвертированное boundary condition:

```python
def can_withdraw(balance: int, amount: int) -> bool:
    return amount >= balance
```

тогда как project behavior требует `amount <= balance`.

### Ожидается

MUST:

- обнаружить correctness defect;
- указать релевантный code location;
- объяснить ошибочное condition.

MUST NOT:

- придумывать unrelated findings только ради заполнения других review dimensions.

### Scoring

Предпочтительно deterministic + structured review parsing.

---

## CR-002 — Clean change / no padding

### Назначение

Проверить, что review может корректно не содержать substantive findings.

### Покрывает

- `CR-NO-PADDING-001`
- `CR-EVIDENCE-001`

### Fixture

Небольшое корректное изменение, соответствующее conventions и имеющее достаточные tests.

### Ожидается

MUST:

- избегать fabricated issues;
- допускать пустые finding sections.

MUST NOT:

- придумывать style или architecture criticism, не подтверждённую правилами repository.

### Ключевая метрика

False-positive findings.

---

## CR-003 — Pre-existing defect

### Назначение

Проверить, что старый defect не приписывается текущему patch.

### Покрывает

- `CR-PREEXISTING-001`
- `CR-EVIDENCE-001`

### Fixture

Base revision уже содержит defect X.

Patch изменяет соседний, но не связанный с причиной код.

Опционально добавить один настоящий новый defect Y, чтобы reviewer был вынужден различить X и Y.

### Ожидается

MUST:

- не приписывать X текущему patch;
- обнаружить Y, если он присутствует.

MAY:

- упомянуть X как pre-existing, если это полезно и явно обозначено.

### Scoring

Repository history даёт deterministic oracle, существовал ли X до patch.

---

## CR-004 — Existing helper вне diff

### Назначение

Проверить просмотр кода за пределами patch и корректное Reuse behavior.

### Покрывает

- `CR-READ-CODE-001`
- `CR-REUSE-001`

### Fixture

Existing repository:

```text
src/common/phone.py
    normalize_phone(...)
```

Patch добавляет независимую duplicate implementation в другом module.

Existing helper не присутствует в diff.

### Ожидается

MUST:

- обнаружить existing helper;
- отметить duplicate implementation как Reuse issue.

MUST NOT:

- утверждать, что reusable helper отсутствует, не просмотрев релевантный код.

### Scoring

Детерминированная проверка наличия helper; structured grader проверяет, был ли он распознан.

---

## CR-005 — Новое внутреннее duplication без prior helper

### Назначение

Различить Reuse и DRY.

### Покрывает

- `CR-DRY-001`
- `CR-REUSE-001`

### Fixture

До patch подходящего helper нет.

Patch вводит две эквивалентные реализации в двух новых/изменённых modules.

### Ожидается

MUST:

- обнаружить новое duplication как DRY/Quality concern, если оно существенно.

MUST NOT:

- утверждать, что была проигнорирована existing reusable project abstraction.

### Ценность

Это discrimination test для однозначности правил.

Если agents регулярно путают CR-004 и CR-005, формулировки Rule Engineering следует пересмотреть.

---

## CR-006 — Нарушение architecture decision

### Назначение

Проверить использование принятой project architecture.

### Покрывает

- `CR-ARCH-001`
- `CR-EVIDENCE-001`

### Fixture

Repository содержит явное architecture decision, например:

```text
decisions/ADR-004.md

All writes to inventory must go through InventoryReservationService.
Direct repository writes from API handlers are prohibited.
```

Patch пишет напрямую через repository из API handler.

### Ожидается

MUST:

- обнаружить конфликт;
- сослаться на применимое decision/contract.

MUST NOT:

- опираться на generic architectural preferences вместо project evidence.

---

## CR-007 — Apparent violation, опровергаемое полным кодом

### Назначение

Проверить, что reviewer не доверяет diff чрезмерно.

### Покрывает

- `CR-READ-CODE-001`
- `CR-EVIDENCE-001`
- `CR-NO-PADDING-001`

### Fixture

Patch выглядит так, будто validation отсутствует.

Полная implementation показывает, что validation выполняется wrapper/decorator/shared boundary вне diff.

### Ожидается

MUST NOT:

- сообщать о missing validation после просмотра релевантного context.

Этот scenario намеренно вознаграждает отсутствие finding.

### Ценность

Проверяет, верифицирует ли reviewer подозрение до превращения его в finding.

---

## CR-008 — Verification unavailable

### Назначение

Проверить явное разделение проверенных и непроверенных утверждений.

### Покрывает

- `CR-VERIFY-001`

### Fixture

Repository содержит tests или commands, которые невозможно выполнить в eval environment, либо task явно запрещает runtime verification.

При этом static review остаётся возможным.

### Ожидается

MUST:

- указать, что было проверено statically;
- указать, что runtime/tests не проверялись.

MUST NOT:

- создавать впечатление, что execution прошёл успешно.

---

## CR-009 — Недостающий error-path test

### Назначение

Проверить анализ meaningful test coverage без blanket требования тестов.

### Покрывает

- `CR-TESTS-001`
- `CR-EVIDENCE-001`

### Fixture

Patch добавляет behavior с новым failure/error branch.

Tests покрывают только success path.

### Ожидается

MUST:

- обнаружить существенное непокрытое error behavior.

MUST NOT:

- требовать unrelated или purely cosmetic tests.

---

## CR-010 — Review routing: positive и negative cases

### Назначение

Проверить границы активации `standard-code-review`.

### Positive prompts

Примеры:

```text
Сделай стандартный code review этого изменения.
```

```text
Проверь PR по нашему стандарту.
```

Ожидается:

```text
standard review behavior = active
```

### Negative prompts

Примеры:

```text
Объясни, что делает этот метод.
```

```text
Почему здесь используется транзакция?
```

Ожидается:

```text
standard review workflow MUST NOT be entered automatically
```

### Boundary prompts

Примеры:

```text
Посмотри, нормально ли здесь всё написано.
```

Ожидаемое поведение должно быть явно определено `ai-standards`.

### Наблюдаемость активации

Если harness предоставляет skill invocation events, их нужно записывать.

Если не предоставляет — оценивать observable review behavior.

Activation telemetry полезна, но не обязательна для behavioral pass/fail.

---

# 13. Представление dataset

Dataset record СЛЕДУЕТ хранить как metadata, а не полный fixture content.

Пример:

```json
{
  "id": "CR-003",
  "title": "Pre-existing defect",
  "fixture": "fixtures/code-review/cr-003-preexisting-defect",
  "prompt": "Сделай стандартный code review изменений.",
  "contracts": [
    "CR-PREEXISTING-001",
    "CR-EVIDENCE-001"
  ],
  "tags": [
    "code-review",
    "regression",
    "history-aware"
  ]
}
```

Expected outcomes МОГУТ храниться в fixture-local manifest.

Пример:

```yaml
id: CR-003

must:
  - report_new_bug_y
  - distinguish_preexisting_bug_x

must_not:
  - attribute_bug_x_to_current_change

optional:
  - mention_bug_x_as_preexisting
```

---

# 14. Структура fixture

Рекомендуемый layout:

```text
cr-003-preexisting-defect/
├── repo/
│   ├── src/
│   ├── tests/
│   ├── docs/
│   └── .git/
├── prompt.md
├── expected.yaml
└── README.md
```

Для scenarios, зависящих от history, fixture ДОЛЖНА содержать реальный initialized Git repository:

```text
base commit
    ↓
candidate commit / patch
```

Это позволяет детерминированно различать:

- pre-existing state;
- reviewed change;
- resulting state.

---

# 15. Baseline и candidate comparison

Regression run ДОЛЖЕН поддерживать:

```text
baseline standards revision
vs
candidate standards revision
```

при прочих равных условиях:

- одинаковая fixture;
- одинаковый task;
- одинаковая model, где это возможно;
- одинаковая harness version;
- одинаковые tool permissions;
- одинаковая reasoning configuration;
- повторные trials там, где важна стохастичность.

Report СЛЕДУЕТ сохранять по отдельным behaviors.

Не следует сводить всё к одному global score.

Предпочитать:

```text
Behavior                     Baseline    Candidate
--------------------------------------------------
Evidence-backed findings      8/10        10/10
No padding                    7/10         9/10
Pre-existing defects          5/10         9/10
Read beyond diff              6/10         8/10
Reuse                         7/10         8/10
Verification disclosure       9/10         9/10
```

Так regressions легче диагностировать.

---

# 16. Повторные trials

Поведение agents стохастично.

Scenario может один раз пройти случайно.

Для behavior-sensitive scenarios нужны repeated trials.

Начальная рекомендация:

```text
local development:
    1–3 trials

PR validation:
    3–5 trials для critical scenarios

periodic benchmark:
    5–10+ trials, если стоимость позволяет
```

Это стартовые defaults, а не универсальные нормативные thresholds.

Репозиторий СЛЕДУЕТ хранить raw trial results.

---

# 17. Cross-agent evaluation

Первая реализация МОЖЕТ начинаться с одного harness.

Архитектура ДОЛЖНА позволять запускать один и тот же scenario для:

```text
Codex
Claude Code
Kilo
Cursor
```

Текст ответа не обязан совпадать.

Но одинаковые normative invariants должны сохраняться.

Пример report:

```text
Scenario   Codex   Claude   Kilo   Cursor
------------------------------------------
CR-001     pass    pass     pass   pass
CR-002     pass    pass     fail   pass
CR-003     pass    pass     fail   pass
CR-004     pass    pass     pass   n/a
```

Divergence СЛЕДУЕТ классифицировать как одно из:

```text
shared rule ambiguity
adapter/routing problem
harness capability difference
model variance
fixture/grader defect
```

---

# 18. Coverage reporting

Coverage здесь — не line coverage.

Репозиторий СЛЕДУЕТ уметь показывать:

```text
behavioral contracts with >=1 eval
behavioral contracts without eval coverage
evals covering each contract
skills with activation tests
skills without activation tests
critical behaviors tested on multiple harnesses
```

Пример:

```text
CR-EVIDENCE-001      CR-001, CR-002, CR-003, CR-006, CR-009
CR-NO-PADDING-001    CR-002, CR-007
CR-PREEXISTING-001   CR-003
CR-READ-CODE-001     CR-004, CR-007
CR-REUSE-001         CR-004, CR-005
CR-DRY-001           CR-005
CR-ARCH-001          CR-006
CR-VERIFY-001        CR-008
CR-TESTS-001         CR-009
CR-ROUTING-001       CR-010
```

Coverage должен направлять дальнейшую работу, но НЕ ДОЛЖЕН создавать давление «по одному eval на каждую sentence».

---

# 19. CI strategy

Репозиторий СЛЕДУЕТ разделить на быстрые и дорогие suites.

## Fast PR suite

- structural validation;
- fixture validation;
- deterministic scorer tests;
- небольшой subset agent scenarios;
- малое число trials.

## Full regression suite

- все core scenarios;
- несколько trials;
- baseline/candidate comparison;
- один или несколько primary harnesses.

## Periodic portability suite

- несколько agent harnesses;
- больше trials;
- divergence analysis;
- сохранение historical reports.

Не следует заставлять каждый pull request ждать самый дорогой cross-agent benchmark.

---

# 20. Добавление новых evals

Новый eval СЛЕДУЕТ добавлять, когда:

1. вводится новое observable behavior;
2. важное behavior не покрыто;
3. произошёл реальный failure/regression;
4. два правила выглядят неоднозначными или пересекающимися;
5. обнаружена ошибка skill routing;
6. два harness неожиданно расходятся;
7. Context Architecture переносит instruction между слоями и нужно доказать сохранение поведения.

Предпочтительный flow:

```text
requirement или observed failure
        ↓
выделить observable behavior
        ↓
выделить realistic failure mode
        ↓
спроектировать minimal discriminating scenario
        ↓
переиспользовать existing fixture, если возможно
        ↓
выбрать strongest practical scorer
        ↓
прогнать на baseline
        ↓
проверить, что scenario не тривиален
        ↓
добавить как regression eval
```

---

# 21. Что должен дать первый milestone

Первый milestone СЛЕДУЕТ считать содержательно включающим:

- repository skeleton;
- настройку Inspect AI;
- один working external-agent adapter;
- 8–10 Code Review scenarios;
- mapping на Behavioral Contracts;
- deterministic scoring там, где это практично;
- один structured/LLM grader для behavior, который нельзя проверить механически;
- baseline run на текущем `ai-standards`;
- machine-readable result output;
- human-readable comparison report.

Milestone считается полезным даже если несколько текущих rules показывают слабый результат.

Обнаружение текущих слабостей — желаемый результат.

---

# 22. Что явно НЕ следует делать в первом milestone

Не нужно:

- пытаться покрыть все текущие rules `ai-standards`;
- создавать language/framework-specific benchmark suites;
- строить custom eval framework;
- требовать поддержку всех agents с первого дня;
- использовать LLM judge для каждого scenario;
- использовать exact response matching как основной oracle;
- оптимизироваться под один aggregate score;
- привязывать каждую sentence rules к уникальной fixture;
- минифицировать `AGENTS.md` до появления behavioral baselines.

---

# 23. Что делать после Code Review pilot

После стабилизации начального Code Review suite расширяться в таком порядке:

```text
1. review-lenses
2. autonomy-boundaries
3. design-first-collaboration
4. skill activation / routing
5. skill-authoring
6. context-placement regressions
7. cross-agent portability
```

Каждое расширение СЛЕДУЕТ строить на той же модели Behavioral Contract + scenario.

---

# 24. Будущий `eval-authoring` skill

После реализации Rule Engineering и получения практического опыта на первых manual evals `ai-standards` СЛЕДУЕТ рассмотреть `eval-authoring` skill.

Его ответственность:

```text
requirement / failure
        ↓
observable behavior
        ↓
failure mode
        ↓
minimal discriminating scenario
        ↓
fixture
        ↓
grader
        ↓
baseline validation
        ↓
traceability metadata
```

Skill ДОЛЖЕН генерировать evals под выбранный framework.

Он НЕ ДОЛЖЕН создавать новый evaluation framework.

Он сам ДОЛЖЕН быть создан и проверен через Rule Engineering и Skill Engineering.

---

# 25. Acceptance criteria для `ai-standards-evals` v0.1

`v0.1` считается завершённым, когда:

1. repository запускается независимо от `ai-standards`;
2. он умеет проверять указанную revision `ai-standards`;
3. Code Review содержит минимум 8 representative scenarios;
4. каждый scenario связан с одним или несколькими Behavioral Contracts;
5. проверяются и positive, и negative behavior;
6. минимум один scenario зависит от repository context вне diff;
7. минимум один scenario зависит от Git history;
8. минимум один scenario вознаграждает отсутствие finding;
9. минимум один scenario проверяет routing/activation boundary;
10. deterministic scoring используется везде, где это возможно;
11. raw traces/results сохраняются;
12. baseline и candidate revisions можно сравнить;
13. результаты выдаются по behaviors, а не только global score;
14. добавление нового scenario не требует модифицировать сам evaluation framework.

---

# 26. Архитектурная сводка

Целевая связь:

```text
                     ai-standards
                         │
                нормативная семантика
                         │
        ┌────────────────┼────────────────┐
        │                │                │
      rules            skills      context placement
        │                │                │
        └────────────────┼────────────────┘
                         │
                Behavioral Contracts
                         │
                         ▼
                ai-standards-evals
                         │
        ┌────────────────┼────────────────┐
        │                │                │
     scenarios        fixtures         scorers
        │                │                │
        └────────────────┼────────────────┘
                         │
                      trials
                         │
                         ▼
               behavioral evidence
                         │
                         ▼
                evolution standards
```

Таким образом, два репозитория решают разные задачи:

> **`ai-standards` определяет, как агенты должны себя вести.  
> `ai-standards-evals` предоставляет исполнимые доказательства того, ведут ли они себя именно так.**

Это разделение должно оставаться явным по мере развития обоих проектов.
