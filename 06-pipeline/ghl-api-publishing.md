# GHL API Publishing Setup

Once configured, scheduling/publishing happens through GHL's API via `scripts/ghl_publish.py` — no manual clicking in Social Planner.

## One-time setup (you do this once, ~5 minutes)

### 1. Create a Private Integration token in GHL

1. In your **sub-account** (location): **Settings → Private Integrations → Create new integration**
2. Name it `Claude Content Manager`
3. Grant scopes: **Social Planner posts** (`social_media_posting.write` / `.readonly`), **Medias** (`medias.write` / `.readonly`)
4. Copy the token (starts with `pit-…`)

### 2. Find your Location ID

Settings → Business Profile → copy the Location ID (or it's visible in the sub-account URL).

### 3. Store both as environment secrets (NOT pasted in chat)

In the Claude Code environment settings for this repo's environment, add:

```
GHL_PI_TOKEN=pit-xxxxxxxx
GHL_LOCATION_ID=xxxxxxxx
```

Secrets in environment variables stay out of the repo and out of the conversation. Never commit them.

### 4. Verify

Ask me to run `python3 scripts/ghl_publish.py --check`. It lists the social accounts GHL sees (both IGs, both YouTube channels). If those appear, publishing is live.

## How weekly publishing runs after setup

1. You approve the Sunday batch (assets in Drive `05-approved/`, copy doc finalized).
2. I fill `01-calendar/publish-queue.csv` — one row per post: datetime, brand, platform account(s), caption, media file.
3. I run `scripts/ghl_publish.py --queue 01-calendar/publish-queue.csv`, which for each row:
   - downloads the asset from Drive,
   - uploads it to the GHL media library,
   - creates the post via the Social Planner API with status **scheduled** at the target time.
4. The script prints a report of every post it scheduled (and anything that failed) — that report gets committed to `06-pipeline/publish-logs/`.

## Known limits

- **IG stories with interactive stickers**: API-published stories can't carry polls/question boxes/sliders. Visual-only stories go through the API; sticker stories stay a 60-second manual job on your phone (usually just the PM slot).
- **Long-form YouTube**: keep uploading natively in YouTube Studio for thumbnails/chapters/premieres. The API handles Shorts and all IG surfaces.
- GHL occasionally versions its API. The script pins API version `2021-07-28`; if GHL changes Social Planner endpoints, the `--check` command will surface it immediately and I'll patch the script.
