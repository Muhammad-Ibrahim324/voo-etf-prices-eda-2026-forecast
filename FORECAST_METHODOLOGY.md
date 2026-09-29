# Forecast methodology and output dictionary

Author: Muhammad Ibrahim Shahrukh

## Fixed-origin experiment

- H is the count of scheduled exchange sessions after the last observed date through December 31, 2026.
- At each origin t, features use information through the close at t. A model issues the complete H-session path at once.
- Targets are `Y[t,h] = log(close[t+h] / close[t])`. Direct multi-output prediction avoids needing future actual volume or recursively fabricated OHLC values.
- The last H observations form the final test; the four immediately preceding H-session blocks are validation targets.
- Each validation model uses expanding history, with target embargo enforced by `training_origin + H <= forecast_origin`. Labels that cross into the forecast period are excluded.
- All preprocessing is fitted only on the training rows. No random time split is used. Feature definitions and hyperparameters are fixed before test evaluation.
- Choose the lowest mean validation NMAE across four folds, lock that model, then report all frozen candidates on the test. The selected model is not changed because another candidate wins on the test.
- Refit the selected model and best validation ML candidate with all labels observable at the last supplied close. No later market data are used.

## Candidate models

| Model | Fixed configuration |
|---|---|
| Last close | Constant path equal to origin close |
| Log drift (252) | Mean trailing 252 daily log changes, extrapolated by horizon |
| Ridge | StandardScaler fitted on training; alpha=100; multi-output |
| Random Forest | 140 trees; depth 8; leaf minimum 15; feature fraction 0.8; seed 42 |
| Extra Trees | 180 trees; depth 10; leaf minimum 12; feature fraction 0.9; seed 42 |

This is a constrained benchmark, not an exhaustive search over every model. A baseline may win. Neural networks or more complex boosting models are not automatically superior for a small single-series forecasting task.

## Metrics

| Metric | Meaning |
|---|---|
| MAE_USD | Mean absolute actual-minus-predicted price error |
| RMSE_USD | Square root of mean squared price error |
| MAPE_pct | Mean absolute error divided by actual price × 100 |
| NMAE_pct | MAE divided by origin price × 100; validation selection criterion |
| MASE_daily_scale | MAE divided by in-sample mean absolute one-day price change |
| R2 | 1 − prediction SSE / actual centered SSE; may be negative |
| skill_vs_last_close_pct | 100 × (1 − model MAE / same-origin last-close MAE) |
| origin_direction_accuracy_pct | Fraction of horizons whose sign relative to origin matches actual |

Direction is measured relative to the fixed origin, not day by day. The H endpoints overlap economically and are correlated; they are not H independent trials. MASE uses a one-day denominator and should not be confused with the same-horizon skill measure.

## Scenario simulation

Take up to 1,260 log returns observable at the origin, subtract their sample mean, sample contiguous blocks of five returns with replacement, concatenate to H sessions, and accumulate them. Multiply the selected path by the exponentiated cumulative shocks. With seed 42 and 5,000 simulated paths, report pointwise quantiles 2.5%, 10%, 90% and 97.5%.

These are empirical shock scenarios centered in log space on the model path, not calibrated predictive distributions. The selected path is not claimed to equal the simulated arithmetic mean. Bands are pointwise, not simultaneous path-coverage bands. Drift, parameter, feature and regime uncertainty are absent. Historic test-path coverage is reported without tuning to that coverage; it is not evidence of reliable long-run calibration.

## Forecast CSV columns

| Column | Description |
|---|---|
| date | Scheduled future session date |
| ticker | Fund ticker symbol |
| horizon_sessions | Sessions after forecast origin |
| selected_model | Validation-selected model name |
| forecast_close | Selected source-scale price forecast |
| scenario_lower_80 | Tenth-percentile simulated price |
| scenario_upper_80 | Ninetieth-percentile simulated price |
| scenario_lower_95 | 2.5th-percentile simulated price |
| scenario_upper_95 | 97.5th-percentile simulated price |
| best_ml_model | Best validation ML candidate |
| best_ml_forecast_close | ML comparison price forecast |
| last_close_baseline | Constant last observed price |

Prices are USD on the supplied source scale. Simulated bands do not claim verified raw-price or total-return interpretation.

## Engineered features and EDA output

`outputs/voo_eda_features.csv` copies history plus daily simple return, log return, running drawdown, annualized 21- and 63-session log-return volatility, 50- and 200-session moving averages, and intraday range as percent of close. Leading missing values are expected where a prior observation or rolling window is unavailable. This derived file is not the clean historical upload.

Model features include lagged returns, 5/10/21/63/126/252-session momentum, rolling volatility and price-to-average ratios, current-session range and return, overnight gap, relative volume, rolling drawdown, and weekday sine/cosine. The notebook exports the exact feature names. Features with incomplete lookbacks are excluded from model fitting; no future-aware imputation is used.

## Reproducibility limits

These backtests protect feature and target timing within one supplied export. They cannot undo retrospective provider revisions. Long overlapping targets reduce effective training sample size. Four validation origins and one test period underrepresent market regimes. No formal significance claim, transaction-cost strategy evaluation or guaranteed ranking is made. For new claims, design additional validation before examining its test outcomes.
