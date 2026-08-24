#!/usr/bin/env python3
"""Extract and optionally annotate local evidence frames for a private session workbook."""
import argparse
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

COLORS = {
    "OBSERVED": (20, 214, 236),
    "INFERRED": (244, 77, 174),
    "UNKNOWN": (245, 181, 55),
}


def font(size: int):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)


def extract(source: Path, timestamp: float, target: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-ss", str(timestamp), "-i", str(source), "-frames:v", "1", str(target)],
        check=True,
    )


def annotate(path: Path, callouts: list[dict]) -> None:
    if not callouts:
        return
    image = Image.open(path).convert("RGB")
    draw = ImageDraw.Draw(image)
    width, height = image.size
    for callout in callouts:
        target = callout.get("target", [0.5, 0.5])
        origin = callout.get("origin", [0.12, 0.16])
        label = str(callout.get("label", "VISIBLE DETAIL"))
        evidence = str(callout.get("evidence_class", "OBSERVED")).upper()
        color = COLORS.get(evidence, COLORS["OBSERVED"])
        sx, sy = round(origin[0] * width), round(origin[1] * height)
        ex, ey = round(target[0] * width), round(target[1] * height)
        draw.line((sx, sy, ex, ey), fill=color, width=max(3, width // 220))
        draw.ellipse((ex - 8, ey - 8, ex + 8, ey + 8), outline=color, width=3)
        box_width = max(160, len(label) * 15)
        draw.rounded_rectangle((sx - 8, sy - 36, sx + box_width, sy - 4), radius=6, fill=(8, 11, 17), outline=color, width=2)
        draw.text((sx + 4, sy - 31), label, fill=color, font=font(max(14, width // 52)))
    image.save(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True, help="JSON with a snapshots list and timestamps in seconds")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--output-manifest", type=Path, help="Defaults to output-dir/workbook_snapshot_manifest.json")
    args = parser.parse_args()
    if not args.source.exists():
        raise SystemExit(f"missing source: {args.source}")
    manifest = json.loads(args.manifest.read_text())
    snapshots = manifest.get("snapshots", [])
    if not snapshots:
        raise SystemExit("snapshot manifest needs at least one snapshot")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for snapshot in snapshots:
        snapshot_id = snapshot.get("id")
        timestamp = snapshot.get("timestamp")
        if not snapshot_id or not isinstance(timestamp, (int, float)) or timestamp < 0:
            raise SystemExit(f"invalid snapshot entry: {snapshot}")
        image_path = args.output_dir / f"{snapshot_id}.png"
        extract(args.source, float(timestamp), image_path)
        annotate(image_path, snapshot.get("callouts", []))
        snapshot["path"] = str(image_path.resolve())
    output_manifest = args.output_manifest or args.output_dir / "workbook_snapshot_manifest.json"
    output_manifest.write_text(json.dumps(manifest, indent=2))
    print(json.dumps({"snapshots": len(snapshots), "manifest": str(output_manifest)}, indent=2))


if __name__ == "__main__":
    main()
