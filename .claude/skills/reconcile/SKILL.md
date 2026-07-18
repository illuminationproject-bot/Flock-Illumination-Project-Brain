---
name: reconcile
description: Reconcile Nashville First work receipts against the card/bank statement for a given month (defaults to last month). Receipts and statements live in Outlook. Usage - /reconcile 2026-06
---

Run a receipt/statement reconciliation for TJ's Nashville First job.

1. Determine the target month: use the argument if given (`YYYY-MM`),
   otherwise the most recent complete calendar month.
2. Check that Microsoft 365 / Outlook tools are available (ToolSearch for
   `outlook email`). If they aren't, stop and tell the user to connect the
   **Microsoft 365** connector on claude.ai and enable it for this chat —
   there is nothing useful to do without mailbox access.
3. Launch the `receipt-reconciler` agent (Agent tool,
   `subagent_type: receipt-reconciler`) with the target month. The agent
   definition (`.claude/agents/receipt-reconciler.md`) holds the full
   procedure: statement lookup, Outlook receipt sweep, matching rules, and
   report format.
4. Relay the summary to the user: matched count, missing receipts (the
   action list), and any ⚠ flags.
5. Commit and push the report if the agent didn't already.

If no statement was found in Outlook or `07-finance/statements/`, the report
is in "prep mode" — remind the user to save the month's statement into
`07-finance/statements/` (or point out the statement email), then re-run
`/reconcile`.
