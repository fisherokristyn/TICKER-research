# -*- coding: utf-8 -*-
r"""
APPLE PRO FORMA - SINGLE-FILE SUBMISSION
Prepared September 24, 2026

This file contains the sourced written analysis, assumptions, review draft,
dated market comparison, executable Python model, and its captured run output.
Run this file with Python 3; it uses only the standard library and needs no
other project files. The captured output at the end is a submission record;
running the file recalculates the statements and runs the checks.

Outstanding assignment item: the reciprocal partner critique and actual
partner answer remain unresolved because their assumption was not supplied.
The challenge to this model is explicitly a draft, not a claimed live exchange.

WRITTEN ANALYSIS

Apple's illustrative equity value is **$1.84 trillion, or about $125 per share**, under the assumptions below. The valuation is anchored to the FY2025 closing balance sheet and uses only FY2023–FY2025 annual filings as historical evidence. It is a fiscal-year-end model, not a September 2026 price target; 2026 interim results are outside this exercise.

| USD millions | FY2023 | FY2024 | FY2025 |
| --- | --- | --- | --- |
| Revenue | [383,285][K2023] | [391,035][K2024] | [416,161][K2025] |
| Gross profit | [169,148][K2023] | [180,683][K2024] | [195,201][K2025] |
| SG&A | [24,932][K2023] | [26,097][K2024] | [27,601][K2025] |
| Net income | [96,995][K2023] | [93,736][K2024] | [112,010][K2025] |
| Inventory, year-end | [6,331][K2023] | [7,286][K2024] | [5,718][K2025] |
| PP&E, net, year-end | [43,715][K2023] | [45,680][K2024] | [49,834][K2025] |
| Shareholders’ equity | [62,146][K2023] | [56,950][K2024] | [73,733][K2025] |

Each linked number identifies its own fiscal year's 10-K. Financial statements are in **Part II, Item 8**, rather than Part I of the filing. Income statement / balance sheet / cash-flow page references are 28 / 30 / 32 in the 2023 filing, and 29 / 31 / 33 in the 2024 and 2025 filings. Depreciation is in Note 5. Figures are USD millions unless stated otherwise.

I opened the filings and directly checked two items:
- FY2025 revenue: **416,161**, on page 29. Subtracting cost of sales of 220,960 gives gross profit of **195,201**. [2025 filing][K2025].
- FY2024 inventory: **7,286**, on page 31; it also agrees with the FY2024 comparative in the next filing. [2024 filing][K2024], [2025 comparative][K2025].

| Metric | FY2023 | FY2024 | FY2025 |
| --- | --- | --- | --- |
| Gross margin | [44.13%][K2023] | [46.21%][K2024] | [46.91%][K2025] |
| SG&A ÷ gross profit | [14.74%][K2023] | [14.44%][K2024] | [14.14%][K2025] |
| Inventory days | [9.61][K2023] | [11.81][K2024] | [10.74][K2025] |
| PP&E depreciation ÷ average net PP&E | [19.81%][K2023] | [18.35%][K2024] | [16.75%][K2025] |
| Effective tax rate | [14.72%][K2023] | [24.09%][K2024] | [15.61%][K2025] |
| Reported revenue growth, calculated | [-2.80%][K2023] | [2.02%][K2024] | [6.43%][K2025] |
| Organic / same-store growth | [Not disclosed][K2023] | [Not disclosed][K2024] | [Not disclosed][K2025] |

These are my calculations from the linked filings, not provider ratios. Gross margin = gross profit / revenue; SG&A intensity = SG&A / gross profit; inventory days = average opening/closing inventory / total cost of sales × 365; depreciation intensity = PP&E depreciation / average opening/closing net PP&E; tax rate = tax provision / pretax income; growth = current / prior-year revenue − 1.

The 365-day convention is standardized: FY2023 had 53 weeks and the next two years had 52. Using total cost of sales also includes Services, so inventory days is a consolidated comparison, not a pure hardware stock-turn measure. [Fiscal calendar][K2025].

| Ratio inputs, USD millions | FY2023 | FY2024 | FY2025 |
| --- | --- | --- | --- |
| Cost of sales | [214,137][K2023] | [210,352][K2024] | [220,960][K2025] |
| Beginning inventory | [4,946][K2023] | [6,331][K2024] | [7,286][K2025] |
| Beginning net PP&E | [42,117][K2023] | [43,715][K2024] | [45,680][K2025] |
| PP&E depreciation (rounded disclosure) | [8,500][K2023] | [8,200][K2024] | [8,000][K2025] |
| Total depreciation and amortization | [11,519][K2023] | [11,445][K2024] | [11,698][K2025] |
| Pretax income | [113,736][K2023] | [123,485][K2024] | [132,729][K2025] |
| Tax provision | [16,741][K2023] | [29,749][K2024] | [20,719][K2025] |
| Prior-year revenue | [394,328][K2023] | [383,285][K2024] | [391,035][K2025] |

PP&E depreciation is approximately $8.5bn, $8.2bn and $8.0bn, respectively; total D&A must not be substituted into that ratio. [2023][K2023], [2024][K2024], [2025][K2025].

| Year | 10-K PP&E cash spending (outflow magnitude) | Stock Analysis “Capital Expenditures” (signed) | Difference in magnitude |
| --- | --- | --- | --- |
| 2023 | [10,959][K2023] | [-10,959][Provider] | 0 |
| 2024 | [9,447][K2024] | [-9,447][Provider] | 0 |
| 2025 | [12,715][K2025] | [-12,715][Provider] | 0 |

The provider comparison was checked on September 24, 2026. Parentheses in the filings and negative provider values both represent cash outflows. The requested provider was unnamed, so I selected [Stock Analysis][Provider]. Its capital-expenditure field matches the filing's PP&E purchase line in all three years; no unresolved numerical difference remains.

Apple does not supply an organic-growth or comparable-store-sales percentage in these MD&As. Growth from stores already owned therefore remains **unresolved / not disclosed**, not 0%. FY2023 MD&A says exchange rates more than explained the reported sales decline; that does not establish a numerical organic or same-store rate. [2023 MD&A][K2023], [2024 MD&A][K2024], [2025 MD&A][K2025].

The FY2024 tax provision includes a $10.2bn one-time net charge related to the State Aid Decision, which makes a mechanical extrapolation of its tax rate inappropriate. [FY2024 MD&A and Note 7][K2024].

| Value | Label | Reason |
| --- | --- | --- |
| Starting revenue: $416,161m; net PP&E: $49,834m; equity: $73,733m | history | FY2025 audited starting balances. [2025 10-K][K2025]. |
| Revenue growth: 5% annually, FY2026–FY2030 | judgment | I use moderate expansion rather than extrapolating a single strong year; it sits between the recent 2.02% and 6.43% annual outcomes. |
| Gross margin: 47% | judgment | I keep profitability close to the latest year instead of assuming further large margin gains. |
| SG&A: 14.5% of gross profit | judgment | I use a level within the observed three-year range, allowing operating costs to rise with the business. |
| R&D: 8.5% of revenue | judgment | I reserve substantial ongoing development spending; R&D stays separate from SG&A. |
| Tax rate: 18% of pretax income; cash tax equals provision | judgment | I allow more tax than the two lower historical rates without repeating the exceptional 2024 charge; timing differences are simplified. |
| Inventory: year-end balance = 11/365 × cost of sales | judgment | I target about eleven days of stock, near the history. This forecast uses ENDING inventory; the historical ratio above uses AVERAGE inventory. |
| PP&E depreciation: 18% of opening net PP&E | judgment | I use a rounded rate near recent depreciation intensity. Opening PP&E makes the roll-forward explicit; the historical comparison uses average PP&E. |
| PP&E capital spending: 3% of revenue | judgment | I maintain physical reinvestment near the latest spending intensity rather than deriving capex from the net PP&E change. |
| Other amortization: $3,698m × revenue / $416,161m; matching other-asset investment | judgment | I separate total D&A from PP&E depreciation and assume equal replacement spending for the other amortizing assets; this prevents a free cash-flow benefit from depletion. |
| Receivables (trade plus vendor), other current assets, deferred revenue: retain FY2025 ratios to sales | judgment | I make these operating balances grow with activity instead of freezing the cash needs of a larger business. |
| Accounts payable: retain FY2025 ratio to cost of sales | judgment | I assume supplier payment terms stay unchanged. |
| Other current liabilities and other non-current assets/liabilities: hold FY2025 dollar balances | judgment | I avoid extending tax and other mixed accounts with an arbitrary sales ratio; detailed tax, lease and asset schedules remain a model limitation. |
| Floor-plan financing: none; accounts payable modeled separately | judgment | No dedicated floor-plan borrowing line was identified. Supplier payables are operating financing and are not relabeled as floor-plan debt. |
| Debt: $98,657m; net new borrowing: zero; interest expense: $3,000m annually | judgment | I assume existing debt is refinanced and use roughly a 3% borrowing cost, keeping financing from driving the operating valuation. |
| Investment income and other nonoperating gains: zero | judgment | I value excess financial assets separately, so I exclude their returns from forecast operating value. |
| Stock compensation: 3% of sales; offsetting repurchases equal that expense | judgment | I charge existing shareholders for equity compensation. Equal-cost repurchases are an approximation for keeping shares constant. |
| Cash and securities: retain opening balances; distribute remaining FCFE after antidilution repurchases | judgment | I use a transparent cash-neutral payout policy. This is a modeling convention, not Apple's announced dividend or repurchase plan. |
| OCI, acquisitions, asset disposals, FX and other equity adjustments: zero | judgment | I omit events I cannot forecast and expose that simplification rather than inserting unexplained balancing amounts. |
| Operating cash reserve: $20,000m | judgment | I retain a working liquidity buffer before treating the rest of cash and securities as excess value. |
| Discount rate (WACC): 9%; sensitivity: 8%–10% | judgment | I require a substantial return for business and equity risk; this is an explicit valuation hurdle, not a claimed market-calibrated CAPM estimate. |
| Terminal cash-flow growth: 2.5%; sensitivity: 2%–3% | judgment | I reduce long-run growth below the forecast rate and keep it below the discount rate; sustained reinvestment remains necessary. |
| Share denominator: 14,773.260m shares at FY2025 year-end | history | Period-end shares, rather than annual weighted-average shares. [2025 10-K][K2025]. |
| Management guidance used: none | guidance | No five-year management forecast is used; all forward operating rates above are my judgments. |

**Assumption challenge — draft for partner review, not a recorded partner quotation:** Your 9% WACC is described as a required return without a dated cost-of-capital calculation, yet terminal value supplies 74.61% of enterprise value and changing WACC from 9% to 8% raises the estimate from $124.61 to $147.40 at the same 2.5% terminal growth; why should 9% carry more weight than either sensitivity endpoint, and what evidence would make you replace it?

**My answer (two sentences):** I chose 9% as the midpoint of the explicit 8%–10% hurdle-rate range to avoid giving the lowest required return the status of a base case, but that is a provisional modeling convention and does not establish that Apple's actual WACC is 9%. I would replace it with a valuation-date estimate built from a same-date Treasury yield, a justified equity-risk premium and beta, borrowing yields, an appropriate interest tax shield, and market-value capital weights, then rerun the valuation and disclose which inputs explain the change.

**Reciprocal review — unresolved:** The partner's judgment row and rationale have not been supplied, so a company-specific attack and the partner's actual answer cannot yet be recorded; neither is attributed to an invented participant.

The following are linked, condensed forecast statements. Depreciation, amortization and stock compensation are already included in the assumed operating cost structure; cash-flow addbacks do not add a second income-statement expense. Figures are rounded only for display.

| USD millions, forecast | FY2026 | FY2027 | FY2028 | FY2029 | FY2030 |
| --- | --- | --- | --- | --- | --- |
| Revenue | 436,969 | 458,818 | 481,758 | 505,846 | 531,139 |
| Cost of sales | 231,594 | 243,173 | 255,332 | 268,099 | 281,503 |
| Gross profit | 205,375 | 215,644 | 226,426 | 237,748 | 249,635 |
| SG&A | 29,779 | 31,268 | 32,832 | 34,473 | 36,197 |
| R&D | 37,142 | 38,999 | 40,949 | 42,997 | 45,147 |
| Operating income | 138,454 | 145,376 | 152,645 | 160,277 | 168,291 |
| Interest expense | 3,000 | 3,000 | 3,000 | 3,000 | 3,000 |
| Pretax income | 135,454 | 142,376 | 149,645 | 157,277 | 165,291 |
| Income taxes | 24,382 | 25,628 | 26,936 | 28,310 | 29,752 |
| Net income | 111,072 | 116,749 | 122,709 | 128,967 | 135,539 |

| USD millions, forecast | FY2026 | FY2027 | FY2028 | FY2029 | FY2030 |
| --- | --- | --- | --- | --- | --- |
| Cash | 35,934 | 35,934 | 35,934 | 35,934 | 35,934 |
| Marketable securities | 96,486 | 96,486 | 96,486 | 96,486 | 96,486 |
| Trade and vendor receivables | 76,605 | 80,435 | 84,457 | 88,680 | 93,114 |
| Inventory | 6,980 | 7,329 | 7,695 | 8,080 | 8,484 |
| Other current assets | 15,314 | 16,080 | 16,884 | 17,728 | 18,615 |
| Net PP&E | 53,973 | 58,022 | 62,031 | 66,041 | 70,088 |
| Other non-current assets | 83,727 | 83,727 | 83,727 | 83,727 | 83,727 |
| Total assets | 369,019 | 378,013 | 387,214 | 396,675 | 406,447 |
| Accounts payable | 73,222 | 76,883 | 80,727 | 84,764 | 89,002 |
| Deferred revenue | 9,508 | 9,983 | 10,482 | 11,006 | 11,557 |
| Other current liabilities | 66,387 | 66,387 | 66,387 | 66,387 | 66,387 |
| Other non-current liabilities | 41,549 | 41,549 | 41,549 | 41,549 | 41,549 |
| Borrowings | 98,657 | 98,657 | 98,657 | 98,657 | 98,657 |
| Total liabilities | 289,323 | 293,459 | 297,803 | 302,363 | 307,152 |
| Shareholders’ equity | 79,696 | 84,554 | 89,411 | 94,312 | 99,295 |
| Assets minus liabilities and equity | -0 | -0 | 0 | -0 | -0 |

| USD millions, forecast | FY2026 | FY2027 | FY2028 | FY2029 | FY2030 |
| --- | --- | --- | --- | --- | --- |
| Net income | 111,072 | 116,749 | 122,709 | 128,967 | 135,539 |
| PP&E depreciation addback | 8,970 | 9,715 | 10,444 | 11,166 | 11,887 |
| Other amortization addback | 3,883 | 4,077 | 4,281 | 4,495 | 4,720 |
| Stock compensation addback | 13,109 | 13,765 | 14,453 | 15,175 | 15,934 |
| Increase in operating working capital (use) | 1,824 | 808 | 849 | 891 | 936 |
| Cash from operations | 135,210 | 143,497 | 151,038 | 158,912 | 167,144 |
| PP&E capital spending (use) | 13,109 | 13,765 | 14,453 | 15,175 | 15,934 |
| Other-asset replacement spending (use) | 3,883 | 4,077 | 4,281 | 4,495 | 4,720 |
| Cash from investing | -16,992 | -17,842 | -18,734 | -19,670 | -20,654 |
| Net new borrowing | 0 | 0 | 0 | 0 | 0 |
| FCFE before dilution adjustment | 118,218 | 125,655 | 132,304 | 139,242 | 146,490 |
| Antidilution repurchases (use) | 13,109 | 13,765 | 14,453 | 15,175 | 15,934 |
| Remaining shareholder distribution (use) | 105,109 | 111,891 | 117,851 | 124,066 | 130,556 |
| Cash from financing | -118,218 | -125,655 | -132,304 | -139,242 | -146,490 |
| Net change in cash | 0 | 0 | 0 | 0 | 0 |

Working capital = trade and vendor receivables + inventory + other current assets − accounts payable − deferred revenue − other current liabilities. Cash, investments and borrowings are excluded. CFO = net income + depreciation + amortization + stock compensation − increase in working capital. Net PP&E = prior net PP&E + capital spending − depreciation. Equity = prior equity + net income + stock compensation − distributions − repurchases. There is no unexplained equity or financing plug.

| Historical cash flow, USD millions | FY2023 | FY2024 | FY2025 |
| --- | --- | --- | --- |
| CFO − PP&E capex | [99,584][K2023] | [108,807][K2024] | [98,767][K2025] |
| Net cash borrowing / (repayment) | [-9,901][K2023] | [-5,998][K2024] | [-8,483][K2025] |
| FCFE = CFO − capex + net borrowing | [89,683][K2023] | [102,809][K2024] | [90,284][K2025] |
| Status | Positive FCFE | Positive FCFE | Positive FCFE |

Historical FCFE here is a cash-based measure before an economic charge for dilution and before discretionary shareholder payouts. No historical or projected year requires a **negative FCFE** label. If a scenario becomes negative, retain the deficit and its funding requirement in the statements; a positive-cash-flow-only subtotal is not a complete equity valuation.

A perpetuity applied to negative cash flow is not a defensible positive going-concern terminal value without a funded path to sustainable positive cash flow.

For valuation, I use **FCFF after the economic cost of stock compensation** = FCFE − stock compensation + after-tax interest. This is discounted at WACC; FCFE itself is not discounted at WACC. Lease costs remain operating costs, so lease liabilities are not also deducted as financial debt.

| USD millions, forecast | FY2026 | FY2027 | FY2028 | FY2029 | FY2030 |
| --- | --- | --- | --- | --- | --- |
| FCFF used in valuation | 107,569 | 114,351 | 120,311 | 126,526 | 133,016 |

End-of-year discounting gives:
- Present value of FY2026–FY2030 FCFF: **$463.9bn**.
- Present value of terminal value: **$1363.3bn**.
- Enterprise value: **$1827.2bn**.
- Add cash and securities $132.420bn, less $20bn operating reserve and $98.657bn financial debt: **+$13.763bn**. Opening financial balances: [FY2025 balance sheet][K2025].
- Equity value: **$1841.0bn**, divided by 14.773260bn shares = **$124.61 per share**.

Terminal value = FY2030 FCFF × 1.025 / (0.09 − 0.025), discounted five years. It contributes **74.6%** of enterprise value. This explicitly assumes cash-flow growth settles to 2.5% with adequate reinvestment; the terminal period is not a sixth fully projected balance sheet.

| Value per share | Terminal growth 2% | 2.5% | 3% |
| --- | --- | --- | --- |
| 8% discount rate | $137.37 | $147.40 | $159.43 |
| 9% discount rate | $117.60 | $124.61 | $132.79 |
| 10% discount rate | $102.79 | $107.91 | $113.77 |

All five forecast balance sheets balance, cash-flow changes reconcile to cash, PP&E rolls forward, and equity rolls forward before rounding (maximum numerical error below $0.001m). Historical gross profit and net income reconcile to the supporting inputs, and all three provider capex comparisons match.

**Unresolved:** The video and its Part 1 template were not provided, so exact agreement with its denominator conventions cannot be verified. Organic/same-store growth is not disclosed. This is a simplified annual model with explicit tax, working-capital, financing and terminal assumptions, not a full tax/lease/security-level forecast.

[K2023]: https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm "Apple FY2023 Form 10-K"
[K2024]: https://www.sec.gov/Archives/edgar/data/320193/000032019324000123/aapl-20240928.htm "Apple FY2024 Form 10-K"
[K2025]: https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm "Apple FY2025 Form 10-K"
[Provider]: https://stockanalysis.com/stocks/aapl/financials/ "Stock Analysis Apple financials"


Dated market comparison (recorded snapshot, not a live quote)

No revolver draw is needed: forecast cash stays at $35.934 billion, above the $20 billion floor.

Holding the comparison to 14.773260 billion shares, the FY2025-based model says $124.61 per share, while the market says $336.94 as of September 24, 2026, at 2:06 p.m. EDT; what changes in growth, margins, or required return would explain that gap?

Quote source: https://stockanalysis.com/stocks/aapl/
The common share count is a comparison convention using the model's FY2025 denominator, not a claim that Apple's actual September 2026 share count is unchanged.

"""

"""Apple five-year linked statements; USD millions, shares in millions.

Adapted from the ABG teaching model; all Apple documentation is embedded above.
Standalone, standard library only. Run: python apple_submission.py
Valuation anchor: FY2025 close; NOT a September 2026 price target.
FY2025 source (Part II Item 8, pp. 29, 31, 33; Note 5):
https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm

Historical opening balances are separate from forward judgments. Depreciation,
amortization and stock compensation are already in operating costs; do not
subtract them again from operating income. See the embedded analysis above for the full
value / label / reason assumption table and history-source grid.
"""

from math import isfinite


# HISTORY: FY2025 closing balance sheet; retain all balances, not a net plug.
OPENING = {
    "year": 2025,
    "revenue": 416_161.0,
    "cost_of_sales": 220_960.0,
    "cash": 35_934.0,
    "securities": 96_486.0,  # 18,763 current + 77,723 non-current
    "receivables": 72_957.0,  # 39,777 trade + 33,180 vendor
    "inventory": 5_718.0,
    "other_current_assets": 14_585.0,
    "ppe": 49_834.0,
    "other_noncurrent_assets": 83_727.0,
    "accounts_payable": 69_860.0,
    "deferred_revenue": 9_055.0,
    "other_current_liabilities": 66_387.0,
    "other_noncurrent_liabilities": 41_549.0,
    "debt": 98_657.0,  # 7,979 commercial paper + 12,350 + 78,328 term debt
    "equity": 73_733.0,
}

# JUDGMENTS, with reasons: no five-year management guidance is used.
REVENUE_GROWTH = 0.05       # Moderate growth between recent annual outcomes.
GROSS_MARGIN = 0.47         # Hold near the latest historical margin.
SGA_TO_GROSS_PROFIT = 0.145 # Within the observed three-year range.
RD_TO_REVENUE = 0.085       # Reserve substantial ongoing development spending.
TAX_RATE = 0.18             # Normalize without repeating 2024's exceptional tax.
INVENTORY_DAYS = 11.0       # Ending inventory target near historical turnover.
DEPRECIATION_TO_OPENING_PPE = 0.18  # Explicit opening-net-PP&E roll-forward.
CAPEX_TO_REVENUE = 0.03     # Physical reinvestment near recent intensity.
BASE_OTHER_AMORTIZATION = 3_698.0  # FY25 D&A 11,698 minus rounded PP&E dep 8,000.
# Judgment: other amortization scales with sales; replacement investment equals
# it, maintaining the opening other non-current assets rather than depleting them.
SBC_TO_REVENUE = 0.03       # Charge shareholders for employee equity awards.
ANNUAL_INTEREST = 3_000.0   # Approximately 3% of fixed, refinanced borrowings.
OPERATING_CASH_RESERVE = 20_000.0  # Retain a liquidity buffer before excess cash.
WACC = 0.09                # Judgment hurdle rate; not a calibrated market CAPM.
TERMINAL_GROWTH = 0.025     # Mature growth below both forecast growth and WACC.
SHARES_OUTSTANDING = 14_773.260  # HISTORY: FY25 period-end shares, not average EPS shares.
YEARS = tuple(range(2026, 2031))
CHECK_TOLERANCE = 1e-7      # USD millions; only floating-point noise is tolerated.

# Remaining judgments:
# - Receivables, other current assets and deferred revenue retain opening sales
#   ratios; accounts payable retain their opening cost-of-sales ratio.
# - Other current liabilities and other non-current liabilities stay fixed.
# - Floor-plan financing: NONE. Supplier payables are modeled as operating debt.
# - Financial debt is refinanced unchanged; no net borrowing or revolver plug.
# - Securities stay fixed. Investment returns are excluded from operating value.
# - No acquisitions, disposals, impairments, OCI, FX or other equity changes.
# - Cash tax equals tax expense; no tax benefit is booked for a forecast loss.
# - Antidilution repurchases use SBC expense as a proxy for cost; distribute
#   remaining positive FCFE. Retain negative FCFE and reduce cash, never equity-
#   plug it away. Stop if the cash reserve would be breached.
# - Terminal FCFF grows at 2.5% with sufficient reinvestment implicit in the base.


ASSET_KEYS = (
    "cash", "securities", "receivables", "inventory", "other_current_assets",
    "ppe", "other_noncurrent_assets",
)
LIABILITY_KEYS = (
    "accounts_payable", "deferred_revenue", "other_current_liabilities",
    "other_noncurrent_liabilities", "debt",
)


def totals(row):
    row["assets"] = sum(row[key] for key in ASSET_KEYS)
    row["liabilities"] = sum(row[key] for key in LIABILITY_KEYS)
    row["liabilities_and_equity"] = row["liabilities"] + row["equity"]


def working_capital(row):
    return (row["receivables"] + row["inventory"] + row["other_current_assets"]
            - row["accounts_payable"] - row["deferred_revenue"]
            - row["other_current_liabilities"])


def require_zero(year, name, gap):
    if not isfinite(gap) or abs(gap) > CHECK_TOLERANCE:
        raise ValueError(
            f"FY{year} {name} failed: gap {gap:+.9f} USD millions; "
            "fix the assumption or statement link."
        )


def validate_inputs():
    for key, value in OPENING.items():
        if not isfinite(value):
            raise ValueError(f"FY2025 opening {key} must be finite")
    assumptions = {
        "growth": REVENUE_GROWTH, "gross margin": GROSS_MARGIN,
        "SG&A ratio": SGA_TO_GROSS_PROFIT, "R&D ratio": RD_TO_REVENUE,
        "tax": TAX_RATE, "inventory days": INVENTORY_DAYS,
        "depreciation": DEPRECIATION_TO_OPENING_PPE, "capex": CAPEX_TO_REVENUE,
        "amortization": BASE_OTHER_AMORTIZATION, "SBC": SBC_TO_REVENUE,
        "interest": ANNUAL_INTEREST, "cash reserve": OPERATING_CASH_RESERVE,
        "WACC": WACC, "terminal growth": TERMINAL_GROWTH,
        "shares": SHARES_OUTSTANDING,
    }
    if not all(isfinite(v) for v in assumptions.values()):
        raise ValueError("All assumptions must be finite")
    if not -1 < REVENUE_GROWTH:
        raise ValueError("Revenue growth must exceed -100%")
    for name in ("gross margin", "SG&A ratio", "R&D ratio", "tax", "depreciation"):
        if not 0 <= assumptions[name] <= 1:
            raise ValueError(f"{name} must be between 0 and 1")
    for name in ("inventory days", "capex", "amortization", "SBC", "interest", "cash reserve"):
        if assumptions[name] < 0:
            raise ValueError(f"{name} must be nonnegative")
    if not -1 < TERMINAL_GROWTH < WACC or WACC <= 0:
        raise ValueError("Require positive WACC and -100% < terminal growth < WACC")
    if SHARES_OUTSTANDING <= 0:
        raise ValueError("Share count must be positive")
    if OPENING["revenue"] <= 0 or OPENING["cost_of_sales"] <= 0:
        raise ValueError("Opening sales and cost of sales must be positive")
    opening = OPENING.copy()
    totals(opening)
    require_zero(2025, "opening balance sheet",
                 opening["assets"] - opening["liabilities_and_equity"])
    if OPENING["cash"] < OPERATING_CASH_RESERVE:
        raise ValueError(f"FY2025 cash reserve failed: gap "
                         f"{OPENING['cash'] - OPERATING_CASH_RESERVE:+.9f} USD millions")


def project():
    validate_inputs()
    prior = OPENING.copy()
    rows = []
    for year in YEARS:
        r = {"year": year, "revenue": prior["revenue"] * (1 + REVENUE_GROWTH)}
        r["gross_profit"] = r["revenue"] * GROSS_MARGIN
        r["cost_of_sales"] = r["revenue"] - r["gross_profit"]
        r["sga"] = r["gross_profit"] * SGA_TO_GROSS_PROFIT
        r["rd"] = r["revenue"] * RD_TO_REVENUE
        r["operating_income"] = r["gross_profit"] - r["sga"] - r["rd"]
        r["interest"] = ANNUAL_INTEREST
        r["pretax_income"] = r["operating_income"] - r["interest"]
        r["tax"] = max(0.0, r["pretax_income"]) * TAX_RATE
        r["net_income"] = r["pretax_income"] - r["tax"]
        r["depreciation"] = prior["ppe"] * DEPRECIATION_TO_OPENING_PPE
        r["amortization"] = BASE_OTHER_AMORTIZATION * r["revenue"] / OPENING["revenue"]
        r["sbc"] = r["revenue"] * SBC_TO_REVENUE
        r["capex"] = r["revenue"] * CAPEX_TO_REVENUE
        r["other_asset_investment"] = r["amortization"]
        r["ppe"] = prior["ppe"] + r["capex"] - r["depreciation"]
        for key in ("receivables", "other_current_assets", "deferred_revenue"):
            r[key] = OPENING[key] * r["revenue"] / OPENING["revenue"]
        r["inventory"] = r["cost_of_sales"] * INVENTORY_DAYS / 365
        r["accounts_payable"] = (OPENING["accounts_payable"] * r["cost_of_sales"]
                                 / OPENING["cost_of_sales"])
        for key in ("other_current_liabilities", "other_noncurrent_liabilities",
                    "securities", "debt"):
            r[key] = prior[key]
        r["other_noncurrent_assets"] = (prior["other_noncurrent_assets"]
                                        + r["other_asset_investment"] - r["amortization"])
        r["working_capital_change"] = working_capital(r) - working_capital(prior)
        r["net_borrowing"] = r["debt"] - prior["debt"]
        r["cfo"] = (r["net_income"] + r["depreciation"] + r["amortization"]
                    + r["sbc"] - r["working_capital_change"])
        r["cfi"] = -r["capex"] - r["other_asset_investment"]
        r["fcfe"] = r["cfo"] + r["cfi"] + r["net_borrowing"]
        r["owner_fcfe"] = r["fcfe"] - r["sbc"]
        r["buybacks"] = min(r["sbc"], max(0.0, r["fcfe"]))
        r["distribution"] = max(0.0, r["fcfe"] - r["buybacks"])
        r["cff"] = r["net_borrowing"] - r["buybacks"] - r["distribution"]
        # Compute cash from flows, never as assets minus liabilities and equity.
        r["cash_change"] = r["cfo"] + r["cfi"] + r["cff"]
        r["cash"] = prior["cash"] + r["cash_change"]
        r["equity"] = (prior["equity"] + r["net_income"] + r["sbc"]
                       - r["buybacks"] - r["distribution"])
        unlevered_tax = max(0.0, r["operating_income"]) * TAX_RATE
        r["interest_tax_shield"] = unlevered_tax - r["tax"]
        r["fcff"] = (r["owner_fcfe"] - r["net_borrowing"] + r["interest"]
                     - r["interest_tax_shield"])
        totals(r)
        rows.append(r)
        prior = r
    return rows


def assert_balanced(rows):
    """Independently recalculate checks; refuse valuation on any failure."""
    validate_inputs()
    if [r["year"] for r in rows] != list(YEARS):
        raise ValueError("Require exactly FY2026-FY2030 in chronological order")
    prior = OPENING
    checks = []
    for r in rows:
        year = r["year"]
        if not all(isfinite(v) for v in r.values()):
            raise ValueError(f"FY{year} contains a nonfinite statement value")
        gaps = {
            "balance sheet": sum(r[k] for k in ASSET_KEYS)
                - sum(r[k] for k in LIABILITY_KEYS) - r["equity"],
            "cash roll-forward": r["cash"] - prior["cash"] - r["cfo"] - r["cfi"] - r["cff"],
            "PP&E roll-forward": r["ppe"] - prior["ppe"] - r["capex"] + r["depreciation"],
            "equity roll-forward": r["equity"] - prior["equity"] - r["net_income"]
                - r["sbc"] + r["buybacks"] + r["distribution"],
            "operating cash flow": r["cfo"] - r["net_income"] - r["depreciation"]
                - r["amortization"] - r["sbc"] + working_capital(r) - working_capital(prior),
            "net income": r["net_income"] - (r["revenue"] - r["cost_of_sales"]
                - r["sga"] - r["rd"] - r["interest"] - r["tax"]),
            "FCFE": r["fcfe"] - r["cfo"] + r["capex"] + r["other_asset_investment"]
                - (r["debt"] - prior["debt"]),
            "FCFF": r["fcff"] - (r["operating_income"]
                - max(0.0, r["operating_income"]) * TAX_RATE
                + r["depreciation"] + r["amortization"] - r["capex"]
                - r["other_asset_investment"] - working_capital(r) + working_capital(prior)),
        }
        for name, gap in gaps.items():
            require_zero(year, name, gap)
        cash_gap = r["cash"] - OPERATING_CASH_RESERVE
        if cash_gap < -CHECK_TOLERANCE:
            raise ValueError(f"FY{year} cash reserve failed: gap {cash_gap:+.9f} USD millions; "
                             "fund the shortfall or change the operating assumptions.")
        for key in ("cash", "inventory", "ppe", "other_noncurrent_assets", "debt"):
            if r[key] < -CHECK_TOLERANCE:
                raise ValueError(f"FY{year} {key} is negative: {r[key]:+.9f}")
        checks.append((year, gaps, cash_gap))
        prior = r
    return checks


def value(rows):
    assert_balanced(rows)
    # Do not conceal cash deficits by clipping them into a full company value.
    if any(r["owner_fcfe"] < 0 or r["fcff"] <= 0 for r in rows):
        positive_pv = sum(max(0.0, r["fcff"]) / (1 + WACC) ** i
                          for i, r in enumerate(rows, 1))
        raise ValueError(
            f"Positive explicit FCFF PV only: {positive_pv:,.3f} USD millions. "
            "A loss-year scenario needs a funded recovery before a full value per share; "
            "negative cash flow cannot support a positive going-concern perpetuity."
        )
    pv_explicit = sum(r["fcff"] / (1 + WACC) ** i for i, r in enumerate(rows, 1))
    terminal = rows[-1]["fcff"] * (1 + TERMINAL_GROWTH) / (WACC - TERMINAL_GROWTH)
    pv_terminal = terminal / (1 + WACC) ** len(rows)
    enterprise = pv_explicit + pv_terminal
    # Operating leases remain in operating expenses; do not deduct them again.
    bridge = OPENING["cash"] + OPENING["securities"] - OPERATING_CASH_RESERVE - OPENING["debt"]
    equity = enterprise + bridge
    return {"pv_explicit": pv_explicit, "pv_terminal": pv_terminal,
            "enterprise": enterprise, "bridge": bridge, "equity": equity,
            "per_share": equity / SHARES_OUTSTANDING,
            "terminal_fraction": pv_terminal / enterprise}


def print_table(title, lines, rows):
    print(f"\n{title} (USD millions)")
    print(f"{'Line':<31}" + "".join(f"FY{r['year']}E".rjust(14) for r in rows))
    for label, key in lines:
        print(f"{label:<31}" + "".join(f"{r[key]:14,.3f}" for r in rows))


def main():
    print("APPLE | FY2025-anchored five-year model | standard library only")
    print("Inputs and reasons: embedded analysis. Forecasts are judgments, not guidance.")
    print("Floor-plan financing: none. Separate operating supplier payables.")
    rows = project()
    print_table("Income statement", (
        ("Revenue", "revenue"), ("Cost of sales", "cost_of_sales"),
        ("Gross profit", "gross_profit"), ("SG&A", "sga"), ("R&D", "rd"),
        ("Operating income", "operating_income"), ("Interest", "interest"),
        ("Pretax income", "pretax_income"), ("Tax", "tax"), ("Net income", "net_income"),
    ), rows)
    print_table("Balance sheet", (
        ("Cash", "cash"), ("Marketable securities", "securities"),
        ("Trade/vendor receivables", "receivables"), ("Inventory", "inventory"),
        ("Other current assets", "other_current_assets"), ("Net PP&E", "ppe"),
        ("Other noncurrent assets", "other_noncurrent_assets"), ("Total assets", "assets"),
        ("Accounts payable", "accounts_payable"), ("Deferred revenue", "deferred_revenue"),
        ("Other current liabilities", "other_current_liabilities"),
        ("Other noncurrent liabilities", "other_noncurrent_liabilities"),
        ("Borrowings", "debt"), ("Equity", "equity"),
        ("Liabilities + equity", "liabilities_and_equity"),
    ), rows)
    print_table("Cash flow and valuation cash flows", (
        ("Net income", "net_income"), ("PP&E depreciation", "depreciation"),
        ("Other amortization", "amortization"), ("Stock compensation", "sbc"),
        ("Increase in working capital", "working_capital_change"), ("Operating cash flow", "cfo"),
        ("PP&E capex (use)", "capex"), ("Other reinvestment (use)", "other_asset_investment"),
        ("Investing cash flow", "cfi"), ("Net borrowing", "net_borrowing"),
        ("FCFE before dilution cost", "fcfe"), ("FCFE after dilution cost", "owner_fcfe"),
        ("Antidilution buybacks (use)", "buybacks"), ("Other distribution (use)", "distribution"),
        ("Financing cash flow", "cff"), ("Change in cash", "cash_change"),
        ("FCFF after dilution cost", "fcff"),
    ), rows)
    for r in rows:
        status = "negative FCFE" if r["fcfe"] < 0 else "positive FCFE"
        print(f"FY{r['year']}: {status}; after-dilution FCFE={r['owner_fcfe']:,.3f}")
    print("\nCHECK BLOCK (gaps in USD millions; full-precision checks precede valuation)")
    checks = assert_balanced(rows)
    opening_assets = sum(OPENING[key] for key in ASSET_KEYS)
    print(f"FY2025 opening balance sheet: PASS; assets = liabilities + equity = {opening_assets:,.3f}")
    for year, gaps, headroom in checks:
        print(f"FY{year}: " + "; ".join(f"{name} gap={gap:+.9f}" for name, gap in gaps.items()))
        print(f"        cash reserve headroom={headroom:,.3f}; PASS")
    v = value(rows)
    print("\nVALUATION: dilution-adjusted FCFF discounted at WACC")
    print(f"WACC={WACC:.2%}; terminal growth={TERMINAL_GROWTH:.2%}; end-year discounting")
    for label, key in (("PV of five explicit years", "pv_explicit"),
                       ("PV of terminal value", "pv_terminal"),
                       ("Enterprise value", "enterprise"),
                       ("Excess financial assets less debt", "bridge"),
                       ("Equity value", "equity")):
        print(f"{label}: {v[key]:,.3f} USD millions")
    print(f"Shares: {SHARES_OUTSTANDING:,.3f} million (FY2025 year-end)")
    print(f"Value per share: ${v['per_share']:.2f}")
    print(f"Terminal share of enterprise value: {v['terminal_fraction']:.2%}")
    print("FY2025-based illustrative value, not a current market-price target.")
    print("No revolver draw: cash remains $35.934bn, above the $20bn floor in this base case.")
    print("\nDATED MARKET COMPARISON (recorded snapshot, not a live quote)")
    print(f"Holding the comparison to {SHARES_OUTSTANDING / 1000:.6f} billion shares, "
          f"the FY2025-based model says ${v['per_share']:.2f} per share, while the market "
          "says $336.94 as of September 24, 2026, at 2:06 p.m. EDT; what changes in "
          "growth, margins, or required return would explain that gap?")
    print("Quote source: https://stockanalysis.com/stocks/aapl/")



if __name__ == "__main__":
    try:
        main()
    except ValueError as exc:
        raise SystemExit(f"MODEL REFUSED: {exc}") from exc


# CAPTURED SUCCESSFUL RUN - SEPTEMBER 24, 2026
# Exit status: 0. Full output follows; checks were not disabled.
# APPLE | FY2025-anchored five-year model | standard library only
# Inputs and reasons: embedded analysis. Forecasts are judgments, not guidance.
# Floor-plan financing: none. Separate operating supplier payables.
# 
# Income statement (USD millions)
# Line                                  FY2026E       FY2027E       FY2028E       FY2029E       FY2030E
# Revenue                           436,969.050   458,817.503   481,758.378   505,846.297   531,138.611
# Cost of sales                     231,593.597   243,173.276   255,331.940   268,098.537   281,503.464
# Gross profit                      205,375.454   215,644.226   226,426.437   237,747.759   249,635.147
# SG&A                               29,779.441    31,268.413    32,831.833    34,473.425    36,197.096
# R&D                                37,142.369    38,999.488    40,949.462    42,996.935    45,146.782
# Operating income                  138,453.643   145,376.326   152,645.142   160,277.399   168,291.269
# Interest                            3,000.000     3,000.000     3,000.000     3,000.000     3,000.000
# Pretax income                     135,453.643   142,376.326   149,645.142   157,277.399   165,291.269
# Tax                                24,381.656    25,627.739    26,936.126    28,309.932    29,752.428
# Net income                        111,071.988   116,748.587   122,709.016   128,967.467   135,538.841
# 
# Balance sheet (USD millions)
# Line                                  FY2026E       FY2027E       FY2028E       FY2029E       FY2030E
# Cash                               35,934.000    35,934.000    35,934.000    35,934.000    35,934.000
# Marketable securities              96,486.000    96,486.000    96,486.000    96,486.000    96,486.000
# Trade/vendor receivables           76,604.850    80,435.093    84,456.847    88,679.689    93,113.674
# Inventory                           6,979.533     7,328.510     7,694.935     8,079.682     8,483.666
# Other current assets               15,314.250    16,079.963    16,883.961    17,728.159    18,614.567
# Net PP&E                           53,972.951    58,022.345    62,031.074    66,040.870    70,087.672
# Other noncurrent assets            83,727.000    83,727.000    83,727.000    83,727.000    83,727.000
# Total assets                      369,018.585   378,012.910   387,213.817   396,675.400   406,446.578
# Accounts payable                   73,221.980    76,883.079    80,727.233    84,763.594    89,001.774
# Deferred revenue                    9,507.750     9,983.138    10,482.294    11,006.409    11,556.730
# Other current liabilities          66,387.000    66,387.000    66,387.000    66,387.000    66,387.000
# Other noncurrent liabilities       41,549.000    41,549.000    41,549.000    41,549.000    41,549.000
# Borrowings                         98,657.000    98,657.000    98,657.000    98,657.000    98,657.000
# Equity                             79,695.855    84,553.694    89,411.290    94,312.397    99,295.075
# Liabilities + equity              369,018.585   378,012.910   387,213.817   396,675.400   406,446.578
# 
# Cash flow and valuation cash flows (USD millions)
# Line                                  FY2026E       FY2027E       FY2028E       FY2029E       FY2030E
# Net income                        111,071.988   116,748.587   122,709.016   128,967.467   135,538.841
# PP&E depreciation                   8,970.120     9,715.131    10,444.022    11,165.593    11,887.357
# Other amortization                  3,882.900     4,077.045     4,280.897     4,494.942     4,719.689
# Stock compensation                 13,109.072    13,764.525    14,452.751    15,175.389    15,934.158
# Increase in working capital         1,823.903       808.445       848.867       891.311       935.876
# Operating cash flow               135,210.176   143,496.843   151,037.820   158,912.081   167,144.168
# PP&E capex (use)                   13,109.072    13,764.525    14,452.751    15,175.389    15,934.158
# Other reinvestment (use)            3,882.900     4,077.045     4,280.897     4,494.942     4,719.689
# Investing cash flow               -16,991.971   -17,841.570   -18,733.649   -19,670.331   -20,653.848
# Net borrowing                           0.000         0.000         0.000         0.000         0.000
# FCFE before dilution cost         118,218.204   125,655.273   132,304.171   139,241.750   146,490.321
# FCFE after dilution cost          105,109.133   111,890.748   117,851.420   124,066.361   130,556.163
# Antidilution buybacks (use)        13,109.072    13,764.525    14,452.751    15,175.389    15,934.158
# Other distribution (use)          105,109.133   111,890.748   117,851.420   124,066.361   130,556.163
# Financing cash flow              -118,218.204  -125,655.273  -132,304.171  -139,241.750  -146,490.321
# Change in cash                          0.000         0.000         0.000         0.000         0.000
# FCFF after dilution cost          107,569.133   114,350.748   120,311.420   126,526.361   133,016.163
# FY2026: positive FCFE; after-dilution FCFE=105,109.133
# FY2027: positive FCFE; after-dilution FCFE=111,890.748
# FY2028: positive FCFE; after-dilution FCFE=117,851.420
# FY2029: positive FCFE; after-dilution FCFE=124,066.361
# FY2030: positive FCFE; after-dilution FCFE=130,556.163
# 
# CHECK BLOCK (gaps in USD millions; full-precision checks precede valuation)
# FY2025 opening balance sheet: PASS; assets = liabilities + equity = 359,241.000
# FY2026: balance sheet gap=-0.000000000; cash roll-forward gap=+0.000000000; PP&E roll-forward gap=-0.000000000; equity roll-forward gap=+0.000000000; operating cash flow gap=-0.000000000; net income gap=+0.000000000; FCFE gap=+0.000000000; FCFF gap=-0.000000000
#         cash reserve headroom=15,934.000; PASS
# FY2027: balance sheet gap=-0.000000000; cash roll-forward gap=+0.000000000; PP&E roll-forward gap=-0.000000000; equity roll-forward gap=+0.000000000; operating cash flow gap=+0.000000000; net income gap=+0.000000000; FCFE gap=+0.000000000; FCFF gap=+0.000000000
#         cash reserve headroom=15,934.000; PASS
# FY2028: balance sheet gap=-0.000000000; cash roll-forward gap=+0.000000000; PP&E roll-forward gap=+0.000000000; equity roll-forward gap=+0.000000000; operating cash flow gap=-0.000000000; net income gap=+0.000000000; FCFE gap=+0.000000000; FCFF gap=+0.000000000
#         cash reserve headroom=15,934.000; PASS
# FY2029: balance sheet gap=-0.000000000; cash roll-forward gap=+0.000000000; PP&E roll-forward gap=-0.000000000; equity roll-forward gap=-0.000000000; operating cash flow gap=-0.000000000; net income gap=-0.000000000; FCFE gap=+0.000000000; FCFF gap=-0.000000000
#         cash reserve headroom=15,934.000; PASS
# FY2030: balance sheet gap=-0.000000000; cash roll-forward gap=+0.000000000; PP&E roll-forward gap=+0.000000000; equity roll-forward gap=+0.000000000; operating cash flow gap=-0.000000000; net income gap=+0.000000000; FCFE gap=-0.000000000; FCFF gap=+0.000000000
#         cash reserve headroom=15,934.000; PASS
# 
# VALUATION: dilution-adjusted FCFF discounted at WACC
# WACC=9.00%; terminal growth=2.50%; end-year discounting
# PV of five explicit years: 463,922.348 USD millions
# PV of terminal value: 1,363,271.744 USD millions
# Enterprise value: 1,827,194.093 USD millions
# Excess financial assets less debt: 13,763.000 USD millions
# Equity value: 1,840,957.093 USD millions
# Shares: 14,773.260 million (FY2025 year-end)
# Value per share: $124.61
# Terminal share of enterprise value: 74.61%
# FY2025-based illustrative value, not a current market-price target.
# No revolver draw: cash remains $35.934bn, above the $20bn floor in this base case.
# 
# DATED MARKET COMPARISON (recorded snapshot, not a live quote)
# Holding the comparison to 14.773260 billion shares, the FY2025-based model says $124.61 per share, while the market says $336.94 as of September 24, 2026, at 2:06 p.m. EDT; what changes in growth, margins, or required return would explain that gap?
# Quote source: https://stockanalysis.com/stocks/aapl/
