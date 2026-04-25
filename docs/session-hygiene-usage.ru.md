# Руководство по Session Hygiene

Англоязычный оригинал: [session-hygiene-usage.md](session-hygiene-usage.md)

Это руководство объясняет, как использовать feature `session-hygiene` из `ai-standards` в подключаемых проектах.

`session-hygiene` — это переиспользуемая process-feature для снижения context drift, stale assumptions и goal substitution в длинных chat sessions.

Feature остаётся tool-neutral. Она не кодирует конкретный context window size, message count или vendor-specific chat behavior.

## Цели

Используйте `session-hygiene`, когда хотите, чтобы агент или команда:

- замечали, когда длинный thread становится рискованно продолжать
- сохраняли critical context вне transient chat memory
- создавали compact handoffs перед началом нового чата
- повторно загружали project rules и task artifacts на границах фаз
- не продолжали молча из stale assumptions

Типовые результаты:

- меньше потерянных constraints
- более понятные phase transitions между design, implementation, review, merge и release
- лучшая continuity между fresh chats
- более reviewable long-running work

## Что покрывает feature

Feature стандартизует shared policy для:

- предупреждения о long-session risk
- handoff summaries
- рекомендаций начать fresh chat
- повторного чтения rules и artifacts при смене фазы работы
- отделения confirmed state от assumptions

Feature сознательно не стандартизует:

- жёсткие message-count, time или token-count limits
- tool-specific context-window behavior
- автоматические chat resets
- перенос полного разговора в summary

Проекты могут добавлять local thresholds, когда есть evidence, что конкретный tool, team или workflow в них нуждается.

## Предупреждение о длинной сессии

Агент должен предупредить пользователя, когда продолжение текущего thread повышает риск:

- context drift
- stale assumptions
- goal substitution
- lost constraints
- hidden decisions, которые трудно review

Предупреждение особенно важно, когда:

- текущая цель несколько раз переформулировалась
- старые решения конфликтуют с новыми instructions
- агент не уверен, какие constraints всё ещё применимы
- review потребует восстанавливать важный context из длинного разговора
- следующий шаг зависит от старого chat context, не зафиксированного в artifact или durable memory

## Handoff Summary

Перед продолжением рискованной длинной сессии агент должен предложить или подготовить compact handoff summary.

Рекомендуемые поля:

- текущая цель
- принятые решения
- затронутые файлы или модули
- active constraints и non-goals
- открытые вопросы
- verification status
- known risks
- recommended next bounded slice

Summary должен быть достаточно коротким, чтобы вставить его в новый чат или project artifact.

Отделяйте:

- confirmed project state
- user-approved decisions
- assumptions
- inferred context

Не превращайте handoff в полный transcript.

## Когда начинать новый чат

Предпочитайте fresh chat, когда:

- работа меняет фазу, например design to implementation, implementation to review, review to merge или merge to release
- текущий context уже нельзя compactly summarize
- следующий slice зависит от project rules или decisions, которые нужно явно перечитать
- агент предупредил о stale assumptions или goal drift
- пользователь хочет снизить context noise перед focused next step

Fresh chat должен начинаться с:

- handoff summary
- relevant project rules
- active context или task artifacts
- next bounded objective

## Повторная загрузка правил и durable context

На границах фаз перечитывайте relevant sources, а не полагайтесь только на chat memory:

- `AGENTS.md`
- project-local AI rules
- ConPort active context, если доступен
- task notes или change plans
- decision records
- module contracts или migration notes

Загружайте только то, что relevant для next slice. Session hygiene не должна становиться broad context loading by default.

## Связь с другими features

- `conport` хранит active context, progress и durable lessons между сессиями.
- `structured-artifacts` даёт change plans, decision records и module contracts, которые делают handoffs конкретными.
- `autonomy-boundaries` определяет, когда long autonomous execution должен остановиться для human review.
- `reasoning-hygiene` удерживает assumptions, edge cases и verification points явными.
- `agent-usage-hygiene` снижает avoidable context и usage waste.

`session-hygiene` фокусируется именно на надёжности active chat session.

## Пример manifest

```toml
features = [
  "conport",
  "design-first-collaboration",
  "reasoning-hygiene",
  "autonomy-boundaries",
  "structured-artifacts",
  "session-hygiene",
]
```

## Практические prompt patterns

Хорошие prompts:

- `Этот чат становится длинным. Подготовь handoff summary и предложи, продолжать здесь или начать новый чат.`
- `Перед следующей фазой перечитай project rules и кратко перечисли только constraints, важные сейчас.`
- `Подготовь new-chat handoff с goal, decisions, risks, verification status и next slice.`
- `Предупреди меня, если context drift или stale assumptions начинают влиять на задачу.`

Избегайте:

- `Продолжай по памяти; правила перепроверять не нужно.`
- `Суммаризируй вообще всё в чате.`
- `Продолжай, даже если цель изменилась.`

Предпочитайте:

- `Если продолжать этот thread рискованнее, чем начать fresh, скажи об этом и подготовь compact handoff.`
