# Video 3 — Investment committee presentation and live demo

**Target** 4:35. **Maximum** 5:00. Read **Say** only. Start at 10 bp and preload the already documented 25 bp comparison as described in the checklist.

**Before recording:** Keep one browser tab on **Strategies** and another on **Historical comparison** at the baseline. Pin the exact figures from the [validation record](validation-and-ai-use.md) and the gates from the [decision memo](decision-memo.md). Rehearse the wait after moving the cost slider.

## 0:00–0:38 | Open with the decision

**Show** App header and **Research settings**. Point to **Market data → Local CSV**, **Estimation window (months) → 36**, and **Trading cost (basis points per dollar) → 10**.

**Say**

I recommend Strategy B for a conditional, non-live pilot. My recommendation for immediate live allocation is zero dollars. There's no authorized live allocation range. This is a fictional one hundred million dollar foundation reserve with a seven-year investment horizon, seven hundred fifty thousand dollars in quarterly payouts, and a rolling five-year objective of inflation plus four percentage points net. Its policy benchmark is sixty percent global stocks and forty percent U.S. investment-grade bonds.

## 0:38–1:24 | Compare risk and return

**Show** **Strategies → Strategy design**, then **Historical comparison**, at the table below the NAV chart. Display the validation table alongside or immediately after for four-decimal values. Streamlit displays these metrics rounded to two decimals.

**Say**

A weights the three ETFs equally. B holds three percent cash and invests the rest sixty-forty. C uses lagged momentum and covariance. At ten basis points, A earned about four point eight two percent net annually, B earned six point nine seven, and C earned four point three one. B also had the highest volatility, about nine point seven percent. Its maximum drawdown was twenty-one point six two percent, compared with fourteen point one eight for A and twenty-one point seven three for C.

**Exact figures to display, not read aloud**

| Strategy | Annualized net return | Realized annualized volatility | Maximum drawdown |
| --- | ---: | ---: | ---: |
| A | 4.8174% | 5.6737% | -14.1808% |
| B | 6.9669% | 9.6964% | -21.6188% |
| C | 4.3129% | 8.4070% | -21.7268% |

## 1:24–2:11 | Show the mandate evidence

**Show** **Strategies → Mandate checks by strategy**. Collapse or expand the panels to show each latest verdict and B's reserve count. Then **Momentum signal → Strategy C blocked rebalances**.

**Say**

The latest rebalance is a separate check from the historical verdict. A fails at the latest date because it holds no qualifying cash. B and C are unverified at the latest date because we lack issuer look-through. All three fail the historical assessment. B targets three percent cash, but it fell below that floor on three thousand forty-three of three thousand seven hundred forty-four closes. C had ten blocked optimization dates and spent much of the early replay in cash. Its latest target matches B because the optimizer selected the lower bound of its equity band.

## 2:11–2:54 | Demonstrate the single cost change

**Show** **Historical comparison**. Move **Trading cost (basis points per dollar)** to **25**, keep **Estimation window (months)** at **36**, and wait for the table. Then display **Before and after** in the validation document.

**Say**

I'll change only the cost slider, from ten to twenty-five basis points. All three net annualized returns fell. B moved from about six point nine seven to six point nine five percent. Targets and verdicts stayed the same, as did C's blocked dates. B paid the largest increase in dollar fees. A had the greatest annualized return decline. The fees were charged against different portfolio values and at different times.

## 2:54–3:32 | Explain the evidence gaps

**Show** **Historical comparison → Rolling five-year return minus CPI + 4%**. Switch to **Committee review → Provisional committee decision**. Point to modeled liquidity and the CIO warning where visible.

**Say**

The replay doesn't fund quarterly payouts or credit interest on cash. The five-day number estimates what might be converted to settled cash, and actual settlement capacity still has to be validated. Dated ETF issuer data are missing, so the eight percent exposure limit remains unverified. CPI is unavailable in this snapshot, so I can't say the rolling objective was achieved. The CIO also needs to define how a calendar-year loss greater than ten percent should be handled.

## 3:32–4:35 | Set the approval gates and conclude

**Show** [Decision memo](decision-memo.md), **Conditions and proposed monitoring**, then **Final committee recommendation**. If useful, return to **Committee review** for the final frame.

**Say**

Before I'd bring a live allocation back to the committee, I'd require a revised policy that keeps at least three percent qualifying assets throughout the modeled holding period. I'd also require funded quarterly payouts, a realistic liquidity plan, and evidence that at least ninety percent can settle in five business days. We'd need dated underlying issuer exposures, CPI data and the rolling five-year evaluation, and a written CIO interpretation of the loss rule. Then I'd rerun the checks and require no hard-rule failures or unresolved hard-rule evidence gaps. Any allocation would still need documented approval from the authorized decision-makers.

B is the research candidate I'd advance because it's transparent, benchmark-oriented, and had the highest net return in this replay. Its historical reserve failures are exactly why the next step is a non-live pilot. My final recommendation is Strategy B for that conditional pilot, with no authorization to deploy foundation assets.
