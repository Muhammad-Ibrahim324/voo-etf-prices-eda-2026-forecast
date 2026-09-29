"""Normalize the supplied yfinance export; never download or fill market prices."""
from pathlib import Path
import hashlib
import json
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / 'data/raw/voo.csv'
raw = pd.read_csv(source, dtype=str)
assert raw.columns.tolist() == ['Price', 'Close', 'High', 'Low', 'Open', 'Volume']
assert raw.iloc[0].tolist() == ['Ticker', 'VOO', 'VOO', 'VOO', 'VOO', 'VOO']
assert raw.iloc[1, 0] == 'Date' and raw.iloc[1, 1:].isna().all()
d = raw.iloc[2:].copy().rename(columns={'Price': 'date', 'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'})
d['date'] = pd.to_datetime(d.date, format='%Y-%m-%d', errors='raise')
for col in ['open', 'high', 'low', 'close', 'volume']:
    d[col] = pd.to_numeric(d[col], errors='raise')
assert np.isfinite(d[['open', 'high', 'low', 'close', 'volume']]).all().all()
exact_duplicates = int(d.duplicated().sum())
d = d.drop_duplicates()
assert not d.date.duplicated().any(), 'Conflicting dates require manual investigation.'
assert (d[['open', 'high', 'low', 'close']] > 0).all().all()
assert (d.volume >= 0).all() and (d.volume % 1 == 0).all()
assert (d.high >= d[['open', 'close', 'low']].max(axis=1) - 1e-8).all()
assert (d.low <= d[['open', 'close', 'high']].min(axis=1) + 1e-8).all()
d = d.sort_values('date').reset_index(drop=True)
d.insert(1, 'ticker', 'VOO')
d = d[['date', 'ticker', 'open', 'high', 'low', 'close', 'volume']]
d['volume'] = d.volume.astype('int64')
d[['open', 'high', 'low', 'close']] = d[['open', 'high', 'low', 'close']].round(6)
target = ROOT / 'voo_daily_clean.csv'
d.to_csv(target, index=False, date_format='%Y-%m-%d', float_format='%.6f')
audit = {'source': 'User-supplied Yahoo Finance export via yfinance (user attribution)',
         'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
         'clean_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
         'raw_lines_after_csv_header': len(raw), 'metadata_rows_removed': 2,
         'exact_duplicate_rows_removed': exact_duplicates, 'observations': len(d),
         'first_date': str(d.date.min().date()), 'last_date': str(d.date.max().date()),
         'missing_values': int(d.isna().sum().sum()), 'price_decimals': 6,
         'latest_close': float(d.close.iloc[-1]), 'zero_volume_rows': int((d.volume == 0).sum()),
         'adjustment_status': 'Unverified; original auto_adjust/back_adjust settings unavailable',
         'collection_timestamp': 'Not supplied', 'preparation_date': '2026-09-29'}
(ROOT / 'outputs/cleaning_audit.json').write_text(json.dumps(audit, indent=2))
print(json.dumps(audit, indent=2))
