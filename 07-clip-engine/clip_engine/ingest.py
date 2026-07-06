"""Stage 1 — Ingest. Get a local source.mp4 from a YouTube URL or a local file."""
from __future__ import annotations

import shutil
from pathlib import Path

from .util import run


def ingest(source: str, work: Path) -> Path:
    """Return path to a local source video. Downloads if `source` is a URL."""
    work.mkdir(parents=True, exist_ok=True)
    out = work / "source.mp4"

    if source.startswith(("http://", "https://")):
        # Best MP4 up to 1080p — plenty for vertical crops, keeps files sane.
        run([
            "yt-dlp",
            "-f", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--merge-output-format", "mp4",
            "-o", str(out),
            source,
        ])
    else:
        src = Path(source).expanduser()
        if not src.exists():
            raise FileNotFoundError(src)
        if src.resolve() != out.resolve():
            shutil.copy(src, out)
    return out
