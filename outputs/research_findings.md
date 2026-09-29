# VOO research findings

Author: Muhammad Ibrahim Shahrukh

## Historical evidence
- 4,037 daily observations, 2010-09-09 through 2026-09-28.
- Latest supplied close: $703.61. This is the source scale; adjustment status is unverified.
- Supplied-series annualized growth: 14.86%; annualized log-return volatility: 17.00%.
- Largest peak-to-trough drawdown: -33.99%, from 2020-02-19 to 2020-03-23.
- Daily return skewness: -0.38; excess kurtosis: 13.59. Large shocks make averages an incomplete risk summary.

## Model evidence
- Validation winner: **Ridge**; best machine-learning candidate: **Ridge**.
- Four fixed-origin 66-session validation folds precede one untouched 66-session test.
- Selected-model test MAE: $16.29; RMSE: $18.62; MAPE: 2.33%.
- The selected model **outperformed** last-close on test MAE; skill: 30.83%.
- The lowest test MAE belongs to **Log drift (252)** ($8.10), which may differ from the validation winner. The final model is deliberately not reselected using this test. A weaker result than a trend baseline limits the evidence for a stable machine-learning advantage.
- Test-path scenario coverage: 100.0% for the nominal 80% band and 100.0% for the nominal 95% band. One path does not establish calibration.

## 2026 projection
- 66 scheduled sessions, 2026-09-29–2026-12-31.
- Selected year-end path value: **$731.34** (+3.94% versus the last supplied close).
- Year-end central 80% simulation range: **$657.48–$809.40**.
- This path describes a fitted statistical scenario. A smooth or rising curve is not evidence that daily prices will behave that way.

## Interpretation and next research steps
Long-run growth coexists with sharp drawdowns. Recent trends can persist, stall or reverse; historical OHLCV alone cannot distinguish those cases reliably. Earnings expectations, interest rates, index composition and market shocks can affect future prices, but none is measured by this model. They are possible drivers, not claims about the current economy.

The test verdict above takes priority over a visually appealing forecast. Four validation origins and one recent test provide limited regime coverage. Overlapping training targets and correlated horizon errors reduce the effective sample size. Expand the origin set across market regimes before drawing strong performance conclusions. Test additional model families and hyperparameters in a new nested validation design, not by repeatedly optimizing this test.

Verify adjustment flags and corporate actions, retain point-in-time snapshots, and add explicitly timestamped exogenous features if available. The present backtest uses one historical export: past adjusted values may have been revised after their original dates. Thus feature/target timing is protected within this snapshot, but full point-in-time data integrity is not established. There is no transaction-cost backtest, no portfolio optimization and no claimed trading edge.

Forecast and historical tables are separate. Scenario bands omit parameter uncertainty and structural breaks. Educational research only; no promised returns.
