from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from scripts.bump_version import (
    VersioningError,
    bump_version,
    create_tag,
    save_release,
)


def _run_git(repo_root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )


def _init_demo_repo(tmp_path: Path) -> Path:
    repo_root = tmp_path / "demo-repo"
    (repo_root / "docs" / "ai").mkdir(parents=True)
    (repo_root / "fragments" / "core").mkdir(parents=True)
    (repo_root / "templates").mkdir(parents=True)
    (repo_root / "scripts").mkdir(parents=True)

    (repo_root / ".gitignore").write_text(
        ".venv/\n__pycache__/\n*.egg-info/\n",
        encoding="utf-8",
    )

    (repo_root / "pyproject.toml").write_text(
        (
            "[project]\n"
            'name = "demo-repo"\n'
            'version = "0.1.0"\n'
            'dependencies = ["typer>=0.12.3,<1.0.0"]\n'
            "\n"
            "[project.scripts]\n"
            'bump-version = "scripts.bump_version:main"\n'
            'ai-sync = "scripts.ai_sync:main"\n'
            "\n"
            "[build-system]\n"
            'requires = ["setuptools>=68", "wheel"]\n'
            'build-backend = "setuptools.build_meta"\n'
            "\n"
            "[tool.setuptools.packages.find]\n"
            'include = ["scripts*"]\n'
            "\n"
            "[tool.ai-standards]\n"
            'version = "0.1.0"\n'
            'release_date = "2026-04-15"\n'
        ),
        encoding="utf-8",
    )
    (repo_root / "registry.toml").write_text(
        '[features]\nconport = ["core/base"]\n\n[stacks]\npython = ["core/base"]\n',
        encoding="utf-8",
    )
    (repo_root / "fragments" / "core" / "base.md").write_text(
        "## Base\n- Demo base rule.\n",
        encoding="utf-8",
    )
    (repo_root / "docs" / "ai" / "project-rules.md").write_text(
        "# Project-Specific AI Rules\n\n- Demo override.\n",
        encoding="utf-8",
    )
    (repo_root / "ai.project.toml").write_text(
        (
            'ai_standards_version = "0.1.0"\n'
            'project_version = "0.1.0"\n'
            'project_release_date = "2026-04-15"\n'
            'fragments = ["core/base"]\n'
            'features = ["conport"]\n'
            'stacks = ["python"]\n'
            'local_overrides = ["docs/ai/project-rules.md"]\n'
            "optional_local_overrides = []\n"
            "\n"
            "[tooling]\n"
            "agents = []\n"
            "\n"
            "[metadata]\n"
            'project_name = "demo-repo"\n'
        ),
        encoding="utf-8",
    )
    (repo_root / "templates" / "project_manifest.toml").write_text(
        (
            'ai_standards_version = "0.1.0"\n'
            'project_version = "replace-me"\n'
            'project_release_date = "YYYY-MM-DD"\n'
            'fragments = ["core/base"]\n'
            'features = ["conport"]\n'
            'stacks = ["python"]\n'
            'local_overrides = ["docs/ai/project-rules.md"]\n'
            "optional_local_overrides = []\n"
            "\n"
            "[tooling]\n"
            "agents = []\n"
            "\n"
            "[metadata]\n"
            'project_name = "replace-me"\n'
        ),
        encoding="utf-8",
    )
    shutil.copyfile(
        Path(__file__).resolve().parents[1] / "scripts" / "ai_sync.py",
        repo_root / "scripts" / "ai_sync.py",
    )
    shutil.copyfile(
        Path(__file__).resolve().parents[1] / "scripts" / "bump_version.py",
        repo_root / "scripts" / "bump_version.py",
    )

    assert subprocess.run(
        ["uv", "lock"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    ).returncode == 0

    assert _run_git(repo_root, "init", "-b", "main").returncode == 0
    assert _run_git(repo_root, "config", "user.name", "Codex Test").returncode == 0
    assert _run_git(repo_root, "config", "user.email", "codex@example.com").returncode == 0
    assert _run_git(repo_root, "add", ".").returncode == 0
    assert _run_git(repo_root, "commit", "-m", "init").returncode == 0
    return repo_root


def test_bump_version_supports_major_minor_and_patch() -> None:
    assert bump_version("0.1.0", "major") == "1.0.0"
    assert bump_version("0.1.0", "minor") == "0.2.0"
    assert bump_version("0.1.0", "patch") == "0.1.1"


def test_save_release_updates_repo_metadata_and_agents(tmp_path: Path) -> None:
    repo_root = _init_demo_repo(tmp_path)

    proposal = save_release(
        repo_root=repo_root,
        part="minor",
        release_date="2026-04-20",
    )

    assert proposal.next_version == "0.2.0"
    pyproject = (repo_root / "pyproject.toml").read_text(encoding="utf-8")
    manifest = (repo_root / "ai.project.toml").read_text(encoding="utf-8")
    template_manifest = (repo_root / "templates" / "project_manifest.toml").read_text(
        encoding="utf-8"
    )
    agents = (repo_root / "AGENTS.md").read_text(encoding="utf-8")

    assert '[project]\nname = "demo-repo"\nversion = "0.1.0"' in pyproject
    assert '[tool.ai-standards]\nversion = "0.2.0"' in pyproject
    assert 'release_date = "2026-04-20"' in pyproject
    assert 'ai_standards_version = "0.2.0"' in manifest
    assert 'project_version = "0.2.0"' in manifest
    assert 'project_release_date = "2026-04-20"' in manifest
    assert 'ai_standards_version = "0.2.0"' in template_manifest
    assert 'project_version = "replace-me"' in template_manifest
    assert "Generated by ai-standards v0.2.0 release date: 2026-04-20" in agents
    assert "Project version: 0.2.0 release date: 2026-04-20" in agents


def test_save_release_requires_clean_worktree(tmp_path: Path) -> None:
    repo_root = _init_demo_repo(tmp_path)
    (repo_root / "README.md").write_text("dirty\n", encoding="utf-8")

    try:
        save_release(repo_root=repo_root)
    except VersioningError as error:
        assert "clean git worktree" in str(error)
    else:
        raise AssertionError("Expected save_release to reject a dirty worktree")


def test_save_command_runs_via_uv_console_script(tmp_path: Path) -> None:
    repo_root = _init_demo_repo(tmp_path)

    result = subprocess.run(
        [
            "uv",
            "run",
            "--frozen",
            "bump-version",
            "save",
            "--version",
            "1.1.0",
            "--release-date",
            "2026-04-16",
        ],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
    assert "Saved version: 1.1.0" in result.stdout
    pyproject = (repo_root / "pyproject.toml").read_text(encoding="utf-8")
    assert '[project]\nname = "demo-repo"\nversion = "0.1.0"' in pyproject
    assert '[tool.ai-standards]\nversion = "1.1.0"' in pyproject


def test_create_tag_requires_main_branch(tmp_path: Path) -> None:
    repo_root = _init_demo_repo(tmp_path)
    assert _run_git(repo_root, "switch", "-c", "feature/demo").returncode == 0

    try:
        create_tag(repo_root)
    except VersioningError as error:
        assert "main" in str(error)
    else:
        raise AssertionError("Expected create_tag to reject non-main branches")


def test_create_tag_creates_annotated_release_tag(tmp_path: Path) -> None:
    repo_root = _init_demo_repo(tmp_path)
    save_release(
        repo_root=repo_root,
        version="1.2.0",
        release_date="2026-05-01",
    )
    assert _run_git(repo_root, "add", ".").returncode == 0
    assert _run_git(repo_root, "commit", "-m", "prepare release").returncode == 0

    tag_name = create_tag(repo_root)

    assert tag_name == "1.2.0-2026-05-01"
    tag_message = _run_git(repo_root, "tag", "-n99", tag_name)
    assert tag_message.returncode == 0
    assert "Release 1.2.0 (2026-05-01)" in tag_message.stdout
