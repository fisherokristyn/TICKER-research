# Editable inputs: money and shares are in millions; rates are decimals.
STARTING_FCFF = 100.0
YEARLY_GROWTH_RATES = (0.08, 0.06, 0.05, 0.04, 0.03)
WACC = 0.10
TERMINAL_GROWTH = 0.03
NON_OPERATING_CASH = 50.0
DEBT = 300.0
DILUTED_SHARES = 50.0

# Additional editable inputs: bounds are decimal shifts (0.01 = 1 percentage point).
SENSITIVITY_WACCS = [0.09, 0.10, 0.11]
SENSITIVITY_TERMINAL_GROWTH_RATES = [0.02, 0.03, 0.04]
# AAPL quote: September 10, 2026, 1:51 PM EDT; USD per share.
# Source: https://stockanalysis.com/stocks/aapl/
# Other inputs remain training values; this is not an Apple-calibrated model.
TARGET_SHARE_PRICE = 325.25
REVERSE_SHIFT_LOWER = -0.05
REVERSE_SHIFT_UPPER = 0.10


def scenario_value(wacc, terminal_growth, growth_shift=0.0):
    """Value a scenario without changing any base inputs."""
    fcff = STARTING_FCFF
    present_value = 0.0
    for year, growth in enumerate(YEARLY_GROWTH_RATES, start=1):
        fcff *= 1 + growth + growth_shift
        present_value += fcff / (1 + wacc) ** year
    terminal_value = fcff * (1 + terminal_growth) / (wacc - terminal_growth)
    enterprise_value = present_value + terminal_value / (1 + wacc) ** 5
    return (enterprise_value + NON_OPERATING_CASH - DEBT) / DILUTED_SHARES


def print_sensitivity():
    print("\nSensitivity: value per diluted share (USD)")
    print("Rows: WACC; columns: terminal growth; other base inputs held fixed.")
    width = 14
    print(f"{'WACC / g':>{width}}" + "".join(
        f"{growth:>{width}.2%}" for growth in SENSITIVITY_TERMINAL_GROWTH_RATES
    ))
    for wacc in SENSITIVITY_WACCS:
        cells = []
        for growth in SENSITIVITY_TERMINAL_GROWTH_RATES:
            if growth >= wacc or wacc <= -1:
                cells.append(f"{'INVALID':>{width}}")
            else:
                cells.append(f"{scenario_value(wacc, growth):>{width}.4f}")
        print(f"{wacc:>{width}.2%}" + "".join(cells))


def print_reverse_dcf():
    import math

    print("\nReverse DCF: uniform shift to all five explicit growth rates")
    print(f"Target share price (USD): {TARGET_SHARE_PRICE:.4f}")
    print(f"Shift bracket (percentage points): {REVERSE_SHIFT_LOWER * 100:.4f} to {REVERSE_SHIFT_UPPER * 100:.4f}")
    print("Held fixed:")
    print(f"  Starting FCFF (USD millions): {STARTING_FCFF:.4f}")
    print("  Base growth rates: " + ", ".join(f"{g:.4%}" for g in YEARLY_GROWTH_RATES))
    print("  Only the common additive shift varies; growth-rate differences stay fixed.")
    print(f"  WACC: {WACC:.4%}; terminal growth: {TERMINAL_GROWTH:.4%}")
    print(f"  Non-operating cash (USD millions): {NON_OPERATING_CASH:.4f}")
    print(f"  Debt (USD millions): {DEBT:.4f}")
    print(f"  Diluted shares (millions): {DILUTED_SHARES:.4f}")
    print("  Five explicit years, annual end-of-year discounting, Gordon terminal value.")

    lower, upper = REVERSE_SHIFT_LOWER, REVERSE_SHIFT_UPPER
    if not all(math.isfinite(x) for x in (lower, upper, TARGET_SHARE_PRICE)):
        print("Invalid reverse-DCF inputs: target and bounds must be finite.")
        return
    if lower >= upper:
        print("Invalid bracket: lower shift must be less than upper shift.")
        return
    if any(g + bound <= -1 for g in YEARLY_GROWTH_RATES for bound in (lower, upper)):
        print("Invalid bracket: an annual growth rate reaches -100% or below.")
        return

    def residual(shift):
        return scenario_value(WACC, TERMINAL_GROWTH, shift) - TARGET_SHARE_PRICE

    f_lower, f_upper = residual(lower), residual(upper)
    if not all(math.isfinite(x) for x in (f_lower, f_upper)):
        print("Cannot solve: bracket valuations are not finite.")
        return
    if f_lower == 0 and f_upper == 0:
        print("No unique solved shift: every shift in this bracket matches the target.")
        return
    if f_lower == 0:
        solved = lower
    elif f_upper == 0:
        solved = upper
    elif (f_lower > 0) == (f_upper > 0):
        print("No solution in that bracket.")
        return
    else:
        for _ in range(200):
            solved = (lower + upper) / 2
            f_mid = residual(solved)
            if abs(f_mid) <= 1e-10:
                break
            if (f_mid > 0) == (f_lower > 0):
                lower, f_lower = solved, f_mid
            else:
                upper = solved
        else:
            print("No solution reported: bisection did not reach the price tolerance.")
            return

    print(f"Solved uniform shift (percentage points): {solved * 100:.8f}")
    print(f"Solved uniform shift (decimal): {solved:.10f}")
    print("Resulting growth rates: " + ", ".join(
        f"{g + solved:.6%}" for g in YEARLY_GROWTH_RATES
    ))
    print(f"Matched value per diluted share (USD): {scenario_value(WACC, TERMINAL_GROWTH, solved):.4f}")


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
    print_sensitivity()
    print_reverse_dcf()


if __name__ == "__main__":
    main()
