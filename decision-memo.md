# Investment committee decision memo

**Meridian Foundation Reserve | FIN 43900 Project 2**  
**To** Investment Committee  
**From** Student investment research team  
**Subject** Strategy B conditional, non-live pilot

## 1. Executive recommendation

Recommend **Strategy B (Cash + 60/40) for a conditional, non-live pilot only**. B is the strongest current research candidate because its allocation is transparent, it is anchored to the policy benchmark, and it produced the highest annualized net return and lowest mean annual turnover of the three strategies in the audited replay. It also had the highest realized volatility. Its **historical mandate verdict is FAIL**. The pilot would test whether reserve maintenance, payouts, and trading can work together under the mandate. Immediate live allocation is **$0**.

## 2. Client mandate and decision context

The fictional foundation has a $100 million portfolio, a seven-year horizon, and a quarterly payout of $750,000. Its return objective is CPI plus four percentage points annually, net of costs, over rolling five-year periods. The policy benchmark is 60% global equities and 40% U.S. investment-grade bonds, with annual rebalancing.

The mandate requires at least 3% in qualifying cash or eligible direct U.S. government securities, at least 90% of portfolio value convertible to settled cash within five business days, an 8% limit per nonexempt single-company issuer, and no more than 25% annual one-way turnover without approval. The portfolio must be long-only and fully invested, with cash counting toward total weights, and must avoid leverage and derivatives. The prototype counts qualifying cash toward the reserve and excludes SHV. The treatment of a calendar-year loss greater than 10% requires CIO clarification. [Proposed mandate](proposed-mandate.md) · [Dashboard rules](../app.py) · [Compliance checks](../compliance.py)

## 3. Strategy comparison

| Strategy | January 2, 2026 target, VT / BND / SHV / cash | Annualized net return | Realized annualized volatility | Maximum drawdown | Mean annual turnover | Latest / historical verdict |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| A · Equal weight | 33.33% / 33.33% / 33.33% / 0% | 4.8174% | 5.6737% | −14.1808% | 3.0963% | FAIL / FAIL |
| B · Cash + 60/40 | 58.20% / 38.80% / 0% / 3.00% | 6.9669% | 9.6964% | −21.6188% | 2.9563% | UNVERIFIED / FAIL |
| C · Risk-aware | 58.20% / 38.80% / 0% / 3.00% | 4.3129% | 8.4070% | −21.7268% | 3.2473% | UNVERIFIED / FAIL |

The table uses the 10 bp baseline. The **benchmark** is a separate 60% VT / 40% BND policy proxy. It rebalances annually and uses the same dates and adjusted ETF prices as the strategies, with explicit trading costs excluded. B sets aside 3% cash and applies the 60/40 split to the remaining 97%.

To reproduce the table, select **Local CSV** in the dashboard, use the frozen market snapshot, and set the estimation window to 36 months and trading costs to 10 basis points per ETF dollar traded. The replay uses 20% covariance shrinkage and observes 3,744 closes from January 3, 2012 through November 20, 2026. Annualized net return compounds the change in NAV over elapsed calendar time. Realized volatility annualizes the standard deviation of daily returns using 252 sessions. Drawdown measures the deepest decline from a prior closing NAV peak. Mean annual turnover uses half the absolute weight changes from the drifted book, including cash, and excludes opening funding. [Market data card](../data/market-data-card.md) · [Results audit](results-audit.md) · [Validation record](validation-and-ai-use.md) · [Metrics code](../metrics.py)

## 4. Financial judgment

- **A** had the lowest realized volatility and shallowest drawdown, but its zero-cash target failed the latest reserve check. Its SHV allocation does not qualify under the prototype reserve rule.
- **B** gives the committee a clear starting point for testing a payout and reserve process. Its historical reserve test failed on **3,043 of 3,744 closes**. At an executed rebalance it resets to 3% cash, but gains in ETF holdings can push the cash percentage below the floor between trades. A latest target that meets the reserve minimum cannot establish ongoing compliance. B's drawdown also exceeded the project's proposed 20% review threshold. That threshold is separate from the unresolved calendar-year loss rule.
- **C** uses lagged 12-month relative momentum to set an equity-weight band, then minimizes variance using trailing covariance estimates. It had ten blocked dates, seven because modeled liquidity left no feasible allocation and three because the numerical bounds had no feasible intersection. It stayed in cash for 1,760 closes before its first execution. All five executed targets matched B, including the latest, where the lower momentum-band bound was binding. These results provide no demonstrated incremental allocation benefit from C's signal and give the committee no basis to prefer its added complexity for this pilot. [Results audit](results-audit.md) · [Strategy code](../strategies.py)

Quarterly payouts would draw down qualifying assets unless replenished. Raising or restoring the reserve could require sales, take time to settle, incur fees, and use part of the turnover allowance. The committee should evaluate these effects together and specify who can authorize remediation. Historical nominal net returns alone cannot establish attainment of the CPI + 4% objective.

## 5. Locked changed-input validation

| Strategy | Net annualized return, 10 bp → 25 bp | Cumulative trading costs, 10 bp → 25 bp |
| --- | ---: | ---: |
| A | 4.8174% → 4.7977% | $226,272.11 → $564,496.42 |
| B | 6.9669% → 6.9480% | $238,326.80 → $594,809.32 |
| C | 4.3129% → 4.2982% | $164,125.66 → $409,722.34 |

Targets, mandate verdicts, and C's blocked dates were unchanged. A lost the most annualized return, about 1.97 bp, while B incurred the largest cumulative dollar cost increase, $356,482.52. Dollar fees reflect the amount traded, while return drag depends on each charge relative to the portfolio value when it occurs and on subsequent compounding. The different NAV paths and trading dates can therefore produce different rankings.

The student's original prediction anticipated lower net returns and largely unchanged mandate checks. The student confirmed that it was written without AI, that no separate AI prediction exists, and that the committed text matched the local original before the run. The initial reference to a separate AI prediction was later corrected by the student. Review the final authorship disclosure before submission. The SHA and timing are author-attested because this workspace could not verify the remote commit. AI assisted with the replay, analysis, and memo. [Verbatim prediction](locked-prediction.md) · [Validation record](validation-and-ai-use.md) · [Author-supplied commit](https://github.com/fisherokristyn/TICKER-research/commit/03325a2bb566c64b438a7680805ec466a82b0c27)

## 6. Conditions and proposed monitoring

| Gate before reconsidering live allocation | Required evidence |
| --- | --- |
| Reserve and quarterly payouts | A revised policy that keeps at least 3% in qualifying assets throughout the modeled holding period, including before and after every $750,000 payout. Show a funding calendar, cash sources, and how replenishment trades affect the annual turnover limit. |
| Settlement liquidity | Confirm with the custodian and execution team that at least 90% of portfolio value can convert to settled cash within five business days at the relevant portfolio size. Document the sale schedule, participation assumptions, and settlement evidence. |
| Issuer exposure | Obtain dated look-through or equivalent reliable underlying exposure data. Aggregate shared issuers across funds and verify the 8% nonexempt limit plus approved exemptions. |
| Return objective | Obtain CPI data and evaluate rolling five-year net results against annualized CPI plus four points. Report coverage, shortfalls, and sensitivity to trading costs. |
| Governance and sign-off | Obtain written CIO interpretation of the calendar-year loss rule. Re-run the mandate checks with the revised policy and complete data. Require zero hard-rule failures, no unresolved hard-rule verification gaps, and documented approval from the authorized investment decision-makers. |

**Proposed pilot cadence.** Monitor modeled qualifying cash and reserve exceptions at each trading close. Review issuer exposure, estimated five-day liquidity, cumulative one-way turnover, costs, and drawdown monthly. Test payout funding and actual settlement assumptions before and after each simulated quarterly payout. At the committee's quarterly review, also report rolling CPI-relative results where full five-year windows exist. Escalate a reserve, issuer, turnover, or liquidity breach, an unfunded payout, or a missing required observation promptly and record the corrective action. These monitoring arrangements are recommendations for committee approval.

## 7. Risks, limitations, and uncertainty

The historical replay is one ETF-based simulation using adjusted prices, modeled fees, and simplified trading and settlement assumptions. It omits quarterly payouts and cash interest, and reinvested ETF distributions are reflected in adjusted returns instead of a spendable cash ledger. No local CPI or issuer look-through data was available. Five-day liquidity is modeled convertibility, and actual settled-cash availability remains unconfirmed. Historical reserve breaches are observed in the replay and remain material.

**FAIL** indicates an observed rule breach or failed modeled check. **UNVERIFIED** indicates missing evidence and provides no compliance clearance. **CIO clarification required** identifies an unresolved policy definition, including the calendar-year loss statement. [Results audit](results-audit.md) · [Validation limitations](validation-and-ai-use.md)

## 8. Final committee recommendation

Approve **Strategy B for a conditional non-live research pilot only**, subject to agreement on the evidence and monitoring plan above. **Immediate live allocation is $0. No live allocation range is authorized.** Reconsider only after verifying compliance, obtaining the missing data, modeling cash flows and settlement realistically, and securing documented committee approval.

Reject or redesign the proposal if the revised model still breaches the reserve or turnover limits, cannot fund recurring payouts, fails the settlement liquidity or issuer tests, or shows persistent material CPI-relative shortfalls under the committee's approved evaluation criteria. Keep live authorization on hold while any required evidence or policy interpretation is unresolved.
