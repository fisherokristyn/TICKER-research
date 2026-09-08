# Editable inputs: money and shares are in millions; rates are decimals.
STARTING_FCFF = 100.0
YEARLY_GROWTH_RATES = (0.08, 0.06, 0.05, 0.04, 0.03)
WACC = 0.10
TERMINAL_GROWTH = 0.03
NON_OPERATING_CASH = 50.0
DEBT = 300.0
DILUTED_SHARES = 50.0


def main():
    if TERMINAL_GROWTH >= WACC:
        raise SystemExit("Error: terminal growth must be less than WACC.")
    if len(YEARLY_GROWTH_RATES) != 5:
        raise SystemExit("Error: provide exactly five yearly growth rates.")
    if WACC <= -1:
        raise SystemExit("Error: WACC must be greater than -1.")
    if DILUTED_SHARES <= 0:
        raise SystemExit("Error: diluted shares must be greater than zero.")

    yearly_fcff = []
    fcff = STARTING_FCFF
    for growth in YEARLY_GROWTH_RATES:
        fcff *= 1 + growth
        yearly_fcff.append(fcff)

    pv_explicit_fcff = sum(
        amount / (1 + WACC) ** year
        for year, amount in enumerate(yearly_fcff, start=1)
    )
    terminal_value = yearly_fcff[-1] * (1 + TERMINAL_GROWTH) / (WACC - TERMINAL_GROWTH)
    pv_terminal_value = terminal_value / (1 + WACC) ** len(yearly_fcff)
    enterprise_value = pv_explicit_fcff + pv_terminal_value
    equity_value = enterprise_value + NON_OPERATING_CASH - DEBT
    value_per_share = equity_value / DILUTED_SHARES
    if enterprise_value == 0:
        raise SystemExit("Error: terminal-value share is undefined when enterprise value is zero.")
    terminal_value_share = pv_terminal_value / enterprise_value

    for year, amount in enumerate(yearly_fcff, start=1):
        print(f"FCFF Year {year} (USD millions): {amount:.4f}")
    print(f"Present value of five explicit FCFF (USD millions): {pv_explicit_fcff:.4f}")
    print(f"Terminal value at Year 5 (USD millions): {terminal_value:.4f}")
    print(f"Present value of terminal value (USD millions): {pv_terminal_value:.4f}")
    print(f"Enterprise value (USD millions): {enterprise_value:.4f}")
    print(f"Equity value (USD millions): {equity_value:.4f}")
    print(f"Value per diluted share (USD): {value_per_share:.4f}")
    print(f"Present value of terminal value / enterprise value (decimal): {terminal_value_share:.4f}")


if __name__ == "__main__":
    main()
