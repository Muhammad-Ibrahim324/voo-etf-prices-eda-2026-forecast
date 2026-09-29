# Historical data dictionary

| Column | Short description | Type | Meaning / unit |
|---|---|---|---|
| `date` | Trading session date | Date | YYYY-MM-DD; U.S. exchange session label |
| `ticker` | Fund ticker symbol | String | Always VOO |
| `open` | Session opening price | Float | USD, supplied source scale |
| `high` | Session highest price | Float | USD, supplied source scale |
| `low` | Session lowest price | Float | USD, supplied source scale |
| `close` | Session closing price | Float | USD, supplied source scale |
| `volume` | Daily shares traded | Integer | Shares; nonnegative |

All prices are USD on the uploaded source scale. Adjustment settings are unverified.
