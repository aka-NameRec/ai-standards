from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from scripts.ai_sync import build_rendered_content, write_rendered_content

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_render_contains_expected_markers(tmp_path: Path) -> None:
    project_root = tmp_path / "demo-project"
    project_root.mkdir()
    (project_root / "docs" / "ai").mkdir(parents=True)

    manifest = (
        'version = "2026.03"\n'
        'fragments = [\n'
        '  "core/base",\n'
        '  "core/git-workflow",\n'
        '  "core/architecture",\n'
        '  "core/error-handling",\n'
        '  "core/python",\n'
        ']\n'
        'features = ["conport", "design-first-collaboration", "grace"]\n'
        'stacks = ["python", "fastapi", "vue"]\n'
        'local_overrides = ["docs/ai/project-rules.md"]\n'
        'optional_local_overrides = ["docs/ai/private-rules.local.md"]\n'
        "\n"
        "[metadata]\n"
        'project_name = "demo-project"\n'
    )
    (project_root / "ai.project.toml").write_text(manifest, encoding="utf-8")
    (project_root / "docs" / "ai" / "project-rules.md").write_text(
        "# Project-Specific AI Rules\n\n- Demo override.\n",
        encoding="utf-8",
    )
    (project_root / "docs" / "ai" / "private-rules.local.md").write_text(
        "# Private AI Rules\n\n- Private local override.\n",
        encoding="utf-8",
    )

    result = build_rendered_content(project_root)

    assert "Generated from ai-standards@2026.03" in result.content
    assert "## Design-First Collaboration" in result.content
    assert "## GRACE Knowledge Structuring" in result.content
    assert "## FastAPI Stack" in result.content
    assert "## Vue Stack" in result.content
    assert "Demo override." in result.content
    assert "Private local override." in result.content


def test_java_spring_stack_can_be_rendered(tmp_path: Path) -> None:
    project_root = tmp_path / "demo-project"
    project_root.mkdir()
    (project_root / "docs" / "ai").mkdir(parents=True)

    manifest = (
        'version = "2026.03"\n'
        'fragments = ["core/base", "core/architecture", "core/error-handling"]\n'
        'features = ["conport"]\n'
        'stacks = ["java-spring"]\n'
        'local_overrides = ["docs/ai/project-rules.md"]\n'
        "\n"
        "[metadata]\n"
        'project_name = "demo-project"\n'
    )
    (project_root / "ai.project.toml").write_text(manifest, encoding="utf-8")
    (project_root / "docs" / "ai" / "project-rules.md").write_text(
        "# Project-Specific AI Rules\n\n- Demo override.\n",
        encoding="utf-8",
    )

    result = build_rendered_content(project_root)

    assert "## Java Spring Stack" in result.content
    assert "Prefer constructor injection over field injection." in result.content


def test_review_lenses_feature_can_be_rendered(tmp_path: Path) -> None:
    project_root = tmp_path / "demo-project"
    project_root.mkdir()
    (project_root / "docs" / "ai").mkdir(parents=True)

    manifest = (
        'version = "2026.03"\n'
        'fragments = ["core/base", "core/architecture"]\n'
        'features = ["review-lenses"]\n'
        'stacks = ["python"]\n'
        'local_overrides = ["docs/ai/project-rules.md"]\n'
        "\n"
        "[metadata]\n"
        'project_name = "demo-project"\n'
    )
    (project_root / "ai.project.toml").write_text(manifest, encoding="utf-8")
    (project_root / "docs" / "ai" / "project-rules.md").write_text(
        "# Project-Specific AI Rules\n\n- Demo override.\n",
        encoding="utf-8",
    )

    result = build_rendered_content(project_root)

    assert "## Multi-Lens Review" in result.content
    assert (
        "Quality over Efficiency when safety, readability, or correctness is at risk."
        in result.content
    )


def test_written_file_matches_rendered_content(tmp_path: Path) -> None:
    project_root = tmp_path / "demo-project"
    project_root.mkdir()
    (project_root / "docs" / "ai").mkdir(parents=True)

    (project_root / "ai.project.toml").write_text(
        (REPO_ROOT / "templates" / "project_manifest.toml").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (project_root / "docs" / "ai" / "project-rules.md").write_text(
        (REPO_ROOT / "templates" / "project_rules.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    result = build_rendered_content(project_root)
    write_rendered_content(result)

    assert result.output_path.read_text(encoding="utf-8") == result.content


def test_render_cli_accepts_default_output_name_with_typer_024_plus(tmp_path: Path) -> None:
    project_root = tmp_path / "demo-project"
    project_root.mkdir()
    (project_root / "docs" / "ai").mkdir(parents=True)

    (project_root / "ai.project.toml").write_text(
        (REPO_ROOT / "templates" / "project_manifest.toml").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    (project_root / "docs" / "ai" / "project-rules.md").write_text(
        (REPO_ROOT / "templates" / "project_rules.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            str(REPO_ROOT / "scripts" / "ai_sync.py"),
            "render",
            "--project-root",
            str(project_root),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert (project_root / "AGENTS.md").exists()


def test_missing_optional_override_does_not_fail(tmp_path: Path) -> None:
    project_root = tmp_path / "demo-project"
    project_root.mkdir()
    (project_root / "docs" / "ai").mkdir(parents=True)

    manifest = (
        'version = "2026.03"\n'
        'fragments = ["core/base", "core/architecture"]\n'
        'features = ["conport"]\n'
        'stacks = ["python"]\n'
        'local_overrides = ["docs/ai/project-rules.md"]\n'
        'optional_local_overrides = ["docs/ai/private-rules.local.md"]\n'
        "\n"
        "[metadata]\n"
        'project_name = "demo-project"\n'
    )
    (project_root / "ai.project.toml").write_text(manifest, encoding="utf-8")
    (project_root / "docs" / "ai" / "project-rules.md").write_text(
        "# Project-Specific AI Rules\n\n- Demo override.\n",
        encoding="utf-8",
    )

    result = build_rendered_content(project_root)

    assert "Demo override." in result.content
    assert "private-rules.local" not in result.content
