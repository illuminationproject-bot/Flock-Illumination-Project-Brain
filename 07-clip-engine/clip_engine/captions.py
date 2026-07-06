"""Stage 7 — Word-by-word karaoke captions as an ASS subtitle file.

We already have per-word timestamps, so we emit ASS with \\k karaoke timing and per-word
color highlights pulled from config. libass (via ffmpeg) burns it in during render.

Timings must be RE-BASED to the clip: word times are absolute in the source, but the cut clip
starts at 0. We subtract the clip start, and if internal filler was dropped the caption may
drift slightly on long clips — acceptable for v1; the Remotion upgrade path removes it entirely.
"""
from __future__ import annotations

from pathlib import Path


def build_ass(clip: dict, work: Path, config: dict) -> Path:
    cap = config["captions"]
    out = work / "captions.ass"
    words = clip.get("words", [])
    clip_start = clip["start"]

    header = _ass_header(cap)
    cues = _group_cues(words, cap["words_per_cue"])
    lines = []
    for cue in cues:
        start = max(0.0, cue[0]["start"] - clip_start)
        end = max(start + 0.2, cue[-1]["end"] - clip_start)
        text = _render_cue(cue, cap, clip_start)
        lines.append(
            f"Dialogue: 0,{_ts(start)},{_ts(end)},Main,,0,0,0,,{text}"
        )
    out.write_text(header + "\n".join(lines) + "\n")
    return out


def _group_cues(words: list[dict], per_cue: int) -> list[list[dict]]:
    return [words[i:i + per_cue] for i in range(0, len(words), per_cue)]


def _render_cue(cue: list[dict], cap: dict, clip_start: float) -> str:
    """One cue = several words; each word gets \\k duration and a highlight color if 'keyword'."""
    highlights = cap.get("highlight_colors", [])
    parts = []
    for i, w in enumerate(cue):
        dur_cs = max(1, int(round((w["end"] - w["start"]) * 100)))   # centiseconds for \\k
        word = w["word"].upper() if cap.get("uppercase") else w["word"]
        # Heuristic keyword highlight: longer content words get the accent color.
        if len(w["word"]) >= 6 and highlights:
            color = highlights[i % len(highlights)]
            parts.append(f"{{\\k{dur_cs}\\c{color}}}{word}{{\\c{cap['primary_color']}}} ")
        else:
            parts.append(f"{{\\k{dur_cs}}}{word} ")
    return "".join(parts).strip()


def _ass_header(cap: dict) -> str:
    bold = -1 if cap.get("weight", "").lower() in ("black", "bold", "900") else 0
    align = {"center": 5, "bottom": 2, "top": 8}.get(cap.get("position", "center"), 5)
    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,{cap['font']},{int(cap['size']) * 4},{cap['primary_color']},&H00000000,&H80000000,{bold},{cap['outline']},{cap['shadow']},{align},60,60,120,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def _ts(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return f"{h}:{m:02d}:{s:05.2f}"
