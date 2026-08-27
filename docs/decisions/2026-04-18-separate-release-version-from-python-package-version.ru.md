---
title: 'DECISION: separate-release-version-from-python-package-version'
permalink: ai-standards/decisions/2026-04-18-separate-release-version-from-python-package-version.ru
---

# DECISION: separate-release-version-from-python-package-version

Англоязычный оригинал: [2026-04-18-separate-release-version-from-python-package-version.md](2026-04-18-separate-release-version-from-python-package-version.md)

## Статус

Accepted

## Дата

2026-04-18

## Контекст

Репозиторий использовал `project.version` из `pyproject.toml` как canonical release version `ai-standards`, одновременно используя uv для управления Python environment вспомогательных скриптов репозитория.

Это смешивало две разные сущности:

- release version репозитория стандартов `ai-standards`
- package version Python support tooling, который рендерит и проверяет эти стандарты

На практике uv записывает версию корневого пакета в `uv.lock`. Из-за этого обычные ai-standards release bumps вели к лишнему churn в lock-файле даже тогда, когда сам Python support package не менялся.

## Решение

Теперь `ai-standards` считает canonical repository release version tool-specific metadata в `pyproject.toml` в полях:

- `tool.ai-standards.version`
- `tool.ai-standards.release_date`

`project.version` остаётся версией Python support tooling package и должен меняться только тогда, когда сам этот пакет меняется существенно, например из-за обновления скриптов или зависимостей.

Self-hosted manifest по-прежнему использует:

- `ai_standards_version`
- `project_version`
- `project_release_date`

и эти значения отражают release state репозитория `ai-standards`, а не package version Python support package.

## Почему

- отделяет repository release semantics от Python package metadata
- предотвращает лишний `uv.lock` churn при обычных релизах стандартов
- хранит release metadata в tool-specific section, соответствующей их фактической области действия
- сохраняет `pyproject.toml` правильным местом для Python tooling configuration
- позволяет заголовкам сгенерированных `AGENTS.md` отражать release state репозитория, а не package internals

## Рассмотренные альтернативы

### Оставить `project.version` и всегда пересобирать `uv.lock`

Отклонено, потому что это сохраняет смысловую путаницу между release version стандартов и версией пакета, а drift lock-файла превращает в рутинную часть release preparation.

### Вынести repository release metadata в отдельный `project.toml`

Отклонено, потому что `pyproject.toml` уже даёт подходящий namespace `tool.*` для repository-local tooling metadata, а отдельный top-level metadata file добавил бы custom complexity, не помогая uv.

## Последствия

### Плюсы

- релизы стандартов могут двигаться без обязательного изменения версии Python-пакета
- `bump_version.py save` больше не обязан менять `project.version`
- release tagging снова опирается на clean repository metadata без incidental lockfile churn

### Минусы или цена

- теперь в репозитории есть две версии, которые нужно чётко различать по смыслу
- документация и тесты должны явно показывать, какую именно версию они проверяют
- старые репозитории, где есть только `project.version`, остаются compatibility case, который tooling должен продолжать читать безопасно

## Затронутые модули

- `pyproject.toml`
- `ai.project.toml`
- `templates/project_manifest.toml`
- `scripts/ai_sync.py`
- `scripts/bump_version.py`
- `tests/test_bump_version.py`
- `README.md`
- `README.ru.md`
- `docs/ai/project-rules.md`
- `docs/ai/project-rules.ru.md`

## Инварианты и ограничения

- `tool.ai-standards.version` является canonical release version этого репозитория
- `project.version` зарезервирован за Python support tooling package
- release tagging остаётся отдельным шагом по отношению к version save и git commits
- repository-local release rules остаются локальными для `ai-standards` и не выносятся в shared fragments

## Проверка

- renderer читает release version из `tool.ai-standards.version` с compatibility fallback
- `bump_version.py save` обновляет `tool.ai-standards.version` и `tool.ai-standards.release_date`, не трогая `project.version`
- tests подтверждают, что обычный release save не меняет версию Python support package

## Связанные артефакты

- [../../scripts/bump_version.py](../../scripts/bump_version.py)
- [../../scripts/ai_sync.py](../../scripts/ai_sync.py)
- [../ai/project-rules.md](../../ai/project-rules.md)
- [../../pyproject.toml](../../pyproject.toml)