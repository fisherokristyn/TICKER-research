"""Close-to-close portfolio research replay, with a separate policy benchmark."""
import numpy as np
import pandas as pd

from compliance import Rule, largest_issuer, mandate_checks, one_way, rebalance, verdict
from data_loader import issuer_snapshot, sessions
from strategies import ACTIVE, BASELINES, decision_inputs, risk_aware


def walk_forward(prices, dollar_volume, window=36, cost_bp=10, shrinkage=.20,
                 participation=.10, turnover_limit=.25, holdings=None):
    complete_months = prices.groupby(prices.index.to_period("M")).tail(1)
    last = prices.index[-1]
    if last != sessions(last.replace(day=1), last + pd.offsets.MonthEnd(0))[-1]:
        complete_months = complete_months.iloc[:-1]
    annual_closes = prices.groupby(prices.index.year).head(1).index
    decisions = {}
    for date in annual_closes:
        prior = prices.index[prices.index < date]
        if not len(prior) or prior[-1].month != 12:
            continue
        inputs = decision_inputs(complete_months, date.year - 1, window, shrinkage)
        if inputs is not None:
            decisions[date] = (prior[-1], *inputs)
    if not decisions:
        raise ValueError("No annual rebalance has enough complete prior history for the chosen estimation window.")

    names = [*BASELINES.keys()][:2] + [ACTIVE, list(BASELINES)[-1]]
    benchmark = names[-1]
    values = {name: np.array([0., 0., 0., 100_000_000.]) for name in names}
    invested = dict.fromkeys(names, False)
    rows, nav_rows, weight_rows = [], [], []
    changes = prices.pct_change()
    snapshot_start = next(iter(decisions))

    def capacity(as_of):
        # Conservatively model sales starting on the next business session.
        settle = 3 if as_of < pd.Timestamp("2017-09-05") else (2 if as_of < pd.Timestamp("2024-05-28") else 1)
        return dollar_volume.loc[as_of].to_numpy() * participation * (5 - settle)

    for date, daily_change in changes.loc[snapshot_start:].iterrows():
        if date in decisions:
            cutoff, observation, momentum, covariance = decisions[date]
            cap = capacity(cutoff)
            lookthrough = issuer_snapshot(holdings, cutoff)
        multiplier = np.append(1 + daily_change.to_numpy(), 1.)
        for name, prior_values in values.items():
            marked = prior_values * multiplier
            if date in decisions:
                nav = marked.sum()
                before = marked / nav
                target, error = BASELINES.get(name), ""
                opening = not invested[name]
                diagnostics = {} if name == ACTIVE else None
                if name == ACTIVE:
                    target, error = risk_aware(momentum, covariance, None if opening else prior_values / prior_values.sum(),
                                               prior_values.sum(), cap, turnover_limit, lookthrough,
                                               diagnostics=diagnostics)
                cost, traded, actual_turnover = 0., 0., 0.
                forecast = np.nan
                rules = []
                if target is not None:
                    proposed, proposed_cost, proposed_traded = rebalance(
                        marked, target, 0 if name == benchmark else cost_bp / 10_000
                    )
                    proposed = np.asarray(proposed)
                    measured_turnover = one_way(before, target)
                    rules = mandate_checks(target, proposed.sum(), cap,
                                           issuer_exposure=largest_issuer(target, lookthrough),
                                           turnover=None if opening else measured_turnover,
                                           turnover_limit=turnover_limit)
                    exposure = np.asarray(target[:3])
                    forecast = np.sqrt(max(0, 12 * (exposure @ covariance @ exposure)))
                    numerical_failure = any(rule.status == "FAIL" for rule in rules)
                    if name != ACTIVE or not numerical_failure:
                        marked, cost, traded = proposed, proposed_cost, proposed_traded
                        actual_turnover = measured_turnover
                        invested[name] = True
                    else:
                        error = "Risk-aware rebalance blocked by a known rule failure at execution"
                else:
                    status = "UNVERIFIED" if not np.isfinite(cap).all() else "FAIL"
                    rules = [Rule("Risk-aware target", status, error)]
                if name != benchmark:
                    rows.append({
                        "Date": date, "Strategy": name, "Verdict": verdict(rules),
                        "Optimization diagnostics": diagnostics,
                        "Rules": rules, "Note": error, "Target": target, "Before": before,
                        "Cost ($)": cost, "Traded ($)": traded,
                        "Turnover": np.nan if opening else actual_turnover,
                        "Opening turnover": actual_turnover if opening else np.nan,
                        "Forecast volatility": forecast, "Observation": observation, "Cutoff": cutoff,
                        "VT momentum": momentum["VT"], "BND momentum": momentum["BND"],
                    })
            values[name] = marked
        nav_rows.append({name: book.sum() for name, book in values.items()})
        weight_rows.append({name: book[3] / book.sum() for name, book in values.items()})

    baseline_date = prices.index[prices.index.get_loc(snapshot_start) - 1]
    index = prices.loc[snapshot_start:].index
    nav = pd.DataFrame([dict.fromkeys(names, 100_000_000.), *nav_rows],
                       index=pd.DatetimeIndex([baseline_date]).append(index))
    cash = pd.DataFrame(weight_rows, index=index)
    return nav, pd.DataFrame(rows), cash
