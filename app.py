"""Streamlit entry point for the Meridian Foundation research prototype."""
from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st

from backtest import walk_forward
from compliance import ASSETS, mandate_checks, verdict
from data_loader import download_cpi, download_market, load_cpi, load_holdings, load_market_snapshot
from metrics import metrics, rolling_objective
from strategies import ACTIVE, BASELINES

ROOT = Path(__file__).resolve().parent

st.set_page_config(page_title="Meridian Reserve | Portfolio Research", page_icon="📊", layout="wide")

get_market = st.cache_data(ttl=3600, show_spinner=False)(download_market)
get_cpi = st.cache_data(ttl=86400, show_spinner=False)(download_cpi)
run_backtest = st.cache_data(show_spinner=False)(walk_forward)


def format_metrics(summary):
    formats = {column: "{:.2%}" for column in summary.columns}
    formats.update({"Sharpe (0% cash proxy)": "{:.2f}", "Total trading cost ($)": "${:,.0f}"})
    return summary.style.format(formats, na_rep="—")


def show_rules(rules):
    st.table(pd.DataFrame([(rule.name, rule.status, rule.detail) for rule in rules],
                          columns=["Rule", "Status", "Evidence"]))


st.title("Meridian Foundation Reserve")
st.caption("FIN 43900 · Portfolio research prototype · USD")
size, objective, policy = st.columns(3)
size.metric("Starting reserve", "$100 million")
objective.metric("Rolling five-year objective", "CPI + 4% net")
policy.metric("Policy benchmark", "60% VT / 40% BND")
st.warning("Calendar-year loss greater than 10% requires CIO clarification. All settings are prototype assumptions pending review.")

st.info("Replay limitations. Quarterly payouts and cash interest are not modeled. ETF issuer look-through "
        "remains unverified where dated holdings are missing. The CPI + 4% objective is unverified "
        "when CPI or overlapping five-year observations are unavailable.")

with st.sidebar:
    st.header("Research settings")
    window = st.slider("Estimation window (months)", 12, 84, 36, step=12)
    cost = st.slider("Trading cost (basis points per dollar)", 0, 50, 10, step=1)
    local_market = ROOT / "data" / "market.csv"
    source = st.radio("Market data", ["Yahoo Finance", "Local CSV"],
                      index=1 if local_market.is_file() else 0)
    market_upload = st.file_uploader("Market data CSV", type="csv") if source == "Local CSV" else None
    cpi_upload = st.file_uploader("Optional CPI CSV override", type="csv")
    holdings_upload = st.file_uploader("Optional dated issuer holdings CSV", type="csv")
    run_stress = st.checkbox("Run stress scenarios")

overview, history, signal_tab, stress, committee = st.tabs(
    ["Strategies", "Historical comparison", "Momentum signal", "Stress tests", "Committee review"]
)

with overview:
    st.subheader("Strategy design")
    st.dataframe(pd.DataFrame(
        [*list(BASELINES.values())[:2], (None, None, 0., .03)],
        index=[*list(BASELINES)[:2], ACTIVE], columns=ASSETS
    ).style.format("{:.2%}", na_rep="Estimated from history"))
    st.caption("SHV does not qualify as reserve cash. Issuer verification requires dated ETF look-through holdings, "
               "including aggregation across funds and security types. ETF wrapper weights do not measure issuer exposure.")

with signal_tab:
    st.subheader("Relative total-return momentum")
    st.table(pd.DataFrame(
        [
            ("Source", f"{source} · dividend- and split-adjusted closes for VT and BND"),
            ("Observation", "Last November trading close and the corresponding November close one year earlier"),
            ("Availability", "Market close plus vendor processing. The cutoff is the last December trading close."),
            ("Lag and trade", "About one month from observation to cutoff. Target executes at the first January close."),
            ("Calculation", "November close ratio minus one. Tilt the nonreserve equity share by ±5 points toward the winner. A tie leaves 60/40."),
            ("Limitations", "Adjusted-price ratios cancel common later adjustments. The prototype lacks archived vendor vintages or corrections."),
        ], columns=["Field", "Definition"]
    ))

with committee:
    st.subheader("Provisional committee decision")
    st.warning("Pending evidence and committee review. No strategy is cleared for implementation.")
    st.markdown(
        "- **Reject or suspend** when a hard rule fails, required evidence is unavailable, or a payout cannot be funded.\n"
        "- **Escalate** at a 20% peak-to-trough net drawdown under the proposed stop policy. "
        "Forecast volatility above 12% is a proposed review flag.\n"
        "- **Resolve before deployment** the calendar-year loss statement, issuer look-through and fund-level instrument eligibility, "
        "liquidity execution evidence, and settlement and payout controls."
    )


try:
    with st.spinner("Loading historical ETF observations..."):
        if source == "Yahoo Finance":
            (prices, volume, zero_volume), market_csv = get_market()
        elif market_upload is not None:
            market_csv = market_upload.getvalue()
            prices, volume, zero_volume = load_market_snapshot(BytesIO(market_csv))
        elif local_market.is_file():
            market_csv = local_market.read_bytes()
            prices, volume, zero_volume = load_market_snapshot(BytesIO(market_csv))
        else:
            raise ValueError("Upload a market CSV or place it in data/market.csv. See the README for the schema.")
except Exception as exc:
    with overview:
        st.error(f"Market data unavailable or invalid. Use a documented local CSV or retry Yahoo Finance. {exc}")
        for name, weights in list(BASELINES.items())[:2]:
            rules = mandate_checks(weights, 100_000_000)
            with st.expander(f"{name} — {verdict(rules)}"):
                show_rules(rules)
        st.info("C · Risk-aware — UNVERIFIED until market history is available.")
    st.stop()

if zero_volume:
    examples = ", ".join(f"{ticker} {date:%Y-%m-%d}" for ticker, date in zero_volume[:5])
    if len(zero_volume) > 5:
        examples += f", and {len(zero_volume) - 5} more"
    st.warning(
        f"Market data quality: retained {len(zero_volume):,} zero-volume row(s) ({examples}). "
        "Prices are retained for returns. A reported zero contributes zero dollars for that session "
        "to the rolling liquidity estimate. It may represent missing upstream volume."
    )

with history:
    st.caption(f"Source: {source} · common history {prices.index[0]:%Y-%m-%d} to {prices.index[-1]:%Y-%m-%d}")
    st.download_button("Download market data snapshot", market_csv, "market.csv", "text/csv")
    st.info("Hypothetical performance replay. Baseline targets are modeled even when checks fail. "
            "C blocks known numerical failures but can be modeled with unavailable issuer evidence. "
            "The committee stop rules are review flags in this research replay.")

holdings = None
try:
    local_holdings = ROOT / "data" / "holdings.csv"
    if holdings_upload is not None:
        holdings = load_holdings(BytesIO(holdings_upload.getvalue()))
    elif local_holdings.is_file():
        holdings = load_holdings(local_holdings)
except (ValueError, OSError) as exc:
    with overview:
        st.warning(f"Issuer evidence will remain unverified. Holdings CSV could not be loaded. {exc}")

try:
    nav, ledger, cash = run_backtest(prices, volume, window, cost, holdings=holdings)
except ValueError as exc:
    with overview:
        st.error(str(exc))
    st.stop()

with overview:
    st.subheader("Mandate checks by strategy")
    latest = ledger.groupby("Strategy", sort=False).tail(1)
    st.caption(f"Common reserve monitoring period: {cash.index[0]:%Y-%m-%d} through "
               f"{cash.index[-1]:%Y-%m-%d} ({len(cash):,} trading closes).")
    reserve_breaches = cash.lt(.03 - 1e-9)
    active_records = ledger.loc[ledger["Strategy"] == ACTIVE]
    active_executed = active_records.loc[active_records["Note"].eq("") & active_records["Target"].notna()]
    if active_executed.empty:
        st.caption(f"C remained in cash for all {len(cash):,} closes. An invested-period comparison is unavailable.")
        invested_breaches = reserve_breaches.iloc[:0]
    else:
        active_start = active_executed["Date"].iloc[0]
        invested_breaches = reserve_breaches.loc[active_start:]
        days_before = len(cash) - len(invested_breaches)
        st.caption(f"C stayed in cash for {days_before:,} trading closes before its first executed rebalance "
                   f"on {active_start:%Y-%m-%d}. The invested-period comparison uses the same "
                   f"{len(invested_breaches):,} closes from that date for all three strategies.")
    for _, row in latest.iterrows():
        strategy = row["Strategy"]
        records = ledger.loc[ledger["Strategy"] == strategy]
        prior = records["Verdict"]
        breaches = int(reserve_breaches[strategy].sum())
        # An annual check cannot certify the issuer and settlement evidence between rebalances.
        overall = "FAIL" if breaches or (prior == "FAIL").any() else "UNVERIFIED"
        with st.expander(f"{strategy} | Overall historical verdict: {overall}", expanded=True):
            st.markdown(f"**Latest rebalance verdict** ({row['Date']:%Y-%m-%d}): **{row['Verdict']}**")
            st.caption(f"Qualifying cash at that close after any modeled trade: {cash.loc[row['Date'], strategy]:.2%}.")
            if row["Target"] is not None:
                st.table(pd.DataFrame([row["Target"], row["Before"]], columns=ASSETS,
                                      index=["Target", "Pre-trade"]).style.format("{:.2%}"))
            elif row["Before"] is not None:
                st.table(pd.DataFrame([row["Before"]], columns=ASSETS,
                                      index=["Pre-trade only"]).style.format("{:.2%}"))
            show_rules(row["Rules"])
            issues = [
                {"Date": event["Date"], "Rule": rule.name, "Status": rule.status, "Evidence": rule.detail}
                for _, event in records.iterrows() for rule in event["Rules"] if rule.status != "PASS"
            ]
            if issues:
                st.markdown("Historical rule exceptions")
                st.dataframe(pd.DataFrame(issues), hide_index=True)
            if row["Note"]:
                st.warning(row["Note"])
            st.write(f"Below 3% qualifying cash on {breaches:,} of {len(cash):,} trading closes "
                     f"({breaches / len(cash):.2%}).")
            if not invested_breaches.empty:
                invested_count = int(invested_breaches[strategy].sum())
                st.caption(f"Common invested-period comparison: {invested_count:,} of "
                           f"{len(invested_breaches):,} closes below 3% ({invested_count / len(invested_breaches):.2%}).")
            st.caption("Other rules are evaluated at proposed annual rebalances.")
            if pd.notna(row["Forecast volatility"]):
                forecast = row["Forecast volatility"]
                st.write(f"Target annualized volatility estimate: {forecast:.2%}")
                if forecast > .12:
                    st.warning("Forecast exceeds the proposed 12% review threshold.")

with history:
    st.line_chart(nav / nav.iloc[0] * 100)
    st.caption("Net index starts at 100 before opening trades. The benchmark has no explicit trading costs.")
    summary = metrics(nav, ledger)
    st.dataframe(format_metrics(summary))
    st.caption("Annualized return uses elapsed calendar time. Volatility and Sharpe use daily returns and 252 sessions. "
               "Sharpe uses a 0% cash-rate proxy. Turnover is half the sum of weight changes from the drifted book. "
               "Opening funding is tracked separately from the annual cap but incurs costs.")
    audit = ledger.drop(columns=["Rules", "Target", "Before", "Optimization diagnostics"])
    st.dataframe(audit, hide_index=True)
    st.download_button("Download rebalance ledger", audit.to_csv(index=False), "rebalance-ledger.csv", "text/csv")
    st.markdown("Adjusted closes model reinvested ETF distributions and embedded fund expenses. Cash earns 0%. "
                "The quarterly $750,000 foundation withdrawals, trade settlement ledger, and payout funding are outside this replay. "
                "Liquidity is a capacity estimate based on 10% of prior 20-session median dollar volume and historical settlement lags. "
                "Missing trading sessions are rejected. Costs include each dollar bought or sold.")
    st.subheader("Rolling five-year return minus CPI + 4%")
    try:
        local_cpi = ROOT / "data" / "cpi.csv"
        if cpi_upload is not None:
            cpi = load_cpi(BytesIO(cpi_upload.getvalue()))
        elif local_cpi.is_file():
            cpi = load_cpi(local_cpi)
        elif source == "Yahoo Finance":
            cpi = get_cpi()
        else:
            cpi = None
        excess = rolling_objective(nav, cpi) if cpi is not None else None
        if excess is None:
            st.warning("CPI + 4% objective ? UNVERIFIED. Local CSV mode is offline. Upload CPI data or add data/cpi.csv.")
        elif excess.empty:
            st.warning("CPI + 4% objective ? UNVERIFIED. No complete overlapping five-year performance and CPI windows.")
        else:
            excess.index = excess.index.to_timestamp(how="end").normalize()
            st.line_chart(excess * 100)
            st.caption("Percentage points above or below the hurdle. CPI-U NSA (FRED CPIAUCNS) is used only for ex-post evaluation.")
    except Exception as exc:
        st.warning(f"CPI + 4% objective ? UNVERIFIED. Upload a FRED CPIAUCNS CSV or place it in data/cpi.csv. {exc}")

with signal_tab:
    st.subheader("Strategy C latest decision")
    decision = active_records.iloc[-1]
    diagnostics = decision["Optimization diagnostics"]
    st.write(f"Observation {decision['Observation']:%Y-%m-%d}, cutoff {decision['Cutoff']:%Y-%m-%d}, "
             f"rebalance {decision['Date']:%Y-%m-%d}.")
    st.write(f"Lagged 12-month momentum: VT {decision['VT momentum']:.2%}, BND {decision['BND momentum']:.2%}.")
    band_low, band_high = diagnostics["bounds"]["Momentum band"]
    st.write(f"Permitted VT weight from the momentum band: {band_low:.2%} to {band_high:.2%} "
             f"of total assets (reference {diagnostics['reference']:.2%}).")
    st.caption("The optimizer fixes qualifying cash at 3% and SHV at 0%, and allocates the balance to VT and BND.")
    if "intersection" in diagnostics:
        low, high = diagnostics["intersection"]
        if low <= high + 1e-9:
            st.write(f"Feasible VT weight after other verified bounds: {low:.2%} to {high:.2%}.")
        else:
            st.write(f"No feasible intersection. Lower bound {low:.2%}, upper bound {high:.2%}.")
    if "binding" in diagnostics:
        binding = ", ".join(diagnostics["binding"]) or "No equity bound at the selected weight"
        st.write(f"Binding equity constraints: {binding}.")
    if any(rule.name == "Single-company issuer" and rule.status == "UNVERIFIED" for rule in decision["Rules"]):
        st.caption("Issuer look-through was unverified and did not constrain this modeled target.")
    blocked = active_records.loc[active_records["Note"].ne(""), ["Date", "Note"]]
    st.subheader("Strategy C blocked rebalances")
    if blocked.empty:
        st.caption("No blocked rebalances in the current replay.")
    else:
        st.dataframe(blocked.rename(columns={"Note": "Reason"}), hide_index=True)
    signal_log = ledger.loc[ledger["Strategy"] == ACTIVE,
                            ["Observation", "Cutoff", "Date", "VT momentum", "BND momentum", "Forecast volatility"]]
    st.dataframe(signal_log, hide_index=True)

with stress:
    st.subheader("Scenario analysis")
    st.caption("Each comparison uses the current sidebar settings as the base. Longer windows can shorten coverage.")
    if run_stress:
        scenarios = [
            ("Base", window, cost, .20, .10, .25),
            ("36-month estimation", 36, cost, .20, .10, .25),
            ("60-month estimation", 60, cost, .20, .10, .25),
            ("84-month estimation", 84, cost, .20, .10, .25),
            ("5 bp trading costs", window, 5, .20, .10, .25),
            ("25 bp trading costs", window, 25, .20, .10, .25),
            ("50 bp trading costs", window, 50, .20, .10, .25),
            ("Unshrunk covariance", window, cost, 0., .10, .25),
            ("50% covariance shrinkage", window, cost, .50, .10, .25),
            ("5% daily liquidity participation", window, cost, .20, .05, .25),
            ("15% annual turnover cap", window, cost, .20, .10, .15),
        ]
        comparisons = []
        with st.spinner("Running historical scenarios..."):
            for label, *settings in scenarios:
                try:
                    path, trades, scenario_cash = run_backtest(prices, volume, *settings, holdings=holdings)
                    active_trades = trades.loc[trades["Strategy"] == ACTIVE]
                    result = metrics(path, trades).loc[ACTIVE].to_dict()
                    reserve_breach = (scenario_cash[ACTIVE] < .03 - 1e-9).any()
                    blocked = (active_trades["Note"] != "").sum()
                    stop = (reserve_breach or (active_trades["Verdict"] != "PASS").any()
                            or result["Maximum drawdown"] <= -.20)
                    comparisons.append({"Scenario": label, "First NAV date": path.index[0].date(),
                                        "Blocked rebalances": blocked, "Stop triggered": bool(stop), **result})
                except ValueError as exc:
                    comparisons.append({"Scenario": label, "Coverage error": str(exc)})
        st.dataframe(pd.DataFrame(comparisons), hide_index=True)
    else:
        st.info("Select Run stress scenarios to compare historical results.")

with committee:
    stop_rows = []
    for name in ledger["Strategy"].unique():
        records = ledger.loc[ledger["Strategy"] == name]
        stop_rows.append({
            "Strategy": name,
            "Failed rebalance checks": int((records["Verdict"] == "FAIL").sum()),
            "Rebalances with unverified rules": sum(any(rule.status == "UNVERIFIED" for rule in rules)
                                                 for rules in records["Rules"]),
            "Reserve breach during drift": bool((cash[name] < .03 - 1e-9).any()),
            "Drawdown stop reached": bool(summary.loc[name, "Maximum drawdown"] <= -.20),
        })
    st.dataframe(pd.DataFrame(stop_rows), hide_index=True)
    st.caption("Payout funding remains unverified. The results are for research review.")
