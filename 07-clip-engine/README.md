# 07 — Clip Engine (the "hands")

An open, self-hosted **Opus.pro-style** pipeline: give it one long video, get back
posted-ready vertical clips — cut, speaker-reframed to 9:16, brand captions burned in.

Where `06-editor-pipeline/` is the **brain** (decides *what* clips should exist and writes the
brief), this is the **hands** (actually renders them). Together they make the original thesis
literally true: **AI does the rough edit, Logan polishes.**

## Why build instead of rent Opus

The three things Opus structurally can't do for this brand — and this engine can:

1. **Brand-exact captions** — your fonts, your keyword-highlight colors, your animation.
   Opus gives ~10 presets. Here the caption style is a config file (`config/brand.yaml`).
2. **Faith-vocabulary correction** — `vocab.py` fixes "Asaph", names, and worship terms in
   the transcript *before* captions burn in. Your #1 recurring caption complaint, gone.
3. **A separate music/worship path** — Opus cuts on speech and butchers performance video.
   Here `--mode music` cuts to feel, not to words. (v2 — stubbed today.)

## The pipeline (8 stages, each a swappable module)

```
run.py
 └─ render.py  (orchestrator)
     1. ingest.py      yt-dlp / local file            → source.mp4
     2. transcribe.py  WhisperX (word timestamps)      → words.json
     3. vocab.py       brand dictionary fixups         → words.json (corrected)
     4. find_moments.py Claude scores self-contained    → clips[] (start/end/title/score)
                        moments for worship-pastor
                        resonance, not generic virality
     5. cut.py         ffmpeg slice + drop internal     → clip_raw.mp4
                        filler/dead-air
     6. reframe.py     MediaPipe face-track + smoothed  → clip_916.mp4
                        crop 16:9 → 9:16 (center-crop
                        fallback if no face)
     7. captions.py    word-by-word ASS karaoke,        → clip.ass
                        brand-styled, keyword highlights
     8. render.py      ffmpeg burn captions + music     → OUT/<slug>.mp4
                        bed at -20dB, write titles.json
```

Every stage writes to `work/<job>/` so you can inspect or restart at any step.

## What's real today vs. stubbed

| Stage | Status |
|---|---|
| ingest, transcribe, vocab, find_moments, cut, captions, render | **Working** (needs deps + API key) |
| reframe (face-track) | **Working**, with a naive-crop fallback; AutoFlip upgrade noted inline |
| music/worship mode | **Stubbed** — v2 |
| B-roll / zoom-punch / progress bar | **Not built** — v3 depth |

This is the **hybrid self-host** path: you own stages 1–8; the only heavy dependency you
don't hand-write is the face detector (MediaPipe). Get a working v1 today, upgrade captions
to [Remotion](https://www.remotion.dev/) (video-as-React) when you want motion-graphics depth.

## Run it

```bash
cd 07-clip-engine
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt          # ffmpeg must be on PATH separately
export ANTHROPIC_API_KEY=sk-...

# One long video → vertical clips in ./OUT
python run.py --input "https://youtu.be/VIDEO_ID" --max-clips 5
python run.py --input ~/footage/flocktalk_ep5.mp4 --mode talk
```

Output per clip: `OUT/<slug>.mp4` (9:16, captioned) + `OUT/<slug>.json` (title, caption,
hashtags, score, source timestamps) — ready to drop into the `06-editor-pipeline` review flow
for Logan's polish pass.

## Cost / infra reality

- **Transcription:** WhisperX is free but wants a GPU (a $0.50/hr cloud GPU does an hour of
  video in minutes). Swap in Deepgram/AssemblyAI (`transcribe.py` has the seam) for
  no-GPU/pay-per-minute.
- **Claude moment-finding:** cents per video.
- **Render:** CPU ffmpeg is fine; a GPU speeds encoding.
- At 1–2 videos/week this runs on a single modest cloud box or even a decent laptop.
