# V — Reviewer questions and evidence check

Prepared October 1, 2026. Status: preparation plus an independently reproduced calculation, not a completed partner discussion.

The available analysis concerns Apple. The partner's actual company has not been confirmed. The questions below apply only if the partner is presenting this saved Apple analysis; otherwise replace them using the partner's actual company, inputs and results before asking. No presenter answers have been supplied or invented.

## Selection and evidence

**Question:** You selected Apple partly because Services could support growth and profitability, and you cite FY2025 Services revenue of USD 109.158bn and a 75.4% gross margin; why does that make Apple suitable for your valuation exercise, and can you locate those figures in the FY2025 10-K and distinguish the reported facts from your expectation that they will persist?

**Follow-up if unsupported:** Which filing table supports the claim, and what evidence supports carrying those economics forward rather than simply describing one historical year?

**Presenter's actual answer:** Not received.

**Specific gap and resolution:** The selection rationale and figures appear in the saved project, but the presenter has not identified or explained the evidence during questioning. Open Item 7's category-sales and gross-margin tables together and record their explanation of why the history is relevant to the forecast.

Cited source to open: [Apple FY2025 Form 10-K](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm). This session has not performed that joint source check.

## Model and valuation

**Question:** Your Apple DCF assumes 5% annual revenue growth, 47% gross margin, 9% WACC and 2.5% terminal growth and produces USD 124.61 per share; walk me from revenue through operating profit, working-capital investment and FCFF to that result, then explain why it differs from your USD 208.22–230.98 peer indication without averaging the methods.

**Follow-up if unsupported:** Please point to the actual model lines and name the date and share basis for each method; which part of the gap comes from different economic assumptions, and which part remains unquantified because the dates, business mixes and share conventions differ?

**Presenter's actual answer:** Not received.

**Specific gap and resolution:** A live explanation tracing the operating assumption has not been recorded, and the numerical contribution of each cause of the DCF/peer disagreement has not been decomposed. Open `apple_proforma.py` and `peer_pe.py` together; record the presenter's explanation and leave any unquantified attribution unresolved.

Value labels: DCF is USD/share at a September 27, 2025 model anchor, using 14,773.260m period-end shares. The peer indication uses September 1, 2026 peer prices and Apple FY2025 reported diluted EPS of USD 7.46, based on annual weighted-average diluted shares. The later market snapshot is USD 336.94 on September 24, 2026 at 2:06 p.m. EDT; it is not an October quote.

## Sensitivity and interpretation

**Question:** Your saved sensitivity tests WACC from 8% to 10% and terminal growth from 2% to 3%, but no Lab 11 operating-driver ranking is present; what ranking can you actually support, how would it depend on the shock sizes and inputs held fixed, and what evidence would make you revise WATCH-DEFER?

**Follow-up if unsupported:** Show the actual Lab 11 base and changed inputs and output rather than naming a driver from intuition; if that record is unavailable, which claimed ranking must remain unresolved, and what observed result would overturn your conclusion?

**Presenter's actual answer:** Not received.

**Specific gap and resolution:** The Lab 11 scenario log and the presenter's decision-changing evidence have not been supplied. Obtain the original scenario inputs, ranges, output and calculation; do not relabel the existing WACC grid as Lab 11 or substitute a newly invented scenario.

## Calculation checked independently

Checked October 1, 2026 by rerunning `apple_proforma.py` functions in memory. The saved model file and its assumptions were not edited. This is a preparatory check, not evidence that a partner attended or answered.

**Claim tested:** Raising WACC from 9% to 10%, with the other model inputs fixed, lowers value from approximately USD 124.61 to USD 107.91 per share while leaving the five forecast cash flows unchanged.

| Item | Base | Changed |
|---|---:|---:|
| WACC | 9% | 10% |
| Terminal growth | 2.5% | 2.5% |
| FY2030 FCFF, USD millions | 133,016.162502 | 133,016.162502 |
| Share count, millions | 14,773.260 | 14,773.260 |
| Value, USD per share | 124.614140 | 107.912982 |
| All five statement checks | Pass | Pass |

Both values use the September 27, 2025 model anchor. All operating assumptions, explicit cash flows, cash/securities, debt, reserve and shares were held fixed. The change is **−USD 16.701158 per share** before rounding.

Trace checked:

1. WACC changes from 0.09 to 0.10.
2. No forecast income-statement, balance-sheet or cash-flow input changes.
3. All five FCFF amounts remain identical; FY2030 FCFF is shown above.
4. Explicit FCFF is discounted by `(1 + WACC) ** year`.
5. Terminal value uses `FCFF_2030 * 1.025 / (WACC - 0.025)` and is discounted five years.
6. The unchanged equity bridge is +USD 13,763m; equity value is divided by 14,773.260m shares.

**Finding:** The check supports the stated arithmetic and discount-rate transmission. It does not establish that 9% is Apple's correct cost of capital, validate an operating-driver ranking, or establish that the model is a current valuation.

**To complete the joint check:** Open `apple_proforma.py` with the presenter, repeat this trace or their actual Lab 11 trace, and record their explanation and whether the joint check supported it. Until then, the partner's identity/company, actual answers, follow-up responses and joint-review outcome remain unresolved.
