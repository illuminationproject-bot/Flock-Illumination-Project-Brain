# Statement drop zone

Put Relay statement exports here. One file per account per month.

- **Where to get them**: Relay dashboard → Accounts → Statements → download.
- **Format**: CSV preferred (the agent parses it directly); PDF also works.
- **Naming**: `YYYY-MM-relay.csv` — add the account name if you export more
  than one, e.g. `2026-06-relay-income.csv`, `2026-06-relay-cogs-card.csv`.

The reconciliation agent reads whatever is here for the target month. If the
month's file is missing it runs in prep mode and reminds you to export it.
