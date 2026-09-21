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
RULE_ID_PATTERN = re.compile(r"^[A-Z]{2,5}-\d{3}$")


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


def test_rule_fragments_and_sections_exist() -> None:
    for rule_id, rule in _load_rule_map().items():
        fragment_path = REPO_ROOT / "fragments" / f"{rule['fragment']}.md"
        assert fragment_path.is_file(), f"{rule_id}: missing fragment {rule['fragment']}"
        content = fragment_path.read_text(encoding="utf-8")
        headings = {
            line.lstrip("#").strip()
            for line in content.splitlines()
            if line.startswith("#")
        }
        assert rule["section"] in headings, (
            f"{rule_id}: section {rule['section']!r} not found in {rule['fragment']}"
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
