#!/usr/bin/env python3
"""Render a private session workbook/playbook PDF using the repository Typst base."""
import argparse
import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from validate_session_workbook import read_json, validate

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates/workbook_typst_base"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--snapshot-manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--title", help="Optional title override")
    args = parser.parse_args()
    if not shutil.which("typst"):
        raise SystemExit("Typst is required. Install Typst, then rerun this command.")
    workbook = read_json(args.input)
    snapshots = read_json(args.snapshot_manifest)
    errors = validate(workbook, snapshots, require_files=True)
    if errors:
        raise SystemExit("INVALID WORKBOOK:\n- " + "\n- ".join(errors))
    snapshot_map = {snapshot["id"]: snapshot for snapshot in snapshots["snapshots"]}
    enriched = json.loads(json.dumps(workbook))
    if args.title:
        enriched["title"] = args.title
    args.output_dir.mkdir(parents=True, exist_ok=True)
    build = args.output_dir / "typst_build"
    if build.exists():
        shutil.rmtree(build)
    shutil.copytree(TEMPLATE, build)
    build_snapshots = build / "snapshots"
    build_snapshots.mkdir()
    for lesson in enriched["lessons"]:
        source = Path(snapshot_map[lesson["snapshot_id"]]["path"])
        target = build_snapshots / f"{lesson['snapshot_id']}{source.suffix.lower()}"
        shutil.copy2(source, target)
        lesson["snapshot_path"] = str(Path("snapshots") / target.name)
    data = build / "workbook_data.json"
    data.write_text(json.dumps(enriched, indent=2))
    output = args.output_dir / "session_workbook_playbook.pdf"
    subprocess.run(["typst", "compile", "workbook.typ", str(output.resolve())], check=True, cwd=build)
    manifest = {
        "created_at": now(),
        "renderer": "typst",
        "input": str(args.input.resolve()),
        "snapshot_manifest": str(args.snapshot_manifest.resolve()),
        "selected_lessons": [lesson["lesson_id"] for lesson in enriched["lessons"]],
        "output": str(output.resolve()),
        "limitations": ["Private source media and snapshots remain outside Git.", "PDF generation does not replace evidence validation or human-watch QC."],
    }
    (args.output_dir / "workbook_build_manifest.json").write_text(json.dumps(manifest, indent=2))
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
