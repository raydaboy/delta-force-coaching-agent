import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_session_workbook import validate


def load(name: str):
    return json.loads((ROOT / "examples" / name).read_text())


def test_sanitized_workbook_example_is_structurally_valid():
    assert validate(load("session_workbook_input.json"), load("workbook_snapshot_manifest.json")) == []


def test_generic_alternative_is_rejected():
    workbook = load("session_workbook_input.json")
    workbook["lessons"][0]["alternative"]["action"] = "Use cover."
    errors = validate(workbook, load("workbook_snapshot_manifest.json"))
    assert any("too generic" in error for error in errors)


def test_missing_snapshot_reference_is_rejected():
    workbook = load("session_workbook_input.json")
    workbook["lessons"][0]["snapshot_id"] = "not-present"
    errors = validate(workbook, load("workbook_snapshot_manifest.json"))
    assert any("snapshot_id" in error for error in errors)
