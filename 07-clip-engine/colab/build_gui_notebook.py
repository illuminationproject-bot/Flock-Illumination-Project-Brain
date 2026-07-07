"""Generate the one-click GUI launcher notebook (Colab).

Two cells: (1) install + load engine + app, (2) launch the web GUI and print its link.
Engine + app.py are embedded as a compressed blob, byte-identical to the repo.
    python colab/build_gui_notebook.py
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
    "clip_engine/render.py", "run.py", "config/brand.yaml", "app.py",
]

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
    "print('Installing (2-3 min)…')\n"
    "import subprocess\n"
    "subprocess.run('pip -q install gradio anthropic yt-dlp pyyaml faster-whisper', shell=True)\n"
    "import base64, io, tarfile\n"
    "BLOB_PARTS = [\n"
    + "".join(f'    "{c}",\n' for c in chunks)
    + "]\n"
    'blob = base64.b64decode("".join(BLOB_PARTS))\n'
    'tarfile.open(fileobj=io.BytesIO(blob), mode="r:gz").extractall(".")\n'
    'print("\\u2705 Ready. Run the next cell to open your app.")\n'
)

cells = [
    md("""
# 🎬 Flock Clip Engine — App Launcher

Two clicks and your app is open in a browser tab.

1. Click ▶ on the box below (installs everything — 2–3 min)
2. Click ▶ on the second box — it prints a link like `https://xxxxx.gradio.live` → **click it**

That link IS your app: paste a Drive link or upload a video, set how many clips, hit **⚡ Make Clips**.
The link stays alive while this tab stays open (up to ~12h per Colab session).
"""),
    code(loader),
    code(r"""
import os
os.environ["GRADIO_SHARE"] = "1"
exec(open("app.py").read())
"""),
]

nb = {
    "nbformat": 4, "nbformat_minor": 0,
    "metadata": {"colab": {"provenance": []},
                 "kernelspec": {"name": "python3", "display_name": "Python 3"},
                 "accelerator": "GPU"},
    "cells": cells,
}

out = ROOT / "colab" / "Flock_Clip_Engine_APP.ipynb"
out.write_text(json.dumps(nb, indent=1))
print("wrote", out, f"({out.stat().st_size // 1024} KB)")
