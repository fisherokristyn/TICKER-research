# Validation and AI use

## Locked Changed-Input Record

- **Pre-test commit evidence.** The author supplied [commit 03325a2bb566c64b438a7680805ec466a82b0c27](https://github.com/fisherokristyn/TICKER-research/commit/03325a2bb566c64b438a7680805ec466a82b0c27) and confirmed before these two runs that the commit predates the designated test and contains the same prediction as the local file. The GitHub page and API were unreachable from this workspace. Commit timing and remote file contents are author-attested.
- **Prediction authorship.** The author confirmed that the prediction was independently written without AI and that there was no separate AI prediction.
- **Preservation.** The verbatim local original is reproduced below. Its status line describes the record at the time of the prediction. The source file remains unchanged. Its SHA-256 is `5e239bbd832562a11c6f67982299569ad5b15076b5ff494ed89d6a48b350806f`.

```text
Locked Changed-Input Record
Input being changed: Transaction costs
Original Value: 10 basis points
New Value: 25 basis points (0.25%)
Prediction (written before running the test)
I predict that increasing transaction costs from 10 to 25 basis points will decrease the net returns of the portfolios because each transaction will become more expensive. I expect Strategy C (Risk-Aware) to be the most sensitive if its optimization and rebalancing decisons result in grater trading activity. However, Strategy A or B could experience a larger reduction of its actual traded dollar volume is higher. 
I expect the mandate compliance results to remain largely unchanged because increasing transaction costs does not directly alter the portfolio's investment restrictions. However, higher costs could affect portfolio weigths, turnover decisons, or feasibility if they are incorporated into the optimization process. 
What would suprise me:
I would be surprised if increaing transaction costs improved net portfolio returns without a corresponding change in trading decisons or portfolio allocations.

Test Status:
Not yet run. This prediction was generated before observing the results of the proposed 25-basis point test.

```

## Reproduction settings

Ran both cases on November 23, 2026, with the same local snapshot through the app's shared `walk_forward` and `metrics` functions. The only changed input was transaction costs per dollar of ETF buys or sales, from 10 to 25 basis points. The snapshot `data/market.csv` has SHA-256 `5e149153700c844fbe38b047952543a46c2a6cf0146686e6c269472e37326d43`, with 4,631 common ETF sessions from June 26, 2008 through November 20, 2026. The replay tracks 3,744 closing observations from January 3, 2012 through November 20, 2026, with a pre-trade NAV reference on December 30, 2011.

Both runs used $100 million starting NAV, 36-month estimation, 20% covariance shrinkage, monthly estimates through November, the existing annual decision calendar, 10% daily volume participation, the 25% annual turnover cap, the existing 3% qualifying cash rule, and the same 60% VT / 40% BND benchmark excluding explicit trading costs. No holdings file was supplied. Monthly CPI was unavailable locally and did not enter the allocation. Reproduce from the project folder with the following Python code.

```python
from backtest import walk_forward
from data_loader import load_market
from metrics import metrics

prices, volume = load_market("data/market.csv")
for cost_bp in (10, 25):
    nav, ledger, cash = walk_forward(
        prices, volume, window=36, cost_bp=cost_bp, shrinkage=.20,
        participation=.10, turnover_limit=.25, holdings=None,
    )
    print(cost_bp, metrics(nav, ledger))
    print(ledger.groupby("Strategy", sort=False).tail(1)[
        ["Date", "Strategy", "Target", "Verdict", "Turnover"]
    ])
    print(ledger.loc[ledger["Note"].ne(""), ["Date", "Strategy", "Note"]])
    print(cash.lt(.03 - 1e-9).sum())
```

## Before and after

Each pair reads 10 bp to 25 bp. Returns are annualized net of modeled trading costs. Volatility is realized annualized volatility. Drawdowns are signed peak-to-trough NAV declines. Mean annual turnover excludes opening funding; cumulative costs include opening trades.

| Strategy | Annualized net return | Annualized volatility | Maximum drawdown | Cumulative trading costs | Mean annual turnover |
| --- | --- | --- | --- | --- | --- |
| A | 4.8174% to 4.7977% | 5.6737% to 5.6740% | -14.1808% to -14.1921% | $226,272.11 to $564,496.42 | 3.0963% to 3.0963% |
| B | 6.9669% to 6.9480% | 9.6964% to 9.6966% | -21.6188% to -21.6298% | $238,326.80 to $594,809.32 | 2.9563% to 2.9563% |
| C | 4.3129% to 4.2982% | 8.4070% to 8.4072% | -21.7268% to -21.7268% | $164,125.66 to $409,722.34 | 3.2473% to 3.2473% |

| Strategy | Latest target in both runs (VT / BND / SHV / cash) | Latest turnover | Latest verdict | Historical verdict | Optimizer feasibility / execution |
| --- | --- | --- | --- | --- | --- |
| A | 33.33% / 33.33% / 33.33% / 0% | 3.5819% | FAIL | FAIL | Static target, 15 modeled executions in both runs |
| B | 58.20% / 38.80% / 0% / 3% | 3.5719% | UNVERIFIED | FAIL | Static target, 15 modeled executions in both runs |
| C | 58.20% / 38.80% / 0% / 3% | 3.5719% | UNVERIFIED | FAIL | Latest target numerically feasible, five modeled executions and ten blocked dates in each run |

Latest proposed rebalance was January 2, 2026. C had the same ten blocked dates and reasons in both runs. Seven failed the total modeled liquidity check and three had incompatible numerical bounds. All scheduled targets and rule statuses matched across the runs. Historical reserve exceptions stayed at 3,744 for A, 3,043 for B, and 1,687 for C. A fails the latest reserve check. B and C pass the latest numerical rules but lack dated issuer look-through. Benchmark results matched across runs.

## Prediction comparison

- **Accurate.** Net returns fell for all three strategies. The mandate verdicts, including their rule-level statuses, held steady. No portfolio improved its net annualized return.
- **Conditional prediction and observed ranking.** C did not have the most dollar trading activity in this replay, so the condition for C to be most sensitive did not occur. C had the highest mean annual percentage turnover but the fewest modeled trades, the lowest cumulative fee increase, and the smallest annualized return decline. B had the largest dollar cost increase ($356,482.52). A experienced the largest annualized return decline (1.97 bp), followed by B (1.89 bp) and C (1.47 bp). Aggregate dollar fees alone did not rank annualized return impact because portfolios have different NAV paths and trade timing.
- **Surprises to discuss.** Increased costs affected realized volatility slightly for all three and deepened the measured drawdown for A and B. C's maximum drawdown was unchanged. The prediction's stated surprise, a net return increase without a decision change, did not occur.

Fees reduce post-trade NAV and therefore change position sizes and future dollar trading amounts even when target weights match. Cost is not an explicit term in C's variance objective. NAV still enters absolute liquidity capacity as a fraction of the book, so another dataset or cost change could affect feasibility or modeled compliance near a boundary. This run showed no such decision or status changes.

## AI assistance

The author provided the pre-test prediction, SHA, and confirmation of the committed contents. Codex ran the controlled replay and automated tests, compared the results with the supplied prediction, and drafted this analysis. There was no AI-generated prediction.

## Human verification

The author's confirmation is the evidence for the pre-test commit. Remote verification remains unavailable from this workspace. Before recording the demo, the author can show the commit and original prediction in GitHub and reproduce both sidebar settings using the local file and a 36-month window. Final interpretation and investment decisions remain the author's.

## Limitations

The replay omits quarterly payouts, cash interest, and actual settlement accounting. Liquidity is modeled. Issuer look-through is unverified and the CPI + 4% objective could not be evaluated without CPI data. The calendar-year loss rule still requires CIO clarification. These are hypothetical results for one snapshot and one cost change, without client approval.

## What I learned from the test

Draft observation for the author to review in their own words. The test separated dollar costs, percentage turnover, and return drag. Those measures ranked the strategies differently. Raising the cost changed net outcomes even while all targets and modeled rule statuses held steady. In another replay, lower NAV could tighten the link between fees and numerical feasibility, so checking the trade ledger matters alongside the return chart.

## Automated verification

`py -m unittest discover -s tests -v` passed all 12 tests. No strategy code, mandate rules, market data, or locked prediction was edited to run this comparison.
