# Руководство по Basic Memory

Англоязычный оригинал: [basic-memory-usage.md](basic-memory-usage.md)

Этот документ объясняет, как использовать feature `basic-memory` из `ai-standards` в подключаемых проектах.

`basic-memory` стандартизует использование Basic Memory как Markdown-first retrieval layer, не позволяя ему превратиться в неконтролируемый источник архитектурной истины.

## Цели

Используйте `basic-memory`, когда хотите, чтобы агент или команда:

- держали durable project knowledge в Git-tracked Markdown
- эффективно искали эти знания между сессиями через Basic Memory
- различали canonical documentation и agent-managed working memory
- избегали accidental documentation drift из-за побочных эффектов индексации
- осознанно реиндексировали базу после событий в репозитории, которые могут сделать graph stale

Типовые результаты:

- меньше скрытого знания, застрявшего в chat history
- лучшее переиспользование существующих project notes и decisions
- меньше дублирующихся documentation files
- более ясные границы между reviewable truth и agent scratch space

## Что покрывает feature

Feature стандартизует shared policy для:

- использования Basic Memory как retrieval layer, а не как canonical source of truth
- разделения canonical documentation и working memory
- проверки на дублирование и противоречия перед обновлением canonical documentation
- защиты repository Markdown от нежелательной frontmatter injection
- определения, когда достаточно filesystem auto-sync, а когда нужна явная reindex

Feature сознательно не стандартизует:

- один обязательный folder layout для всех проектов
- один конкретный cloud или local deployment mode для Basic Memory
- одну универсальную schema для всех типов notes
- автоматический promotion working notes в canonical documentation

## Canonical Documentation и Working Memory

Считайте canonical documentation:

- `docs/decisions/**`
- `docs/architecture/**`
- `MODULE_CONTRACT.md`
- эквивалентные локальные artifacts, которые фиксируют принятые constraints, contracts или decisions

Считайте working memory:

- `docs/ai-memory/**`
- investigation notes
- handoff notes
- implementation gotchas
- временные findings, которые ещё развиваются

Canonical documentation должна меняться только по явному запросу пользователя. Working memory может обновляться автономно, когда это помогает сохранить полезный context.

## Безопасность Frontmatter

Basic Memory умеет внедрять frontmatter во время sync. Для greenfield knowledge bases это может быть полезно, но для существующей Git-tracked documentation это рискованно, потому что может массово изменить много файлов без явного documentation request.

Для репозиториев, где Markdown считается reviewable project knowledge, предпочтительно:

- `ensure_frontmatter_on_sync=false`

Разрешайте frontmatter injection только если проект явно хочет, чтобы Basic Memory управлял этим metadata lifecycle.

## Политика реиндексации

Обычные file edits внутри индексируемых директорий должны полагаться на стандартный filesystem sync Basic Memory.

Проверяйте status после:

- `git pull`
- `git merge`
- `git rebase`
- branch switch или checkout
- применения большого patch, который меняет много индексируемых Markdown files

Запускайте явный project reindex после:

- массовых file renames, moves или deletes внутри индексируемых директорий
- interrupted indexing или incomplete embeddings
- изменения indexed root path для проекта
- изменения permalink behavior или frontmatter-sync policy
- первой индексации существующего большого documentation tree

Предпочитайте такие operational patterns:

- `bm status --project <project>`
- `bm reindex --project <project>`
- `bm reindex --project <project> --embeddings`
- `bm reindex --project <project> --full`

Используйте самый узкий reindex, который решает обнаруженную проблему.

## Связь с другими features

- `structured-artifacts` определяет, какие Markdown artifacts считаются plans, decision records и module contracts.
- `session-hygiene` определяет, когда агент должен повторно загружать релевантный durable context между фазами или чатами.
- `conport` остаётся полезным для transient operational context и handoff storage.
- `design-first-collaboration` удерживает явными intent, boundaries и non-goals до реализации.

`basic-memory` дополняет эти features, делая Git-tracked Markdown проще для поиска и переиспользования. Он не заменяет reviewable documentation и явные human decisions.

## Пример manifest

```toml
features = [
  "conport",
  "basic-memory",
  "structured-artifacts",
  "session-hygiene",
]
```

## Практические prompt patterns

Хорошие prompts:

- `Сначала поищи в Basic Memory notes, прежде чем создавать новую design note.`
- `Проверь, не существует ли уже это решение в docs/decisions или ai-memory, прежде чем писать что-то новое.`
- `После этого merge проверь status Basic Memory и запускай reindex только если docs graph устарел.`
- `Зафиксируй этот implementation gotcha в working memory, а не в canonical documentation.`

Избегайте:

- `Перенеси всё из working notes в docs/decisions.`
- `Пусть Basic Memory переписывает repository docs как считает нужным.`
- `Делай полный reindex в каждой сессии независимо от необходимости.`

Предпочитайте:

- `Сначала используй Basic Memory для поиска, а затем обнови минимальный корректный Markdown artifact.`
