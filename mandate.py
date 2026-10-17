"""Check Meridian's holdings-based mandate rules; all weights are percentages."""

from collections import defaultdict
from math import isclose


# Editable inputs: holding, issuer, redemption days, reserve eligibility.
HOLDINGS = [
    ("Cash", "none", 0, True),
    ("Treasury bills", "U.S. Treasury", 1, True),
    ("Treasury 10-year note", "U.S. Treasury", 1, True),
    ("Global equity index fund", "diversified fund", 2, False),
    ("Investment-grade bond fund", "diversified fund", 3, False),
    ("Private real estate fund", "diversified fund", 90, False),
    ("Acme Corp bonds", "Acme Corp", 4, False),
    ("Acme Corp stock", "Acme Corp", 1, False),
]

# Weights follow the same order as HOLDINGS; use percentage points, not fractions.
CANDIDATES = {
    "A": [2, 2, 10, 60, 26, 0, 0, 0],
    "B": [1, 0, 0, 55, 20, 15, 5, 4],
    "C": [1, 1, 0, 70, 20, 0, 0, 8],
    # Checker counterexample: all cash; meeting S2's return objective is unproven.
    "D": [100, 0, 0, 0, 0, 0, 0, 0],
}
RESERVE_SIZE = 100  # USD millions
QUARTERLY_DISTRIBUTION = 0.75  # USD millions
QUARTERS_TO_COVER = 4
LIQUIDITY_WINDOW = 5  # business days
MINIMUM_LIQUID_SHARE = 90  # percent
ISSUER_LIMIT = 8  # percent
EXEMPT_ISSUERS = {"none", "U.S. Treasury", "diversified fund"}


def check_candidate(name, weights, reserve_minimum):
    if len(weights) != len(HOLDINGS):
        raise ValueError(f"Candidate {name}: provide one weight per holding")

    reserve_weight = 0.0
    liquid_weight = 0.0
    company_weights = defaultdict(float)
    for (holding, issuer, days, eligible), weight in zip(HOLDINGS, weights):
        if eligible:
            reserve_weight += weight
        if days <= LIQUIDITY_WINDOW:
            liquid_weight += weight
        if issuer not in EXEMPT_ISSUERS:
            company_weights[issuer] += weight

    total = sum(weights)
    lowest = min(weights)
    largest_company = max(company_weights.values(), default=0.0)
    checks = [
        ("Weights sum to 100%", total,
         isclose(total, 100.0, rel_tol=0.0, abs_tol=1e-9)),
        ("Long-only (lowest weight)", lowest, lowest >= 0),
        (f"Reserve >= {reserve_minimum:.1f}%", reserve_weight,
         reserve_weight >= reserve_minimum),
        (f"Redeemable in {LIQUIDITY_WINDOW} business days >= "
         f"{MINIMUM_LIQUID_SHARE:.1f}%", liquid_weight,
         liquid_weight >= MINIMUM_LIQUID_SHARE),
        (f"Largest single company <= {ISSUER_LIMIT:.1f}%", largest_company,
         largest_company <= ISSUER_LIMIT),
    ]

    print(f"\nCandidate {name}")
    failures = 0
    for label, value, passed in checks:
        print(f"  {label}: {value:.1f}% {'pass' if passed else 'FAIL'}")
        failures += not passed
    print("  Calendar-year loss: requires CIO clarification")
    verdict = ("passes every checkable rule" if failures == 0
               else f"fails {failures} rule(s)")
    print(f"  Verdict: {verdict}")


def main():
    reserve_minimum = (
        QUARTERS_TO_COVER * QUARTERLY_DISTRIBUTION / RESERVE_SIZE * 100
    )
    print(f"Reserve minimum: {reserve_minimum:.1f}%")
    for name, weights in CANDIDATES.items():
        check_candidate(name, weights, reserve_minimum)


if __name__ == "__main__":
    main()
