"""Stage 8 — Orchestrator. Burn captions, mix optional music bed, emit final MP4 + metadata.

Also the top-level pipeline entry (`process`) that runs all stages for one source video and
writes finished clips to OUT/. This is what run.py calls.
"""
from __future__ import annotations

import os
from pathlib import Path

from . import captions as captions_mod
from . import cut as cut_mod
from . import find_moments as find_mod
from . import ingest as ingest_mod
from . import reframe as reframe_mod
from . import transcribe as transcribe_mod
from . import vocab as vocab_mod
from .util import load_config, run, slugify, write_json


def process(source: str, out_dir: Path, work_root: Path, *, mode: str = "talk",
            max_clips: int = 6, music: Path | None = None,
            config_path: str | None = None) -> list[Path]:
    config = load_config(config_path) if config_path else load_config()
    out_dir.mkdir(parents=True, exist_ok=True)
    job = work_root / slugify(source.split("/")[-1] or "job")
    job.mkdir(parents=True, exist_ok=True)

    print("1/8 ingest…");        src = ingest_mod.ingest(source, job)
    print("2/8 transcribe…");    words = transcribe_mod.transcribe(src, job)
    print("3/8 vocab fixups…");  vocab_mod.apply_vocab(words, config)

    if mode == "music":
        raise NotImplementedError(
            "music/worship mode is a v2 stub — it needs beat-synced cutting instead of "
            "speech-based moment finding. Use --mode talk for now."
        )

    print("4/8 find moments…");  clips_json = find_mod.find_moments(words, job, config, max_clips)
    clips = _read(clips_json)["clips"]
    print(f"    found {len(clips)} clips")

    finals: list[Path] = []
    for i, clip in enumerate(clips):
        cdir = job / f"clip_{i:02d}"; cdir.mkdir(exist_ok=True)
        print(f"5/8 cut clip {i} ({clip['title'][:40]})…");  raw = cut_mod.cut(src, clip, cdir, config)
        print(f"6/8 reframe clip {i}…");                     framed = reframe_mod.reframe(raw, cdir, config)
        print(f"7/8 captions clip {i}…");                    ass = captions_mod.build_ass(clip, cdir, config)
        print(f"8/8 render clip {i}…")
        finals.append(_burn(framed, ass, clip, out_dir, config, music))
    return finals


def _burn(video: Path, ass: Path, clip: dict, out_dir: Path, config: dict,
          music: Path | None) -> Path:
    slug = slugify(clip["title"])
    out = out_dir / f"{slug}.mp4"
    vf = f"subtitles={ass.name}"

    cmd = ["ffmpeg", "-y", "-i", str(video.resolve())]
    if music:
        db = config["audio"]["music_bed_db"]
        cmd += ["-stream_loop", "-1", "-i", str(music.resolve()),
                "-filter_complex",
                f"[0:v]{vf}[v];[1:a]volume={db}dB[bg];[0:a][bg]amix=inputs=2:duration=first[a]",
                "-map", "[v]", "-map", "[a]"]
    else:
        cmd += ["-vf", vf]
    cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-c:a", "aac", "-b:a", "160k", str(out.resolve())]
    run(cmd, cwd=str(ass.parent))

    write_json(out_dir / f"{slug}.json", {
        "title": clip["title"], "hook": clip.get("hook"), "why": clip.get("why"),
        "score": clip.get("score"), "kind": clip.get("kind"),
        "source_start": clip["start"], "source_end": clip["end"],
        "file": out.name,
    })
    return out


def _read(p: Path):
    import json
    return json.loads(Path(p).read_text())
