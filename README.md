I used OpenAI ChatGPT and Codex to assist with planning, coding, debugging, and documentation.

The analysis, validation, and final investment decision are my own. This project is for educational purposes and is not investment advice.

# FIN 43900 Project 2 ? Investment Management Application

Run the Meridian Foundation mandate checker with `py mandate.py`.

## Run on Windows

Use Python 3.12 or 3.13 and open PowerShell in this project folder. In an environment
where the Python launcher selects a compatible version, run:

```powershell
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

If `py` defaults to a different version, select an installed compatible version, for
example `py -3.13 -m pip install -r requirements.txt` followed by
`py -3.13 -m streamlit run app.py`. Run tests with
`py -m unittest discover -s tests -v` using the same interpreter. The mandate and
trade arithmetic tests also run on standard Python without the UI dependencies.

## Historical inputs

The app requests actual VT, BND, and SHV daily history from Yahoo Finance using
[yfinance](https://ranaroussi.github.io/yfinance/reference/yfinance.price_history.html).
If the download is unavailable, select **Local CSV** and upload a file or place
it at `data/market.csv`. Use the header `date,ticker,adj_close,close,volume`.
Supply one row per ETF per NYSE trading session in the common period, with ISO
dates (YYYY-MM-DD), USD split- and dividend-adjusted close, closing price on
the same split basis as volume, and share volume. Retain the vendor, download
date, and adjustment conventions with the file. Use consecutive sessions
and enough history for the selected estimation window plus a January trade.
The dashboard can export the loaded snapshot. Check data redistribution rights
before uploading snapshots to GitHub.

The rolling hurdle uses monthly U.S. CPI-U, all items, not seasonally adjusted
([FRED CPIAUCNS](https://fred.stlouisfed.org/series/CPIAUCNS)). If needed, upload a
FRED CSV or save it as `data/cpi.csv` with header `observation_date,CPIAUCNS`.

Optional issuer evidence can be uploaded or placed at `data/holdings.csv`.
Use `ticker,as_of,available,issuer,weight,exempt`. Dates are ISO dates, weights
are fractions, and exemption flags are true or false. Each dated ETF snapshot
must cover 100% of the fund, with underlying holdings mapped to consistent
ultimate issuer IDs and a documented exemption policy. Use the historical
publication date for `available`. The app uses the latest eligible snapshot
published before the decision day and at most 45 days old. A missing snapshot
for a positive ETF weight leaves the issuer check UNVERIFIED. Current holdings
cannot attest to historical compliance.

## Prototype conventions

- The signal and covariance use data through November. The trading decision
  freezes at the final December close and the replay trades at the first January close
  after rechecking modeled capacity and turnover. Modern adjusted-price histories
  can contain vendor corrections and are not archived point-in-time vintages.
- Market returns use adjusted closes and assume reinvested ETF distributions.
  Cash earns zero. The replay excludes quarterly foundation withdrawals, actual
  settlement balances, taxes, and unmodeled fees. The committee view leaves
  payout funding and operational readiness unresolved.
- The 60/40 benchmark has annual rebalancing and no explicit transaction costs.
  Modeled ETF trading charges apply on both buys and sales. Opening funding
  incurs costs and is reported separately from the annual turnover cap.
- Baselines remain visible as hypothetical results even when their targets fail.
  The active replay skips numerically infeasible targets. It may show hypothetical
  results despite missing issuer evidence, which never clears a portfolio for trading.
  Risk and committee stops are review flags in this prototype.
- Infeasibility, historical rule failures, and missing evidence are visible in
  the dashboard. No strategy has committee approval. The calendar-year loss
  statement still requires CIO clarification.

### Download and use a local snapshot

Run `py download_data.py` with the interpreter used for Streamlit. The script
downloads and validates the daily Yahoo series and writes `data/market.csv` and
`data/market-data-card.md`. Existing snapshots are preserved. To save a refresh
under a separate filename, use `py download_data.py --output data/market-refresh.csv`.
Yahoo must have published the most recent completed NYSE session for all three
ETFs. If it has not, retry later. A network error or a gap in the common sample
stops the export.

Start the app with `py -m streamlit run app.py`. Select **Local CSV** in the
sidebar. It automatically reads `data/market.csv` if present, or you can upload
a different snapshot under **Market data CSV**. In this mode the app makes no
Yahoo or FRED requests. To evaluate the inflation hurdle offline, also supply
`data/cpi.csv` or use **Optional CPI CSV override**. The dashboard labels the
objective UNVERIFIED if CPI or overlapping five-year observations are missing.
