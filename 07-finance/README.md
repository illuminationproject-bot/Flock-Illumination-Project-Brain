# 07 — Finance: Nashville First receipt reconciliation

Monthly loop for reconciling **work receipts against the card/bank statement**
for TJ's job at Nashville First. Both receipts and statements arrive in the
work **Outlook** mailbox.

## One-time setup

Connect the **Microsoft 365** connector on claude.ai (Settings → Connectors →
Microsoft 365) with the Nashville First work account, and enable it for the
chat. Without it the agent has no way to read Outlook and will stop and say so.

## How to run it

1. Make sure the month's statement is findable: either it's an email in
   Outlook (the agent will search for it) or you drop a downloaded copy in
   `statements/` named like `2026-06-statement.pdf` / `.csv` / `.xlsx`.
2. Run **`/reconcile 2026-06`** (or just ask: "reconcile June").
3. Read `reconciliations/2026-06.md` and work the "missing receipts" action
   list.

If no statement is found, the agent still runs in **prep mode**: it
inventories the month's receipt emails and flags issues — it just can't do
the final statement match yet.

## What the agent does

- Searches Outlook for the month's receipts, invoices, and order
  confirmations (including PDF attachments and forwarded receipts).
- Finds the statement (statement email in Outlook, or a file in
  `statements/`).
- Matches each statement transaction to a receipt (exact amount, date within
  ~3 days, normalized vendor descriptors — the descriptor table lives in the
  agent file and grows with each run).
- Writes `reconciliations/YYYY-MM.md`: matched table, missing-receipt action
  list, unmatched receipts, and ⚠ flags.
- **Strictly read-only in Outlook** — it never sends, forwards, deletes, or
  moves anything in the work mailbox.

Full procedure: `.claude/agents/receipt-reconciler.md`.

## Folder layout

```
07-finance/
  statements/         Optional drop zone for downloaded statements (YYYY-MM-*)
  reconciliations/    Agent output: one report per month (YYYY-MM.md)
```
