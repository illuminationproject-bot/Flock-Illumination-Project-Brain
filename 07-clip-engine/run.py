#!/usr/bin/env python3
"""Clip Engine CLI — one long video in, brand-styled vertical clips out.

    python run.py --input "https://youtu.be/ID" --max-clips 5
    python run.py --input ~/footage/ep5.mp4 --music ~/brand/bed.mp3

Requires: ffmpeg on PATH, ANTHROPIC_API_KEY set, deps from requirements.txt.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from clip_engine.render import process


def main() -> None:
    ap = argparse.ArgumentParser(description="Self-hosted Opus-style clip engine")
    ap.add_argument("--input", required=True, help="YouTube URL or local video path")
    ap.add_argument("--out", default="OUT", help="output dir for finished clips")
    ap.add_argument("--work", default="work", help="scratch dir for intermediates")
    ap.add_argument("--mode", default="talk", choices=["talk", "music"], help="pipeline mode")
    ap.add_argument("--max-clips", type=int, default=6)
    ap.add_argument("--music", default=None, help="optional music bed (mixed at brand -20dB)")
    ap.add_argument("--config", default=None, help="path to brand.yaml (default: config/brand.yaml)")
    args = ap.parse_args()

    clips = process(
        source=args.input,
        out_dir=Path(args.out),
        work_root=Path(args.work),
        mode=args.mode,
        max_clips=args.max_clips,
        music=Path(args.music) if args.music else None,
        config_path=args.config,
    )
    print(f"\nDone. {len(clips)} clips in {args.out}/:")
    for c in clips:
        print(f"  • {c.name}")


if __name__ == "__main__":
    main()
