<!-- Source: SQLAlchemy documentation, community best practices -->
<!-- Imported: 2026-04-10 -->
<!-- Adaptation: normalized for UMA2, aligned with core/architecture repository pattern -->

## SQLAlchemy Stack

### Session Management
- Manage sessions through context managers or dependency injection; never hold long-lived sessions across request boundaries.
- Commit and rollback explicitly; do not rely on autocommit.
- Close sessions deterministically; prefer `with Session() as session:` or framework-managed scoped sessions.
- Use one session per unit of work; do not share sessions across threads.

### Models
- Use declarative mapping for model definitions.
- Keep models focused on schema, columns, relationships, and constraints; do not place business logic in models.
- Define relationships with explicit `back_populates` instead of `backref` for clarity.
- Use `__table_args__` for composite constraints and indexes.

### Repository Pattern
- Place all database queries behind repository-style abstractions; services must not call `session.query()`, `session.execute()`, or `select()` directly.
- Repositories receive a session as a dependency, not as a global.
- Return domain objects or DTOs from repositories, not raw `Row` objects.

### Loading Strategies
- Specify loading strategies explicitly (`joinedload`, `selectinload`, `subqueryload`) at the query site; do not rely on lazy loading in request-handling code.
- Use `raiseload('*')` in performance-sensitive paths to surface unintended lazy loads early.
- Prefer `selectinload` for collections and `joinedload` for single-valued relationships unless query shape demands otherwise.

### Transactions
- Define transactional boundaries explicitly at the service or use-case level.
- Do not nest `session.begin()` unless using savepoints intentionally.
- Dispatch side effects (task queues, event publishing) after commit, not inside the transaction.

### Migrations
- Use Alembic for all schema changes; treat migrations as explicit design decisions.
- Generate migrations with `--autogenerate` but always review the result before applying.
- Keep migration files in version control; do not skip or rewrite applied migrations.

### Connection Pooling
- Configure pool size, max overflow, and pool recycle deliberately for the deployment environment.
- Use `pool_pre_ping=True` to handle stale connections in long-running processes.
