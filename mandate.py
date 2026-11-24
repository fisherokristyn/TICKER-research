
# FIN 43900 - Lab 13
# Meridian Foundation Portfolio Mandate Checker

# -----------------------------
# EDITABLE INPUTS
# -----------------------------

RESERVE_SIZE = 100.0  # USD millions
QUARTERLY_DISTRIBUTION = 0.75
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW = 5
MIN_LIQUID_SHARE = 90.0
ISSUER_LIMIT = 8.0

# Holding: (issuer, business days to redeem, reserve-eligible)

holdings = {
    "Cash": ("none", 0, True),
    "Treasury bills": ("U.S. Treasury", 1, True),
    "Treasury 10-year note": ("U.S. Treasury", 1, True),
    "Global equity index fund": ("diversified fund", 2, False),
    "Investment-grade bond fund": ("diversified fund", 3, False),
    "Private real estate fund": ("diversified fund", 90, False),
    "Acme Corp bonds": ("Acme Corp", 4, False),
    "Acme Corp stock": ("Acme Corp", 1, False),
}

# Portfolio weights in the same order as the holdings above

candidates = {
    "A": [2, 2, 10, 60, 26, 0, 0, 0],
    "B": [1, 0, 0, 55, 20, 15, 5, 4],
    "C": [1, 1, 0, 70, 20, 0, 0, 8],
    "D": [3, 97, 0, 0, 0, 0, 0, 0],
}

# Issuers exempt from the 8% concentration limit

EXEMPT_ISSUERS = {
    "none",
    "U.S. Treasury",
    "diversified fund"
}

# -----------------------------
# CALCULATE RESERVE MINIMUM
# -----------------------------

reserve_minimum = (
    QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION
    / RESERVE_SIZE * 100
)

print(f"Reserve minimum: {reserve_minimum:.1f}%")

# -----------------------------
# CHECK EACH PORTFOLIO
# -----------------------------

for name, weights in candidates.items():

    print(f"\nCandidate {name}")
    failures = 0

    def check(label, value, passed):
        global failures

        status = "pass" if passed else "FAIL"

        print(f"{label}: {value:.1f} {status}")

        if not passed:
            failures += 1

    # Rule 1: Weights sum to 100%
    check(
        "Weights sum to 100",
        sum(weights),
        abs(sum(weights) - 100) < 0.000001
    )

    # Rule 2: Long-only
    check(
        "Long-only (lowest weight)",
        min(weights),
        min(weights) >= 0
    )

    # Rule 3: Reserve minimum
    reserve_weight = sum(
        weight
        for weight, (_, days, eligible)
        in zip(weights, holdings.values())
        if eligible
    )

    check(
        "Reserve-eligible weight",
        reserve_weight,
        reserve_weight >= reserve_minimum
    )

    # Rule 4: Liquidity
    liquid_weight = sum(
        weight
        for weight, (_, days, eligible)
        in zip(weights, holdings.values())
        if days <= LIQUIDITY_WINDOW
    )

    check(
        "Redeemable within 5 days",
        liquid_weight,
        liquid_weight >= MIN_LIQUID_SHARE
    )

    # Rule 5: Issuer concentration
    issuer_totals = {}

    for weight, (issuer, days, eligible) in zip(
        weights, holdings.values()
    ):
        if issuer not in EXEMPT_ISSUERS:
            issuer_totals[issuer] = (
                issuer_totals.get(issuer, 0) + weight
            )

    largest_company = max(
        issuer_totals.values(),
        default=0
    )

    check(
        "Largest single company",
        largest_company,
        largest_company <= ISSUER_LIMIT
    )

    # Rule 6: Requires CIO clarification
    print("Calendar-year loss: requires CIO clarification")

    # Final verdict
    if failures == 0:
        print("Verdict: passes every checkable rule")
    else:
        print(f"Verdict: fails {failures} rule(s)")
