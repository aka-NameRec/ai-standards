---
title: 0tkod0x — Единое версионирование релиза вокруг meta.toml
permalink: ai-standards/tasks/0tkod0x-unify-release-versioning-meta-toml-ru
---

# 0tkod0x — Единое версионирование релиза вокруг meta.toml

Англоязычный оригинал: [0tkod0x-unify-release-versioning-meta-toml.md](0tkod0x-unify-release-versioning-meta-toml.md)

Дата: 2026-09-01 · Ветка: `feature/0tkod0x-unify-release-versioning` · Пользовательская задача: [#11](https://github.com/aka-NameRec/ai-standards/issues/11)

## Повод

Пользовательская задача #11: данные о версии релиза были размазаны по трём местам — `ai.project.toml` (`ai_standards_version`, `project_version`, `project_release_date`) и `pyproject.toml` (`[project] version` для пакета тулинга, `[tool.ai-standards] version` / `release_date` для релиза стандартов). При селф-хостинге ai-standards `project_version` в собственном манифесте получала версию стандартов, а пин в манифесте называл только версию, тогда как релизные теги именуются `<version>-<date>`. Предложение верифицировано по коду до реализации; план реализации утверждён пользователем с двумя явными решениями: обнулить `[project] version` до `0.0.0` с комментарием-указателем и подтвердить формат пина `<version>-<date>`.

## Что сделано

- **`meta.toml`** (новый, корень репозитория): секция `[release]` с обязательными `version = "2.2.1"` и `date = "2026-08-30"` — единственный источник истины о релизе.
- **`pyproject.toml`**: секция `[tool.ai-standards]` удалена; `[project] version = "0.0.0"` с комментарием-указателем на `meta.toml`; `uv.lock` обновлён (ai-standards 1.3.0 → 0.0.0).
- **`scripts/ai_sync.py`**: `_load_release_metadata` читает `meta.toml [release]` (`version`, `date`, оба обязательны через `_expect_string`); новый хелпер `_release_pin()`; все четыре точки проверки дрейфа (`render`, `update`, `check`, `doctor`) сравнивают пин манифеста с полным пином; `project_version` / `project_release_date` удалены из `Manifest` и из рендера шапки; `init-project` сеет полный пин; старый fallback-ключ `version` в манифесте остаётся читаемым для старых развёртываний.
- **`scripts/bump_version.py`**: `_load_release_state` читает `meta.toml`; `_update_pyproject` заменён на `_update_meta`; `save_release` штампует полный пин `<version>-<date>` в манифесты и больше не пишет ключи `project_*`; docstring команды `tag` называет `meta.toml`.
- **Манифесты**: селф-хостед `ai.project.toml` и `templates/project_manifest.toml` несут только `ai_standards_version = "2.2.1-2026-08-30"`.
- **Шаблоны скилла `update-ai-standards`** (SKILL/claude/cursor): версия релиза читается из `meta.toml [release]`; `[feature_meta].since` сравнивается с версией из пина; шаг 7 пишет полный пин.
- **Документация**: примеры и раздел Versioning в README (en+ru) переписаны вокруг полного пина; правила Release Workflow в `ai/project-rules.md` (+ `.ru.md`) переведены на `meta.toml`; `docs/standards-update-usage.md` (+ `.ru.md`) называет формат пина; в Inputs контракта модуля ai-sync добавлен `meta.toml`; в CHANGELOG добавлена секция `Unreleased`.
- **Decision record** `docs/decisions/2026-09-01-unify-release-versioning-meta-toml.md` (+ `.ru.md`); решение о разделении версий от 2026-04-18 помечено как Superseded (en+ru).
- **Тесты**: оба набора переведены на фикстуры `meta.toml` и формат пина; тесты дрейфа проверяют полный используемый пин.

## Проверки

106 тестов прошли (`uv run pytest`); `uv run mypy scripts/` чисто; `uv run ruff check scripts tests` чисто (5 ошибок линта в `templates/ai-infrastructure/scripts/code_index.py` существовали до этого изменения — подтверждено через `git stash` — и лежат вне линт-скоупа репозитория `scripts`/`tests`); `ai-sync render` + `check` идемпотентны; `ai-sync doctor` сообщает 0 ошибок и отсутствия `standards-version-drift`.

## Намеренно не сделано

- Без поднятия версии: `meta.toml` по-прежнему несёт 2.2.1 / 2026-08-30; подготовка релиза и тегирование — отдельный шаг по релизному workflow проекта.
- Без миграции потребителей: развёртывания со старым голым форматом пина увидят штатный отчёт о дрейфе, пока не прогонится скилл `update-ai-standards` — это и есть путь обновления.
- Существующие ошибки линта в развёртываемом шаблоне `code_index.py` оставлены отдельной задаче.

## Контекст для следующей сессии

- На следующем релизе `bump-version save` поднимает `meta.toml [release]` и штампует новый полный пин в оба манифеста; пин совпадает с именем тега, который создаёт `bump-version tag`.
- `uv.lock` больше не шумит при релизах только стандартов, потому что заглушка версии пакета никогда не меняется.

## Наблюдения

- [fact] Пин манифеста `ai_standards_version` теперь равен имени релизного тега, поэтому пин развёртывания проверяется напрямую по `git tag`.
- [decision] Release metadata живут только в `meta.toml [release]`; `[project] version` в `pyproject.toml` — постоянная заглушка `0.0.0` и не является версией релиза.
- [fact] Дрейф выявляется сравнением пина манифеста с `<version>-<date>` в четырёх командах: `render`, `update`, `check` и `doctor`.
- [fact] Старые манифесты с голым ключом `version` продолжают рендериться; голые пины `ai_standards_version` сообщают дрейф с новым исходником до обновления.

## Связи

- relates_to [[РЕШЕНИЕ: unify-release-versioning-meta-toml]]
- relates_to [[Модульный контракт: scripts/ai_sync.py]]
- localized counterpart of [[0tkod0x — Unified Release Versioning Around meta.toml]]
