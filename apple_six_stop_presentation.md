# Apple: from company selection to a conditional valuation conclusion

Presentation script and evidence displays • Prepared October 1, 2026

This document follows the six required stops. Evidence is drawn from the saved project files; market quotes are dated snapshots, not current prices. A PowerPoint could not be exported because the required presentation runtime loader was unavailable.

## 1. Target selection

**Display: Apple was a credible business to investigate, but price remained the question.**

| Selection evidence | Initial interpretation |
|---|---|
| Products plus recurring Services | A business model whose revenue mix and profitability can be traced through annual filings |
| Three consecutive 10-Ks and positive earnings | Enough consistent disclosure to construct a history, forecast statements, and use both DCF and P/E |
| Initial project call: WATCH-DEFER | Attractive operating characteristics did not yet establish an attractive entry price |

**Say:** “I selected Apple because I could investigate how its device ecosystem supports Products and Services revenue using public filings. My initial view was WATCH-DEFER: Apple looked worth studying, but I had not shown that its future cash flows justified its price. The initial project’s decision date was September 1, 2026; the later model is explicitly anchored to the FY2025 balance sheet, so I must not present it as an updated September 2026 valuation.”

**Show the existing evidence:** `Apple_AAPL_Project_1_Edition_A.md`, opening Decision and Operating-value driver sections. The selection rationale is an analyst judgment; it is not a company forecast.

**Transition:** “The next step was to establish what Apple actually reported.”

## 2. Company and evidence

**Display: the Services mix is central to the operating question.**

| FY2025 business evidence | Reported amount | Why it matters |
|---|---:|---|
| Products revenue | USD 307.003bn | Device demand remains a major driver |
| Services revenue | USD 109.158bn | Recurring digital services can change the sales mix |
| Products / Services gross margin | 36.8% / 75.4% | Equal revenue growth in the two categories has different profit implications |

Source: [Apple FY2025 10-K, Item 7, category sales and gross-margin tables; Item 8](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm).

| History, USD millions | FY2023 | FY2024 | FY2025 |
|---|---:|---:|---:|
| Revenue | 383,285 | 391,035 | 416,161 |
| Gross profit | 169,148 | 180,683 | 195,201 |
| SG&A | 24,932 | 26,097 | 27,601 |
| Net income | 96,995 | 93,736 | 112,010 |
| Inventory | 6,331 | 7,286 | 5,718 |
| Net PP&E | 43,715 | 45,680 | 49,834 |
| Shareholders’ equity | 62,146 | 56,950 | 73,733 |

Column sources: [FY2023 10-K](https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm), [FY2024 10-K](https://www.sec.gov/Archives/edgar/data/320193/000032019324000123/aapl-20240928.htm), [FY2025 10-K](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm). Item 8 income statement / balance sheet pages: 28 / 30 for 2023; 29 / 31 for 2024 and 2025. The cell-by-cell source grid is in `apple.md` and embedded in `apple_submission.py`.

**Say:** “Apple earns revenue from devices and related Services. I used annual periods ending September 30, 2023, September 28, 2024, and September 27, 2025, and kept dollars in millions throughout the model. I checked FY2025 revenue directly and reconciled revenue less cost of sales to gross profit; I also checked FY2024 inventory against the balance sheet and the next filing’s comparative. The financial statements are in Part II, Item 8, not Part I.”

**Evidence limits to show:** FY2023 spans 53 weeks, while FY2024 and FY2025 span 52. Organic and same-store growth percentages are not disclosed in the reviewed MD&As. The 2024 tax rate includes an exceptional State Aid charge, so it is not extrapolated mechanically. Later 2026 information exists but is not incorporated into this annual-model exercise.

## 3. Your pro-forma

**Display: historical ratios became explicit judgments, not automatic forecasts.**

| Driver | Historical observation, FY2023 / 2024 / 2025 | Forecast judgment |
|---|---|---|
| Revenue growth | −2.80% / 2.02% / 6.43% | 5% annually |
| Gross margin | 44.13% / 46.21% / 46.91% | 47% |
| SG&A / gross profit | 14.74% / 14.44% / 14.14% | 14.5% |
| Inventory days | 9.61 / 11.81 / 10.74, average inventory | 11 days, ending inventory |
| PP&E depreciation intensity | 19.81% / 18.35% / 16.75%, average net PP&E | 18% of opening net PP&E |
| Tax rate | 14.72% / 24.09% / 15.61% | 18% |

Sources: calculations in `apple.md` from the three linked filings. Inventory days use total cost of sales and 365 days; Services costs are included. Forecast and historical inventory/PP&E denominator conventions differ as shown.

**Say:** “I assumed moderate revenue growth and held gross margin near the latest year. Apple-specific links include separate R&D spending at 8.5% of sales, supplier payables tied to cost of sales, and an economic charge for stock compensation. There is no floor-plan financing. Services mix motivates the assumptions, but the model uses consolidated sales and margin rather than a separate Services forecast, which limits how directly it tests that thesis.”

**Display: the linked statements and signed cash flows. All amounts USD millions.**

| Forecast | FY2026 | FY2027 | FY2028 | FY2029 | FY2030 |
|---|---:|---:|---:|---:|---:|
| Revenue | 436,969 | 458,818 | 481,758 | 505,846 | 531,139 |
| Net income | 111,072 | 116,749 | 122,709 | 128,967 | 135,539 |
| Operating cash flow | +135,210 | +143,497 | +151,038 | +158,912 | +167,144 |
| Investing cash flow | −16,992 | −17,842 | −18,734 | −19,670 | −20,654 |
| Financing cash flow | −118,218 | −125,655 | −132,304 | −139,242 | −146,490 |
| Ending cash | 35,934 | 35,934 | 35,934 | 35,934 | 35,934 |
| Assets − liabilities − equity | 0 | 0 | 0 | 0 | 0 |

Source: `apple_proforma_output.txt`, full statements and CHECK BLOCK; values rounded for display, checks run before rounding. The same evidence is embedded in `apple_submission.py`.

**Say:** “Cash is calculated from cash flows, and equity rolls forward from earnings and shareholder distributions. They are not unexplained balancing plugs. Cash stays above the USD 20,000m floor because the payout policy distributes available cash after investment; no revolver draw is needed or modeled. The checks also reconcile PP&E, operating cash flow, FCFE and FCFF, and the tests demonstrate that broken links stop valuation. Balanced statements establish accounting consistency, not forecast accuracy.”

## 4. Valuation

**Display: Apple DCF, with its date and share basis beside the value.**

**USD 124.61 per share — FY2025-end valuation anchor: September 27, 2025; denominator: 14,773.260 million period-end shares; not a current price target.**

| DCF bridge | USD millions |
|---|---:|
| PV of FY2026–FY2030 FCFF | 463,922.348 |
| PV of terminal value | 1,363,271.744 |
| Enterprise value | 1,827,194.093 |
| Add cash and marketable securities | +132,420.000 |
| Less operating cash reserve | −20,000.000 |
| Less financial debt, carrying amount | −98,657.000 |
| Equity value | 1,840,957.093 |

**Say:** “I discounted FCFF after charging stock compensation at a judgmental 9% WACC, with 2.5% terminal growth and end-of-year discounting. FCFE is shown in the statements but is not discounted at WACC. I added financial assets, retained an operating cash buffer, and deducted financial debt before dividing by period-end shares. Lease costs remain operating costs, so lease liabilities are not separately deducted again. Terminal value is 74.61% of enterprise value; the 9% rate is a provisional hurdle, not a completed market-based WACC estimate.”

Source: `apple_proforma.py`, `value()` and `apple_proforma_output.txt`; [FY2025 balance sheet and debt note](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm). Debt uses carrying value, not the different principal total.

**Display: the peer method answers a different question.**

| Peer | September 1, 2026 price / annual reported GAAP diluted EPS | P/E | Qualification |
|---|---|---:|---|
| Microsoft | USD 501.02 / USD 17.95, FY ended June 30, 2026 | 27.911978x | Enterprise cloud/software mix; reported earnings include investment gains |
| Alphabet Class A | USD 335.02 / USD 10.82, FY ended December 31, 2025 | 30.963031x | Advertising-led; Class A price matches Class A EPS |

**Peer indication: USD 208.22–230.98 per AAPL share; median USD 219.60 — comparison date September 1, 2026; Apple FY2025 reported diluted EPS USD 7.46, calculated on annual weighted-average diluted shares (15,004.697m), not the DCF’s period-end denominator.**

**Say:** “These peers share platform and ecosystem characteristics but are qualified comparators, not operating twins. P/E transfers a market earnings multiple directly to Apple’s reported EPS; DCF values explicit cash-flow assumptions. Fiscal periods, dates and share conventions differ, so I do not average these values. P/E is computable because all admitted annual EPS figures are positive, but reported investment gains and business mix limit its interpretation. Removing Microsoft leaves USD 230.98, up USD 11.38; removing Alphabet leaves USD 208.22, down USD 11.38, on the same September 1 peer-analysis basis.”

Evidence: rerun `peer_pe.py`; source table in `Apple_AAPL_Project_1_Edition_A.md`. Primary earnings sources: [Apple FY2025 release](https://www.apple.com/newsroom/2025/10/apple-reports-fourth-quarter-results/), [Microsoft FY2026 release](https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast), [Alphabet FY2025 10-K, Note 12](https://www.sec.gov/Archives/edgar/data/1652044/000165204426000018/goog-20251231.htm). The project records same-date Nasdaq prices; these are saved evidence, not newly fetched October quotes.

**Display: keep the saved market comparisons and reverse DCF distinct.**

| Record | Price and date | Basis / interpretation |
|---|---|---|
| Original peer-project market price | USD 325.13, September 1, 2026 close | Actual AAPL quote per share, compared with annual diluted EPS |
| Later saved quote | USD 336.94, September 24, 2026, 2:06 p.m. EDT | Actual AAPL quote; holding the model’s 14,773.260m shares fixed is a comparison convention, not a claim about current shares |
| Old reverse-DCF target | USD 325.25, September 10, 2026, 1:51 p.m. EDT, as recorded in `dcf.py` | Actual-price target applied to synthetic classroom cash-flow inputs |

Saved later quote source: [Stock Analysis AAPL](https://stockanalysis.com/stocks/aapl/), archived in `apple_submission.py`. None of these is an October 1 live quote.

**Reverse-DCF result displayed verbatim:** `No solution in that bracket.`

Held fixed in the old script: starting FCFF USD 100m; base annual growth 8%, 6%, 5%, 4%, 3%; WACC 10%; terminal growth 3%; nonoperating cash USD 50m; debt USD 300m; 50m diluted shares; five end-of-year periods. Only a uniform growth-rate shift varies, between −5 and +10 percentage points.

**Say:** “I reran the saved reverse-DCF script and it returned no solution in its bracket. Its capital structure, shares and cash-flow base are synthetic, so this is not an Apple implied-growth finding; the synthetic USD 27.4974 per-share base result, on 50m shares with no valid Apple valuation date, receives no weight. An Apple-specific reverse DCF remains unresolved, and widening a synthetic bracket would not fix the company mismatch.”

## 5. Sensitivity and drivers

**Display: existing Apple sensitivity, separate from the missing Lab 11 record.**

All cells: **USD per share; September 27, 2025 model anchor; 14,773.260m period-end shares.** Forecast operations, cash, securities, debt and share count stay fixed.

| WACC / terminal growth | 2.0% | 2.5% | 3.0% |
|---|---:|---:|---:|
| 8% | 137.37 | 147.40 | 159.43 |
| 9% | 117.60 | **124.61** | 132.79 |
| 10% | 102.79 | 107.91 | 113.77 |

| Change from base | Output change, USD/share |
|---|---:|
| WACC 9% → 8%, terminal growth held at 2.5% | +22.78 |
| WACC 9% → 10%, terminal growth held at 2.5% | −16.70 |
| Terminal growth 2.5% → 2%, WACC held at 9% | −7.01 |
| Terminal growth 2.5% → 3%, WACC held at 9% | +8.18 |

Deltas calculated before rounding. Joint tested range: USD 102.79–159.43 per share, on the same FY2025 anchor and share basis. Source: `apple-model.json`, `sensitivity`, and `apple.md`.

**Say:** “WACC changes the discounting and the terminal-value denominator, so it changes value without changing the five explicit statements. Terminal growth changes the continuing value, also without changing those five statements. In these selected ranges, WACC produces the larger one-variable spread, but that does not establish which assumption is more uncertain or more important under different ranges.”

**Display: how operating changes would flow through the statements.**

| Driver changed | Causal link in this model |
|---|---|
| Revenue growth | Sales → gross profit, SG&A and R&D; also receivables, inventory, payables, capex and SBC → cash flows → valuation |
| Gross margin | Gross profit → operating income and tax; cost of sales changes inventory and payables → working-capital cash flow |
| Capex | Investing outflow now → higher PP&E → later depreciation; assumed operating margins constrain how much tax benefit the model captures |
| Inventory days | Inventory → working-capital investment → CFO and cash available for distribution; no direct sales benefit is assumed |

**Lab 11 status: unresolved.** No saved Lab 11 base/changed operating inputs, prescribed ranges, outputs or driver ranking were found in the supplied workspace. The table above is the existing valuation sensitivity, not a relabeled Lab 11 result. A complete Lab 11 slide requires its actual scenario log; no operating-driver ranking is asserted here.

**Say:** “Even a completed ranking would be conditional on the chosen shock sizes and other inputs held fixed. It would measure model sensitivity, not probability, forecast accuracy, causation established from real-world data, or interactions between simultaneous shocks. Signed negative cash flows must remain in any changed scenario; they cannot be removed to improve the answer.”

## 6. Interpretation

**Display: retain a conditional WATCH-DEFER, with concrete revision tests.**

| Evidence to investigate next | What could change the conclusion |
|---|---|
| Latest filings, including 2026 interim results | Update the operating base, tax timing, cash, debt and shares to one decision date |
| Separate Products and Services forecast | Test whether slower Services growth still supports sufficient cash generation |
| Dated Treasury yield, equity risk premium, beta, borrowing yields and capital weights | Replace the provisional 9% WACC with a justified estimate |
| Apple-specific reverse DCF | Identify the growth or margin assumptions required by a same-date market quote |
| Actual Lab 11 scenario record | Establish which tested operating changes most affect this model and why |

**Say:** “My conditional conclusion remains WATCH-DEFER, not a current trading recommendation. I began with a credible business and an untested valuation thesis; I now have a reconciled Apple-specific annual model whose assumptions produce a value substantially below the saved quote, plus a separately qualified peer indication. That gives me a question about the market’s expectations, not proof that the market is wrong.”

**Say:** “I would move toward INITIATE-BUY if a consistently dated valuation, including updated evidence and conservative Services assumptions, supports a meaningful margin of safety. I would move toward DO NOT INITIATE if an updated analysis remains materially below the same-date price across justified assumptions and the reverse DCF requires performance the evidence does not support. The peer comparison, FY2025 model and September quotes are not synchronized enough to support a stronger current conclusion.”

**Show the challenged judgment:** `apple.md`, the two-sentence defense below the assumption table: 9% is provisional and would be replaced by a valuation-date cost-of-capital estimate. The reciprocal partner response remains missing; a draft challenge is not presented as a completed live exchange.

**Closing question:** “What sustained operating performance and required return would make the saved market price reasonable, and which filing evidence would persuade me that those assumptions are achievable?”

## Evidence files to keep open while presenting

| Stop | Saved exhibit |
|---|---|
| Target selection | `Apple_AAPL_Project_1_Edition_A.md`: original decision and falsification question |
| Company and evidence | `apple.md`: linked history grid, ratio table, two direct checks |
| Pro-forma | `apple_submission.py`: assumptions, opening balances, executable model and captured output |
| Valuation | `apple_proforma_output.txt`: valuation bridge; `peer_pe.py`: peer results; `dcf.py`: explicitly synthetic reverse-DCF limitation |
| Sensitivity and drivers | `apple-model.json`: saved sensitivity; Lab 11 scenario record still required |
| Interpretation | `apple.md`: challenged discount-rate judgment; original project decision rules |

Reproduction commands in the supplied Windows workspace:

```powershell
& 'C:\Users\krist\miniconda3\python.exe' -B .\apple_submission.py
& 'C:\Users\krist\miniconda3\python.exe' -B .\peer_pe.py
& 'C:\Users\krist\miniconda3\python.exe' -B .\dcf.py
```

The third command reproduces the classroom-model limitation; it does not produce an Apple valuation. No conflicting methods are averaged in this presentation.
