# 07 — Finance: receipt ↔ statement reconciliation

Monthly bookkeeping loop for **CELLADOOR LLC** (The Illumination Project + Flock).
The goal: every transaction on the Relay bank statement has a receipt attached,
and anything weird gets flagged before it becomes a problem.

## How to run it

1. **Export the statement** from Relay: Accounts → Statements → pick the month
   → download **CSV** (PDF works too). Do this for each account/card you use.
2. **Drop the file(s)** in `statements/`, named like `2026-06-relay.csv`
   (see `statements/README.md`).
3. **Run `/reconcile 2026-06`** in Claude Code (or just ask: "reconcile June").
4. **Read the report** in `reconciliations/2026-06.md` and work the
   "missing receipts" action list — usually: find the receipt email and
   forward it into Relay, or download it from the vendor's billing portal.

If you skip step 1–2, the agent still runs in **prep mode**: it inventories the
month's receipt emails and Relay activity notifications, and flags issues — it
just can't do the final statement match until a statement file exists.

## What the agent does

- Sweeps Gmail for the month's receipts/invoices (Notion, Google Workspace,
  Meta Ads, GoDaddy, Stripe/ManyChat, Indepreneur, …) and Relay notifications
  (ACH deposits, receipt requests, failed payments).
- Matches each statement transaction to a receipt (exact amount, date within
  3 days, normalized vendor names).
- Writes `reconciliations/YYYY-MM.md`: matched table, missing-receipt action
  list, unmatched receipts, income summary, and ⚠ flags.
- Labels matched receipt emails with Gmail label **"Files/ Receipts/Proofs"**
  so the label becomes your receipt archive.
- It never sends email, never deletes anything, and never touches your money —
  read-only everywhere except that one label.

The full agent procedure lives in `.claude/agents/receipt-reconciler.md`
(including the vendor-descriptor table — add new vendors there as they appear).

## Folder layout

```
07-finance/
  statements/         Drop Relay statement exports here (YYYY-MM-relay.csv)
  reconciliations/    Agent output: one report per month (YYYY-MM.md)
```
