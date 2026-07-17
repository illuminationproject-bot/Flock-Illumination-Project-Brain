# Flock / Illumination Project — Content & Marketing Brain

This repo is the operating system for social content and marketing across two brands:

| Brand | Role | Channels |
|---|---|---|
| **The Illumination Project** | Artist brand — music, message, performance | YouTube, YouTube Shorts, Instagram (feed, reels, stories) |
| **Flock** | Community brand — the movement, member content, funnel into Skool | YouTube, YouTube Shorts, Instagram (feed, reels, stories) |

## Folder map

```
01-calendar/        Master content calendar, weekly posting schedule, GHL bulk-upload CSV template
02-ghl/             GoHighLevel Social Planner setup + content approval workflow
03-marketing/       GHL + Skool integrated marketing system (funnels, automations, nurture)
04-analytics/       Weekly analytics report template + KPI definitions
05-ideas/           Content pillars + daily content ideas (3/day, logged by date)
06-pipeline/        Footage bank (Drive + iCloud archive) and GHL API publishing setup
07-finance/         Receipt ↔ Relay statement reconciliation (run /reconcile)
scripts/            ghl_publish.py — schedules posts through the GHL API
```

## The weekly rhythm

| Day | What happens |
|---|---|
| **Sunday** | Batch approval: next week's content delivered for review (captions, cuts, graphics) |
| **Monday** | Approved content loaded/scheduled in GHL Social Planner; weekly analytics report reviewed |
| **Daily** | 3 stories, 1–2 reels/shorts per brand, 1 feed post/carousel go out on schedule; 3 new content ideas logged in `05-ideas/` |
| **Tue + Fri** | Long-form YouTube uploads (8+ min) |

## Daily deliverable slots (per brand)

- 3 × Instagram stories
- 1–2 × Instagram reels / YouTube Shorts (same asset, platform-adapted)
- 1 × feed post or carousel (image/graphic)
- 1–2 × full YouTube videos (8+ min) **per week**

Start with `01-calendar/master-plan.md`.
