from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_standard_playbook_defines_required_sections_and_evidence_boundary():
    text = (ROOT / "docs" / "tactical_playbook_standard.md").read_text()
    for heading in (
        "## Match Objective",
        "## Match Overview",
        "## Tactical Decision Breakdown",
        "## Core Rules & Practice Plan",
        "## Evidence Limits",
    ):
        assert heading in text
    for label in ("OBSERVED", "INFERRED", "UNKNOWN"):
        assert label in text


def test_delta_force_playbook_uses_the_standard_and_stays_media_free():
    text = (ROOT / "examples" / "delta_force_extraction_tactical_playbook.md").read_text()
    for heading in (
        "## Match Objective",
        "## Match Overview",
        "## Tactical Decision Breakdown",
        "## Core Rules & Practice Plan",
        "## Evidence Limits",
    ):
        assert heading in text
    assert "Position Exposed" in text
    assert ".mp4" not in text.lower()
    assert "/home/" not in text
