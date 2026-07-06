# Live → Waterfall SOP (v2)

**The pipeline:** one live stream / raw upload / call recording → 1 main thesis video +
2–3 chapter videos + 3–5 shorts + text derivatives, with **AI doing the rough assembly and
research, and the editor doing taste, branding, animation, and polish.**

This improves the v1 draft (transcribe → chapters → thesis video → chapter videos → shorts →
editor package → email). The v1 steps all survive — each stage below names what changed and why.

**Division of labor, one line:** AI decides *what* (selects, structure, packaging research,
rough cuts). The editor decides *how it feels* (pacing, motion, grade, sound, final design).

**Confirmed decisions (TJ, 2026-07-04):**
- Cadence: **1–2 lives/week plus a few live coaching calls** — calls enter at Stage 0 like any recording
- Canonical NLE: **Premiere Pro + After Effects** — rough cuts hand off as Premiere
  text-based-editing projects / XML; AE owns animation and motion polish
- Thumbnails: **AI supplies PNG mockups; the editor builds the final layered PSDs** from them
- Approvals: **approve-by-exception confirmed** — the autonomy ladder below is live, and
  shorts skip pre-approval once the editor reaches Level 2
- Task management: packages are assigned in **Asana** (*Content Packages — Editor Pipeline*
  project); the workflow itself lives in the Notion 🎬 Shoot Briefs database
- Automation: the AI lane (Stages 1–6) runs as a scheduled agent — see `automation/`

Companion docs:
- `editor-creative-brief-template.md` — the brief that rides with every package
- `editor-handoff-email-template.md` — the handoff email/Loom script
- `hormozi-research-brief.md` — why the system is shaped this way
- Notion: 🎨 Editor Brand Guide (visual identity), 📋 Editor Onboarding & SOP (weekly rhythm)

---

## Realistic volume math (don't chase "200/day")

Hormozi's real number is ~250/week with an 18-person team. Ours, honestly:

| Per live/pillar recording | Pieces |
|---|---|
| Main thesis video | 1 |
| Chapter videos (8–12 min, quality-gated) | 2–3 |
| Shorts (repurpose + native) | 3–5 |
| Text derivatives (captions, carousel, Skool post, X/threads) | 4–6 |
| **Total per pillar** | **10–15** |

Two pillar recordings/week ≈ **20–30 pieces/week** with one editor + AI. That's the honest
ceiling for this headcount — and per Hormozi's own doctrine, early volume exists to *generate
data*, so the Analytics Log (Notion) is what turns volume into growth.

---

## Stage 0 — Intake (was: "Live ends on YouTube - video is pulled")

Three entry points, one destination:

1. **Live ends on YouTube** → download source file (yt-dlp or YouTube Studio download)
2. **Raw footage upload** (shoot day, performance, visualizer footage)
3. **Call recording** (Zoom/Meet/Riverside)

**Same steps regardless of source:**
- File lands in Drive: `Flock Content/<Pipeline>/<YYYY-MM-DD>/RAW/` (structure per Onboarding SOP)
- Name it: `YYYY-MM-DD_ContentType_Description.mp4`
- Create ONE Notion Content Calendar row for the pillar, status `In edit`
- TJ records the 60-sec voice note (best moments, flags, intended CTA) — this is the seed of
  the creative brief and the highest-value 60 seconds TJ spends in this whole pipeline

**Automation target:** an n8n/Make watcher on the RAW folder that auto-creates the Notion row
and kicks off Stage 1. Until that exists, this is a manual 5-minute step.

## Stage 1 — Transcribe + Edit Map (was: "Transcribe and look for umms/uhhs")

**Upgrade:** filler-word removal is a one-click Descript feature — don't spend AI effort
"looking for umms." The AI's real job is producing a structured **Edit Map**:

1. Ingest into **Descript** → auto-transcript → one-click remove filler words + dead air →
   this IS the rough cut, no timeline scrubbing
2. Run the transcript through Claude with the Edit Map prompt (AI Prompt Library) to produce:
   - **Chapter list** with timestamps and one-line summaries
   - **Thesis statement** — the one idea the whole recording argues for
   - **Keeper moments** — quotable lines, energy peaks, story beats (timestamped)
   - **Hook candidates** — the 5 strongest cold-open moments
   - **Cut list** — tangents, restarts, tech issues, anything that dies in the edit
   - **Flags** — names/terms the captions will get wrong (faith vocabulary, song titles)
3. Save the Edit Map as a doc in the shoot's Drive folder — every later stage reads from it

## Stage 2 — Main thesis video (was: "Edit one main thesis video, 3 titles + thumbnails")

**Packaging BEFORE final edit** — decide the promise first so the edit can open on it:

1. **Titles:** 3 candidates, each backed by research, not vibes:
   - **1of10.com:** find 3–5 outlier videos in our niche whose packaging overperformed their
     channel baseline — note the title *patterns*, don't copy the titles
   - **vidIQ:** check search volume / competition on the core phrase
   - Each candidate names the **insight or tension**, not the topic (existing SOP rule)
2. **Thumbnail concept comps:** 2–3 rough mockups per title (AI-generated or screenshot
   composites). These are **direction, not designs** — the editor beats them, never traces
   them. Each comp ships with the 1of10 reference screenshots that inspired it.
3. **AI rough cut:** apply the Edit Map cut list in Descript; structure = strongest hook
   moment cold open → thesis → chapters in argument order → CTA
4. **Handoff artifact:** Descript → **Premiere timeline export** (or Premiere text-based
   editing project) + marked transcript. Never hand the editor a flattened MP4 to re-edit.

## Stage 3 — Chapter videos (was: "same process for every distinguishable chapter")

**Upgrade: quality-gate instead of "every chapter."** Forcing every chapter into a video
fills the channel with C-material and burns editor hours. Run the Segment Identifier prompt
(AI Prompt Library) and only greenlight chapters that pass all three:

- [ ] Opens clean — doesn't depend on the rest of the recording for context
- [ ] Self-contained argument or story with a natural ending
- [ ] Passes the stranger test: would someone who's never heard of us click this title?

Expect **2–3 per live**, not 6. Each greenlit chapter gets the full Stage 2 treatment
(3 researched titles + comps + rough cut). Upload unlisted first (existing SOP rule).

## Stage 4 — Shorts (was: "scrub chapters, analyze trends, 3–5 shorts")

1. **Opus Clip** on the full recording → candidate list with scores
2. Merge with the Edit Map's keeper moments (Opus misses quiet-but-powerful moments —
   especially worship/testimony beats; the Edit Map catches them)
3. **Trend scrub:** check 1of10 outliers + what's currently running on our reference
   channels (Brand Guide list) — pick formats, not topics, to ride
4. Select **3–5**, split per the Onboarding SOP's two lanes:
   - **Repurpose shorts** — "moments from the show," reference the episode
   - **Native shorts** — standalone, re-engineered hook (Native Short prompt), these are
     the reach drivers
5. AI drafts per short: hook rewrite (Hook prompt), 3 caption options (Caption prompt),
   platform copy. Editor owns caption styling, pacing, and motion.
6. **Triage rule (the throughput unlock):** editor gives **full polish to the top 2** (best
   hook scores); remaining shorts ship with brand caption preset + QC only. Don't
   hand-animate all five.

## Stage 5 — Editor package (was: "compile all data and files")

One folder per pillar: `Flock Content/<Pipeline>/<YYYY-MM-DD>/PACKAGE/`

```
PACKAGE/
├── 00-BRIEF.md              ← creative brief (see template) — the first thing opened
├── 01-timelines/            ← Premiere project / Descript timeline export / Opus XML
├── 02-transcript-editmap/   ← full transcript + Edit Map + cut list
├── 03-packaging/
│   ├── titles.md            ← 3 per video, with the research receipts (1of10/vidIQ)
│   ├── thumb-comps/         ← AI concept comps, labeled CONCEPT — BEAT THIS
│   └── thumb-PSDs/          ← layered brand PSD templates (fonts/colors/safe areas locked)
├── 04-shorts/               ← per short: rough cut + hook rewrite + captions + platform copy
└── 05-references/           ← links: 2–3 reference videos for THIS package + Brand Guide
```

**PSD note (confirmed):** AI supplies **PNG mockups**; the editor designs the final layered
PSDs from them. The move is a **master PSD template per content type** (built once by the
editor, approved by TJ) with locked brand layers + swappable text/image layers. AI comps
show *what* to make; the PSD is *where* it gets made.

## Stage 6 — Handoff (was: "prepare and draft email")

- AI drafts the handoff email from `editor-handoff-email-template.md`, auto-filled from the
  Edit Map + package manifest. TJ (or the automation) sends it.
- Notion Content Calendar rows created for every deliverable in the package, status `In edit`,
  Drive links attached (existing SOP rules apply from here).
- Long-term: this email becomes an n8n notification and the package manifest is the source
  of truth; the email is just the doorbell.

## Stage 7 — Review loop (new — this is what makes creative freedom safe)

**Two gates, not continuous notes:**

- **Gate 1 — Direction check (24h after handoff):** editor sends ONE 60–90 sec Loom on the
  main video only: chosen title direction, thumbnail direction, grade mode, pacing intent.
  TJ replies with a voice note: green-light or redirect. *Cheap to change here.*
- **Gate 2 — Final QC (delivery):** existing QC checklist (Editor SOP §5). TJ reviews within
  2 business days. Two revision rounds included (existing policy).

**No notes between gates.** That's the deal that makes freedom real: the editor gets a
protected creative window, TJ gets two guaranteed steering moments.

**Earned autonomy ladder (Ralston principle — editor owns the channel end-to-end):**

| Level | When | What changes |
|---|---|---|
| 1 — Calibration | Packages 1–3 | Both gates + written rationale for choices |
| 2 — Trusted | Hit rate ≥ 80% at Gate 2 | Gate 1 optional; shorts skip TJ pre-approval |
| 3 — Owner | Consistent + analytics-literate | Editor schedules directly; TJ reviews *published* work weekly; approval by exception |

Level 3 requires amending the current "nothing posts without TJ approval" rule — see open
questions. Approval-on-everything is the #1 throughput cap in the current system.

---

## The weekly loop that improves the machine

Already built in Notion (Analytics Log, Mondays). Two additions:
1. Log **which AI-generated titles/hooks won** — the prompt library gets edited based on
   what the audience actually clicked. The prompts are living documents.
2. Log **retention delta between polished and preset-only shorts.** If preset-only shorts
   retain equally well, polish budget moves to long-form. This is the Hormozi
   "simplification test" run on our own data instead of trusting the internet.

## Known inconsistencies to resolve (v1 docs)

- Two editor SOPs exist in Notion (📹 Editor SOP under Strategy Hub vs 📋 Editor Onboarding
  & SOP under Flock Content System) with conflicting turnarounds and output counts → merge
  into one, keep the other as a redirect stub.
- Onboarding SOP says **Buffer** for scheduling; this repo's system is built on **GHL Social
  Planner** → pick one (GHL, presumably) and update the SOP.
- Gmail/vidIQ password is in plain text in the Brand Guide → move to a password manager,
  rotate the password, share via manager with the editor.
