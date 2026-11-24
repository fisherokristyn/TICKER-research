# Video 2 — Code walkthrough

**Target** 4:30. **Maximum** 5:00. Read **Say** only. Keep code at a readable zoom and jump directly to symbols.

**Before recording:** Open the Streamlit baseline and pin VS Code tabs in this order: `app.py`, `data_loader.py`, `mandate.py`, `compliance.py`, `strategies.py`, `backtest.py`, `metrics.py`, `tests/test_portfolios.py`, `tests/test_replay.py`, then `docs/validation-and-ai-use.md`. Pre-position the terminal at the test summary.

## 0:00–0:36 | Entry point and navigation

**Show** VS Code, [app.py](../app.py), the `st.sidebar` and `st.tabs` blocks. Switch to the browser long enough to point to the tabs, then return to VS Code.

**Say**

I'll follow the data from the dashboard through the backtest and back to the results. Streamlit is the entry point. The sidebar selects the market source, estimation window, and trading cost. The tabs separate the strategy rules, historical comparison, momentum signal, stress tests, and committee review. The app calls the shared replay code, so the interface and the saved validation use the same portfolio engine.

## 0:36–1:10 | Inputs and validation

**Show** [data_loader.py](../data_loader.py), `COLUMNS`, `validate_market_values`, and `load_market_snapshot`. Briefly show [market data card](../data/market-data-card.md).

**Say**

I use Local CSV for a repeatable demo. The snapshot contains daily data for VT, BND, and SHV. The loader checks the column names, duplicate ticker and date pairs, valid prices, and complete common NYSE sessions. A reported zero-volume BND observation is retained and flagged. Its adjusted price still enters returns, while that day's zero dollar volume enters the modeled liquidity input.

## 1:10–1:46 | Rules and allocations

**Show** [mandate.py](../mandate.py), editable inputs, then [compliance.py](../compliance.py), `mandate_checks`, `verdict`, and `largest_issuer`. Open [strategies.py](../strategies.py) at `BASELINES`.

**Say**

The original Lab Thirteen checker is still available. The app uses a separate compliance module that returns a status and evidence for each rule. A known failure takes precedence, and missing evidence remains unverified. Strategy A weights the three ETFs equally. Strategy B holds three percent cash and splits the balance sixty-forty between VT and BND. The benchmark holds VT and BND sixty-forty with no cash sleeve.

## 1:46–2:24 | Lagged signal and optimizer

**Show** In `strategies.py`, `decision_inputs`, then `risk_aware`. Use **Momentum signal → Strategy C latest decision** to show the observation, cutoff, and rebalance dates.

**Say**

For C, I compare twelve-month adjusted-price returns ending in November. The trailing covariance uses monthly returns through that same observation month. The decision cuts off at the last December close, and the replay uses the first January close for execution. The signal shifts the equity band, and the optimizer minimizes variance within that band and other available numerical bounds. If they don't intersect, the replay records a blocked trade. The date checks limit look-ahead, though the downloaded data aren't archived as originally published.

## 2:24–3:13 | Replay, costs, and turnover

**Show** [backtest.py](../backtest.py), `walk_forward`, first at decision construction and then at `marked`, `measured_turnover`, and `numerical_failure`. Switch to `one_way` and `rebalance` in `compliance.py`.

**Say**

The engine walks forward one session at a time. It marks the old holdings through the January close before assigning new targets. Turnover is half the total absolute difference between target and drifted weights, including cash. Fees apply to ETF dollars bought or sold, and the rebalance solves for post-cost NAV. Opening trades incur costs and sit outside reported annual turnover. C is rechecked at execution and blocks known numerical failures. The two baseline replays can still show hypothetical trades after failed checks. None of that confirms actual settlement or issuer exposure.

## 3:13–3:47 | Metrics and reporting

**Show** [metrics.py](../metrics.py), `metrics` and `rolling_objective`. In Streamlit, show **Historical comparison**, its results table, then **Strategies → Mandate checks by strategy**.

**Say**

The metrics module calculates annualized return, realized volatility, drawdown, turnover, and cost from the replay. The benchmark uses the same dates and adjusted ETF prices, without explicit trading fees. The dashboard separates the latest rebalance check from historical reserve exceptions. The CPI function requires matched inflation data, which this snapshot lacks. The model also leaves out actual settlement balances, quarterly payouts, and cash interest.

## 3:47–4:30 | Tests and the controlled run

**Show** `test_portfolios.py` at the optimizer diagnostics test and `test_replay.py` at the walk-forward and CSV tests. Show the terminal's 12-test result, then [Validation and AI use](validation-and-ai-use.md), **Before and after**.

**Say**

The twelve-test suite passed. It covers mandate boundaries, infeasibility, trading-cost arithmetic, timing, the file upload, and zero-volume handling. The locked validation held the data and thirty-six-month window fixed and raised costs from ten to twenty-five basis points. Net returns fell for all three strategies. Targets, verdicts, and blocked dates held steady. That's what I want the walkthrough to demonstrate: how to trace a dashboard number back to an input, a calculation, and a check.
