TABLE = """row,ticker,month,published,index
1,AAA,2026-01,2026-02-10,101.0
2,AAA,2026-02,2026-03-10,104.0
3,AAA,2026-03,2026-04-10,109.0
4,AAA,2026-02,2026-03-25,103.0
5,BBB,2026-01,2026-02-10,98.0
6,BBB,2026-02,2026-03-10,97.0
7,BBB,2026-02,2026-03-10,97.0
8,BBB,2026-03,2026-04-10,92.0
9,CCC,2026-01,2026-02-10,110.0
10,CCC,2026-02,2026-04-05,112.0
11,,2026-02,2026-03-10,99.0
12,CCC,2026-02,2026-03-10,111.0
"""
DECISION_DATE = "2026-03-31"

import csv
from datetime import date
from decimal import Decimal
from io import StringIO


def read_rows():
    rows = []
    for record in csv.DictReader(StringIO(TABLE.strip())):
        rows.append({
            "row": int(record["row"]),
            "ticker": record["ticker"].strip(),
            "month": date.fromisoformat(record["month"].strip() + "-01"),
            "published": date.fromisoformat(record["published"].strip()),
            "index": Decimal(record["index"].strip()),
        })
    return rows


def report_rule(number, label, before, after):
    kept = {row["row"] for row in after}
    removed = [row["row"] for row in before if row["row"] not in kept]
    print(f"Rule {number} ({label}): removed {len(removed)}; "
          f"rows {removed}; remaining {len(after)}")


def deduplicate(rows):
    seen = set()
    result = []
    for row in rows:
        # Row number is an identifier, not part of the observation.
        key = (row["ticker"], row["month"], row["published"], row["index"])
        if key not in seen:
            seen.add(key)
            result.append(row)
    return result


def latest_publications(rows):
    latest = {}
    for row in rows:
        key = (row["ticker"], row["month"])
        old = latest.get(key)
        if old is None or row["published"] > old["published"]:
            latest[key] = row
        elif row["published"] == old["published"] and row["index"] != old["index"]:
            raise ValueError(f"Conflicting values on the same publication date: {key}")
    return sorted(latest.values(), key=lambda row: row["row"])


def print_panel(panel):
    print("\nAs-of panel")
    print(f"{'Row':>3}  {'Ticker':6}  {'Month':7}  {'Published':10}  {'Index':>8}")
    for row in sorted(panel, key=lambda r: (r["ticker"], r["month"])):
        print(f"{row['row']:>3}  {row['ticker']:6}  {row['month']:%Y-%m}  "
              f"{row['published']}  {row['index']:>8}")


def signal(panel, ticker):
    observations = {r["month"]: r["index"] for r in panel if r["ticker"] == ticker}
    if not observations:
        return "N/A (no observations)"
    latest_month = max(observations)
    previous_month = (date(latest_month.year - 1, 12, 1) if latest_month.month == 1
                      else date(latest_month.year, latest_month.month - 1, 1))
    label = f"{latest_month:%Y-%m} vs {previous_month:%Y-%m}"
    if previous_month not in observations:
        return f"{label}: N/A (previous calendar month missing)"
    previous = observations[previous_month]
    if previous == 0:
        return f"{label}: N/A (previous index is zero)"
    change = (observations[latest_month] / previous - 1) * 100
    return f"{label}: {change:+.2f}%"


def main():
    cutoff = date.fromisoformat(DECISION_DATE)
    rows = read_rows()
    if len({r['row'] for r in rows}) != len(rows):
        raise ValueError("Row numbers must be unique")
    print(f"Decision date: {cutoff}\nStarting rows: {len(rows)}")

    identified = [r for r in rows if r["ticker"]]
    report_rule(1, "missing ticker", rows, identified)
    clean = deduplicate(identified)
    report_rule(2, "exact duplicate", identified, clean)
    knowable = [r for r in clean if r["published"] <= cutoff]
    report_rule(3, "published after decision date", clean, knowable)
    panel = latest_publications(knowable)
    report_rule(4, "superseded publication", knowable, panel)
    print_panel(panel)

    # Retain basic cleaning, but deliberately ignore the publication cutoff.
    naive_panel = latest_publications(clean)
    tickers = sorted({r["ticker"] for r in clean})
    print("\nAs-of signals")
    for ticker in tickers:
        print(f"{ticker}: {signal(panel, ticker)}")
    print("\nNaive signals (publication cutoff ignored)")
    for ticker in tickers:
        print(f"{ticker}: {signal(naive_panel, ticker)}")


if __name__ == "__main__":
    main()
