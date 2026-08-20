# Импорт Django Stack в ai-standards

**Дата:** 2026-04-10

## Структура источников

### Источник 1: awesome-cursorrules — `python-django-best-practices`

- **URL:** https://github.com/PatrickJS/awesome-cursorrules/blob/main/rules/python-django-best-practices-cursorrules-prompt-fi/.cursorrules
- **Описание:** Набор высокоуровневых правил для Django: CBV vs FBV, ORM, middleware, кеширование, безопасность, тестирование, query optimization. Не содержит конкретной архитектурной философии вокруг сервисного слоя.

### Источник 2: HackSoft Django Styleguide

- **URL:** https://github.com/HackSoftware/Django-Styleguide
- **Описание:** Детальный стайлгайд (6.1k stars) с чёткой архитектурой: services (write), selectors (read), тонкие views/APIs, nested serializers, Celery-паттерны, тестирование по слоям, exception handling. Основной принцип: **бизнес-логика живёт в сервисном слое, а не во views/serializers/forms/signals/managers**.

---

## Классификация правил

### Из awesome-cursorrules — принятые (KEEP / ADAPT)

| # | Правило (оригинал) | Решение | Причина |
|---|---|---|---|
| 1 | Prefer CBVs for complex views, FBVs for simpler | **adapt** | Применимо к API views, но уточняем в контексте DRF APIView |
| 2 | Leverage ORM, avoid raw SQL unless necessary | **keep** | Универсальное, не дублирует core |
| 3 | Use middleware for cross-cutting concerns | **keep** | Общая практика |
| 4 | Optimize with select_related/prefetch_related | **keep** | Конкретная и полезная рекомендация |
| 5 | Apply security best practices (CSRF, XSS, SQLi) | **keep** | Дюрабельная рекомендация |
| 6 | Use cache framework | **keep** | Общий совет |
| 7 | Async views + Celery for I/O-bound ops | **adapt** | Объединено с Celery-правилами из HackSoft |

### Из awesome-cursorrules — отклонённые (REJECT)

| # | Правило | Причина отклонения |
|---|---|---|
| A | "Follow MVT pattern strictly" | Конфликтует с сервисным слоем — мы добавляем services/selectors поверх MVT |
| B | "Keep business logic in models and forms" | **Прямой конфликт** с нашим ключевым принципом — бизнес-логика в services |
| C | "Use Django signals to decouple error handling" | Конфликтует с HackSoft guideline — signals только для decoupling несвязанных вещей |
| D | "Use Django's form and model form classes for validation" | Слишком привязан к Django forms; в API-first мире валидация через сериализаторы и service layer |
| E | "Customize error pages (404, 500)" | Проект-специфично, не дюрабельно |
| F | "Use built-in auth framework" | Проект-специфично |

### Из HackSoft Django Styleguide — принятые (KEEP)

| # | Правило | Решение |
|---|---|---|
| 1 | Business logic in services, not views/serializers/forms/signals/managers | **keep** (ключевой принцип) |
| 2 | Selectors for read operations | **keep** |
| 3 | `<entity>_<action>` naming for services/selectors | **keep** |
| 4 | `<Entity><Action>Api` naming for API views | **keep** |
| 5 | Keyword-only args + type annotations for services | **keep** |
| 6 | Call `full_clean()` before `save()` in services | **keep** |
| 7 | Use DB constraints for integrity | **keep** |
| 8 | Models: fields, Meta, clean, simple @property | **keep** |
| 9 | Complex validation → service layer | **keep** |
| 10 | Prefer `APIView` over generic views, nest Input/OutputSerializer | **keep** |
| 11 | Prefer `Serializer` over `ModelSerializer` | **keep** |
| 12 | Celery tasks как тонкие обёртки вокруг services | **keep** |
| 13 | `transaction.on_commit` для dispatch задач | **keep** |
| 14 | Tests по слоям: services/selectors/models | **keep** |
| 15 | Signals только для unrelated decoupling (cache invalidation) | **keep** |

### Из HackSoft Django Styleguide — отклонённые (REJECT)

| # | Правило | Причина |
|---|---|---|
| A | Settings folder structure (config/django/, config/settings/) | Проект-специфично, cookie-cutter territory |
| B | BaseModel с created_at/updated_at | Полезно, но слишком конкретная реализация |
| C | `inline_serializer` utility | Инструмент-специфичный хелпер, не архитектурное правило |
| D | `get_paginated_response` utility | Утилита, не архитектурное правило |
| E | HackSoft-specific exception handler implementation | Слишком конкретная реализация; оставляем архитектурный принцип |
| F | `_task` suffix convention for task imports | Слишком гранулярно для стандартов |

---

## Конфликт: `core/architecture.md` vs Django ORM в сервисах

### Суть проблемы

В `fragments/core/architecture.md` есть два правила:

```
- Service layers must not use ORM directly.
- Database access must stay behind repository-style abstractions.
```

Этот core-фрагмент подключается ко **всем** проектам через манифест (`core/architecture` в `ai.project.toml`).

### Откуда это правило

Правило продвигает классический enterprise-паттерн **Repository Pattern**: бизнес-логика (services) не знает о конкретном способе хранения данных, а обращается к абстракции (репозиторий / data access layer). Такой подход хорошо работает в Java Spring, .NET, чистой архитектуре — и в стеке `java-spring` он отражён напрямую:

```
- Keep business logic in services and keep persistence concerns behind repositories.
- Do not inject repositories directly into controllers.
```

### С чем конфликтует

В Django-мире (и конкретно в HackSoft Django Styleguide с 6.1k stars) принят **другой паттерн**. Сервисы напрямую работают с Django ORM:

```python
# Типичный Django service по HackSoft Styleguide
def user_create(*, email: str, name: str) -> User:
    user = User(email=email)      # ORM напрямую
    user.full_clean()              # ORM напрямую
    user.save()                    # ORM напрямую
    return user
```

А selectors — это фактически read-side абстракция:

```python
# Selector — "репозиторий для чтения"
def user_list(*, filters=None) -> QuerySet[User]:
    qs = User.objects.all()        # ORM напрямую
    return BaseUserFilter(filters, qs).qs
```

То есть в Django:

- **ORM сам является persistence-абстракцией** — он уже абстрагирует SQL, поддерживает разные бэкенды, имеет QuerySet API.
- Оборачивать ORM в ещё один слой Repository — это **не идиоматичный Django**, создаёт лишний boilerplate и противоречит философии фреймворка.
- Selectors де-факто выполняют роль "read repository".
- Сервисы де-факто выполняют роль "write repository" + бизнес-логика.

### Сравнение подходов

| | `core/architecture.md` | Django Styleguide |
|---|---|---|
| Может ли сервис вызывать ORM? | Нет (`must not use ORM directly`) | Да — это стандарт |
| Persistence abstraction | Отдельный слой (Repository) | ORM = abstraction, selectors = read layer |
| Где это работает хорошо | Java Spring, .NET, FastAPI с SQLAlchemy | Django |

Если применить `core/architecture.md` буквально к Django-проекту, агент будет вынужден создавать промежуточный Repository-слой между сервисами и ORM — что Django-сообщество считает антипаттерном.

### Принятое решение

В `fragments/stacks/django.md` добавлено стек-специфичное уточнение:

```
- In Django, the ORM is the persistence abstraction; services and selectors interact with models through it.
  Extract complex or reusable queries into selectors rather than inlining them in services.
```

Это работает по принципу **"стек уточняет core"** — общее правило остаётся для стеков, где Repository-паттерн уместен (Java Spring и т.д.), а Django-стек легитимно адаптирует его под свои идиомы.

### Варианты дальнейшего развития

1. **Оставить как есть** — Django stack уточняет общее правило для своего контекста (стек-специфичные правила имеют приоритет). Минимальное изменение.
2. **Смягчить формулировку в core** — например, заменить `must not use ORM directly` на `should abstract database access appropriately for the stack`.
3. **Добавить explicit override** — оговорить в `core/architecture.md`, что стеки могут переопределять persistence-паттерн.

Рекомендуется **вариант 1** — это наиболее минимальное изменение, и стек-правила по логике должны уточнять core-правила.

---

## Save Lifecycle — паттерн оркестрации CRUD через view/viewset

### Идея

View (или viewset) выступает **единой точкой оркестрации** жизненного цикла сохранения — вместо Django-сигналов. Базовый класс определяет метод `save()`, который вызывается при создании и обновлении. Конкретные view/viewset'ы переопределяют `save()`, чтобы добавить логику **до** и **после** сохранения. Бизнес-логика при этом живёт в `services/`; view только оркестрирует вызовы.

Паттерн одинаково работает в DRF (через сериализаторы) и в чистом Django (через формы). Ниже описаны оба варианта.

---

### DRF: базовый viewset

```python
from rest_framework.viewsets import ModelViewSet


class BaseModelViewSet(ModelViewSet):
    """
    Единая точка save() для pre- и post-save логики.

    Переопределяйте save() в потомке:
    1. serializer.instance — текущее состояние модели (None при создании).
    2. serializer.validated_data — данные от пользователя (dict).
    3. additional_data — доп. поля, передаваемые в serializer.save().
    """

    def save(self, serializer, additional_data: dict = None):
        serializer.save(**additional_data) if additional_data else serializer.save()

    def perform_update(self, serializer):
        self.save(serializer)

    def perform_create(self, serializer):
        self.save(serializer)
```

### Plain Django: базовый CBV

```python
from django.views.generic import CreateView, UpdateView


class BaseFormSaveView:
    """
    Миксин с единой точкой save() для pre- и post-save логики.

    Переопределяйте save() в потомке:
    1. form.instance — текущее состояние модели.
    2. form.cleaned_data — данные от пользователя (dict).
    3. additional_data — доп. поля, устанавливаемые на instance перед save().
    """

    def save(self, form, additional_data: dict = None):
        instance = form.save(commit=False)
        if additional_data:
            for key, value in additional_data.items():
                setattr(instance, key, value)
        instance.save()
        form.save_m2m()
        return instance

    def form_valid(self, form):
        self.object = self.save(form)
        return HttpResponseRedirect(self.get_success_url())


class BaseCreateView(BaseFormSaveView, CreateView):
    pass


class BaseUpdateView(BaseFormSaveView, UpdateView):
    pass
```

---

### Описание паттерна

Конкретные view/viewset'ы переопределяют `save()`, чтобы добавить логику до и после сохранения. Сам `save()` работает одинаково для create и update — различия определяются по текущему состоянию объекта (`None` при создании).

| Элемент | DRF | Plain Django |
|---|---|---|
| Текущее состояние модели | `serializer.instance` | `form.instance` |
| Данные от пользователя | `serializer.validated_data` | `form.cleaned_data` |
| Инъекция доп. полей | `serializer.save(**additional_data)` | `setattr` на `instance` перед `save()` |
| Хук создания/обновления | `perform_create` / `perform_update` | `form_valid` |
| Что переопределять | `save()` в viewset | `save()` в view |

---

### Типовые варианты использования

#### Pre-save: валидация и нормализация

**DRF:**
```python
class OrderViewSet(BaseModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def save(self, serializer):
        validate_order_totals(serializer.validated_data, serializer.instance)
        additional_data = normalize_order_status(serializer.validated_data, serializer.instance)
        super().save(serializer, additional_data=additional_data)
```

**Plain Django:**
```python
class OrderUpdateView(BaseUpdateView):
    model = Order
    form_class = OrderForm

    def save(self, form):
        validate_order_totals(form.cleaned_data, form.instance)
        additional_data = normalize_order_status(form.cleaned_data, form.instance)
        return super().save(form, additional_data=additional_data)
```

#### Post-save: побочные эффекты

**DRF:**
```python
class AssetViewSet(BaseModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer

    def save(self, serializer):
        super().save(serializer)
        recalculate_owner_totals(serializer.instance)
```

**Plain Django:**
```python
class AssetUpdateView(BaseUpdateView):
    model = Asset
    form_class = AssetForm

    def save(self, form):
        instance = super().save(form)
        recalculate_owner_totals(instance)
        return instance
```

#### Pre-save + post-save: полный жизненный цикл

**DRF:**
```python
class PaymentViewSet(BaseModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def save(self, serializer):
        init_instance = serializer.instance
        validated = serializer.validated_data

        # PRE-SAVE
        check_payment_limits(init_instance, validated)
        reset_split_amounts(init_instance, validated)

        # SAVE
        super().save(serializer)

        # POST-SAVE
        result = serializer.instance
        if not result.accepted_at:
            result.accepted_at = result.created_at
            result.save()
        sync_related_report(result)
```

**Plain Django:**
```python
class PaymentUpdateView(BaseUpdateView):
    model = Payment
    form_class = PaymentForm

    def save(self, form):
        init_instance = form.instance
        cleaned = form.cleaned_data

        # PRE-SAVE
        check_payment_limits(init_instance, cleaned)
        reset_split_amounts(init_instance, cleaned)

        # SAVE
        result = super().save(form)

        # POST-SAVE
        if not result.accepted_at:
            result.accepted_at = result.created_at
            result.save()
        sync_related_report(result)
        return result
```

#### Инъекция контекста запроса

**DRF:**
```python
class CommentViewSet(BaseModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def save(self, serializer):
        additional_data = {'updated_by': self.request.user}
        if not serializer.instance:
            additional_data['created_by'] = self.request.user
        super().save(serializer, additional_data)
```

**Plain Django:**
```python
class CommentCreateView(BaseCreateView):
    model = Comment
    form_class = CommentForm

    def save(self, form):
        return super().save(form, additional_data={
            'created_by': self.request.user,
            'updated_by': self.request.user,
        })
```

---

### Типичные категории override по фазе

| Фаза | Примеры задач |
|---|---|
| **pre-save** | Валидация бизнес-правил, нормализация данных, проверка лимитов, нормализация datetime-полей |
| **additional_data** | Инъекция `created_by`/`updated_by`, привязка к текущему пользователю |
| **post-save** | Автозаполнение derived-полей, пересчёт агрегатов, синхронизация связанных моделей |
| **pre + post** | Валидация → save → пересчёт, синхронизация, закрытие/переоткрытие записей |

### Связь с сервисным слоем

Бизнес-логика (валидаторы, калькуляторы, синхронизаторы) живёт в `services/`. View/viewset `save()` **оркестрирует** вызовы сервисных функций вокруг точки сохранения, но не содержит бизнес-логику inline.

### Роль сигналов

Сигналы **сохраняются** только для задач, которые должны срабатывать **независимо от точки входа**:
- Аудит-лог / activity stream (`pre_save`, `post_save`, `pre_delete`, `post_delete`, `m2m_changed`)
- Отслеживание автора изменений (middleware-level `pre_save`)

Доменная и бизнес-логика в сигналах **не размещается**.

---

## Изменённые файлы

| Файл | Содержание |
|---|---|
| `fragments/stacks/django.md` | Базовые правила Django: ORM, модели, constraints, security, config, кеш, query optimization, тестирование, сигналы |
| `fragments/stacks/django-service-layer.md` | Сервисный слой: services/selectors, `full_clean()`, Celery, тестирование по слоям |
| `fragments/stacks/django-naming.md` | Naming conventions: `<entity>_<action>`, `<Entity><Action>Api`, именование тестов |
| `fragments/stacks/django-drf.md` | DRF: APIView, Input/OutputSerializer, Serializer vs ModelSerializer |
| `fragments/stacks/django-save-lifecycle.md` | Save lifecycle: DRF viewset pattern + plain Django CBV pattern, роль сигналов |
| `registry.toml` | Обновлён — добавлены `django`, `django-service-layer`, `django-naming`, `django-drf`, `django-save-lifecycle` |

## Использование в downstream-проектах

Фрагменты собираются в нужной комбинации:

```toml
# Django API проект (полный стек)
stacks = [
  "python",
  "django",
  "django-service-layer",
  "django-naming",
  "django-drf",
  "django-save-lifecycle",
  "postgres",
]
```

```toml
# Django без DRF (шаблоны, формы)
stacks = [
  "python",
  "django",
  "django-service-layer",
  "django-save-lifecycle",
  "postgres",
]
```

```toml
# Django минимальный (без service layer, без lifecycle)
stacks = [
  "python",
  "django",
  "postgres",
]
```

## Проверки

Все проверки проекта пройдены:

- `uv run ruff check` — All checks passed
- `uv run mypy .` — Success: no issues found
- `uv run pytest` — 10 passed
