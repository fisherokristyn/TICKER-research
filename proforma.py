"""Five-year ABG three-statement teaching model (USD millions).

Editable inputs preserve the labels supplied in the case: fact, history,
guidance, or judgment. Standard library only.
"""

# Opening FY2025 balance sheet and operating base (case inputs)
OPENING = {
    "revenue": 17_999.0,
    "inventory": 2_135.8,
    "ppe": 3_070.4,
    "other_assets": 6_371.6,
    "cash": 40.4,
    "floor_plan": 2_027.0,
    "term_debt": 3_572.0,
    "revolver": 0.0,
    "other_liabilities": 2_127.5,
    "equity": 3_891.7,
}

# Assumptions and provenance labels
ORGANIC_REVENUE_GROWTH = 0.018                 # judgment
GROSS_MARGIN = 0.1705                          # judgment
SGA_TO_GROSS_PROFIT = (0.665, 0.655, 0.645, 0.645, 0.645)  # judgment
DEPRECIATION_TO_OPENING_PPE = 82.4 / 3_070.4   # history
ANNUAL_IMPAIRMENT = 120.0                      # judgment; non-cash
ANNUAL_CAPEX = 250.0                           # guidance
TAX_RATE = 0.255                               # judgment
INVENTORY_DAYS = 2_135.8 / (17_999.0 - 3_071.7) * 365  # history
FLOOR_PLAN_TO_INVENTORY = 2_027.0 / 2_135.8    # history
OTHER_WORKING_CAPITAL_TO_REVENUE_CHANGE = 0.008  # judgment
MINIMUM_CASH = 25.0                            # history
REVOLVER_LIMIT = 850.0                         # judgment
REVOLVER_RATE = 0.06                           # judgment
ANNUAL_DEBT_REPAYMENT = 150.0                  # judgment
ANNUAL_SHARE_BUYBACK = 150.0                   # judgment
FLOOR_PLAN_RATE = 0.0467                       # history
TERM_DEBT_RATE = 0.0544                        # history
COST_OF_EQUITY = 0.10                          # judgment
TERMINAL_GROWTH = 0.025                        # judgment
SHARES_OUTSTANDING = 17.951349                 # fact; millions, 2026-06-30 10-Q

YEARS = tuple(range(2026, 2031))


def project():
    """Project the linked statements, computing cash last in every year."""
    prior = OPENING.copy()
    rows = []

    for year, sga_ratio in zip(YEARS, SGA_TO_GROSS_PROFIT):
        # Income statement
        revenue = prior["revenue"] * (1 + ORGANIC_REVENUE_GROWTH)
        gross_profit = revenue * GROSS_MARGIN
        cost_of_sales = revenue - gross_profit
        sga = gross_profit * sga_ratio
        depreciation = prior["ppe"] * DEPRECIATION_TO_OPENING_PPE
        impairment = ANNUAL_IMPAIRMENT
        operating_income = gross_profit - sga - depreciation - impairment
        interest = (prior["floor_plan"] * FLOOR_PLAN_RATE
                    + prior["term_debt"] * TERM_DEBT_RATE
                    + prior["revolver"] * REVOLVER_RATE)
        pretax_income = operating_income - interest
        tax = max(0.0, pretax_income) * TAX_RATE
        net_income = pretax_income - tax

        # Balance sheet except cash
        inventory = cost_of_sales * INVENTORY_DAYS / 365
        floor_plan = inventory * FLOOR_PLAN_TO_INVENTORY
        ppe = prior["ppe"] + ANNUAL_CAPEX - depreciation
        revenue_change = revenue - prior["revenue"]
        other_working_capital_change = (
            OTHER_WORKING_CAPITAL_TO_REVENUE_CHANGE * revenue_change
        )
        other_assets = prior["other_assets"] + other_working_capital_change - impairment
        debt_repayment = min(ANNUAL_DEBT_REPAYMENT, prior["term_debt"])
        term_debt = prior["term_debt"] - debt_repayment
        other_liabilities = prior["other_liabilities"]
        equity = prior["equity"] + net_income - ANNUAL_SHARE_BUYBACK

        # Cash flow to equity, then cash and revolver last
        fcfe = (net_income + depreciation + impairment - ANNUAL_CAPEX
                - (inventory - prior["inventory"])
                - other_working_capital_change
                + (floor_plan - prior["floor_plan"])
                - debt_repayment)
        cash_before_financing = prior["cash"] + fcfe - ANNUAL_SHARE_BUYBACK
        revolver = prior["revolver"]
        cash = cash_before_financing

        if cash < MINIMUM_CASH:
            draw = MINIMUM_CASH - cash
            if revolver + draw > REVOLVER_LIMIT:
                raise ValueError(f"FY{year}E revolver limit exceeded")
            revolver += draw
            cash += draw
        elif revolver > 0:
            repayment = min(revolver, cash - MINIMUM_CASH)
            revolver -= repayment
            cash -= repayment

        row = {
            "year": year, "revenue": revenue, "gross_profit": gross_profit,
            "sga": sga, "depreciation": depreciation,
            "impairment": impairment, "operating_income": operating_income,
            "interest": interest, "pretax_income": pretax_income,
            "tax": tax, "net_income": net_income, "inventory": inventory,
            "ppe": ppe, "other_assets": other_assets, "cash": cash,
            "floor_plan": floor_plan, "term_debt": term_debt,
            "revolver": revolver, "other_liabilities": other_liabilities,
            "equity": equity, "fcfe": fcfe,
        }
        row["assets"] = cash + inventory + ppe + other_assets
        row["liabilities_and_equity"] = (
            floor_plan + term_debt + revolver + other_liabilities + equity
        )
        row["balance_gap"] = row["assets"] - row["liabilities_and_equity"]
        rows.append(row)
        prior = row

    return rows


def assert_balanced(rows):
    """Refuse to value statements that fail either required check."""
    for row in rows:
        if abs(row["balance_gap"]) > 1e-7:
            raise ValueError(
                f"FY{row['year']}E balance check failed: gap {row['balance_gap']:.1f}"
            )
        if row["cash"] + 1e-7 < MINIMUM_CASH:
            raise ValueError(
                f"FY{row['year']}E cash check failed: "
                f"{row['cash']:.1f} below {MINIMUM_CASH:.1f}"
            )


def print_table(title, lines, rows):
    print(f"\n{title} (USD millions)")
    print(f"{'Line':<24}" + "".join(f"FY{r['year']}E".rjust(12) for r in rows))
    for label, key in lines:
        print(f"{label:<24}" + "".join(f"{r[key]:12.1f}" for r in rows))


def main():
    rows = project()
    print_table("Income statement", (
        ("Revenue", "revenue"), ("Gross profit", "gross_profit"),
        ("SG&A", "sga"), ("Depreciation", "depreciation"),
        ("Impairment", "impairment"), ("Operating income", "operating_income"),
        ("Interest", "interest"), ("Pretax income", "pretax_income"),
        ("Tax", "tax"), ("Net income", "net_income"),
    ), rows)
    print_table("Balance sheet", (
        ("Cash", "cash"), ("Inventory", "inventory"), ("PP&E", "ppe"),
        ("Other assets", "other_assets"), ("Total assets", "assets"),
        ("Floor plan", "floor_plan"), ("Term debt", "term_debt"),
        ("Revolver", "revolver"), ("Other liabilities", "other_liabilities"),
        ("Equity", "equity"), ("Liabilities + equity", "liabilities_and_equity"),
    ), rows)
    print_table("Cash flow", (("Free cash flow to equity", "fcfe"),), rows)

    print("\nChecks")
    for row in rows:
        cash_check = row["cash"] >= MINIMUM_CASH - 1e-7
        print(f"FY{row['year']}E: assets - liabilities - equity = "
              f"{row['balance_gap']:.1f}; cash >= minimum = {cash_check}")
    assert_balanced(rows)

    pv_fcfe = sum(r["fcfe"] / (1 + COST_OF_EQUITY) ** i
                  for i, r in enumerate(rows, start=1))
    sustainable_fcfe = rows[-1]["fcfe"] + ANNUAL_DEBT_REPAYMENT
    terminal_value_2030 = (sustainable_fcfe * (1 + TERMINAL_GROWTH)
                           / (COST_OF_EQUITY - TERMINAL_GROWTH))
    pv_terminal = terminal_value_2030 / (1 + COST_OF_EQUITY) ** len(rows)
    equity_value = pv_fcfe + pv_terminal
    value_per_share = equity_value / SHARES_OUTSTANDING

    print("\nEquity valuation")
    print(f"Equity value (USD millions): {equity_value:.1f}")
    print(f"Share of value after 2030: {pv_terminal / equity_value:.1%}")
    print(f"Value per share: ${value_per_share:.2f}")


if __name__ == "__main__":
    main()
