# SQLAlchemy Stack — обоснование и покрытие

**Дата:** 2026-04-10

## Зачем нужен отдельный фрагмент для SQLAlchemy

SQLAlchemy — основной ORM для Python-проектов за пределами Django (FastAPI, Flask, Starlette, чистые сервисы). В отличие от Django ORM, SQLAlchemy требует **явного управления** на нескольких уровнях, которые Django скрывает за своими абстракциями:

| Аспект | Django ORM | SQLAlchemy |
|---|---|---|
| Сессии | Автоматические (request middleware) | Ручные — нужно создавать, закрывать, commit/rollback |
| Транзакции | Неявные (ATOMIC_REQUESTS) | Явные — нужно определять границы |
| Загрузка связей | Lazy по умолчанию, достаточно безопасно | Lazy по умолчанию, но опасно в async и API-контексте |
| Миграции | Встроенные (`makemigrations`) | Отдельный инструмент (Alembic) |
| Пул соединений | Управляется Django | Нужна явная конфигурация |

Без формализованных правил агент может:
- Оставлять незакрытые сессии (утечки соединений)
- Полагаться на lazy loading и получать N+1 или `DetachedInstanceError`
- Вызывать `session.query()` напрямую из сервисов, нарушая разделение слоёв
- Не указывать стратегии загрузки, что приводит к непредсказуемой производительности
- Генерировать миграции без ревью

## Связь с core/architecture.md

Правила `core/architecture.md` **идеально ложатся на SQLAlchemy** без адаптации (в отличие от Django, где потребовалось стек-специфичное уточнение):

```
- Service layers must not use ORM directly.
- Database access must stay behind repository-style abstractions.
```

В SQLAlchemy-проектах repository-паттерн — это стандартная практика:
- Репозиторий получает сессию через DI
- Репозиторий выполняет запросы и возвращает доменные объекты
- Сервис не знает о `session`, `select()`, `query()`

Это делает `sqlalchemy` стек полностью совместимым с core-правилами без конфликтов.

## Что покрывают правила

### 1. Управление сессиями
Главный источник багов в SQLAlchemy-проектах. Правила требуют:
- Context managers или DI для управления жизненным циклом сессии
- Явный commit/rollback (не autocommit)
- Одна сессия на единицу работы, без sharing между потоками
- Детерминистическое закрытие сессий

### 2. Модели
- Declarative mapping как стандарт
- Модели = схема + связи, не бизнес-логика
- Явные `back_populates` вместо `backref`
- Составные constraints через `__table_args__`

### 3. Repository pattern
- Все запросы к БД — через репозитории
- Сервисы не вызывают `session.query()` / `session.execute()` / `select()` напрямую
- Репозитории возвращают доменные объекты, не сырые `Row`

### 4. Стратегии загрузки
Одна из самых частых ошибок — полагаться на lazy loading:
- В синхронном коде это вызывает N+1
- В async коде это вызывает `MissingGreenlet` / `DetachedInstanceError`
- Правила требуют явного указания `joinedload`, `selectinload`, `subqueryload`
- `raiseload('*')` в критичных путях для раннего обнаружения проблем

### 5. Транзакции
- Явные границы на уровне сервиса / use-case
- Side effects (очереди, события) — после commit, не внутри транзакции
- Savepoints — только сознательно

### 6. Миграции (Alembic)
- Все изменения схемы через Alembic
- `--autogenerate` с обязательным ревью
- Миграции в VCS, без перезаписи применённых

### 7. Пул соединений
- Явная настройка `pool_size`, `max_overflow`, `pool_recycle`
- `pool_pre_ping=True` для long-running процессов

## Типовое использование

```toml
# FastAPI + SQLAlchemy + PostgreSQL
stacks = [
  "python",
  "fastapi",
  "sqlalchemy",
  "postgres",
]
```

Фрагмент `sqlalchemy` сочетается с:
- `fastapi` — типовая связка для API-сервисов
- `postgres` — правила миграций и схемы дополняют друг друга
- `python` — базовые правила языка
- `core/architecture` — repository pattern работает без конфликтов
