# Content Package Agent — Playbook

**What it is:** a scheduled AI agent (Claude Code routine, runs daily) that executes the AI
lane of `../live-to-waterfall-sop.md` (Stages 1–6) so TJ's only jobs are recording and the
60-sec voice note, and the editor's only jobs are taste and polish.

**Trigger:** daily check of the Notion **🎬 Shoot Briefs** database
(`collection://a8cf3a64-d12f-4c1c-b0b8-cd1df7d43088`).
A row enters the pipeline when TJ sets **Status = Editing**. Rows whose Notes contain the
marker `🤖 AI package prepared` are already done and get skipped (idempotency).

## What the agent does per row (max 2 rows per run)

1. **Read the brief row** — content type, key moments, CTA, deadline, Key link, notes.
2. **Get the transcript.** If Key link is a YouTube URL (ended live or unlisted upload),
   pull captions/transcript. If the row only points at a Drive folder of raw footage, the
   agent works from the brief fields and flags that a Descript transcript is still needed.
3. **Edit Map** (prompt in `../new-ai-prompts.md`): thesis, chapters, keeper moments,
   hook candidates, cut list, caption flags.
4. **Packaging research:** 3 title candidates + thumbnail text + PNG-mockup concept
   description for the main video and each chapter that passes the quality gate
   (self-contained open, complete argument, stranger test). Expect 2–3 chapters, not all.
5. **Shorts selection:** 3–5 moments, split repurpose vs native, hook rewrite + 3 caption
   options each; mark the top 2 for full polish (triage rule).
6. **Write the package into the Notion row** (page content): brief, edit map, packaging,
   shorts list — so the workflow lives where the editor already looks.
7. **Create Asana tasks** in the *Content Packages — Editor Pipeline* project, section
   *📦 Package Ready*: one parent task per package assigned to **Logan** (the editor), due per
   the row's Deadline, with subtasks per deliverable and links to the Notion row + Drive
   folder. *(Logan's Asana gid + email TBD — confirm before arming; placeholder until then.)*
8. **Draft the handoff email** in Gmail (draft only, never auto-send) from
   `../editor-handoff-email-template.md`.
9. **Stamp the row:** append `🤖 AI package prepared <date>` to Notes. Status stays
   `Editing` until the editor delivers.

If no rows qualify, the run ends silently.

## What stays human

- TJ: record, set Status = Editing, drop the voice note, Gate 1 green-light, Gate 2 QC.
- Logan (Premiere + After Effects): the actual edit, animation, grade, sound, caption
  styling, final PSD thumbnails built from the AI's PNG mockups.

## Rendering real clips (proven in-session, 2026-07-07)

The agent doesn't just write cut lists — it RUNS `07-clip-engine/` inside its own session:

1. `pip install faster-whisper imageio-ffmpeg pyyaml` (+ symlink the imageio ffmpeg binary
   onto PATH; no system ffmpeg needed)
2. Get the source video **from Google Drive via the Drive MCP tool** — NOT from YouTube
   (YouTube's CDN blocks datacenter IPs; TJ's RAW folder in Drive is the ingest point)
3. `CLIP_ENGINE_ASR=faster_whisper CLIP_ENGINE_ASR_MODEL=small` → transcribe
4. Read the transcript, pick clips, write `my_clips.json` — the agent IS the brain, so
   `run.py --clips-file my_clips.json` needs **no Anthropic API key**
5. Upload finished clips + sidecar JSONs back to the Drive package folder

## Known limits (be honest with yourself, agent)

- YouTube downloads fail from datacenter IPs (403/bot-check) — always ingest from Drive.
- CPU transcription: use `small` model; a 60-min recording takes a while — process the
  Edit Map first, render clips second, so a slow run still delivers the packaging.
- Face tracking may be unavailable (no cv2/mediapipe) — the engine center-crops
  automatically; note it in the handoff so Logan checks framing.
- Cron minimum is hourly; daily is the chosen cadence. A just-ended live gets packaged the
  next morning.
