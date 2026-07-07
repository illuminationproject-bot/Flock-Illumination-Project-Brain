"""Stage 2 — Transcribe with WORD-LEVEL timestamps.

Word timestamps are the foundation of the whole engine: exact cut points, karaoke captions,
and speaker-aware reframing all depend on knowing when each word is said.

Backends:
  - "mlx"      → MLX Whisper, GPU-accelerated on Apple Silicon (Metal). Best on a Mac.
  - "whisperx" → self-hosted, needs CUDA for speed; runs on CPU elsewhere (incl. Mac).
  - "deepgram" → GPU-free / pay-per-minute API (seam left for you to fill).

Output schema (words.json):
    {"words": [{"word": "faithfulness", "start": 12.34, "end": 12.98, "speaker": "SPEAKER_00"}, ...]}
"""
from __future__ import annotations

import os
from pathlib import Path

from .util import write_json


def transcribe(video: Path, work: Path, backend: str | None = None,
               model: str = "large-v2", diarize: bool = True) -> Path:
    # Default: MLX on Apple Silicon (Metal GPU), else WhisperX.
    backend = backend or os.getenv("CLIP_ENGINE_ASR", "auto")
    if backend == "auto":
        backend = "mlx" if _is_apple_silicon() else "whisperx"

    out = work / "words.json"
    if backend == "mlx":
        words = _mlx(video, model=model)
    elif backend in ("faster", "faster_whisper"):
        words = _faster_whisper(video, model=model)
    elif backend == "whisperx":
        words = _whisperx(video, model=model, diarize=diarize)
    elif backend == "deepgram":
        words = _deepgram(video)
    else:
        raise ValueError(f"unknown transcribe backend: {backend}")
    write_json(out, {"words": words})
    return out


def _faster_whisper(video: Path, model: str) -> list[dict]:
    """faster-whisper — light, no alignment/diarization deps, word timestamps built in.

    Good default for Colab/Windows/Linux without a full WhisperX install. Single speaker.
    """
    from faster_whisper import WhisperModel

    device = "cuda" if _has_cuda() else "cpu"
    compute = "float16" if device == "cuda" else "int8"
    # CLIP_ENGINE_ASR_MODEL overrides (e.g. "small" for fast CPU runs); else map the request.
    size = os.getenv("CLIP_ENGINE_ASR_MODEL") or \
        {"large-v2": "large-v2", "large-v3": "large-v3", "medium": "medium"}.get(model, "medium")

    m = WhisperModel(size, device=device, compute_type=compute)
    segments, _ = m.transcribe(str(video), word_timestamps=True, vad_filter=True)

    words: list[dict] = []
    for seg in segments:
        for w in (seg.words or []):
            words.append({
                "word": w.word.strip(),
                "start": round(float(w.start), 3),
                "end": round(float(w.end), 3),
                "speaker": "SPEAKER_00",
            })
    return words


def _mlx(video: Path, model: str) -> list[dict]:
    """MLX Whisper — GPU-accelerated on Apple Silicon via Metal.

    No diarization (single speaker assumed); for multi-person podcasts where you need
    speaker labels, use the whisperx backend with HF_TOKEN instead.
    """
    import mlx_whisper

    # Map friendly model names to MLX community repos; large-v3 is the quality default.
    repo = {
        "large-v2": "mlx-community/whisper-large-v2-mlx",
        "large-v3": "mlx-community/whisper-large-v3-mlx",
        "medium": "mlx-community/whisper-medium-mlx",
    }.get(model, "mlx-community/whisper-large-v3-mlx")

    result = mlx_whisper.transcribe(
        str(video), path_or_hf_repo=repo, word_timestamps=True,
    )
    words: list[dict] = []
    for seg in result.get("segments", []):
        for w in seg.get("words", []):
            if w.get("start") is None:
                continue
            words.append({
                "word": w["word"].strip(),
                "start": round(float(w["start"]), 3),
                "end": round(float(w["end"]), 3),
                "speaker": "SPEAKER_00",
            })
    return words


def _is_apple_silicon() -> bool:
    import platform
    return platform.system() == "Darwin" and platform.machine() == "arm64"


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
