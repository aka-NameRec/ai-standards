---
title: 'РЕШЕНИЕ: unify-release-versioning-meta-toml'
permalink: ai-standards/decisions/2026-09-01-unify-release-versioning-meta-toml-ru
---

# РЕШЕНИЕ: unify-release-versioning-meta-toml

Англоязычный оригинал: [2026-09-01-unify-release-versioning-meta-toml.md](2026-09-01-unify-release-versioning-meta-toml.md)

## Статус

Принято

Заменяет решение [2026-04-18-separate-release-version-from-python-package-version.ru.md](2026-04-18-separate-release-version-from-python-package-version.ru.md).

## Дата

2026-09-01

## Контекст

Данные о версии релиза были размазаны по трём местам, два из которых провоцировали путаницу:

- `ai.project.toml` нёс `ai_standards_version` (голая версия), плюс `project_version` и `project_release_date`.
- `pyproject.toml` нёс `[project] version` (python-пакет тулинга) и `[tool.ai-standards] version` / `release_date` (релиз стандартов).

При селф-хостинге ai-standards `project_version` в собственном манифесте получала версию стандартов, размывая два понятия, которые решение 2026-04-18 разделило. Пин в манифесте к тому же называл только версию, тогда как релизные теги именуются `<version>-<date>` (`bump-version tag`).

## Решение

- `meta.toml` в корне репозитория — единственный источник истины о релизе: секция `[release]` с `version` и `date`, оба поля обязательны.
- Секция `[tool.ai-standards]` удалена из `pyproject.toml`; `[project] version` зафиксирован заглушкой `0.0.0` — python-пакет тулинга отдельно больше не версионируется.
- Пин в манифесте проекта-потребителя — единственный ключ `ai_standards_version` в полном формате `<version>-<date>`, совпадающем с именем релизного тега; ключи `project_version` и `project_release_date` выведены из употребления.
- Скрипты читают `[release]` из `meta.toml`; проверки дрейфа сравнивают пин манифеста с полным пином через один хелпер.

## Почему так

- один файл, один смысл: ни дублирования ключей между манифестом и `pyproject.toml`
- пин теперь равен имени тега — пин развёртывания проверяется напрямую по `git tag`
- обнуление версии пакета снимает вопрос «какая из двух версий изменилась» при релизах только стандартов и убирает шум в `uv.lock`, потому что заглушка никогда не меняется

## Рассмотренные альтернативы

### Оставить `[tool.ai-standards]` в `pyproject.toml` (решение 2026-04-18)

Отклонено: tool-специфичное пространство имён по-прежнему смешивает release metadata стандартов с метаданными python-упаковки и держит в манифестах дублирующие `project_version` / `project_release_date`.

### Голый пин версии без даты

Отклонено: пин `2.2.1` не различает повторные релизы с исправленной датой и не совпадает с именем тега.

## Последствия

### Плюсы

- release metadata в одном файле с обязательными `version` и `date`
- пин == имя тега: проверяется тривиально
- манифесты проектов-потребителей сокращаются до одного ключа версии

### Минусы и компромиссы

- развёртывания со старым голым форматом пина будут сообщать о дрейфе, пока не прогонится скилл `update-ai-standards` — штатный путь обновления
- появился новый файл верхнего уровня `meta.toml`; возражение 2026-04-18 о лишних файлах перевешивается удалением `[tool.ai-standards]` и дублей в манифестах

## Затронутые модули

- `meta.toml` (новый)
- `pyproject.toml`
- `ai.project.toml`
- `templates/project_manifest.toml`
- `scripts/ai_sync.py`
- `scripts/bump_version.py`
- `tests/test_ai_sync.py`
- `tests/test_bump_version.py`
- `templates/standards-update/*`
- `docs/architecture/2026-09-01-module-contract-ai-sync.ru.md`

## Инварианты и ограничения

- `meta.toml [release]` (`version`, `date`) — каноничные release metadata; оба поля обязательны.
- `ai_standards_version` в манифестах — `<version>-<date>`; старый голый ключ `version` в манифесте остаётся читаемым для старых развёртываний.
- Создание релизного тега остаётся отдельным шагом по отношению к сохранению версии и git commit.
- Значения `[feature_meta].since` остаются голыми версиями; при сравнении с развёртыванием используется часть пина до даты.

## Проверки

- `uv run pytest`, `uv run mypy scripts/`
- `uv run ai-sync check --project-root .` проходит с полным пином в селф-хостед манифесте
- `uv run bump-version save` обновляет `meta.toml` и штампует полные пины в манифесты

## Связанные артефакты

- [../../meta.toml](../../meta.toml)
- [../../scripts/ai_sync.py](../../scripts/ai_sync.py)
- [../../scripts/bump_version.py](../../scripts/bump_version.py)
- [2026-04-18-separate-release-version-from-python-package-version.ru.md](2026-04-18-separate-release-version-from-python-package-version.ru.md)
