"""Shared helpers: config loading, ffmpeg/ffprobe wrappers, slugs."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import yaml

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "brand.yaml"


def load_config(path: Path | str = CONFIG_PATH) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def slugify(text: str, maxlen: int = 60) -> str:
    s = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    s = re.sub(r"[\s_-]+", "-", s)
    return s[:maxlen].strip("-") or "clip"


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    """Run a subprocess, raising with captured stderr on failure."""
    proc = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if proc.returncode != 0:
        raise RuntimeError(
            f"command failed ({proc.returncode}): {' '.join(cmd)}\n{proc.stderr[-2000:]}"
        )
    return proc


def probe_dimensions(video: Path) -> tuple[int, int]:
    """Return (width, height) of the first video stream.

    Prefers ffprobe; falls back to parsing `ffmpeg -i` stderr when ffprobe isn't installed
    (some ffmpeg builds ship without it).
    """
    if shutil.which("ffprobe"):
        proc = run([
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height", "-of", "json", str(video),
        ])
        stream = json.loads(proc.stdout)["streams"][0]
        return int(stream["width"]), int(stream["height"])

    # Fallback: ffmpeg prints stream info to stderr and exits non-zero (no output file).
    proc = subprocess.run(["ffmpeg", "-i", str(video)], capture_output=True, text=True)
    m = re.search(r"Video:.*?(\d{2,5})x(\d{2,5})", proc.stderr)
    if not m:
        raise RuntimeError(f"could not determine dimensions of {video}")
    return int(m.group(1)), int(m.group(2))


def write_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False))


def read_json(path: Path):
    return json.loads(Path(path).read_text())
