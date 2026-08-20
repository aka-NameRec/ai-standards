# DECISION: bump-version-console-script

Англоязычный оригинал: [2026-04-21-bump-version-console-script.md](2026-04-21-bump-version-console-script.md)

## Статус

Accepted

## Дата

2026-04-21

## Контекст

Release workflow для `ai-standards` уже использовал `scripts/bump_version.py`, но для этого нужно было помнить вызов через `python -m`. Репозиторий управляется через `uv`, поэтому release tool лучше отдать как стандартный console script, чтобы workflow стал проще и согласованнее.

## Решение

Expose release workflow как console script `bump-version` и оставить `scripts/bump_version.py` как implementation module.

## Почему

- позволяет запускать release workflow как `uv run bump-version ...`
- сохраняет implementation в обычном Python module, но даёт ему нормальное CLI имя
- снижает friction в release workflow без изменения semantics операций version save и tag

## Рассмотренные альтернативы

### Оставить только `python -m scripts.bump_version`

Отклонено, потому что этот способ сложнее запомнить и он хуже сочетается с `uv`-first workflow репозитория.

### Переименовать сам файл скрипта в `bump-version.py`

Отклонено, потому что implementation уже удобно живёт как module, а hyphenated name лучше подходит именно для CLI entry point, а не для Python module path.

## Последствия

### Плюсы

- release-команды становятся короче и проще для передачи между людьми
- `uv run bump-version` начинает работать напрямую из workflow репозитория
- тесты могут покрывать тот же путь запуска, который используют пользователи

### Минусы или цена

- в репозитории теперь поддерживаются и module path, и console script name
- документация и project rules должны ссылаться на CLI name, а не на module path

## Затронутые модули

- `pyproject.toml`
- `scripts/bump_version.py`
- `tests/test_bump_version.py`
- `README.md`
- `README.ru.md`
- `docs/ai/project-rules.md`
- `docs/ai/project-rules.ru.md`

## Инварианты и ограничения

- release tagging по-прежнему требует чистого worktree и ветки `main`
- `bump-version save` должен по-прежнему не менять `project.version`
- CLI name должен оставаться стабильным, потому что он становится частью public repository workflow

## Проверка

- `uv run bump-version --help` резолвит console script
- `uv run bump-version save ...` обновляет repository release metadata в demo repository
- `tests/test_bump_version.py` покрывает console-script path

## Связанные артефакты

- [../../scripts/bump_version.py](../../scripts/bump_version.py)
- [../../tests/test_bump_version.py](../../tests/test_bump_version.py)
- [../2026-04-18-separate-release-version-from-python-package-version.md](2026-04-18-separate-release-version-from-python-package-version.md)
