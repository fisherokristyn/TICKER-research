"""Consistent portfolio statistics for the research replay."""
import numpy as np
import pandas as pd

from data_loader import sessions


def metrics(nav, ledger):
    returns = nav.pct_change().dropna()
    days = (nav.index[-1] - nav.index[0]).days
    annual_return = (nav.iloc[-1] / nav.iloc[0]) ** (365.25 / days) - 1
    daily_volatility = returns.std()
    summary = pd.DataFrame({
        "Annualized return": annual_return,
        "Annualized volatility": daily_volatility * np.sqrt(252),
        "Sharpe (0% cash proxy)": returns.mean() / daily_volatility.replace(0, np.nan) * np.sqrt(252),
        "Maximum drawdown": (nav / nav.cummax() - 1).min(),
        "Mean annual turnover": ledger.groupby(["Strategy", ledger["Date"].dt.year])["Turnover"]
        .sum(min_count=1).groupby(level=0).mean(),
        "Total trading cost ($)": ledger.groupby("Strategy")["Cost ($)"].sum(),
    })
    benchmark = nav.columns[-1]
    summary.loc[benchmark, "Total trading cost ($)"] = 0.
    return summary.reindex(nav.columns)


def rolling_objective(nav, cpi):
    monthly = nav.groupby(nav.index.to_period("M")).last()
    # Exclude the pre-trade reference and any unfinished final trading month.
    monthly = monthly.iloc[1:]
    last = nav.index[-1]
    last_session = sessions(last.replace(day=1), last + pd.offsets.MonthEnd(0))[-1]
    if last != last_session:
        monthly = monthly.iloc[:-1]
    net_cagr = (monthly / monthly.shift(60)) ** .2 - 1
    aligned_cpi = cpi.reindex(monthly.index)
    hurdle = (aligned_cpi / aligned_cpi.shift(60)) ** .2 - 1 + .04
    return net_cagr.sub(hurdle, axis=0).dropna(how="all")
