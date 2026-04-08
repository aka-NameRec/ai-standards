# AGENTS.md instructions

## Documentation Language Policy

- Keep English files as the source of truth for maintained project documentation.
- Maintain a Russian localized equivalent for `README.md` and every maintained file under `docs/`.
- Use the `.ru.md` suffix for Russian localized equivalents.
- Update the English original and its Russian localized equivalent in the same change set whenever either document changes.
- If a new maintained documentation file is added under `docs/`, add its Russian localized equivalent in the same task unless the user explicitly approves an exception.
- Preserve links between English originals and Russian localized equivalents where practical.
- Do not create Russian or English equivalents for files under `docs/` whose names contain `-log-`.
- Treat `docs/*-log-*.md` files as chat exports that must remain in their original language and original form.

## Documentation Scope

- This synchronization rule applies to `README.md` and maintained documentation in `docs/`.
- Files under `docs/` with `-log-` in the name are excluded from the bilingual synchronization rule.
- Templates, generated files, and historical artifacts outside `docs/` are not automatically in scope unless the user asks for localization.

## Workflow

- Before editing documentation, check whether the paired English or Russian file also requires an update.
- When creating a new documentation pair, prefer `name.md` for English and `name.ru.md` for Russian.
- Do not rewrite, translate, or pair chat export files whose names contain `-log-`.
