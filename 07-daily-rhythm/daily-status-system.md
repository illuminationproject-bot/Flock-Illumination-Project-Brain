# Daily Status System — 8am / 1pm / 8pm

An automated three-touch daily cadence, delivered by Claude, built on the Hormozi
day-design principles in `hormozi-traffic-blocks-and-day-design.md`. Source of
truth for tasks is **Asana → FLOCK/IP** project (see `asana-snapshot-2026-07-04.md`).

## The three touches

### ☀️ 8:00 AM — Morning status + Big 3
- Pull today's due + overdue tasks from Asana FLOCK/IP.
- Note where the Creator Games launch stands (which send is due, which Skool post).
- Output the **Big 3**: the three highest-leverage things for the day.
  - Tag each **Build / Promote / Deliver** (Hormozi 4/4/4).
  - At least one is always a **Promote** (traffic) item.
  - If a 🏆 CG send is due today, it is almost always Big-3 #1.
- Name the **morning maker block** to protect (peak hours).

### 🕐 1:00 PM — Midday checkpoint
- What of the Big 3 is done / not done.
- Reset the afternoon **traffic block**: the one Promote thing that still must ship.
- Flag anything time-sensitive (a launch send, a Skool post not yet posted).

### 🌙 8:00 PM — Evening sprint + late-night stretch
- **Evening sprint:** one concrete, finishable block for tonight (a maker task).
- **Late-night project (if energy allows):** a stretch/deep item to reach for only
  if there's gas left — never an obligation. Usually pulled from the Product Backlog
  (course build-out, templates) since those don't have hard dates.

## Big 3 rules
1. Exactly three. If everything is a priority, nothing is.
2. ≥1 Promote/traffic item, every day.
3. Hard-dated launch sends outrank undated backlog work.
4. Overdue > due-today > upcoming.

## Delivery
Delivered as durable scheduled triggers (Claude Code Remote) — each firing spins
up a fresh session, re-reads Asana + this repo, and sends the update via push +
email. Times are in **America/Chicago (Central)**.

| Trigger | Local time | Cron (CT) |
|---|---|---|
| Morning status + Big 3 | 8:00 AM | `3 8 * * *` |
| Midday checkpoint | 1:00 PM | `7 13 * * *` |
| Evening sprint + late-night | 8:00 PM | `2 20 * * *` |

> Minutes are nudged off :00 on purpose (scheduler hygiene). To change times or
> pause, ask Claude to update/delete the triggers.
