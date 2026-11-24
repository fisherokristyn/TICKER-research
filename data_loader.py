"""Historical inputs for the Meridian research dashboard."""
from io import BytesIO
from urllib.request import urlopen

import numpy as np
import pandas as pd
import pandas_market_calendars as calendars

TICKERS = ("VT", "BND", "SHV")
COLUMNS = ("date", "ticker", "adj_close", "close", "volume")
CPI_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=CPIAUCNS"


def sessions(start, end):
    return calendars.get_calendar("NYSE").valid_days(start, end).tz_localize(None)


def validate_market_values(frame):
    for field in COLUMNS[2:]:
        raw = frame[field]
        numeric = pd.to_numeric(raw, errors="coerce").astype(float)
        invalid = ~np.isfinite(numeric) | (numeric < 0 if field == "volume" else numeric <= 0)
        if invalid.any():
            examples = ", ".join(
                f"{row.ticker} {row.date:%Y-%m-%d} {field}={row.value!r}"
                for row in frame.loc[invalid, ["ticker", "date"]]
                .assign(value=raw[invalid]).head(5).itertuples(index=False)
            )
            requirement = "nonnegative" if field == "volume" else "positive"
            raise ValueError(f"{field} must contain finite {requirement} numbers. "
                             f"{int(invalid.sum())} invalid row(s): {examples}.")
        frame[field] = numeric


def load_market(source):
    prices, capacity, _ = load_market_snapshot(source)
    return prices, capacity


def load_market_snapshot(source):
    """Validate a CSV and report retained zero-volume rows in the common sample."""
    frame = pd.read_csv(source)
    if not set(COLUMNS).issubset(frame):
        raise ValueError("Market CSV needs date, ticker, adj_close, close, volume.")
    frame = frame.loc[:, list(COLUMNS)].copy()
    frame["date"] = pd.to_datetime(frame["date"], format="%Y-%m-%d")
    if frame["date"].isna().any():
        raise ValueError("Market CSV contains missing dates.")
    if set(frame["ticker"]) != set(TICKERS) or frame.duplicated(["date", "ticker"]).any():
        raise ValueError("Provide unique daily rows for exactly VT, BND, and SHV.")
    validate_market_values(frame)
    wide = frame.pivot(index="date", columns="ticker")
    first = frame.groupby("ticker")["date"].min().max()
    last = frame.groupby("ticker")["date"].max().min()
    if first >= last:
        raise ValueError("The three ETFs have no usable common history.")
    wide = wide.loc[first:last].sort_index()
    expected = sessions(first, last)
    if not wide.index.equals(expected) or wide.isna().any().any():
        raise ValueError("Common ETF history has missing or unexpected NYSE sessions. Supply consecutive daily data.")
    adjusted = wide["adj_close"].loc[:, list(TICKERS)]
    dollar_volume = (wide["close"] * wide["volume"]).loc[:, list(TICKERS)]
    observed = frame.loc[frame["date"].between(first, last) & frame["volume"].eq(0)]
    zero_volume = [(row.ticker, row.date) for row in observed.itertuples(index=False)]
    return adjusted, dollar_volume.rolling(20, min_periods=20).median(), zero_volume


def latest_completed_session(as_of):
    calendar = calendars.get_calendar("NYSE")
    day = as_of.tz_convert("America/New_York").date()
    schedule = calendar.schedule(day - pd.Timedelta(days=14), day)
    return schedule.index[schedule["market_close"] <= as_of][-1]


def fetch_market(as_of):
    """Return the strict common Yahoo sample and adjustment diagnostics."""
    import yfinance as yf

    last = latest_completed_session(as_of)
    exclusive_end = (last + pd.Timedelta(days=1)).date().isoformat()
    frames = {}
    for ticker in TICKERS:
        try:
            history = yf.Ticker(ticker).history(
                start="2000-01-01", end=exclusive_end, interval="1d",
                auto_adjust=False, back_adjust=False, actions=True,
                repair=False, keepna=True, raise_errors=True, timeout=15,
            )
        except Exception as exc:
            raise RuntimeError(f"Yahoo Finance {ticker}: {type(exc).__name__}: {exc}") from exc
        if history.empty:
            raise ValueError(f"Yahoo Finance returned no rows for {ticker}.")
        dates = history.index
        if dates.tz is not None:
            dates = dates.tz_convert("America/New_York").tz_localize(None)
        dates = dates.normalize()
        if dates.has_duplicates or dates.hasnans or not dates.is_monotonic_increasing:
            raise ValueError(f"{ticker} returned duplicate, missing, or unordered session dates.")
        history.index = dates
        if dates[-1] != last:
            raise ValueError(f"{ticker} ends on {dates[-1]:%Y-%m-%d}; expected {last:%Y-%m-%d}.")
        frames[ticker] = history

    first = max(history.index[0] for history in frames.values())
    expected = sessions(first, last)
    rows, diagnostics = [], []
    for ticker, history in frames.items():
        common = history.loc[first:last]
        if not common.index.equals(expected):
            missing = expected.difference(common.index).strftime("%Y-%m-%d").tolist()
            unexpected = common.index.difference(expected).strftime("%Y-%m-%d").tolist()
            raise ValueError(f"{ticker} common-calendar mismatch. Missing {len(missing)} {missing[:5]}; "
                             f"unexpected {len(unexpected)} {unexpected[:5]}.")
        data = pd.DataFrame({
            "date": common.index,
            "ticker": ticker,
            "adj_close": common["Adj Close"].to_numpy(),
            "close": common["Close"].to_numpy(),
            "volume": common["Volume"].to_numpy(),
        })
        validate_market_values(data)
        zero_dates = data.loc[data["volume"].eq(0), "date"]
        factor = (data["adj_close"] / data["close"]).set_axis(common.index)
        shift = factor.pct_change().abs()
        actions = common.reindex(columns=["Dividends", "Capital Gains", "Stock Splits"], fill_value=0).ne(0).any(axis=1)
        unlinked = shift[(shift > .001) & ~actions]
        diagnostics.append({
            "ticker": ticker, "source_first": history.index[0].date().isoformat(),
            "excluded_earlier_rows": len(history) - len(common),
            "adjustment_factor_changes": int((shift > .00001).sum()),
            "adjusted_to_close_min": float(factor.min()), "adjusted_to_close_max": float(factor.max()),
            "zero_volume_dates": zero_dates.dt.strftime("%Y-%m-%d").tolist(),
            "unlinked_shifts": [f"{date:%Y-%m-%d} ({change:.2%})" for date, change in unlinked.items()],
        })
        rows.append(data)
    frame = pd.concat(rows, ignore_index=True).sort_values(["date", "ticker"])
    return frame, diagnostics


def download_market():
    frame, _ = fetch_market(pd.Timestamp.now(tz="UTC"))
    csv = frame.to_csv(index=False).encode()
    return load_market_snapshot(BytesIO(csv)), csv


def load_cpi(source):
    frame = pd.read_csv(source, na_values=["."])
    if not {"observation_date", "CPIAUCNS"}.issubset(frame):
        raise ValueError("CPI CSV needs observation_date and CPIAUCNS.")
    dates = pd.to_datetime(frame["observation_date"]).dt.to_period("M")
    values = pd.to_numeric(frame["CPIAUCNS"], errors="raise")
    if dates.isna().any() or dates.duplicated().any() or (values.dropna() <= 0).any() or np.isinf(values).any():
        raise ValueError("CPI requires unique months and positive index values.")
    return pd.Series(values.to_numpy(), index=pd.PeriodIndex(dates)).sort_index()


def download_cpi():
    with urlopen(CPI_URL, timeout=8) as response:
        return load_cpi(BytesIO(response.read()))
def load_holdings(source):
    """Load complete fund snapshots mapped to ultimate issuers by the data supplier."""
    frame = pd.read_csv(source)
    fields = {"ticker", "as_of", "available", "issuer", "weight", "exempt"}
    if not fields.issubset(frame):
        raise ValueError("Holdings CSV needs ticker, as_of, available, issuer, weight, exempt.")
    frame = frame[list(fields)].copy()
    for field in ("as_of", "available"):
        frame[field] = pd.to_datetime(frame[field], format="%Y-%m-%d")
    frame["weight"] = pd.to_numeric(frame["weight"], errors="raise")
    frame["issuer"] = frame["issuer"].fillna("").str.strip()
    exempt = frame["exempt"].astype(str).str.lower()
    if (frame.empty or not set(frame["ticker"]).issubset(TICKERS)
            or frame[["as_of", "available"]].isna().any().any()
            or (frame["available"] < frame["as_of"]).any()
            or frame["issuer"].eq("").any() or not exempt.isin(["true", "false"]).all()
            or not np.isfinite(frame["weight"]).all() or (frame["weight"] < 0).any()):
        raise ValueError("Holdings contain invalid symbols, dates, issuer IDs, weights, or exemption flags.")
    frame["exempt"] = exempt.eq("true")
    snapshots = frame.groupby(["ticker", "as_of", "available"])["weight"].sum()
    if not np.allclose(snapshots, 1., atol=1e-6, rtol=0):
        raise ValueError("Each holdings snapshot must cover 100% of the fund.")
    if (frame.groupby("issuer")["exempt"].nunique() > 1).any():
        raise ValueError("An issuer cannot be both exempt and nonexempt.")
    return frame


def issuer_snapshot(holdings, cutoff):
    """Select fresh underlying issuer rows actually available by the decision date."""
    result = {}
    if holdings is None:
        return result
    eligible = holdings.loc[(holdings["available"] < cutoff)
                            & (holdings["as_of"] >= cutoff - pd.Timedelta(days=45))]
    for ticker, rows in eligible.groupby("ticker"):
        as_of = rows["as_of"].max()
        rows = rows.loc[rows["as_of"] == as_of]
        rows = rows.loc[rows["available"] == rows["available"].max()]
        result[ticker] = rows.loc[~rows["exempt"]].groupby("issuer")["weight"].sum().to_dict()
    return result
