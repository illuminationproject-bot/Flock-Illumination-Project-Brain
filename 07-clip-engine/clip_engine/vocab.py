"""Stage 3 — Faith/production vocabulary correction.

Whisper mangles names and worship terms ("Asaph", "Flock Talk", artist names). We fix them in
the word stream BEFORE captions burn in — the single biggest quality win over Opus, which has
no idea what these words are. Driven entirely by config/brand.yaml -> vocab_fixups.
"""
from __future__ import annotations

import re
from pathlib import Path

from .util import read_json, write_json


def apply_vocab(words_json: Path, config: dict) -> Path:
    data = read_json(words_json)
    fixups = config.get("vocab_fixups", {}) or {}
    if not fixups:
        return words_json

    # Sort by phrase length desc so multi-word fixes ("flock talk") win over single words.
    ordered = sorted(fixups.items(), key=lambda kv: -len(kv[0].split()))
    words = data["words"]
    text_tokens = [w["word"] for w in words]

    for wrong, right in ordered:
        n = len(wrong.split())
        if n == 1:
            for w in words:
                if _norm(w["word"]) == _norm(wrong):
                    w["word"] = _preserve_case(w["word"], right)
        else:
            # Multi-word: slide a window and rewrite the span, keeping per-word timings.
            i = 0
            while i <= len(words) - n:
                window = " ".join(_norm(t) for t in text_tokens[i:i + n])
                if window == _norm(wrong):
                    replacement = right.split()
                    for j, rep in enumerate(replacement[:n]):
                        words[i + j]["word"] = rep
                    i += n
                else:
                    i += 1
            text_tokens = [w["word"] for w in words]

    write_json(words_json, data)
    return words_json


def _norm(s: str) -> str:
    return re.sub(r"[^\w]", "", s).lower()


def _preserve_case(original: str, replacement: str) -> str:
    if original.isupper():
        return replacement.upper()
    if original[:1].isupper():
        return replacement[:1].upper() + replacement[1:]
    return replacement
