<!-- Source: https://github.com/PatrickJS/awesome-cursorrules/blob/main/rules/python-django-best-practices-cursorrules-prompt-fi/.cursorrules -->
<!-- Imported: 2026-04-10 -->
<!-- Adaptation: normalized for UMA2, reduced to durable framework-level Django guidance -->

## Django Stack

### Existing Code
- When modifying existing code, follow the architectural patterns already established in that module or app (e.g., fat models, logic in views, signal-driven flows).
- Do not introduce a new architectural pattern into a module that follows a different convention unless the user explicitly asks to refactor.
- When the codebase mixes patterns, keep new code consistent with the nearest surrounding context.

### Models
- Keep models focused on data modeling: fields, `Meta`, `clean` for simple multi-field validation, and simple derived `@property` values on non-relational fields.
- Use database constraints (`CheckConstraint`, `UniqueConstraint`) for integrity rules the database can enforce.
- Move properties that span multiple relations or risk N+1 queries out of the model.
- In Django, the ORM is the persistence abstraction; application code interacts with models through it.

### Signals
- Use signals only for cross-cutting model lifecycle events that must fire regardless of the entry point (audit logging, activity tracking).
- Do not use signals for orchestrating domain or business logic.

### Query Optimization
- Use `select_related` and `prefetch_related` deliberately for related-object fetching.
- Prefer lazy loading and address N+1-sensitive queries explicitly.

### Security & Configuration
- Apply Django security defaults (CSRF, SQL injection protection, XSS prevention) and do not weaken them without explicit justification.
- Use `django-environ` or equivalent for environment-based configuration; never commit secrets.
- Use Django's cache framework with an appropriate backend for frequently accessed data.

### Testing
- Organize tests mirroring the module structure.
- Model tests should validate `clean`, properties, and methods without hitting the database when possible.
- Use `factory_boy` or equivalent factories for test data setup.
