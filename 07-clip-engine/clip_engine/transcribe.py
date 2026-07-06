"""Stage 2 — Transcribe with WORD-LEVEL timestamps.

Word timestamps are the foundation of the whole engine: exact cut points, karaoke captions,
and speaker-aware reframing all depend on knowing when each word is said.

Default backend: WhisperX (self-hosted, needs a GPU for real speed).
Swap seam: set backend="deepgram" to go GPU-free / pay-per-minute (implement in _deepgram).

Output schema (words.json):
    {"words": [{"word": "faithfulness", "start": 12.34, "end": 12.98, "speaker": "SPEAKER_00"}, ...]}
"""
from __future__ import annotations

import os
from pathlib import Path

from .util import write_json


def transcribe(video: Path, work: Path, backend: str = "whisperx",
               model: str = "large-v2", diarize: bool = True) -> Path:
    out = work / "words.json"
    if backend == "whisperx":
        words = _whisperx(video, model=model, diarize=diarize)
    elif backend == "deepgram":
        words = _deepgram(video)
    else:
        raise ValueError(f"unknown transcribe backend: {backend}")
    write_json(out, {"words": words})
    return out


def _whisperx(video: Path, model: str, diarize: bool) -> list[dict]:
    import whisperx  # imported lazily so the rest of the engine runs without torch installed

    device = "cuda" if _has_cuda() else "cpu"
    compute = "float16" if device == "cuda" else "int8"

    asr = whisperx.load_model(model, device, compute_type=compute)
    audio = whisperx.load_audio(str(video))
    result = asr.transcribe(audio, batch_size=16)

    # Forced alignment -> real word-level timestamps
    align_model, meta = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], align_model, meta, audio, device,
                            return_char_alignments=False)

    speakers = {}
    if diarize and os.getenv("HF_TOKEN"):
        dia = whisperx.DiarizationPipeline(use_auth_token=os.getenv("HF_TOKEN"), device=device)
        diarization = dia(audio)
        result = whisperx.assign_word_speakers(diarization, result)

    words: list[dict] = []
    for seg in result["segments"]:
        for w in seg.get("words", []):
            if "start" not in w:  # unaligned tokens (rare) — skip
                continue
            words.append({
                "word": w["word"].strip(),
                "start": round(float(w["start"]), 3),
                "end": round(float(w["end"]), 3),
                "speaker": w.get("speaker", "SPEAKER_00"),
            })
    return words


def _deepgram(video: Path) -> list[dict]:
    """No-GPU alternative. Fill in with the Deepgram SDK (nova-2, diarize, word timestamps).

    Left as an explicit seam so the choice of transcription backend never leaks into the
    rest of the pipeline — everything downstream only reads words.json.
    """
    raise NotImplementedError(
        "Deepgram backend not wired yet. Use backend='whisperx', or implement here: "
        "deepgram.listen.prerecorded with smart_format+diarize+utterances and map word timings."
    )


def _has_cuda() -> bool:
    try:
        import torch
        return torch.cuda.is_available()
    except Exception:
        return False
