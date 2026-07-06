# Quickstart — Apple Silicon Mac

Tested: the ffmpeg pipeline (cut → reframe → captions → burn) runs green end-to-end and
outputs a 1080×1920 captioned MP4. Below is the exact setup to run it on your Mac against a
real Flock Talk episode.

## 1. System deps (Homebrew)

```bash
brew install ffmpeg python@3.11
# Montserrat Black for the brand caption look:
brew install --cask font-montserrat
```

## 2. Python env

```bash
cd 07-clip-engine
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...      # for moment-finding + titles
```

## 3. Transcription on Apple Silicon — pick one

WhisperX uses CTranslate2, which on Mac runs on **CPU** (no Metal/GPU). It works but is slow
on a full hour. Two better options for a "beefy Mac":

- **Fastest on Apple Silicon — MLX Whisper** (uses the GPU via Metal):
  ```bash
  pip install mlx-whisper
  ```
  Then set `backend="mlx"` — a tiny adapter needs adding to `transcribe.py` (~15 lines wrapping
  `mlx_whisper.transcribe(..., word_timestamps=True)`). Ask Claude to "add the MLX backend."
- **No local model at all — Deepgram API** (no GPU, pay per minute): fill in the `_deepgram`
  seam in `transcribe.py`; set `backend="deepgram"`.
- **Just works, slower — WhisperX on CPU**: the default. Fine for a 20-30 min clip; expect
  several minutes on a full hour.

## 4. Run it

```bash
# A real episode from YouTube:
python run.py --input "https://youtu.be/YOUR_EPISODE" --max-clips 5

# Or a local file, with your IP music bed under it at the brand -20dB:
python run.py --input ~/Footage/flocktalk_ep5.mp4 --music ~/Brand/ip-bed.mp3 --max-clips 5
```

Finished clips land in `OUT/` — each `.mp4` (1080×1920, captioned) with a `.json` sidecar
(title, hook, score, source timestamps) ready to drop into the `06-editor-pipeline` review
flow for Logan's polish pass.

## 5. First-run tips

- Start with `--max-clips 2` on a short video to see output fast, then scale up.
- Tune the look in `config/brand.yaml` — font, highlight colors, words-per-cue, min/max clip
  length. No code changes needed.
- If a clip's crop wanders on multi-person coaching-call footage, that's the reframe fallback;
  the MediaPipe speaker-tracking upgrade (or Google AutoFlip) is the fix — flagged in
  `reframe.py`.
- The two things this container test could NOT exercise (no GPU/API here): WhisperX
  transcription and Claude moment-finding. Everything downstream of them is proven. Your first
  Mac run is the real test of those two stages.
