"""Policy tests for the rule traceability map (issue #17, Phase 2).

The map at ``rule_map.toml`` carries stable rule IDs used by eval tooling;
the IDs never render into ``AGENTS.md``. These tests are the deterministic
assertion half of the map's own verifiability requirement: every referenced
fragment and section must exist, and IDs must stay well-formed and unique.
"""

import re
import tomllib
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
RULE_MAP_PATH = REPO_ROOT / "rule_map.toml"
SCENARIOS_DIR = REPO_ROOT / "docs" / "scenarios"
RULE_ID_PATTERN = re.compile(r"^[A-Z]{2,5}-\d{3}$")
SCENARIO_ID_PATTERN = re.compile(r"^([A-Z]{2,5}-\d{3})-")


def _load_rule_map() -> dict[str, dict[str, Any]]:
    data = tomllib.loads(RULE_MAP_PATH.read_text(encoding="utf-8"))
    rules = data.get("rules")
    assert isinstance(rules, dict), "rule_map.toml must define a [rules] table"
    return rules


def test_rule_map_exists_and_is_not_empty() -> None:
    assert RULE_MAP_PATH.is_file(), "rule_map.toml must exist at the repository root"
    rules = _load_rule_map()
    assert rules, "the rule map must not be empty"


def test_rule_ids_are_well_formed_and_unique() -> None:
    seen: set[str] = set()
    for rule_id in _load_rule_map():
        assert RULE_ID_PATTERN.match(rule_id), f"bad rule id: {rule_id}"
        assert rule_id not in seen, f"duplicate rule id: {rule_id}"
        seen.add(rule_id)


def _rule_source_path(rule: dict[str, Any]) -> Path:
    if "source" in rule:
        return REPO_ROOT / str(rule["source"])
    return REPO_ROOT / "fragments" / f"{rule['fragment']}.md"


def test_rule_fragments_and_sections_exist() -> None:
    for rule_id, rule in _load_rule_map().items():
        source_path = _rule_source_path(rule)
        assert source_path.is_file(), f"{rule_id}: missing source {source_path.name}"
        content = source_path.read_text(encoding="utf-8")
        headings = {
            line.lstrip("#").strip()
            for line in content.splitlines()
            if line.startswith("#")
        }
        assert rule["section"] in headings, (
            f"{rule_id}: section {rule['section']!r} not found in {source_path.name}"
        )


def test_rule_behaviors_and_scenario_refs_are_well_formed() -> None:
    for rule_id, rule in _load_rule_map().items():
        behavior = str(rule["behavior"]).strip()
        assert behavior, f"{rule_id}: behavior must be a non-empty statement"
        assert "\n" not in behavior, f"{rule_id}: behavior must stay on one line"
        scenarios = rule["scenarios"]
        assert isinstance(scenarios, list), f"{rule_id}: scenarios must be a list"
        assert all(isinstance(s, str) and s for s in scenarios), (
            f"{rule_id}: scenario references must be non-empty strings"
        )


def test_rule_ids_stay_out_of_rendered_content() -> None:
    """IDs are tooling metadata: the self-hosted render must not contain them."""
    agents_md = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "RE-00" not in agents_md, "rule IDs must never render into AGENTS.md"
    assert "RVW-0" not in agents_md, "rule IDs must never render into AGENTS.md"


def _scenario_files() -> dict[str, Path]:
    files: dict[str, Path] = {}
    if not SCENARIOS_DIR.is_dir():
        return files
    for path in sorted(SCENARIOS_DIR.glob("*.md")):
        if path.name.endswith(".ru.md") or path.name.startswith("scenario-format"):
            continue
        match = SCENARIO_ID_PATTERN.match(path.name)
        assert match, f"scenario file name must start with an id: {path.name}"
        assert match.group(1) not in files, f"duplicate scenario id: {path.name}"
        files[match.group(1)] = path
    return files


def test_scenario_files_match_the_id_convention() -> None:
    scenario_files = _scenario_files()
    assert scenario_files, "the scenarios directory must hold at least one contract"
    for scenario_id, path in scenario_files.items():
        ru_pair = path.with_name(path.name.replace(".md", ".ru.md"))
        assert ru_pair.is_file(), f"{scenario_id}: missing localized pair {ru_pair.name}"


def test_rule_map_scenario_references_resolve() -> None:
    known_scenarios = set(_scenario_files())
    for rule_id, rule in _load_rule_map().items():
        for scenario_id in rule["scenarios"]:
            assert scenario_id in known_scenarios, (
                f"{rule_id}: scenario reference {scenario_id} has no contract file"
            )


FORMAT_HEADINGS_EN = (
    "## Fixture",
    "## Enabled Features",
    "## Prompt",
    "## Expected Observable Invariants",
    "## Forbidden Outcomes",
    "## Observations",
    "## Relations",
)
FORMAT_HEADINGS_RU = (
    "## Фикстура",
    "## Включённые features",
    "## Prompt",
    "## Ожидаемые наблюдаемые инварианты",
    "## Запрещённые исходы",
    "## Наблюдения",
    "## Связи",
)
TRIGGER_HEADINGS_EN = (
    "## Enabled Features",
    "## Positive Cases",
    "## Negative Cases",
    "## Boundary Cases",
    "## Observations",
    "## Relations",
)
TRIGGER_HEADINGS_RU = (
    "## Включённые features",
    "## Позитивные кейсы",
    "## Негативные кейсы",
    "## Пограничные кейсы",
    "## Наблюдения",
    "## Связи",
)


def _has_fenced_prompt(content: str) -> bool:
    lines = content.splitlines()
    prompt_starts = [i for i, line in enumerate(lines) if line.strip() == "## Prompt"]
    if not prompt_starts:
        return False
    start = prompt_starts[0]
    end = next(
        (i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")),
        len(lines),
    )
    return any(line.startswith("```") for line in lines[start + 1 : end])


def _is_trigger_set(content: str) -> bool:
    return "Activation trigger set" in content


def test_scenario_files_follow_the_format_contract() -> None:
    """docs/scenarios/scenario-format.md defines this structure; tests enforce it."""
    known_rules = set(_load_rule_map())
    for scenario_id, path in _scenario_files().items():
        content = path.read_text(encoding="utf-8")
        headings = TRIGGER_HEADINGS_EN if _is_trigger_set(content) else FORMAT_HEADINGS_EN
        for heading in headings:
            assert heading in content, f"{scenario_id}: missing heading {heading!r}"
        if not _is_trigger_set(content):
            assert _has_fenced_prompt(content), (
                f"{scenario_id}: prompt must be a fenced block"
            )
        referenced = set(re.findall(r"`([A-Z]{2,5}-\d{3})`", content))
        unknown = referenced - known_rules
        assert not unknown, f"{scenario_id}: unknown rule ids {sorted(unknown)}"


def test_scenario_ru_pairs_follow_the_format_contract() -> None:
    for scenario_id, path in _scenario_files().items():
        ru_pair = path.with_name(path.name.replace(".md", ".ru.md"))
        content = ru_pair.read_text(encoding="utf-8")
        is_trigger = _is_trigger_set(path.read_text(encoding="utf-8"))
        headings = TRIGGER_HEADINGS_RU if is_trigger else FORMAT_HEADINGS_RU
        for heading in headings:
            assert heading in content, f"{scenario_id}: missing heading {heading!r}"
