#!/usr/bin/env python3
"""FFmpeg coaching-video renderer (runs locally / on-device, no cloud needed).

Consumes ``contextual_coaching_map.json`` (``selected_fights``) plus an optional
source gameplay video and produces a single H.264/AAC MP4. Each selected fight
becomes a segment:

  * footage is trimmed from the source (if a source is supplied), otherwise a
    solid title card is generated;
  * a caption overlay (question / reveal) is burned in via a Pillow-rendered
    PNG (no drawtext/font dependency);
  * optional narration is synthesized with Kokoro (feature-detected; silent if
    unavailable).

Segments are concatenated with the FFmpeg concat demuxer.
"""
import argparse, json, subprocess, sys, tempfile, wave
from pathlib import Path

FFMPEG = "ffmpeg"
FPS = 30
WIDTH, HEIGHT = 1920, 1080


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, text=True, capture_output=True, **kw)


# ---------------------------------------------------------------------------
# Text / caption rendering (Pillow, feature-detected)
# ---------------------------------------------------------------------------
def _font(size):
    from PIL import ImageFont
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            try:
                return ImageFont.truetype(c, size)
            except Exception:
                pass
    return ImageFont.load_default()


def _wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def make_caption_png(title, question, reveal, out_path, w=WIDTH, h=HEIGHT):
    from PIL import Image, ImageDraw
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    pad = 60
    box_h = int(h * 0.34)
    d.rectangle([0, h - box_h, w, h], fill=(8, 11, 20, 210))
    d.rectangle([0, h - box_h, 10, h], fill=(232, 72, 43, 255))
    x = pad
    y = h - box_h + 30
    title_font = _font(46)
    q_font = _font(54)
    a_font = _font(40)
    if title:
        d.text((x, y), title, font=title_font, fill=(232, 72, 43, 255))
        y += 60
    if question:
        for ln in _wrap(d, "Q: " + question, q_font, w - 2 * pad):
            d.text((x, y), ln, font=q_font, fill=(255, 255, 255, 255))
            y += 64
    if reveal:
        for ln in _wrap(d, "A: " + reveal, a_font, w - 2 * pad):
            d.text((x, y), ln, font=a_font, fill=(200, 210, 225, 255))
            y += 50
    img.save(out_path)


# ---------------------------------------------------------------------------
# Optional TTS (Kokoro, feature-detected)
# ---------------------------------------------------------------------------
def synth(text, out_wav, voice="af_sarah"):
    try:
        from kokoro_onnx import Kokoro
    except Exception:
        return False
    model = Path("/root/.cache/kokoro/kokoro-v1.0.int8.onnx")
    voices = Path("/root/.cache/kokoro/voices-v1.0.bin")
    model = Path(
        __import__("os").environ.get("KOKORO_MODEL", str(model))
    )
    voices = Path(
        __import__("os").environ.get("KOKORO_VOICES", str(voices))
    )
    if not model.exists() or not voices.exists():
        return False
    try:
        k = Kokoro(str(model), str(voices))
        audio, sr = k.create(text, voice=voice, speed=1.0, lang="en-us")
        import numpy as np
        audio = np.asarray(audio, dtype="float32")
        pcm = (audio * 32767).clip(-32768, 32767).astype("<i2").tobytes()
        with wave.open(str(out_wav), "wb") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(int(sr))
            f.writeframes(pcm)
        return True
    except Exception as e:
        print(f"[tts] Kokoro failed: {e}", file=sys.stderr)
        return False


def pad_wav_to(in_wav, out_wav, duration_s, sr=24000):
    import numpy as np
    with wave.open(str(in_wav), "rb") as f:
        n = f.getnframes()
        raw = f.readframes(n)
        data = np.frombuffer(raw, dtype="<i2").astype("float32") / 32768.0
    total = int(duration_s * sr)
    if data.size < total:
        data = np.concatenate([data, np.zeros(total - data.size, dtype="float32")])
    else:
        data = data[:total]
    pcm = (data * 32767).clip(-32768, 32767).astype("<i2").tobytes()
    with wave.open(str(out_wav), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sr)
        f.writeframes(pcm)


# ---------------------------------------------------------------------------
# Segment building
# ---------------------------------------------------------------------------
def build_segment(fight, idx, work, source, fps, voice):
    seg = work / f"seg_{idx:03d}.mp4"
    cap_png = work / f"cap_{idx:03d}.png"
    tts_wav = work / f"tts_{idx:03d}.wav"
    tts_wav_padded = work / f"tts_{idx:03d}_p.wav"

    fid = fight.get("fight_id", f"fight_{idx:03d}")
    question = fight.get("question") or "What was the decision point here?"
    reveal = fight.get("reveal") or fight.get("outcome") or ""
    start = float(fight.get("source_start", fight.get("start", 0)) or 0)
    end = float(fight.get("source_end", fight.get("end", 0)) or 0)
    dur = max(round(end - start, 2), 4.0)

    make_caption_png(f"Fight {fid}", question, reveal, cap_png)

    # base video
    base = work / f"base_{idx:03d}.mp4"
    if source and Path(source).exists():
        run([
            FFMPEG, "-y", "-ss", f"{start}", "-to", f"{end}", "-i", str(source),
            "-vf", f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=decrease,pad={WIDTH}:{HEIGHT}:(ow-iw)/2:(oh-ih)/2",
            "-r", str(fps), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
            str(base),
        ])
    else:
        run([
            FFMPEG, "-y", "-f", "lavfi", "-i", f"color=c=0x0b0e14:s={WIDTH}x{HEIGHT}:r={fps}:d={dur}",
            "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
            "-r", str(fps), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-t", f"{dur}",
            str(base),
        ])

    # overlay caption
    step = base
    if cap_png.exists():
        step = work / f"ov_{idx:03d}.mp4"
        run([
            FFMPEG, "-y", "-i", str(base), "-i", str(cap_png),
            "-filter_complex", "[1:v]format=rgba[ov];[0:v][ov]overlay=0:(H-h)",
            "-r", str(fps), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "copy",
            str(step),
        ])

    # optional narration
    used_tts = synth(f"{question} {reveal}", tts_wav, voice=voice)
    if used_tts:
        pad_wav_to(tts_wav, tts_wav_padded, dur)
        run([
            FFMPEG, "-y", "-i", str(step), "-i", str(tts_wav_padded),
            "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest",
            str(seg),
        ])
        print(f"[seg {idx}] built with TTS narration ({dur}s)")
    else:
        seg.write_bytes(step.read_bytes())
        print(f"[seg {idx}] built (no TTS) ({dur}s)")

    # cleanup intermediates
    for f in (base, cap_png, tts_wav, tts_wav_padded):
        try:
            if f != seg:
                f.unlink()
        except OSError:
            pass
    if step != seg:
        try:
            step.unlink()
        except OSError:
            pass
    return seg


def main(argv=None):
    ap = argparse.ArgumentParser(description="Render a coaching episode with FFmpeg.")
    ap.add_argument("--workdir", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--source", type=Path)
    ap.add_argument("--fps", type=int, default=FPS)
    ap.add_argument("--voice", default="af_sarah")
    ap.add_argument("--no-tts", action="store_true")
    args = ap.parse_args(argv)
    w = args.workdir
    w.mkdir(parents=True, exist_ok=True)
    cmap = json.loads((w / "contextual_coaching_map.json").read_text())
    fights = cmap.get("selected_fights", [])
    if not fights:
        print("INVALID: no selected_fights in contextual_coaching_map.json", file=sys.stderr)
        return 1

    global_synth_off = args.no_tts
    segs = []
    for i, f in enumerate(fights, 1):
        segs.append(build_segment(f, i, w, args.source, args.fps, args.voice))

    if len(segs) == 1:
        args.output.write_bytes(segs[0].read_bytes())
    else:
        list_file = w / "concat.txt"
        list_file.write_text("\n".join(f"file '{s.resolve()}'" for s in segs) + "\n")
        run([
            FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
            str(args.output),
        ])
    for s in segs:
        try:
            s.unlink()
        except OSError:
            pass
    print(json.dumps({"backend": "ffmpeg", "segments": len(segs), "output": str(args.output)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
