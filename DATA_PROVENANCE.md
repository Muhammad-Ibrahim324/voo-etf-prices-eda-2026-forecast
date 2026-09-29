# VOO data provenance

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
