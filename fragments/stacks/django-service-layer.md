<!-- Source: https://github.com/HackSoftware/Django-Styleguide -->
<!-- Imported: 2026-04-10 -->
<!-- Adaptation: normalized for UMA2, extracted service-layer architecture as a composable fragment -->

## Django Service Layer

### Architecture
- Keep views, API endpoints, and Celery tasks thin; delegate all business logic to services.
- Place write operations (create, update, delete) in service functions or classes under `<app>/services.py`.
- Place read operations and query building in selector functions under `<app>/selectors.py`.
- Do not put business logic in views, serializers, forms, model `save` methods, signals, or custom managers.
- In Django, the ORM is the persistence abstraction; services and selectors interact with models through it. Extract complex or reusable queries into selectors rather than inlining them in services.

### Service Conventions
- Use keyword-only arguments for service and selector signatures and provide type annotations.
- Call `full_clean()` on model instances before `save()` in services to trigger model-level validation.
- Move complex validation and cross-relation logic to the service layer.
- Use `django-filter` or equivalent filtering abstractions inside selectors.

### Celery & Background Tasks
- Treat Celery tasks as thin entry points: fetch data, call the appropriate service, handle retries at the task level.
- Dispatch tasks via `transaction.on_commit` to guarantee data consistency.
- Keep error handling and retry logic in the task; keep business logic in the service.

### Testing
- Organize tests by layer: `tests/services/`, `tests/selectors/`, `tests/models/`, mirroring the module structure.
- Service tests should hit the database and mock only external calls and async tasks.
