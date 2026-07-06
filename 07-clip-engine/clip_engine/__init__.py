"""Clip Engine — self-hosted Opus.pro-style vertical-clip renderer.

Stages: ingest -> transcribe -> vocab -> find_moments -> cut -> reframe -> captions -> render.
Each module is independently runnable and writes intermediate artifacts to work/<job>/ so any
stage can be inspected or restarted.
"""

__version__ = "0.1.0"
