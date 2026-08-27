---
title: 'DECISION: basic-memory-knowledge-tree-boundary'
permalink: ai-standards/decisions/2026-08-20-basic-memory-knowledge-tree-boundary.ru
---

# DECISION: basic-memory-knowledge-tree-boundary

English version: [2026-08-20-basic-memory-knowledge-tree-boundary.md](2026-08-20-basic-memory-knowledge-tree-boundary.md)

## Status

Accepted

Это решение заменяет рекомендацию про frontmatter из [2026-05-19-add-basic-memory-feature.ru.md](2026-05-19-add-basic-memory-feature.ru.md). Остальная часть того решения остаётся в силе.

## Date

2026-08-20

## Context

Feature `basic-memory` вышел с защитной рекомендацией: предпочитать `ensure_frontmatter_on_sync=false` при индексации существующего Git-tracked Markdown. Рекомендация исходила из того, что Basic Memory натравливают на репозиторий, где уже лежит смешанный Markdown, и защищалась от последствий флагом.

Практика этой посылки дала четыре отказа в одном workspace:

- Проекты, зарегистрированные на корнях репозиториев, индексировали вендорные зависимости, metadata сборки и офисные документы так, будто это заметки. В одном проекте оказалось 143 не-Markdown записи из 216.
- Одного `ensure_frontmatter_on_sync=false` не хватило. Файлы, у которых frontmatter уже был, всё равно переписывались во время sync — из-за этого пришлось добавить второй флаг, `disable_permalinks=true`.
- С отключёнными permalinks любой URL `memory://` разрешался против пустой колонки permalink и не возвращал ничего. Обход графа молча деградировал до нечёткого поиска по заголовку, что воспринимается как «инструмент — просто поисковая строка».
- `ai-sync init-project` раскладывал файл из `local_overrides` в `docs/ai/project-rules.md` — внутрь дерева, которое проект естественно отдаёт Basic Memory. Индексатор проставил в этот файл frontmatter. Поскольку `_read_override` конкатенирует файл дословно, следующий render выдал бы YAML-блок посреди сгенерированного `AGENTS.md`.

Последний отказ решающий: собственный scaffolding стандарта помещал rendering input внутрь дерева знаний, поэтому ловушку наследовал каждый downstream-проект.

## Decision

Проект Basic Memory указывает на выделенное дерево знаний, а не на корень репозитория.

Любой файл внутри этого дерева — заметка. Rendering inputs, сгенерированный вывод, templates и machine-owned Markdown живут вне дерева. `ai-sync init-project` раскладывает `local_overrides` в `ai/project-rules.md` вместо `docs/ai/project-rules.md`.

На дереве, где остались только заметки, генерация permalinks остаётся включённой, потому что через permalinks разрешаются адресация `memory://` и обход графа. Пара `ensure_frontmatter_on_sync=false` плюс `disable_permalinks=true` понижается до fallback для legacy-дерева, которое пока нельзя сузить, а потеря `memory://` фиксируется как её цена.

`_read_fragment`, `_read_override` и `_read_optional_override` срезают ведущий блок frontmatter, поэтому нарушение правила размещения не может дойти до сгенерированного вывода.

`ai-sync doctor` проверяет проект на соответствие этим правилам: размещение оверрайдов, согласованность frontmatter и заголовка заметки, наличие observations и relations, а при включённой feature `basic-memory` — конфигурацию самого индексатора. Он выдаёт механические находки и ненулевой exit code при ошибках, поэтому детерминированная половина аудита принадлежит коду и может работать в CI.

`ai-sync doctor --fix` применяет починки, вытекающие из правила, а не из решения: переносит rendering inputs из дерева и перенаправляет манифест, восстанавливает отсутствующие frontmatter title и заголовки, удаляет опустевшие каталоги. Сходится за один проход и предупреждает, когда откатить его нечем. Переименование исключено намеренно: конвенция требует осмысленного слага, а транслитерация заголовка даёт ровно то нечитаемое имя, ради ухода от которого конвенция и заведена.

Починка, требующая суждения, принадлежит скиллу, а не рендеру. Шаблон `audit-knowledge-tree` поставляется для всех четырёх agent adapters и гейтится feature `basic-memory`. Он берёт отчёт `doctor`, классифицирует каждый файл и чинит по одному файлу с подтверждением. Ему запрещено синтезировать observations, переписывать verbatim-источники и удалять заметки.

Читатель манифеста не менялся: `local_overrides` остаётся свободным списком путей, объявляемым в каждом проекте, поэтому существующие проекты продолжают рендериться из своих текущих расположений.

## Why

- флаг защищал от симптома, тогда как корневой причиной был индексируемый корень
- выделенное дерево убирает вендорные и сгенерированные файлы из retrieval вместо того, чтобы их терпеть
- сохранение permalinks возвращает `memory://` и обход графа, которые защитный default молча отключал
- размещение rendering inputs вне дерева делает утечку в `AGENTS.md` структурно невозможной, а не просто маловероятной
- срезание frontmatter на рендере сохраняет гарантию, даже если проект всё равно нарушит правило размещения

## Alternatives Considered

### Оставить рекомендацию про флаг и только срезать frontmatter на рендере

Отклонено. Срезание защищает сгенерированный файл, но исходные файлы всё равно мутируют на диске и попадают в commit. В этом репозитории это означало бы frontmatter в `fragments/**` и `templates/**`, которые копируются в downstream-проекты.

### Перенести только правило размещения, без срезания на рендере

Отклонено. Правило размещения носит рекомендательный характер, его ничто не проверяет. Этот репозиторий доказал, что правило нарушается его же собственным инструментом, поэтому рендеру нужна гарантия, не зависящая от соблюдения.

### Сломать контракт манифеста, захардкодив новый путь оверрайда

Отклонено. `local_overrides` объявляется в каждом проекте и читается дословно, поэтому смена места scaffolding существующие проекты не затрагивает. Хардкод создал бы breaking change без всякой выгоды.

## Consequences

### Benefits

- качество retrieval растёт, потому что в графе лежат заметки, а не содержимое репозитория
- адресация `memory://` и `build_context` работают по умолчанию, а не отказывают молча
- сгенерированный `AGENTS.md` не может получить frontmatter из индексируемого оверрайда
- новые проекты раскладываются в правильную форму без миграции

### Costs Or Tradeoffs

- существующие проекты должны сузить корень Basic Memory и вынести `local_overrides` из дерева знаний; ни то, ни другое этим изменением не автоматизировано
- включение permalinks на существующем дереве даёт разовый миграционный commit, добавляющий `permalink:` в каждую заметку
- проекты, сознательно индексирующие корень репозитория, сохраняют fallback-флаги и теряют `memory://`

## Affected Modules

- `fragments/tools/basic-memory.md`
- `scripts/ai_sync.py`
- `templates/project_manifest.toml`
- `templates/knowledge-tree/audit-knowledge-tree.SKILL.md`
- `templates/knowledge-tree/audit-knowledge-tree.claude.md`
- `templates/knowledge-tree/audit-knowledge-tree.cursor.mdc`
- `templates/ai-infrastructure/deploy-ai-knowledge-stack.SKILL.md`
- `templates/ai-infrastructure/deploy-ai-knowledge-stack.claude.md`
- `templates/ai-infrastructure/deploy-ai-knowledge-stack.cursor.mdc`
- `docs/basic-memory-usage.md`
- `docs/basic-memory-usage.ru.md`
- `README.md`
- `README.ru.md`
- `ai.project.toml`
- `ai/project-rules.md`
- `ai/project-rules.ru.md`
- `AGENTS.md`
- `tests/test_ai_sync.py`

## Invariants And Constraints

- корень проекта Basic Memory содержит заметки и ничего кроме них
- rendering inputs никогда не размещаются внутри индексируемого дерева знаний
- сгенерированный вывод никогда не несёт frontmatter, унаследованный от rendering input
- `local_overrides` остаётся списком путей, объявляемым в проекте, поэтому место scaffolding — это default, а не контракт
- отключение permalinks — зафиксированный компромисс, а не молчаливый default

## Verification

- `pytest tests/` проходит, включая тест, который рендерит проштампованный оверрайд и проверяет, что frontmatter не попал в вывод
- `_strip_frontmatter` оставляет содержимое нетронутым, когда ведущий `---` не закрыт
- `init-project` раскладывает `ai/project-rules.md`, а не `docs/ai/project-rules.md`
- простановка frontmatter в собственный `ai/project-rules.md` этого репозитория и повторный render оставляют `AGENTS.md` побайтово идентичным
- self-hosted `AGENTS.md` рендерится с переписанным фрагментом
- `ai-sync doctor`, запущенный на этом репозитории, сообщает об ошибке из-за его собственного индексируемого корня
- проверка имени файла судит только каталоги, на которые претендует конвенция, и допускает локализованные пары вида `<name>.ru.md`
- `--fix` выравнивает заголовок первого уровня, не трогая более глубокий с тем же текстом
- отклонённое перенаправление манифеста ничего не перемещает, поэтому проект продолжает рендериться
- `sync-templates` раскладывает `audit-knowledge-tree` только при включённой `basic-memory`

## Related Artifacts

- [../basic-memory-usage.ru.md](../basic-memory-usage.ru.md)
- [../basic-memory-usage.md](../basic-memory-usage.md)
- [../../fragments/tools/basic-memory.md](../../fragments/tools/basic-memory.md)
- [../../scripts/ai_sync.py](../../scripts/ai_sync.py)
- [2026-05-19-add-basic-memory-feature.ru.md](2026-05-19-add-basic-memory-feature.ru.md)