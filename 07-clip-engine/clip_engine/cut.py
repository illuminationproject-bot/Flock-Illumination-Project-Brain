"""Stage 5 — Cut. Slice the clip out of the source, optionally removing internal dead air.

Simple version: one ffmpeg trim on [start, end].
drop_internal_filler: split the clip's words into speech runs, drop gaps longer than
`gap_threshold`, and concat the pieces — this is where mid-clip "umms"/pauses actually vanish.
"""
from __future__ import annotations

from pathlib import Path

from .util import run


def cut(source: Path, clip: dict, work: Path, config: dict, gap_threshold: float = 0.7) -> Path:
    out = work / "cut.mp4"
    start, end = clip["start"], clip["end"]

    if config["clips"].get("drop_internal_filler") and clip.get("words"):
        segments = _speech_runs(clip["words"], gap_threshold)
    else:
        segments = [(start, end)]

    if len(segments) == 1:
        s, e = segments[0]
        run([
            "ffmpeg", "-y", "-ss", f"{s:.3f}", "-to", f"{e:.3f}", "-i", str(source),
            "-c:v", "libx264", "-c:a", "aac", "-preset", "veryfast", str(out),
        ])
        return out

    # Multi-segment: trim each run, then concat. Keeps A/V in sync per piece.
    # Re-encode on concat (not -c copy) so segments with independent GOPs join cleanly.
    parts = []
    for i, (s, e) in enumerate(segments):
        p = work / f"part_{i:02d}.mp4"
        run([
            "ffmpeg", "-y", "-ss", f"{s:.3f}", "-to", f"{e:.3f}", "-i", str(source.resolve()),
            "-c:v", "libx264", "-c:a", "aac", "-preset", "veryfast", str(p.resolve()),
        ])
        parts.append(p)
    concat_file = work / "concat.txt"
    # Absolute paths inside the list so the concat demuxer resolves regardless of cwd.
    concat_file.write_text("".join(f"file '{p.resolve()}'\n" for p in parts))
    run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file.resolve()),
        "-c:v", "libx264", "-c:a", "aac", "-preset", "veryfast", str(out.resolve()),
    ])
    return out


def _speech_runs(words: list[dict], gap: float) -> list[tuple[float, float]]:
    """Collapse words into continuous speech runs, breaking on silences > gap seconds."""
    runs: list[list[float]] = []
    for w in words:
        if runs and w["start"] - runs[-1][1] <= gap:
            runs[-1][1] = w["end"]
        else:
            runs.append([w["start"], w["end"]])
    # small padding so we don't clip breaths at run edges
    return [(max(0, s - 0.08), e + 0.08) for s, e in runs]
