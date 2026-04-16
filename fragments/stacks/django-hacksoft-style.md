<!-- Source: https://github.com/HackSoftware/Django-Styleguide -->
<!-- Imported: 2026-04-16 -->
<!-- Adaptation: extracted as an explicit opt-in architectural style for Django projects that adopt the HackSoft service-and-selector approach -->

## Django HackSoft Style

### Scope
- This fragment is an opt-in architectural style, not a Django baseline.
- Use it when the project explicitly adopts a service-and-selector application layer across Django and DRF entry points.

### Architecture
- Keep views, API endpoints, admin actions, and background tasks thin; orchestration belongs to the application layer.
- Place write workflows in services and reusable read/query workflows in selectors.
- Do not put business workflows in serializers, forms, model `save()` methods, signals, or custom managers.
- Use explicit service and selector boundaries so orchestration, validation placement, and side effects remain reviewable.

### Boundaries
- Treat serializers and forms as boundary validation and mapping tools, not as the home of business rules.
- Prefer explicit orchestration over implicit signal-driven flows for project-internal behavior.
- When post-commit side effects matter, dispatch them via `transaction.on_commit`.

### Testing
- Organize tests by application layer when the project uses this style, such as `tests/services/`, `tests/selectors/`, and `tests/apis/`.
