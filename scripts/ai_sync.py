from __future__ import annotations

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, cast

import typer

MANIFEST_FILE_NAME = "ai.project.toml"
GENERATED_MARKER = "Generated from ai-standards"
DEFAULT_OUTPUT_NAME = "AGENTS.md"
PROJECT_ROOT_OPTION = typer.Option(..., exists=True, file_okay=False, resolve_path=True)
OUTPUT_NAME_OPTION: object = typer.Option(...)

app = typer.Typer(add_completion=False, no_args_is_help=True)


class SyncError(RuntimeError):
    """Raised when AI standards rendering cannot continue safely."""


@dataclass(frozen=True)
class Registry:
    features: dict[str, list[str]]
    stacks: dict[str, list[str]]


@dataclass(frozen=True)
class Manifest:
    version: str
    fragments: list[str]
    features: list[str]
    stacks: list[str]
    local_overrides: list[str]
    optional_local_overrides: list[str]
    metadata: dict[str, str]


@dataclass(frozen=True)
class RenderResult:
    project_root: Path
    output_path: Path
    content: str
    fragment_ids: list[str]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_toml(path: Path) -> dict[str, object]:
    if not path.exists():
        raise SyncError(f"Required file does not exist: {path}")
    try:
        loaded = cast(dict[str, object], tomllib.loads(path.read_text(encoding="utf-8")))
    except tomllib.TOMLDecodeError as error:
        raise SyncError(f"Invalid TOML in {path}: {error}") from error
    return loaded


def _load_registry(repo_root: Path) -> Registry:
    data = _load_toml(repo_root / "registry.toml")
    features = _expect_mapping_of_string_lists(data, "features", "registry")
    stacks = _expect_mapping_of_string_lists(data, "stacks", "registry")
    return Registry(features=features, stacks=stacks)


def _load_manifest(project_root: Path) -> Manifest:
    data = _load_toml(project_root / MANIFEST_FILE_NAME)
    metadata_raw = _expect_optional_table(data, "metadata", "manifest")
    metadata: dict[str, str] = {}
    for key, value in metadata_raw.items():
        if not isinstance(value, str):
            raise SyncError("All metadata values must be strings")
        metadata[key] = value

    return Manifest(
        version=_expect_string(data, "version", "manifest"),
        fragments=_expect_string_list(data, "fragments", "manifest"),
        features=_expect_string_list(data, "features", "manifest"),
        stacks=_expect_string_list(data, "stacks", "manifest"),
        local_overrides=_expect_string_list(data, "local_overrides", "manifest"),
        optional_local_overrides=_expect_optional_string_list(
            data,
            "optional_local_overrides",
            "manifest",
        ),
        metadata=metadata,
    )


def _expect_string(data: dict[str, object], key: str, context: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise SyncError(f"Expected non-empty string '{key}' in {context}")
    return value


def _expect_string_list(data: dict[str, object], key: str, context: str) -> list[str]:
    value = data.get(key)
    if not isinstance(value, list) or not value:
        raise SyncError(f"Expected non-empty list '{key}' in {context}")
    if not all(isinstance(item, str) and item for item in value):
        raise SyncError(f"Every item in '{key}' in {context} must be a non-empty string")
    return list(value)


def _expect_optional_string_list(data: dict[str, object], key: str, context: str) -> list[str]:
    value = data.get(key, [])
    if not isinstance(value, list):
        raise SyncError(f"Expected list '{key}' in {context}")
    if not all(isinstance(item, str) and item for item in value):
        raise SyncError(f"Every item in '{key}' in {context} must be a non-empty string")
    return list(value)


def _expect_optional_table(
    data: dict[str, object],
    key: str,
    context: str,
) -> dict[str, object]:
    value = data.get(key, {})
    if not isinstance(value, dict):
        raise SyncError(f"Expected table '{key}' in {context}")

    result: dict[str, object] = {}
    for mapping_key, mapping_value in value.items():
        if not isinstance(mapping_key, str):
            raise SyncError(f"Expected string key inside '{key}' in {context}")
        result[mapping_key] = mapping_value
    return result


def _expect_mapping_of_string_lists(
    data: dict[str, object],
    key: str,
    context: str,
) -> dict[str, list[str]]:
    value = _expect_optional_table(data, key, context)
    result: dict[str, list[str]] = {}
    for mapping_key, mapping_value in value.items():
        if not isinstance(mapping_value, list) or not mapping_value:
            raise SyncError(
                f"Expected non-empty list for '{mapping_key}' inside '{key}' in {context}"
            )
        if not all(isinstance(item, str) and item for item in mapping_value):
            raise SyncError(
                f"Every fragment id for '{mapping_key}' inside '{key}' in {context} "
                "must be a string"
            )
        result[mapping_key] = list(mapping_value)
    return result


def _resolve_fragment_ids(manifest: Manifest, registry: Registry) -> list[str]:
    resolved: list[str] = []
    seen: set[str] = set()

    for fragment_id in manifest.fragments:
        _append_fragment_id(resolved, seen, fragment_id)

    for feature_name in manifest.features:
        if feature_name not in registry.features:
            raise SyncError(f"Unknown feature '{feature_name}' in {MANIFEST_FILE_NAME}")
        for fragment_id in registry.features[feature_name]:
            _append_fragment_id(resolved, seen, fragment_id)

    for stack_name in manifest.stacks:
        if stack_name not in registry.stacks:
            raise SyncError(f"Unknown stack '{stack_name}' in {MANIFEST_FILE_NAME}")
        for fragment_id in registry.stacks[stack_name]:
            _append_fragment_id(resolved, seen, fragment_id)

    return resolved


def _append_fragment_id(resolved: list[str], seen: set[str], fragment_id: str) -> None:
    if fragment_id not in seen:
        resolved.append(fragment_id)
        seen.add(fragment_id)


def _read_fragment(repo_root: Path, fragment_id: str) -> str:
    fragment_path = repo_root / "fragments" / f"{fragment_id}.md"
    if not fragment_path.exists():
        raise SyncError(f"Fragment does not exist: {fragment_path}")
    return fragment_path.read_text(encoding="utf-8").strip()


def _read_override(project_root: Path, relative_path: str) -> str:
    override_path = project_root / relative_path
    if not override_path.exists():
        raise SyncError(f"Local override does not exist: {override_path}")
    return override_path.read_text(encoding="utf-8").strip()


def _read_optional_override(project_root: Path, relative_path: str) -> str | None:
    override_path = project_root / relative_path
    if not override_path.exists():
        return None
    return override_path.read_text(encoding="utf-8").strip()


def build_rendered_content(
    project_root: Path,
    output_name: str = DEFAULT_OUTPUT_NAME,
) -> RenderResult:
    repo_root = _repo_root()
    registry = _load_registry(repo_root)
    manifest = _load_manifest(project_root)
    fragment_ids = _resolve_fragment_ids(manifest, registry)

    sections: list[str] = []
    for fragment_id in fragment_ids:
        sections.append(_read_fragment(repo_root, fragment_id))

    for relative_path in manifest.local_overrides:
        sections.append(_read_override(project_root, relative_path))

    for relative_path in manifest.optional_local_overrides:
        optional_content = _read_optional_override(project_root, relative_path)
        if optional_content is not None:
            sections.append(optional_content)

    metadata_lines = [
        f"<!-- {GENERATED_MARKER}@{manifest.version}. Do not edit manually. -->",
        f"<!-- Source: {repo_root} -->",
        f"<!-- Project: {project_root} -->",
        f"<!-- Fragments: {', '.join(fragment_ids)} -->",
    ]
    if manifest.metadata:
        for key in sorted(manifest.metadata):
            metadata_lines.append(f"<!-- Metadata {key}: {manifest.metadata[key]} -->")

    content = "\n\n".join(metadata_lines + ["\n".join(sections)]).strip() + "\n"
    return RenderResult(
        project_root=project_root,
        output_path=project_root / output_name,
        content=content,
        fragment_ids=fragment_ids,
    )


def write_rendered_content(result: RenderResult) -> None:
    result.output_path.write_text(result.content, encoding="utf-8")


def ensure_generated_file(result: RenderResult) -> None:
    if not result.output_path.exists():
        raise SyncError(f"Generated file does not exist: {result.output_path}")

    existing = result.output_path.read_text(encoding="utf-8")
    if GENERATED_MARKER not in existing:
        raise SyncError(
            f"{result.output_path} exists but is not marked as generated by ai-standards"
        )


def _copy_template_if_missing(source_path: Path, destination_path: Path) -> bool:
    if destination_path.exists():
        return False
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    destination_path.write_text(source_path.read_text(encoding="utf-8"), encoding="utf-8")
    return True


@app.command()
def render(
    project_root: Annotated[Path, PROJECT_ROOT_OPTION],
    output_name: Annotated[str, OUTPUT_NAME_OPTION] = DEFAULT_OUTPUT_NAME,
) -> None:
    """Render AGENTS.md for a downstream project."""

    result = build_rendered_content(project_root=project_root, output_name=output_name)
    write_rendered_content(result)
    typer.echo(f"Rendered {result.output_path}")


@app.command()
def update(
    project_root: Annotated[Path, PROJECT_ROOT_OPTION],
    output_name: Annotated[str, OUTPUT_NAME_OPTION] = DEFAULT_OUTPUT_NAME,
) -> None:
    """Alias for render, intended for explicit standards updates."""

    result = build_rendered_content(project_root=project_root, output_name=output_name)
    write_rendered_content(result)
    typer.echo(f"Updated {result.output_path}")


@app.command()
def check(
    project_root: Annotated[Path, PROJECT_ROOT_OPTION],
    output_name: Annotated[str, OUTPUT_NAME_OPTION] = DEFAULT_OUTPUT_NAME,
) -> None:
    """Check that the generated file matches the current manifest and standards."""

    result = build_rendered_content(project_root=project_root, output_name=output_name)
    ensure_generated_file(result)
    existing = result.output_path.read_text(encoding="utf-8")
    if existing != result.content:
        raise SyncError(
            f"{result.output_path} is out of date. Run the render or update command."
        )
    typer.echo(f"{result.output_path} is up to date")


@app.command("init-project")
def init_project(
    project_root: Annotated[Path, PROJECT_ROOT_OPTION],
) -> None:
    """Create starter manifest and project-local override templates."""

    repo_root = _repo_root()
    created_paths: list[Path] = []
    manifest_created = _copy_template_if_missing(
        repo_root / "templates" / "project_manifest.toml",
        project_root / MANIFEST_FILE_NAME,
    )
    if manifest_created:
        created_paths.append(project_root / MANIFEST_FILE_NAME)

    project_rules_created = _copy_template_if_missing(
        repo_root / "templates" / "project_rules.md",
        project_root / "docs" / "ai" / "project-rules.md",
    )
    if project_rules_created:
        created_paths.append(project_root / "docs" / "ai" / "project-rules.md")

    grace_map_created = _copy_template_if_missing(
        repo_root / "templates" / "grace_map.md",
        project_root / "docs" / "ai" / "grace-map.md",
    )
    if grace_map_created:
        created_paths.append(project_root / "docs" / "ai" / "grace-map.md")

    if not created_paths:
        typer.echo("No files created. Project is already initialized.")
        return

    for path in created_paths:
        typer.echo(f"Created {path}")


def main() -> None:
    try:
        app()
    except SyncError as error:
        typer.echo(f"Error: {error}", err=True)
        raise typer.Exit(code=1) from error


if __name__ == "__main__":
    main()
