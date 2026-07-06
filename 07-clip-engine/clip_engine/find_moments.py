"""Stage 4 — Find self-contained clip moments with Claude.

This is the "virality score" everyone thinks is secret sauce. It's an LLM reading the
transcript and returning scored, self-contained segments — but tuned via config['audience']
to worship-pastor resonance instead of generic virality, which is exactly where a custom
engine beats Opus.

Returns clips with EXACT start/end seconds, snapped to real word boundaries so cuts never
clip a syllable.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from .util import read_json, write_json

MODEL = os.getenv("CLIP_ENGINE_MODEL", "claude-sonnet-5")


def find_moments(words_json: Path, work: Path, config: dict, max_clips: int = 6) -> Path:
    from anthropic import Anthropic

    words = read_json(words_json)["words"]
    if not words:
        raise RuntimeError("no words to analyze — did transcription run?")

    transcript = _timestamped_transcript(words)
    clip_cfg = config["clips"]
    system = (
        "You are a short-form clip strategist. You find self-contained moments in a long "
        "recording that would work as standalone vertical clips. You return STRICT JSON only."
    )
    user = f"""Audience: {config['audience']}

Find up to {max_clips} clips in the transcript below. Each clip MUST:
- be between {clip_cfg['min_seconds']} and {clip_cfg['max_seconds']} seconds long
- open on a hook that lands within {clip_cfg['hook_must_land_within_seconds']} seconds
- contain ONE complete idea with a real ending (not trailing off)
- stand alone: a stranger with zero context understands it

For each clip return:
  "start": seconds (float, use the timestamp of the first word),
  "end": seconds (float, timestamp AFTER the last word),
  "title": insight/tension, not topic (<60 chars),
  "hook": the exact opening line,
  "why": one sentence on why it resonates with THIS audience,
  "score": 1-10 (hook strength + completeness + audience resonance),
  "kind": "native" (works cold) or "repurpose" (references the show)

Return JSON: {{"clips": [ ... ]}} sorted by score desc. No prose.

TRANSCRIPT (each line: [start-end] text):
{transcript}"""

    client = Anthropic()
    # Generous ceiling: models with extended thinking spend tokens before the JSON answer.
    resp = client.messages.create(
        model=MODEL, max_tokens=16000, system=system,
        messages=[{"role": "user", "content": user}],
    )
    # Models may emit thinking blocks before the text block — join only text content.
    reply_text = "".join(getattr(block, "text", "") for block in resp.content)
    clips = _parse_json(reply_text)["clips"]
    clips = [_snap_to_words(c, words) for c in clips]
    clips = [c for c in clips if c]                      # drop un-snappable
    clips.sort(key=lambda c: c.get("score", 0), reverse=True)
    clips = clips[:max_clips]

    out = work / "clips.json"
    write_json(out, {"clips": clips})
    return out


def _timestamped_transcript(words: list[dict], group: int = 12) -> str:
    lines, i = [], 0
    while i < len(words):
        chunk = words[i:i + group]
        start, end = chunk[0]["start"], chunk[-1]["end"]
        text = " ".join(w["word"] for w in chunk)
        lines.append(f"[{start:.2f}-{end:.2f}] {text}")
        i += group
    return "\n".join(lines)


def _snap_to_words(clip: dict, words: list[dict]) -> dict | None:
    """Snap requested start/end to the nearest actual word boundaries."""
    try:
        start = min(words, key=lambda w: abs(w["start"] - float(clip["start"])))["start"]
        end = min(words, key=lambda w: abs(w["end"] - float(clip["end"])))["end"]
    except (KeyError, ValueError):
        return None
    if end - start < 3:
        return None
    clip["start"], clip["end"] = round(start, 3), round(end, 3)
    # attach the word list for this clip so captions.py doesn't re-search
    clip["words"] = [w for w in words if start - 1e-3 <= w["start"] < end + 1e-3]
    return clip


def _parse_json(text: str) -> dict:
    """Extract the JSON object from a model reply, tolerating fences and surrounding prose."""
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1].removeprefix("json").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start != -1 and end > start:
            return json.loads(text[start:end + 1])
        raise RuntimeError(
            f"model reply contained no JSON (length {len(text)}; first 300 chars: {text[:300]!r})"
        )
