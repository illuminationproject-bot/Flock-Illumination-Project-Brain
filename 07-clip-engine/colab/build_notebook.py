"""Generate a self-contained Colab notebook that embeds the (tested) engine and runs it.

The engine files are tar.gz-compressed and base64-embedded, so the notebook is small and the
code inside it is byte-identical to the repo — no repo clone or GitHub auth needed.
Re-run whenever the engine changes:
    python colab/build_notebook.py
"""
import base64
import io
import json
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = [
    "clip_engine/__init__.py", "clip_engine/util.py", "clip_engine/ingest.py",
    "clip_engine/transcribe.py", "clip_engine/vocab.py", "clip_engine/find_moments.py",
    "clip_engine/cut.py", "clip_engine/reframe.py", "clip_engine/captions.py",
    "clip_engine/render.py", "run.py", "config/brand.yaml",
]

# Pack engine -> tar.gz -> base64 -> 100-char chunks (keeps notebook lines short/valid)
buf = io.BytesIO()
with tarfile.open(fileobj=buf, mode="w:gz") as tar:
    for p in FILES:
        tar.add(ROOT / p, arcname=p)
blob = base64.b64encode(buf.getvalue()).decode()
chunks = [blob[i:i + 100] for i in range(0, len(blob), 100)]


def code(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": src.strip("\n").splitlines(keepends=True)}


def md(src):
    return {"cell_type": "markdown", "metadata": {},
            "source": src.strip("\n").splitlines(keepends=True)}


loader = (
    "import base64, io, tarfile\n"
    "BLOB_PARTS = [\n"
    + "".join(f'    "{c}",\n' for c in chunks)
    + "]\n"
    'blob = base64.b64decode("".join(BLOB_PARTS))\n'
    'tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz").extractall(".")\n'
    'print("\\u2705 Engine loaded.")\n'
)

cells = [
    md("""
# 🎬 Flock Clip Engine — runs in your browser

Turns one long video into captioned vertical clips. **Nothing gets installed on your computer** — this all runs on Google's machines.

**How to use this page (once, top to bottom):**
1. *(Optional but faster)* Menu bar → **Runtime → Change runtime type → T4 GPU → Save**
2. Click the **▶ play button** on the left edge of each gray box below, **in order**. Wait for each to finish (the spinner stops) before the next.
3. Box 3 is where you paste your video link and API key.

At the end, a zip of your clips downloads to your computer.
"""),
    md("### 1️⃣ Install the tools (2–3 min). Click ▶ and wait."),
    code(r"""
!pip -q install anthropic yt-dlp pyyaml faster-whisper
!pip -q install mediapipe opencv-python-headless || echo "(no face tracking — will center-crop)"
print("\n✅ Install done. Go to step 2.")
"""),
    md("### 2️⃣ Load the engine. Click ▶ (instant)."),
    code(loader),
    md("""
### 3️⃣ Your settings — edit the two lines, then click ▶

- **VIDEO_URL** — paste a YouTube link, e.g. a Flock Talk episode
- **ANTHROPIC_API_KEY** — get one at [console.anthropic.com](https://console.anthropic.com) → API Keys → Create Key (starts with `sk-ant-`)
"""),
    code(r"""
VIDEO_URL = "https://youtu.be/PASTE_YOUR_VIDEO_LINK"  #@param {type:"string"}
ANTHROPIC_API_KEY = "sk-ant-PASTE_YOUR_KEY"           #@param {type:"string"}
MAX_CLIPS = 3                                          #@param {type:"integer"}
print("✅ Saved. Video:", VIDEO_URL, "| clips:", MAX_CLIPS, "— go to step 4.")
"""),
    md("### 4️⃣ Make the clips. Click ▶ and let it cook (5–15 min; the first run also downloads the speech model)."),
    code(r"""
import os
os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY
os.environ["CLIP_ENGINE_ASR"] = "faster_whisper"

from pathlib import Path
from clip_engine.render import process

clips = process(source=VIDEO_URL, out_dir=Path("OUT"), work_root=Path("work"),
                mode="talk", max_clips=int(MAX_CLIPS))
print(f"\n✅ Done — {len(clips)} clips made. Go to step 5 to download.")
for c in clips: print("   •", c.name)
"""),
    md("### 5️⃣ Download your clips. Click ▶ — `clips.zip` saves to your computer."),
    code(r"""
!zip -qr clips.zip OUT
from google.colab import files
files.download("clips.zip")
print("✅ If no download started: click the 📁 folder icon on the left, right-click clips.zip → Download.")
"""),
    md("""
---
**Tweak the look:** open the 📁 folder icon on the left → `config` → double-click `brand.yaml` — fonts, highlight colors, clip length all live there. Re-run step 4 after editing.

**Something errored?** Copy the red text and paste it to Claude — it built this and will fix it.
"""),
]

nb = {
    "nbformat": 4, "nbformat_minor": 0,
    "metadata": {"colab": {"provenance": []},
                 "kernelspec": {"name": "python3", "display_name": "Python 3"},
                 "accelerator": "GPU"},
    "cells": cells,
}

out = ROOT / "colab" / "Flock_Clip_Engine.ipynb"
out.write_text(json.dumps(nb, indent=1))
print("wrote", out, f"({out.stat().st_size // 1024} KB, blob {len(blob)//1024} KB)")
