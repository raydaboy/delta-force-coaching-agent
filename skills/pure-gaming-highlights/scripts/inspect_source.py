#!/usr/bin/env python3
"""Inspect a gameplay video with ffprobe and emit reusable JSON metadata."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def inspect(path: Path) -> dict:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=filename,format_name,duration,size:stream=index,codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels,language",
        "-of",
        "json",
        str(path),
    ]
    completed = subprocess.run(command, check=True, capture_output=True, text=True)
    payload = json.loads(completed.stdout)
    payload["input"] = str(path.resolve())
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--json-out", type=Path, help="Optional path for the JSON report")
    args = parser.parse_args()

    if not args.input.is_file():
        print(f"Input file does not exist: {args.input}", file=sys.stderr)
        return 2
    try:
        result = inspect(args.input)
    except (subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        print(f"ffprobe failed: {exc}", file=sys.stderr)
        return 1

    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
