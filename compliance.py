"""Independent mandate checks and portfolio arithmetic."""
from dataclasses import dataclass

from math import isfinite

ASSETS = ("VT", "BND", "SHV", "Cash")
EPS = 1e-9


@dataclass(frozen=True)
class Rule:
    name: str
    status: str
    detail: str


def mandate_checks(weights, nav, capacity=None, issuer_exposure=None, turnover=None, turnover_limit=.25):
    """Capacity is modeled settled dollars by ETF; issuer exposure is verified look-through."""
    weights = tuple(map(float, weights))
    if len(weights) != 4 or not all(map(isfinite, weights)):
        raise ValueError("Expected four finite portfolio weights in VT, BND, SHV, Cash order.")

    def check(name, condition, detail):
        status = "UNVERIFIED" if condition is None else ("PASS" if condition else "FAIL")
        return Rule(name, status, detail)

    liquidity = None
    if weights[3] >= 0.90 - EPS:
        liquidity = weights[3]
    elif capacity is not None and nav > 0 and all(isfinite(value) and value >= 0 for value in capacity):
        liquidity = weights[3] + sum(min(weight, cap / nav) for weight, cap in zip(weights[:3], capacity))
    if issuer_exposure is None and all(abs(weight) <= EPS for weight in weights[:3]):
        issuer_exposure = 0.0
    return [
        check("Weight sum", abs(sum(weights) - 1) <= EPS, f"{sum(weights):.2%}; required 100%"),
        check("Long-only", min(weights) >= -EPS, f"Lowest weight {min(weights):.2%}; required ≥ 0%"),
        check("Qualifying reserve", weights[3] >= .03 - EPS, f"Cash {weights[3]:.2%}; required ≥ 3%; SHV excluded"),
        check("Five-day liquidity", None if liquidity is None else liquidity >= .90 - EPS,
              "Capacity evidence unavailable" if liquidity is None else f"Portfolio value modeled convertible to settled cash within five business days: {liquidity:.2%}; required ≥ 90%"),
        check("Single-company issuer", None if issuer_exposure is None or not isfinite(issuer_exposure) else issuer_exposure <= .08 + EPS,
              "Dated underlying issuer holdings unavailable" if issuer_exposure is None
              else f"Largest nonexempt exposure {issuer_exposure:.2%}; limit 8%"),
        check("Annual turnover", None if turnover is None or not isfinite(turnover) else turnover <= turnover_limit + EPS,
              "Opening funding reported separately" if turnover is None
              else f"{turnover:.2%}; limit {turnover_limit:.0%}"),
    ]


def verdict(rules):
    statuses = {rule.status for rule in rules}
    if "FAIL" in statuses:
        return "FAIL"
    return "UNVERIFIED" if "UNVERIFIED" in statuses else "PASS"


def one_way(before, after):
    return sum(abs(new - old) for old, new in zip(before, after, strict=True)) / 2


def rebalance(values, weights, cost_rate):
    """Solve for post-cost NAV and trade ETFs into the specified post-cost weights."""
    nav = sum(values)
    low, high = 0.0, nav
    for _ in range(48):
        middle = (low + high) / 2
        traded = sum(abs(middle * weight - value) for weight, value in zip(weights[:3], values[:3]))
        if middle + cost_rate * traded > nav:
            high = middle
        else:
            low = middle
    post_nav = (low + high) / 2 if cost_rate else nav
    post_values = [post_nav * weight for weight in weights]
    return post_values, nav - post_nav, sum(abs(new - old) for old, new in zip(values[:3], post_values[:3]))

def largest_issuer(weights, issuer_rows):
    combined = {}
    for asset, fund_weight in zip(ASSETS[:3], weights[:3], strict=True):
        if fund_weight <= EPS:
            continue
        if asset not in issuer_rows:
            return None
        for issuer, issuer_weight in issuer_rows[asset].items():
            combined[issuer] = combined.get(issuer, 0.) + fund_weight * issuer_weight
    return max(combined.values(), default=0.)
