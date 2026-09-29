# VOO ETF Historical Prices 2010–2026

**Author:** Muhammad Ibrahim Shahrukh

## Kaggle listing — copy-ready metadata

**Title (35 characters):** VOO ETF Historical Prices 2010–2026

**Subtitle (71 characters):** Vanguard S&P 500 ETF data with EDA, risk analysis and 2026 ML forecasts

**Suggested notebook title:** VOO ETF: EDA & 2026 ML Price Forecasts

**Suggested dataset slug:** `voo-etf-historical-prices-2010-2026`

**Suggested tags:** Finance, Time Series, Investing, Data Visualization, Regression, ETFs

## Dataset description

Explore 4,037 daily observations of the Vanguard S&P 500 ETF (VOO), spanning September 9, 2010 through September 28, 2026. This beginner-friendly dataset turns a user-supplied Yahoo Finance/yfinance export into one tidy CSV with a single header, readable column names, chronological dates, daily OHLC prices and trading volume.

Use it to practice pandas, visualize long-term price changes, calculate returns and drawdowns, examine volatility and monthly patterns, and build time-series forecasting experiments. VOO is an ETF tracking the S&P 500; this file contains ETF observations, not S&P 500 index levels.

The companion notebook combines colorful Plotly dashboards with static chart companions and clear explanations. It compares Ridge, Random Forest and Extra Trees with last-close and log-drift baselines using four time-ordered, fixed-origin validation folds and a separate final test. It projects the remaining scheduled 2026 sessions and reports dollar errors, relative errors, baseline skill and simulation-based uncertainty scenarios. Forecasts are kept in a separate file and never mixed into historical observations.

Prices retain the uploaded source basis and are rounded to six decimals. The original adjustment settings and download timestamp were not supplied, so prices are not labeled as verified unadjusted prices or verified total-return data. There are no missing cells, duplicate dates, nonpositive prices, zero-volume observations or invalid OHLC relationships in the cleaned snapshot. No market observations were imputed or removed as outliers.

Author: **Muhammad Ibrahim Shahrukh**. Intended for educational analysis and reproducible research; no guaranteed forecasts or investment returns.

## File description

`voo_daily_clean.csv` contains 4,037 chronologically ordered daily VOO observations from September 9, 2010 to September 28, 2026, with seven columns: date, ticker, open, high, low, close and volume. Dates use YYYY-MM-DD, price fields contain six decimal places on the supplied Yahoo Finance/yfinance source scale, and volume is an integer number of shares. The file has a single header and no missing values or duplicate dates. Adjustment status is unverified; the file contains historical observations only, with forecasts provided separately.

## Column descriptions

Each short description has one to five words.

| Column | Short description | Type | Meaning / unit |
|---|---|---|---|
| `date` | Trading session date | Date | YYYY-MM-DD; U.S. exchange session label |
| `ticker` | Fund ticker symbol | String | Always VOO |
| `open` | Session opening price | Float | USD, supplied source scale |
| `high` | Session highest price | Float | USD, supplied source scale |
| `low` | Session lowest price | Float | USD, supplied source scale |
| `close` | Session closing price | Float | USD, supplied source scale |
| `volume` | Daily shares traded | Integer | Shares; nonnegative |

## Beginner quick start

```python
import pandas as pd
df = pd.read_csv('voo_daily_clean.csv', parse_dates=['date'])
df = df.sort_values('date')
df['daily_return'] = df['close'].pct_change(fill_method=None)
df['drawdown'] = df['close'] / df['close'].cummax() - 1
print(df.head())
```

The first daily return is naturally missing because the file has no preceding observation. Weekends and exchange holidays are not missing price rows. Keep trading-session dates intact rather than filling every calendar day.

## Questions this dataset can answer

- What is VOO? An ETF designed to track the S&P 500, not the index itself.
- What does this file cover? Daily OHLCV observations from 2010-09-09 to 2026-09-28.
- Is the data adjusted? The original flags are unknown, so adjustment status is unverified.
- Are forecasts real observations? No. Only `voo_daily_clean.csv` is the clean historical dataset; `outputs/voo_forecast_2026.csv` contains modeled scenarios.
- Does a low error guarantee profits? No. Forecast evaluation does not establish a profitable trading strategy.

## Provenance and collection methodology

- **Underlying provider:** [Yahoo Finance — VOO historical data](https://finance.yahoo.com/quote/VOO/history/).
- **Acquisition tool reported by the user:** [yfinance](https://github.com/ranaroussi/yfinance), an unofficial Python interface to Yahoo Finance data.
- **Original input:** `data/raw/voo.csv`, supplied by the user. It has a `Price` header, a `Ticker` metadata row, a `Date` metadata row, and daily OHLCV observations.
- **Known context:** ticker VOO, daily observations, observed range 2010-09-09 to 2026-09-28. Fund identity: [Vanguard VOO](https://investor.vanguard.com/investment-products/etfs/profile/voo).
- **Unknown original settings:** collection timestamp, yfinance version, exact API call, start/end arguments, `auto_adjust`, `back_adjust`, `repair`, actions and pre/post-market settings. No original collection code was supplied. The structure is consistent with a daily multi-index export but does not prove those settings.
- **Preparation:** September 29, 2026. This project processes the uploaded snapshot offline; it does not fetch, extend or independently verify individual prices against Yahoo Finance.
- **Price-basis limitation:** adjusted-looking decimal values are insufficient to establish adjustment flags. No dividend/split reconstruction, adjustment reversal or total-return claim is made. Later provider revisions may change historical values.

### Exact transformations

1. Validate the expected six-column raw export and its two metadata rows.
2. Remove only those metadata rows; parse the date with `%Y-%m-%d` and numeric fields strictly.
3. Check finite values, positive OHLC, integer nonnegative volume, high/low bounds and date uniqueness.
4. Remove exact duplicated observations if any; fail on conflicting observations for a date. This snapshot contained zero duplicates.
5. Rename columns to lowercase and add `ticker=VOO` explicitly.
6. Sort ascending by date; order columns as date, ticker, open, high, low, close, volume.
7. Round prices to six decimal places (maximum rounding error approximately 0.0000005 USD); store volume as integers; export UTF-8 CSV without an index.
8. Compare observation dates with the XNYS calendar. No missing or unexpected full-day sessions were found. XNYS is used as the U.S. equity calendar proxy for NYSE Arca-listed VOO.
9. Save SHA-256 hashes and an audit log in `outputs/cleaning_audit.json`. Returns and features are calculated only inside the notebook and exported separately.

No interpolation, forward filling, winsorization, split correction, outlier deletion, new prices or synthetic observations enter the historical CSV.

### Refreshing responsibly

Archive each new raw snapshot separately. Record the UTC download timestamp, ticker, interval, exact yfinance version and every download argument. Explicitly choose adjustment flags rather than relying on package defaults; preserve corporate-action columns and raw/adjusted prices when available. The original command cannot be reconstructed with certainty. Re-run the cleaner only for a compatible raw schema, check provider revisions, and repeat all validation before replacing a published version. This notebook deliberately targets a snapshot ending during 2026; change the forecast end date and revisit validation if extending it to another year.

### Reuse and citation

The yfinance software license does not grant rights to the underlying Yahoo data. Its project documentation describes personal-use restrictions and points to Yahoo's terms. **No open-data redistribution license is asserted by this package.** Attribution is not a substitute for rights: review the applicable terms before public Kaggle or GitHub data publication. Code and original documentation also have no newly assigned license.

Suggested citation: Muhammad Ibrahim Shahrukh (2026), *VOO ETF Historical Prices 2010–2026*, user-supplied Yahoo Finance/yfinance snapshot through September 28, 2026. Add the final Kaggle URL or DOI after publication.

