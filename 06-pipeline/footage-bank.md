# Footage Bank & Asset Pipeline

## Source locations (provided by owner, 2026-07-04)

- **Google Drive content dump folder:** https://drive.google.com/drive/folders/1yA-_XBl0QW20J1R0pgRvK3SrVyLe-fUM (folder ID `1yA-_XBl0QW20J1R0pgRvK3SrVyLe-fUM`)
- **iCloud archive (all footage ever):**
  - VIDEO: https://www.icloud.com/iclouddrive/0eb_iPGDJ4Vyq9q8DUyZ62ZAg#VIDEO
  - https://www.icloud.com/iclouddrive/08bDP4DoaE9d_Sxa1YnP8HBug
  - https://www.icloud.com/iclouddrive/073KD3sfxjFEGjy1NBMCZVLrQ

> Access status (2026-07-04): network policy opened — Drive pulls **working**
> (see `drive-inventory.md`). iCloud links resolve but are set to
> "Only invited people" (`publicPermission: NONE`); owner must switch each
> share to **"Anyone with the link"** before pulls work.
> GHL API host reachable; awaiting `GHL_PI_TOKEN` + `GHL_LOCATION_ID`
> environment variables.

Three storage layers feed the content machine:

```
iCloud (deep archive — all footage ever)
   └─ curated pulls ──► Google Drive /Flock-IP-Content/ (working library — what I can access directly)
                              └─ finished assets ──► GHL Media Library (what gets published, via API)
```

## Google Drive — working library structure

```
/Flock-IP-Content/
├── 00-inbox/              ← drop anything new here; I sort it
├── 01-raw/
│   ├── performances/
│   ├── studio/
│   ├── talking-head/
│   └── b-roll/
├── 02-archive-pulls/      ← footage pulled from the iCloud bank for remixing
├── 03-edits-in-progress/
├── 04-for-review/         ← my finished cuts land here (Sunday approval batch)
│   └── Week-of-YYYY-MM-DD/
├── 05-approved/           ← you move/mark approved items here; these get scheduled
│   └── Week-of-YYYY-MM-DD/
├── 06-published/          ← archived after posting, named with post date + platform
└── evergreen/             ← approved re-runnable content (backup library)
```

Naming convention for finished assets: `YYYY-MM-DD_BRAND_SLOT_hook-slug.mp4`
(e.g. `2026-07-10_IP_reel1_voice-memo-to-final.mp4`) — date and slot match the GHL publish queue CSV.

## iCloud — the deep archive

iCloud has no API I can call directly, so it works as the cold-storage bank with two bridge options:

1. **Shared-link pulls (lightweight, per-request):** create an iCloud shared folder link for a batch of footage ("2019 live shows", "old studio sessions") and send me the link. I attempt direct download from the share link; anything that won't download cleanly, drop into Drive `00-inbox/` instead.
2. **Standing sync (recommended, set up once):** on a Mac, mirror chosen iCloud folders into the Drive working library automatically — either Google Drive for desktop syncing a folder that lives inside iCloud Drive, or `rclone` on a schedule (`rclone sync ~/Library/Mobile\ Documents/... gdrive:Flock-IP-Content/02-archive-pulls/`). After that, "give me everything from X era" is just a folder move on your phone/Mac.

### How the bank gets used for trending formats

When a trending format fits an old clip, I pull from `02-archive-pulls/`, recut to the format (9:16 crop, hook text, trending structure), and it enters the normal approval flow. The daily idea log flags these as `Format remix — needs archive pull: {what to look for}` so you know exactly which old footage to surface when I can't find it in Drive.

## What I do in this pipeline

- Sort `00-inbox/`, pull and process raw video with ffmpeg (cut shorts from long-form, 16:9→9:16 crops, trims, caption burn-in, thumbnails, quote graphics, carousel slides)
- Deliver finished, named assets + copy doc to `04-for-review/Week-of-.../`
- After approval: upload media to GHL and schedule posts via the API (see `ghl-api-publishing.md`)
- Archive published assets and keep `evergreen/` stocked
