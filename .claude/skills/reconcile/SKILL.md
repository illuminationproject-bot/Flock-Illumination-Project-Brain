---
name: reconcile
description: Reconcile receipts against the Relay bank statement for a given month (defaults to last month). Usage - /reconcile 2026-06
---

Run a receipt/statement reconciliation for CELLADOOR LLC.

1. Determine the target month: use the argument if given (`YYYY-MM`),
   otherwise the most recent complete calendar month.
2. Launch the `receipt-reconciler` agent (Agent tool,
   `subagent_type: receipt-reconciler`) with the target month. That agent
   definition (`.claude/agents/receipt-reconciler.md`) holds the full
   procedure: statement lookup, Gmail receipt sweep, matching rules, report
   format, and labeling.
3. When it finishes, relay the summary to the user: matched count, missing
   receipts (the action list), income total, and any ⚠ flags — especially
   failed/retrying payments.
4. Commit and push the report if the agent didn't already.

If no statement file exists for the month, the report will be in "prep mode" —
remind the user to export the month's statement from Relay
(Accounts → Statements) and drop it in `07-finance/statements/` (CSV
preferred), then re-run `/reconcile`.
