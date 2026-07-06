# Monthly Close Agent (CFO-level) — Playbook

**What it is:** a scheduled AI agent (Claude Code routine, runs the 2nd of each month) that
executes the Notion prompt "Monthly Close Summary (CFO-level)" from the Prompt Repository —
without TJ having to paste anything.

## What the agent does each run

1. **Gather inputs** for the month that just ended: search Gmail and Google Drive for the
   P&L, bank/QuickBooks exports, Stripe/PayPal payout summaries, invoices
   (queries like "profit and loss", "P&L", "statement <Month>", "payout").
2. **Produce the CFO summary** per the prompt spec (no fluff, plain language, flag anomalies):
   1. Revenue summary (by stream — music, Flock/Skool, Asaph cohort, shows, other)
   2. Expense summary (top categories)
   3. Cash position (start → end)
   4. Unexpected / unusual items to review
   5. 3 recommendations for next month
3. **Publish:** create a Notion page `💰 Monthly Close — <Month YYYY>` under the AI
   Automation Hub page, and draft (never auto-send) a Gmail email to TJ with the summary.
4. **If the data can't be found:** still create the page — listing exactly what was searched
   and what's missing — and draft an email to TJ asking for the P&L. Silence is not an
   acceptable failure mode.

## Data hygiene rules

- Financial figures are stated with their source ("per QuickBooks P&L export, Drive file X").
- Anything estimated or inferred is labeled as such.
- The agent never moves money, never replies to vendors, never sends email — drafts only.
