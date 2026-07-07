"""Flock Clip Engine — GUI.

A Gradio web app over the clip pipeline: paste a Drive/YouTube link or upload a video,
click Make Clips, watch progress, download finished 9:16 captioned clips.

Run locally / in Colab:
    pip install gradio
    python app.py            # or demo.launch(share=True) from a notebook

The same file deploys unchanged to a Hugging Face Space or any small server.
"""
from __future__ import annotations

import os
import re
import traceback
from pathlib import Path

import gradio as gr

from clip_engine.render import process

BRAND = {"amber": "#F7C404", "ink": "#101820"}


def _normalize_source(url: str) -> str:
    """Turn Drive share links into direct-download URLs; pass everything else through."""
    url = (url or "").strip()
    m = re.search(r"drive\.google\.com/file/d/([A-Za-z0-9_-]+)", url)
    if not m:
        m = re.search(r"drive\.google\.com/(?:open|uc)\?.*id=([A-Za-z0-9_-]+)", url)
    if m:
        return f"https://drive.usercontent.google.com/download?id={m.group(1)}&export=download&confirm=t"
    return url


def make_clips(video_file, video_url, api_key, max_clips, model_size,
               progress=gr.Progress(track_tqdm=False)):
    logs: list[str] = []

    def log(msg):
        logs.append(msg)
        return "\n".join(logs)

    try:
        source = video_file if video_file else _normalize_source(video_url)
        if not source:
            yield log("⚠️ Give me a video: upload one or paste a link."), []
            return
        key = (api_key or os.getenv("ANTHROPIC_API_KEY", "")).strip()
        if not key:
            yield log("⚠️ Paste your Anthropic API key (console.anthropic.com → API Keys)."), []
            return
        os.environ["ANTHROPIC_API_KEY"] = key
        os.environ["CLIP_ENGINE_ASR"] = "faster_whisper"
        os.environ["CLIP_ENGINE_ASR_MODEL"] = model_size

        yield log("🎬 Starting — download/ingest…"), []
        yield log("   (transcription is the long step: roughly ⅓–1× the video's length on CPU)"), []

        clips = process(
            source=str(source), out_dir=Path("OUT_GUI"), work_root=Path("work_gui"),
            mode="talk", max_clips=int(max_clips),
        )
        if not clips:
            yield log("😕 Pipeline finished but produced no clips — the transcript may be "
                      "empty or too short. Try a longer/clearer recording."), []
            return
        files = [str(c) for c in clips]
        yield log(f"✅ Done — {len(files)} clips. Click each to preview, hover for download."), files
    except Exception as e:
        yield log(f"❌ Error: {e}\n\nDetails for Claude:\n{traceback.format_exc()[-1200:]}"), []


with gr.Blocks(title="Flock Clip Engine") as demo:
    gr.Markdown(
        f"""
# 🎬 Flock Clip Engine
Long recording in → captioned vertical clips out. Brand style lives in `config/brand.yaml`.
<span style="color:{BRAND['amber']}">AI does the rough cut — the editor does the polish.</span>
"""
    )
    with gr.Row():
        with gr.Column(scale=1):
            video_url = gr.Textbox(label="Video link (Google Drive share link or direct URL)",
                                   placeholder="https://drive.google.com/file/d/…/view")
            video_file = gr.Video(label="…or upload a video", sources=["upload"])
            api_key = gr.Textbox(label="Anthropic API key", type="password",
                                 placeholder="sk-ant-…  (used only for this run)")
            with gr.Row():
                max_clips = gr.Slider(1, 6, value=4, step=1, label="How many clips")
                model_size = gr.Dropdown(["base", "small"], value="base",
                                         label="Transcription quality (small = better, slower)")
            go = gr.Button("⚡ Make Clips", variant="primary", size="lg")
        with gr.Column(scale=1):
            status = gr.Textbox(label="Progress", lines=12, interactive=False)
            outputs = gr.Files(label="Finished clips (download)")

    go.click(make_clips, [video_file, video_url, api_key, max_clips, model_size],
             [status, outputs])

if __name__ == "__main__":
    demo.launch(share=os.getenv("GRADIO_SHARE", "1") == "1",
                theme=gr.themes.Soft(primary_hue="amber"))
