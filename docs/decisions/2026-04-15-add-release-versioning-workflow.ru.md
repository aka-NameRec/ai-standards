# DECISION: add-release-versioning-workflow

Англоязычный оригинал: [2026-04-15-add-release-versioning-workflow.md](2026-04-15-add-release-versioning-workflow.md)

## Статус

Accepted

Частично superseded 2026-04-18 документом [2026-04-18-separate-release-version-from-python-package-version.ru.md](2026-04-18-separate-release-version-from-python-package-version.ru.md) в части расположения canonical repository release version.

## Дата

2026-04-15

## Контекст

У `ai-standards` уже была версия пакета в `pyproject.toml`, но не было стандартизованного для репозитория способа хранить дату релиза, project-local метаданные self-hosted версии и безопасно создавать релизные теги.

Репозиторию также был нужен повторяемый release workflow, который удерживает package metadata, self-hosted manifest metadata и заголовки сгенерированных `AGENTS.md` в согласованном состоянии, не связывая commit и tag в один автоматический шаг.

## Решение

`ai-standards` стандартизует локальный для репозитория release workflow, построенный вокруг:

- `pyproject.toml` как source of truth для `project.version`
- `tool.ai-standards.release_date` в `pyproject.toml`
- self-hosted manifest metadata в `ai.project.toml`
- `scripts/bump_version.py` для операций preview, save и tag

Workflow оставляет сохранение версии, git commit и создание релизного тега отдельными шагами.

## Почему

- сохраняет packaging metadata совместимыми с соглашениями `pyproject.toml`
- делает self-hosted version metadata явными вместо перегрузки полей манифеста
- позволяет заголовкам сгенерированных `AGENTS.md` последовательно отражать и release metadata репозитория, и project-local version metadata
- делает release tagging безопаснее за счёт требования чистого worktree и ветки `main`

## Рассмотренные альтернативы

### Хранить `release_date` прямо в `[project]`

Отклонено, потому что custom release metadata должны жить в tool-specific section, а не в стандартизованных package metadata.

### Переиспользовать `ai.project.toml.version` для локальной версии проекта

Отклонено, потому что репозиторий уже использовал `version` как marker зависимости на стандарты. Явные поля понятнее и безопаснее.

### Создавать тег как часть команды сохранения версии

Отклонено, потому что tagging до review-подтверждённого commit создаёт лишний release-risk и слишком жёстко связывает разные шаги workflow.

## Последствия

### Плюсы

- release metadata теперь имеют явные и проверяемые sources of truth
- у репозитория появляется повторяемый безопасный workflow подготовки релиза
- заголовки `AGENTS.md` могут последовательно показывать release state

### Минусы или цена

- схема манифеста становится немного более явной и немного более многословной
- подготовка релиза теперь затрагивает несколько согласованных файлов, а не только `pyproject.toml`

## Затронутые модули

- `pyproject.toml`
- `ai.project.toml`
- `templates/project_manifest.toml`
- `scripts/ai_sync.py`
- `scripts/bump_version.py`
- `README.md`
- `README.ru.md`
- `docs/ai/project-rules.md`
- `docs/ai/project-rules.ru.md`

## Инварианты и ограничения

- `scripts/bump_version.py save` требует чистого git worktree
- `scripts/bump_version.py tag` требует чистого git worktree и ветки `main`
- release tagging остаётся отдельным шагом по отношению к сохранению версии и git commit
- project-specific release rules остаются локальными для `ai-standards` и не выносятся в shared fragments

## Проверка

- renderer tests покрывают новые поля метаданных манифеста
- release workflow tests покрывают поведение preview/save/tag
- проверки репозитория остаются зелёными

## Связанные артефакты

- [../../scripts/bump_version.py](../../scripts/bump_version.py)
- [../../scripts/ai_sync.py](../../scripts/ai_sync.py)
- [../ai/project-rules.md](../../ai/project-rules.md)
- [../../pyproject.toml](../../pyproject.toml)
- [../../ai.project.toml](../../ai.project.toml)
