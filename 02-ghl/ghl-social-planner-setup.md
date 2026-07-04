# GHL Social Planner — Setup & Publishing

How scheduling and publishing runs through GoHighLevel for both brands.

## 1. Connect the channels (Marketing → Social Planner → Settings)

| Channel | How | Notes |
|---|---|---|
| Instagram — Illumination Project | Connect via the linked **Facebook Business Page** (IG must be a Business/Creator account) | Enables feed, reels, and stories publishing |
| Instagram — Flock | Same, via Flock's FB page | Keep both connected in the same sub-account |
| YouTube — Illumination Project | Connect Google account, pick the channel | Shorts publish as regular video uploads ≤3 min in 9:16 — GHL/YouTube auto-classifies them as Shorts |
| YouTube — Flock | Same | |

**Story caveat:** Instagram's API supports scheduled story publishing for Business accounts, but interactive stickers (polls, question boxes, sliders) can't be added via API. Plan: schedule the 3 daily story *visuals* through GHL, and add stickers manually when a story needs one (the PM slot usually does). Alternatively use GHL's mobile-notification flow for sticker stories.

## 2. Organize inside Social Planner

- **Categories/tags:** create one per pillar (`music`, `teaching`, `bts`, `flock`, `story`, `invite`) so the calendar view shows the mix at a glance and analytics can be sliced by pillar.
- **Hashtag snippets:** save 3–4 hashtag sets as reusable snippets (music niche, community niche, teaching niche) instead of retyping.
- **Recurring posts:** set recurring story slots (8:00 / 12:30 / 19:30) so empty slots are visible ahead of time.

## 3. Scheduling workflow (weekly, Mondays)

1. All approved assets live in the shared Drive folder (`/Content/Week-of-YYYY-MM-DD/approved`).
2. Bulk-load text posts + schedule via **CSV upload** (Social Planner → New Post → Upload from CSV). Use `../01-calendar/ghl-bulk-upload-template.csv` — keep columns matched to GHL's current sample CSV (download theirs once and mirror it; they occasionally change headers).
3. Video posts (reels/shorts) are scheduled individually — CSV upload doesn't attach video reliably; budget ~30 min to slot the week's videos.
4. Everything is scheduled with status **Scheduled**, *except* anything not yet approved, which stays **Draft**.
5. Long-form YouTube: upload natively in YouTube Studio (better control over thumbnail, chapters, end screens, premiere), not through GHL. GHL handles the promotion posts around it.

## 4. What GHL is used for beyond publishing

- **Unified calendar view** across both brands and all platforms — this is the single source of truth for what goes out when.
- **Approval statuses** — drafts vs. scheduled (see `approval-workflow.md`).
- **Automations** — DM keyword → workflow → Skool invite (see `../03-marketing/ghl-skool-system.md`).
- **Reporting** — Social Planner statistics feed the weekly report (see `../04-analytics/weekly-report-template.md`).
