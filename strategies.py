"""Static portfolios and a bounded, one-dimensional variance minimization."""
from math import isfinite

from compliance import EPS

BASELINES = {
    "A · Equal weight": (1/3, 1/3, 1/3, 0.),
    "B · Cash + 60/40": (.582, .388, 0., .03),
    "Benchmark · 60/40": (.60, .40, 0., 0.),
}
ACTIVE = "C · Risk-aware"


def decision_inputs(monthly, year, window, shrinkage):
    import numpy as np

    end = monthly.index[monthly.index.to_period("M") == f"{year}-11"]
    if not len(end):
        return None
    history = monthly.loc[:end[-1]].tail(max(window, 12) + 1)
    if len(history) < max(window, 12) + 1:
        return None
    momentum = history[["VT", "BND"]].iloc[-1] / history[["VT", "BND"]].iloc[-13] - 1
    returns = history.pct_change().iloc[-window:]
    covariance = returns.cov().to_numpy()
    covariance = (1 - shrinkage) * covariance + shrinkage * np.diag(np.diag(covariance))
    return history.index[-1], momentum, covariance


def risk_aware(momentum, covariance, before, nav, capacity, turnover_limit, issuer_rows=None, *, diagnostics=None):
    """Minimize variance with fixed cash and a bounded equity/bond sleeve."""
    sleeve = .97
    direction = int(momentum["VT"] > momentum["BND"]) - int(momentum["VT"] < momentum["BND"])
    reference = sleeve * (.60 + .05 * direction)
    lower, upper = reference - .05 * sleeve, reference + .05 * sleeve
    bounds = {"Momentum band": (lower, upper)}
    if diagnostics is not None:
        diagnostics.update(reference=reference, bounds=bounds)
    if before is not None:
        a, b = before[0], sleeve - before[1]
        budget = 2 * turnover_limit - abs(before[2]) - abs(.03 - before[3])
        if budget < abs(a - b) - EPS:
            return None, "Turnover leaves no feasible allocation"
        bounds["Turnover"] = ((a + b - budget) / 2, (a + b + budget) / 2)
        lower = max(lower, bounds["Turnover"][0])
        upper = min(upper, bounds["Turnover"][1])
    if capacity is None or not all(isfinite(cap) and cap >= 0 for cap in capacity):
        return None, "Five-day capacity evidence unavailable"
    equity_cap, bond_cap = (cap / nav for cap in capacity[:2])
    required = .90 - .03
    if equity_cap + bond_cap < required - EPS:
        return None, "Five-day liquidity leaves no feasible allocation"
    bounds["Five-day liquidity"] = (required - bond_cap, sleeve + equity_cap - required)
    lower = max(lower, bounds["Five-day liquidity"][0])
    upper = min(upper, bounds["Five-day liquidity"][1])
    if issuer_rows is not None and {"VT", "BND"} <= issuer_rows.keys():
        vt, bnd = issuer_rows["VT"], issuer_rows["BND"]
        for issuer in vt.keys() | bnd.keys():
            slope = vt.get(issuer, 0.) - bnd.get(issuer, 0.)
            room = .08 - sleeve * bnd.get(issuer, 0.)
            if slope > EPS:
                issuer_upper = room / slope
                bounds[f"Issuer limit ({issuer})"] = (None, issuer_upper)
                upper = min(upper, issuer_upper)
            elif slope < -EPS:
                issuer_lower = room / slope
                bounds[f"Issuer limit ({issuer})"] = (issuer_lower, None)
                lower = max(lower, issuer_lower)
            elif room < -EPS:
                return None, "Underlying issuer limit leaves no feasible allocation"
    if diagnostics is not None:
        diagnostics["intersection"] = (lower, upper)
    if lower > upper + EPS:
        return None, "Signal band and hard numerical limits have no feasible intersection"
    equity_var, bond_var, cross = covariance[0][0], covariance[1][1], covariance[0][1]
    curvature = equity_var + bond_var - 2 * cross
    optimum = sleeve * (bond_var - cross) / curvature if curvature > 1e-15 else reference
    equity = min(max(optimum, lower), upper)
    if diagnostics is not None:
        binding = []
        for label, (floor, ceiling) in bounds.items():
            if floor is not None and abs(equity - floor) <= EPS:
                binding.append(f"{label} lower bound")
            if ceiling is not None and abs(equity - ceiling) <= EPS:
                binding.append(f"{label} upper bound")
        diagnostics["binding"] = binding
    return (equity, sleeve - equity, 0., .03), ""
