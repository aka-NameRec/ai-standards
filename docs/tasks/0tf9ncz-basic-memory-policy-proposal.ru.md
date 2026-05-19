# Задача 0tf9ncz: предложение по политике Basic Memory

Англоязычный оригинал: [0tf9ncz-basic-memory-policy-proposal.md](0tf9ncz-basic-memory-policy-proposal.md)

## Статус

Подготовлено как change proposal. В shared fragments пока не внедрено.

## Цель

Определить минимальные изменения в `ai-standards`, необходимые для официальной фиксации следующей модели памяти:

- `docs/decisions/**`, `docs/architecture/**` и module contracts являются canonical project knowledge.
- Изменения canonical documentation требуют явного запроса человека.
- `docs/ai-memory/**` является agent-managed working memory.
- `Basic Memory` является предпочтительным retrieval и indexing layer над Git-tracked Markdown knowledge.
- `ConPort` понижается с durable project memory до transient session memory и handoff storage.

## Файлы для изменения

- [../../fragments/tools/conport.md](../../fragments/tools/conport.md)
- [../../fragments/process/structured-artifacts.md](../../fragments/process/structured-artifacts.md)
- [../../fragments/process/session-hygiene.md](../../fragments/process/session-hygiene.md)
- [../session-hygiene-usage.md](../session-hygiene-usage.md)
- [../session-hygiene-usage.ru.md](../session-hygiene-usage.ru.md)
- [../structured-artifacts-usage.md](../structured-artifacts-usage.md)
- [../structured-artifacts-usage.ru.md](../structured-artifacts-usage.ru.md)
- [../../README.md](../../README.md)
- [../../README.ru.md](../../README.ru.md)

## Обязательные изменения политики

### 1. Переопределить ConPort как transient memory

Текущие shared wording трактуют ConPort как durable project memory для decisions, progress, glossary terms и active context.

Требуемое изменение:

- Сохранить требование загружать релевантный ConPort context в начале задачи, когда MCP server доступен.
- Заменить durable-memory wording на transient operational-memory wording.
- Ограничить назначение ConPort session handoff, active context, recent progress, investigation state и compact next-step summaries.
- Явно указать, что durable project knowledge должно жить в Git-tracked Markdown, а не только в ConPort.

Предлагаемая формулировка для `fragments/tools/conport.md`:

```md
## ConPort Usage
- At the start of each task or session, load relevant ConPort context when the MCP server is available.
- Use ConPort for transient operational memory such as active context, recent progress, investigation state, and session handoffs.
- Do not treat ConPort as the canonical source of durable project truth.
- Record durable architectural, operational, and module-boundary knowledge in Git-tracked Markdown artifacts.
- Prefer targeted retrieval over large context dumps.
- Before logging substantial new knowledge, align with the user if the workspace follows a confirmation-based ConPort workflow.
- After significant work, update ConPort with the result, rationale, and next steps when the user wants the memory synchronized.
```

### 2. Ввести явное разделение canonical и working memory

Текущие shared rules разделяют decision records и ConPort, но не задают явный canonical-documentation layer и agent-managed working-memory layer.

Требуемое изменение:

- Определить canonical documentation как Git-tracked project knowledge.
- Определить agent working memory как не-canonical, но reviewable Markdown.
- Сделать `docs/ai-memory/**` рекомендуемым местом для agent-managed memory в downstream projects, которые включают эту модель.

Предлагаемая формулировка для `fragments/process/structured-artifacts.md`:

```md
## Decision Records
- Create a short decision record when an architectural or operational choice will matter for future changes and code review.
- Use decision records and module contracts for durable repository history.
- Use agent working memory for evolving context, temporary findings, and notes that are not yet accepted as canonical documentation.
- Keep one decision record focused on one choice, its rationale, alternatives, and consequences.
```

Добавить новый раздел после `Decision Records`:

```md
## Canonical Documentation And Agent Working Memory
- Treat `docs/decisions/**`, `docs/architecture/**`, `MODULE_CONTRACT.md`, and equivalent local artifacts as canonical project knowledge.
- Treat `docs/ai-memory/**` as agent-managed working memory rather than canonical truth.
- Durable conclusions must be promoted from working memory into canonical documentation only on explicit user request.
- Working memory should link to canonical documents when they already exist instead of duplicating them.
```

### 3. Защитить canonical docs от автономных правок

Текущие shared rules поощряют structured artifacts, но не запрещают явно тихие правки canonical documentation в ходе несвязанной implementation work.

Требуемое изменение:

- Добавить write policy, запрещающую autonomous edits в canonical documentation.
- Разрешить autonomous edits только в agent working memory.
- Потребовать deduplication и contradiction checks перед изменением canonical documentation.

Предлагаемая формулировка для `fragments/process/structured-artifacts.md`:

```md
## Canonical Documentation Write Policy
- Do not modify canonical documentation unless the user explicitly asks to record, update, reconcile, supersede, or remove durable project knowledge.
- Before modifying canonical documentation, search related decision records, architecture docs, module contracts, and agent working memory.
- Prefer updating an existing canonical document over creating a duplicate.
- If new knowledge contradicts existing canonical documentation, do not silently resolve the conflict unless the user has already made the decision in the current task.
- When a decision supersedes an older one, preserve the old document as historical context and add a clear supersession link.
```

### 4. Обновить session hygiene в пользу project artifacts и working memory

Текущая language в `session-hygiene` всё ещё называет ConPort одним из default durable-memory destinations.

Требуемое изменение:

- Перенести предпочтение с `ConPort or another durable memory mechanism` на `project artifacts, agent working memory, or another durable memory mechanism`.
- Сохранить ConPort как optional handoff mechanism, а не основной durable-memory target.

Предлагаемые изменения для `fragments/process/session-hygiene.md`:

- Заменить:
  `Do not rely on transient chat memory for critical constraints; move them into project artifacts, ConPort, or another durable memory mechanism.`
- На:
  `Do not rely on transient chat memory for critical constraints; move them into project artifacts, agent working memory, ConPort handoff notes, or another durable memory mechanism.`

- Заменить:
  `Update durable memory only for decisions, progress, or lessons that should survive the session.`
- На:
  `Update durable memory only for decisions, progress, lessons, or working-memory notes that should survive the session, and keep canonical versus non-canonical status explicit.`

### 5. Обновить usage guides под новый memory stack

Текущие usage guides описывают ConPort и structured artifacts так, что ConPort всё ещё остаётся центральной reusable durable-memory feature.

Требуемое изменение:

- В guide для `session-hygiene` указать, что агент перечитывает релевантные project artifacts, module contracts, decision records и ConPort handoff только по необходимости.
- В guide для `structured-artifacts` определить, когда знание должно жить в decision record, module contract или `docs/ai-memory/**`.
- Добавить примеры, различающие:
  - promotion canonical decision по явному запросу
  - обычные autonomous updates в `docs/ai-memory/**`
  - optional ConPort handoff synchronization

### 6. Упомянуть Basic Memory как preferred retrieval layer

Сейчас в `ai-standards` нет shared wording для `Basic Memory`.

Требуемое изменение:

- Упомянуть `Basic Memory` в `README.md` и `README.ru.md` как пример Git-friendly retrieval layer для Markdown knowledge.
- Сохранить формулировку достаточно tool-agnostic, чтобы downstream projects могли использовать и другой Markdown indexing layer.
- Не делать `Basic Memory` обязательным в core fragments.

Предлагаемая README wording:

```md
- Prefer Git-tracked Markdown as the source of durable project knowledge.
- A Markdown indexing and retrieval layer such as Basic Memory may be used to search and reuse that knowledge efficiently across sessions.
- Keep canonical documentation and agent-managed working memory distinct even when the same retrieval layer indexes both.
```

## Не-цели

- Не добавлять автоматически `Basic Memory` setup instructions, CLI commands или MCP-specific operational steps в core fragments.
- Не удалять поддержку ConPort из `ai-standards`; сохранить её как optional transient-memory feature.
- Не заставлять каждый проект принимать именно `docs/ai-memory/**`; допускать эквивалентные local paths через project-specific rules.

## Порядок внедрения

1. Обновить `fragments/tools/conport.md`.
2. Обновить `fragments/process/structured-artifacts.md`.
3. Обновить `fragments/process/session-hygiene.md`.
4. Освежить English и Russian usage guides.
5. Освежить `README.md` и `README.ru.md`.
6. Перегенерировать репозиторный `AGENTS.md` и прогнать renderer и test checks.

## Проверка

При внедрении проверить:

- `uv run python scripts/ai_sync.py render --project-root .`
- `uv run python scripts/ai_sync.py check --project-root .`
- `uv run ruff check`
- `uv run mypy`
- `uv run python -m pytest`

## Ожидаемый результат

После внедрения `ai-standards` официально поддержит модель памяти, в которой:

- Git-tracked Markdown является durable project knowledge source of truth;
- canonical documentation защищена от autonomous edits;
- agent working memory остаётся записываемой без лишнего трения;
- `Basic Memory` естественно встраивается как retrieval layer;
- `ConPort` остаётся полезным, но больше не конкурирует с canonical project knowledge.