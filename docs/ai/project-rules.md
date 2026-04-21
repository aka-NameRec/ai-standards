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

## Release Workflow

- Repository release metadata lives in `pyproject.toml` under `tool.ai-standards.version` and `tool.ai-standards.release_date`.
- `project.version` in `pyproject.toml` describes the Python support tooling package, not the canonical release version of the `ai-standards` repository.
- Change `project.version` only when the Python support package itself changes in a way that warrants a package-version bump, such as script or dependency changes.
- Self-hosted manifest metadata lives in `ai.project.toml` under `ai_standards_version`, `project_version`, and `project_release_date`.
- Use `bump-version` for release-version preview, save, and tag operations in this repository.
- `bump-version save` is allowed only on a clean git worktree.
- `bump-version tag` is allowed only on a clean git worktree and only from the `main` branch.
- Use `ai-sync` for rendering and validating `AGENTS.md` in this repository.
- Release tagging remains a separate step from version saving and from git commits.
- If a merged change set updates the repository release version, create and push the corresponding annotated release tag as the required follow-up step.
