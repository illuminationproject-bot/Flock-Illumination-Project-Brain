# Integrated Marketing System — GHL + Skool

Content is the top of the funnel. GHL is the middle (capture, nurture, track). Skool (the Flock community) is the destination and monetization layer.

## The funnel

```
Reels/Shorts/YT (reach)
        │  CTA: "join the Flock" / DM keyword / link in bio
        ▼
GHL landing page (flock link-in-bio + opt-in)
        │  captures name/email/phone → contact + tags in GHL
        ▼
Skool community (free tier) ── engagement, classroom content, calls
        │  nurture via GHL email/SMS
        ▼
Paid layer (paid Skool tier / offer / music+merch/events)
```

## Build list in GHL

### 1. Link-in-bio funnel page
- One GHL page for each brand's bio link. Buttons: Join the Flock (Skool), Latest release, Latest YouTube video, email opt-in (free lead magnet — e.g., unreleased track, meditation/track pack, or mini-course lesson).
- Every button click is tracked; opt-in creates a contact tagged by source (`src:ig-ip`, `src:ig-flock`, `src:yt`).

### 2. DM keyword automations
- IG automation: comment/DM keyword (e.g., **"FLOCK"**) → auto-DM with the Skool invite link → contact created in GHL with tag `kw:flock`.
- Use one keyword per campaign so attribution stays clean (e.g., "LIGHT" for a release, "FLOCK" for community).
- Every reel CTA should use either the keyword or link-in-bio — never a dead-end.

### 3. Pipelines
- **Community pipeline:** New lead → Invited to Skool → Joined Skool → Active (7-day) → Paid.
- Move stages via workflow triggers: form submitted, link clicked, tag added. Skool join detection: Skool → Zapier/Make webhook → GHL inbound webhook adds tag `skool:joined` (Skool has no native GHL integration; this is the standard bridge).

### 4. Nurture sequences (GHL workflows)
- **New lead (Day 0–7):** welcome email w/ Skool link → story email (why the project exists) → best-of content email → invite to next community call → SMS nudge if unopened.
- **Joined Skool:** onboarding email (how to get value in 10 min) → check-in at day 3 → ascension invite at day 14 (paid tier/offer).
- **Cold re-engagement (30 days inactive):** best 3 pieces of content that month + one clear CTA.

### 5. Weekly newsletter
- One GHL email broadcast per week (send Thu or Sun): this week's drop, one teaching, one community win, one CTA. Pulls directly from the week's content — zero extra writing.

## Skool side

- **Free tier = Flock.** Classroom holds the deeper teaching content that reels tease ("full breakdown inside the Flock").
- Weekly community call or live listening session — promoted by Wednesday/Saturday Flock content slots.
- Skool posts get repurposed *back* into social: member wins → Wednesday spotlight content; hot discussion threads → reel topics.

## Attribution loop

Because every entry point is tagged (`src:*`, `kw:*`), the weekly report can answer: which platform, which content pillar, and which CTA style actually fills the Flock. Double down accordingly.
