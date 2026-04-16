from __future__ import annotations

import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Annotated, cast

import typer

from scripts.ai_sync import build_rendered_content, write_rendered_content

VERSION_PATTERN = re.compile(r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$")
PART_VALUES: tuple[str, ...] = ("major", "minor", "patch")
app = typer.Typer(add_completion=False, no_args_is_help=False)


class VersioningError(RuntimeError):
    """Raised when release versioning cannot continue safely."""


@dataclass(frozen=True)
class ReleaseState:
    version: str
    release_date: str


@dataclass(frozen=True)
class ProposedRelease:
    current_version: str
    current_release_date: str
    next_version: str
    next_release_date: str


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _load_toml(path: Path) -> dict[str, object]:
    loaded = cast(dict[str, object], tomllib.loads(path.read_text(encoding="utf-8")))
    return loaded


def _expect_table(data: dict[str, object], key: str, context: str) -> dict[str, object]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise VersioningError(f"Expected table '{key}' in {context}")
    return cast(dict[str, object], value)


def _expect_string(data: dict[str, object], key: str, context: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise VersioningError(f"Expected non-empty string '{key}' in {context}")
    return value


def _load_release_state(repo_root: Path) -> ReleaseState:
    data = _load_toml(repo_root / "pyproject.toml")
    project = _expect_table(data, "project", "pyproject")
    tool = _expect_table(data, "tool", "pyproject")
    ai_standards = _expect_table(tool, "ai-standards", "pyproject.tool")
    return ReleaseState(
        version=_expect_string(project, "version", "pyproject.project"),
        release_date=_expect_string(
            ai_standards,
            "release_date",
            "pyproject.tool.ai-standards",
        ),
    )


def _parse_version(version: str) -> tuple[int, int, int]:
    match = VERSION_PATTERN.fullmatch(version)
    if match is None:
        raise VersioningError(
            f"Unsupported version '{version}'. Expected semantic version like 0.2.0."
        )
    return (
        int(match.group("major")),
        int(match.group("minor")),
        int(match.group("patch")),
    )


def _validate_release_date(value: str) -> str:
    try:
        date.fromisoformat(value)
    except ValueError as error:
        raise VersioningError(
            f"Unsupported release date '{value}'. Expected YYYY-MM-DD."
        ) from error
    return value


def bump_version(current_version: str, part: str) -> str:
    if part not in PART_VALUES:
        supported_parts = ", ".join(PART_VALUES)
        raise VersioningError(
            f"Unsupported part '{part}'. Expected one of: {supported_parts}."
        )
    major, minor, patch = _parse_version(current_version)
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    return f"{major}.{minor}.{patch + 1}"


def propose_release(
    repo_root: Path,
    part: str = "minor",
    explicit_version: str | None = None,
    explicit_release_date: str | None = None,
) -> ProposedRelease:
    current = _load_release_state(repo_root)
    next_version = (
        explicit_version
        if explicit_version is not None
        else bump_version(current.version, part)
    )
    _parse_version(next_version)
    next_release_date = (
        _validate_release_date(explicit_release_date)
        if explicit_release_date is not None
        else date.today().isoformat()
    )
    return ProposedRelease(
        current_version=current.version,
        current_release_date=current.release_date,
        next_version=next_version,
        next_release_date=next_release_date,
    )


def _run_git(repo_root: Path, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )


def ensure_clean_worktree(repo_root: Path) -> None:
    result = _run_git(repo_root, ["status", "--porcelain"])
    if result.returncode != 0:
        raise VersioningError(result.stderr.strip() or "Failed to inspect git status.")
    if result.stdout.strip():
        raise VersioningError("Release operations require a clean git worktree.")


def ensure_main_branch(repo_root: Path) -> None:
    result = _run_git(repo_root, ["branch", "--show-current"])
    if result.returncode != 0:
        raise VersioningError(
            result.stderr.strip() or "Failed to read current git branch."
        )
    if result.stdout.strip() != "main":
        raise VersioningError("Release tags may only be created from the 'main' branch.")


def ensure_tag_absent(repo_root: Path, tag_name: str) -> None:
    result = _run_git(
        repo_root,
        ["rev-parse", "-q", "--verify", f"refs/tags/{tag_name}"],
    )
    if result.returncode == 0:
        raise VersioningError(f"Tag '{tag_name}' already exists.")


def _replace_single_match(
    pattern: str,
    replacement: str,
    content: str,
    context: str,
) -> str:
    updated, count = re.subn(pattern, replacement, content, count=1, flags=re.MULTILINE)
    if count != 1:
        raise VersioningError(f"Could not update {context}.")
    return updated


def _update_pyproject(repo_root: Path, version: str, release_date: str) -> None:
    path = repo_root / "pyproject.toml"
    content = path.read_text(encoding="utf-8")
    content = _replace_single_match(
        r'(?ms)(^\[project\]\n.*?^version = )"[^"]+"',
        rf'\1"{version}"',
        content,
        "pyproject project.version",
    )
    if "[tool.ai-standards]" in content:
        content = _replace_single_match(
            r'(?ms)(^\[tool\.ai-standards\]\n.*?^release_date = )"[^"]+"',
            rf'\1"{release_date}"',
            content,
            "pyproject tool.ai-standards.release_date",
        )
    else:
        content = (
            content.rstrip()
            + f'\n\n[tool.ai-standards]\nrelease_date = "{release_date}"\n'
        )
    path.write_text(content, encoding="utf-8")


def _update_manifest_file(
    path: Path,
    ai_standards_version: str | None = None,
    project_version: str | None = None,
    project_release_date: str | None = None,
) -> None:
    content = path.read_text(encoding="utf-8")
    if ai_standards_version is not None:
        if re.search(r"^ai_standards_version = ", content, flags=re.MULTILINE):
            content = _replace_single_match(
                r'(^ai_standards_version = )"[^"]+"',
                rf'\1"{ai_standards_version}"',
                content,
                f"{path.name} ai_standards_version",
            )
        elif re.search(r"^version = ", content, flags=re.MULTILINE):
            content = _replace_single_match(
                r'(^version = )"[^"]+"',
                rf'ai_standards_version = "{ai_standards_version}"',
                content,
                f"{path.name} ai_standards_version",
            )
        else:
            content = f'ai_standards_version = "{ai_standards_version}"\n' + content
    if project_version is not None:
        if re.search(r"^project_version = ", content, flags=re.MULTILINE):
            content = _replace_single_match(
                r'(^project_version = )"[^"]+"',
                rf'\1"{project_version}"',
                content,
                f"{path.name} project_version",
            )
        else:
            content = f'project_version = "{project_version}"\n' + content
    if project_release_date is not None:
        if re.search(r"^project_release_date = ", content, flags=re.MULTILINE):
            content = _replace_single_match(
                r'(^project_release_date = )"[^"]+"',
                rf'\1"{project_release_date}"',
                content,
                f"{path.name} project_release_date",
            )
        else:
            content = f'project_release_date = "{project_release_date}"\n' + content
    path.write_text(content, encoding="utf-8")


def save_release(
    repo_root: Path,
    part: str = "minor",
    version: str | None = None,
    release_date: str | None = None,
) -> ProposedRelease:
    ensure_clean_worktree(repo_root)
    proposal = propose_release(
        repo_root=repo_root,
        part=part,
        explicit_version=version,
        explicit_release_date=release_date,
    )
    _update_pyproject(repo_root, proposal.next_version, proposal.next_release_date)
    _update_manifest_file(
        repo_root / "ai.project.toml",
        ai_standards_version=proposal.next_version,
        project_version=proposal.next_version,
        project_release_date=proposal.next_release_date,
    )
    _update_manifest_file(
        repo_root / "templates" / "project_manifest.toml",
        ai_standards_version=proposal.next_version,
    )
    rendered = build_rendered_content(repo_root, repo_root=repo_root)
    write_rendered_content(rendered)
    return proposal


def build_tag_name(repo_root: Path) -> str:
    release = _load_release_state(repo_root)
    return f"{release.version}-{release.release_date}"


def create_tag(repo_root: Path) -> str:
    ensure_clean_worktree(repo_root)
    ensure_main_branch(repo_root)
    tag_name = build_tag_name(repo_root)
    ensure_tag_absent(repo_root, tag_name)
    release = _load_release_state(repo_root)
    result = _run_git(
        repo_root,
        [
            "tag",
            "-a",
            tag_name,
            "-m",
            f"Release {release.version} ({release.release_date})",
        ],
    )
    if result.returncode != 0:
        raise VersioningError(
            result.stderr.strip() or f"Failed to create tag '{tag_name}'."
        )
    return tag_name


def _echo_preview(proposal: ProposedRelease) -> None:
    typer.echo(f"Current version: {proposal.current_version}")
    typer.echo(f"Current release date: {proposal.current_release_date}")
    typer.echo(f"Proposed version: {proposal.next_version}")
    typer.echo(f"Proposed release date: {proposal.next_release_date}")


@app.command()
def preview(
    part: Annotated[str, typer.Option("--part")] = "minor",
    version: Annotated[str | None, typer.Option("--version")] = None,
    release_date: Annotated[str | None, typer.Option("--release-date")] = None,
) -> None:
    """Preview the next release version."""

    proposal = propose_release(
        repo_root=_repo_root(),
        part=part,
        explicit_version=version,
        explicit_release_date=release_date,
    )
    _echo_preview(proposal)


@app.command()
def save(
    part: Annotated[str, typer.Option("--part")] = "minor",
    version: Annotated[str | None, typer.Option("--version")] = None,
    release_date: Annotated[str | None, typer.Option("--release-date")] = None,
) -> None:
    """Save release metadata into repository files on a clean worktree."""

    proposal = save_release(
        repo_root=_repo_root(),
        part=part,
        version=version,
        release_date=release_date,
    )
    typer.echo(f"Saved version: {proposal.next_version}")
    typer.echo(f"Saved release date: {proposal.next_release_date}")


@app.command()
def tag() -> None:
    """Create an annotated release tag from pyproject.toml on main."""

    tag_name = create_tag(_repo_root())
    typer.echo(tag_name)


if __name__ == "__main__":
    try:
        if len(sys.argv) == 1:
            preview()
        else:
            app()
    except VersioningError as error:
        typer.echo(f"Error: {error}", err=True)
        raise typer.Exit(code=1) from error
