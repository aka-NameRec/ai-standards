# Project-Specific AI Rules

Russian localized version: [project-rules.ru.md](project-rules.ru.md)

## Documentation Language Policy

- Keep English files as the source of truth for maintained project documentation.
- Maintain a Russian localized equivalent for `README.md` and every maintained file under `docs/`.
- Use the `.ru.md` suffix for Russian localized equivalents.
- Update the English original and its Russian localized equivalent in the same change set whenever either document changes.
- If a new maintained documentation file is added under `docs/`, add its Russian localized equivalent in the same task unless the user explicitly approves an exception.
- Preserve links between English originals and Russian localized equivalents where practical.
- Use only repository-relative paths in links to repository files inside maintained documentation.
- Do not use absolute local filesystem paths such as `/home/...` in repository documentation links.
- Do not create Russian or English equivalents for chat exports anywhere under `docs/`; historical exports live in `docs/archive/**`.
- Treat chat exports — files whose names contain `-log-`, kept in `docs/archive/**` — as verbatim sources that must remain in their original language and original form.

## Documentation Scope

- This synchronization rule applies to `README.md` and maintained documentation in `docs/`.
- Files under `docs/` with `-log-` in the name are excluded from the bilingual synchronization rule; they live in `docs/archive/**`.
- Templates, generated files, and historical artifacts outside `docs/` are not automatically in scope unless the user asks for localization.

## Workflow

- Before editing documentation, check whether the paired English or Russian file also requires an update.
- When creating a new documentation pair, prefer `name.md` for English and `name.ru.md` for Russian.
- Do not rewrite, translate, or pair chat export files whose names contain `-log-`.

## Release Workflow

- Repository release metadata lives in `meta.toml` under `[release]` (`version` and `date`).
- `version` in `pyproject.toml` is a `0.0.0` placeholder for the Python support tooling package; the canonical release version and date live only in `meta.toml`.
- The release pin in `ai.project.toml` is `ai_standards_version` in the full `<version>-<date>` format, identical to the release tag name; `project_version` and `project_release_date` keys are retired.
- Use `bump-version` for release-version preview, save, and tag operations in this repository.
- `bump-version save` is allowed only on a clean git worktree.
- `bump-version tag` is allowed only on a clean git worktree and only from the `main` branch.
- Use `ai-sync` for rendering and validating `AGENTS.md` in this repository.
- Release tagging remains a separate step from version saving and from git commits.
- If a merged change set updates the repository release version, create and push the corresponding annotated release tag as the required follow-up step.
