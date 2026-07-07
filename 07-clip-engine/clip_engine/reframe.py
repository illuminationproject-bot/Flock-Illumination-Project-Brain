"""Stage 6 — Reframe 16:9 -> 9:16 with speaker tracking (the hard part Opus sells).

Approach: detect the face each frame (MediaPipe), pick the dominant face, compute a target
crop-x centered on it, smooth the crop path over time (exponential smoothing) so it glides
instead of jittering, then let ffmpeg apply the per-time crop.

Fallbacks, in order:
  1. No mediapipe installed OR no faces found      -> static center crop (always works)
  2. Faces found                                    -> smoothed face-tracked crop

Production upgrade path: swap this module for Google MediaPipe **AutoFlip**, which adds
saliency + shot-boundary awareness. This file is the seam; nothing downstream changes.
"""
from __future__ import annotations

from pathlib import Path

from .util import probe_dimensions, run

OUT_W, OUT_H = 1080, 1920                          # canonical vertical canvas (matches captions)


def reframe(clip_video: Path, work: Path, config: dict) -> Path:
    out = work / "reframe.mp4"
    W, H = probe_dimensions(clip_video)
    target_w = int(round(H * 9 / 16)) & ~1         # crop width (force even for libx264)

    if target_w >= W:                              # already vertical-ish: crop then normalize
        run(["ffmpeg", "-y", "-i", str(clip_video),
             "-vf", f"crop={min(W, target_w)}:{H},scale={OUT_W}:{OUT_H}",
             "-c:a", "copy", str(out)])
        return out

    centers = _tracked_centers(clip_video, W, H, config)
    if not centers:
        # Static center crop fallback, upscaled to the canonical canvas
        x = (W - target_w) // 2
        run(["ffmpeg", "-y", "-i", str(clip_video),
             "-vf", f"crop={target_w}:{H}:{x}:0,scale={OUT_W}:{OUT_H}",
             "-c:a", "copy", str(out)])
        return out

    # Build a time-varying crop x-expression from smoothed centers via ffmpeg sendcmd.
    # sendcmd needs a relative filename (its path parser chokes on ':' etc), so we run with
    # cwd=work and reference the basename, while input/output stay absolute.
    cmds = work / "crop.cmd"
    half = target_w / 2
    lines = []
    for t, cx in centers:
        x = max(0, min(W - target_w, cx - half))
        lines.append(f"{t:.2f} crop x {x:.1f};")
    cmds.write_text("\n".join(lines))
    run(["ffmpeg", "-y", "-i", str(clip_video.resolve()),
         "-vf", f"sendcmd=f={cmds.name},crop={target_w}:{H}:0:0,scale={OUT_W}:{OUT_H}",
         "-c:a", "copy", str(out.resolve())], cwd=str(work))
    return out


def _tracked_centers(video: Path, W: int, H: int, config: dict, fps_sample: float = 4.0):
    """Sample frames, find dominant face center-x per sample, exponentially smooth the path.

    Any failure here (missing libs, mediapipe API changes, codec issues) returns [] so the
    caller falls back to a static center crop instead of crashing the pipeline.
    """
    try:
        import cv2
        import mediapipe as mp
        detector = mp.solutions.face_detection.FaceDetection(model_selection=1,
                                                             min_detection_confidence=0.5)
    except Exception as e:
        print(f"    (face tracking unavailable — center crop instead: {e})")
        return []

    cap = cv2.VideoCapture(str(video))
    src_fps = cap.get(cv2.CAP_PROP_FPS) or 30
    step = max(1, int(src_fps / fps_sample))
    smoothing = float(config["reframe"].get("smoothing", 0.85))

    raw = []
    idx = 0
    smoothed_cx = W / 2
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if idx % step == 0:
            t = idx / src_fps
            res = detector.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if res.detections:
                # dominant = largest box
                best = max(res.detections,
                           key=lambda d: d.location_data.relative_bounding_box.width)
                box = best.location_data.relative_bounding_box
                cx = (box.xmin + box.width / 2) * W
                smoothed_cx = smoothing * smoothed_cx + (1 - smoothing) * cx
            raw.append((t, smoothed_cx))
        idx += 1
    cap.release()
    detector.close()
    return raw
