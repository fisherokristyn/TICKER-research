"""Download a validated, reusable Yahoo Finance snapshot for the Streamlit app."""
import argparse
from hashlib import sha256
from io import BytesIO
from pathlib import Path
import sys

import pandas as pd
import yfinance as yf

from data_loader import fetch_market, load_market

DEFAULT = Path(__file__).resolve().parent / "data" / "market.csv"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT, help="New CSV path (default data/market.csv)")
    args = parser.parse_args()
    target = args.output
    card = target.with_name(f"{target.stem}-data-card.md")
    try:
        for path in (target, card):
            if path.exists():
                raise FileExistsError(f"{path} exists. Choose a new filename with --output.")
        as_of = pd.Timestamp.now(tz="UTC")
        frame, diagnostics = fetch_market(as_of)
        retrieved = pd.Timestamp.now(tz="UTC")
        csv = frame.to_csv(index=False).encode("utf-8")
        prices, _ = load_market(BytesIO(csv))
        report = [
            "# ETF market data card", "",
            f"- Retrieved at {retrieved.isoformat()}. Session cutoff assessed at {as_of.isoformat()}.",
            f"- Source is Yahoo Finance daily history via yfinance {yf.__version__}. "
            "[History API](https://ranaroussi.github.io/yfinance/reference/yfinance.price_history.html)",
            f"- Common NYSE sessions from {prices.index[0]:%Y-%m-%d} through {prices.index[-1]:%Y-%m-%d}, inclusive.",
            f"- {len(frame):,} rows, {len(prices):,} per ETF. Missing required values and duplicate ticker/date rows both zero.",
            f"- CSV SHA-256 is `{sha256(csv).hexdigest()}`.",
            "- Requests start before these funds launched. Only pre-overlap rows are excluded. "
            "Internal gaps, invalid values, and missing latest sessions prevent export. "
            "No fills, vendor repairs, rounding, or synthetic observations are applied.",
            "- USD Yahoo Adj Close is used for returns and includes the vendor's split and distribution adjustments. "
            "Yahoo Close and Volume are retained as published for liquidity. Close is generally split-adjusted; "
            "it does not include the distribution adjustment in Adj Close. Dividend/capital-gain timing, "
            "market price versus NAV, and subsequent vendor corrections can cause differences versus sponsor returns. "
            "This snapshot is not a point-in-time vintage.",
            "- Zero volume reported by yfinance is retained with its price and session and counts as zero "
            "in the liquidity input. yfinance can normalize missing upstream volume to zero. "
            "A listed zero does not establish that no shares traded.",
            "- Diagnostics compare Adj Close / Close over time. Changes larger than 0.10% without a same-date "
            "Yahoo corporate-action row are flagged for review. This is a consistency screen, not sponsor reconciliation.",
            "",
            "| ETF | First Yahoo row | Earlier rows excluded | Adj Close / Close range | Factor changes > 0.001% | Unlinked shifts > 0.10% |",
            "| --- | --- | ---: | --- | ---: | --- |",
        ]
        for row in diagnostics:
            report.append(
                f"| {row['ticker']} | {row['source_first']} | {row['excluded_earlier_rows']} | "
                f"{row['adjusted_to_close_min']:.6f}–{row['adjusted_to_close_max']:.6f} | "
                f"{row['adjustment_factor_changes']} | {', '.join(row['unlinked_shifts']) or 'None'} |"
            )
        zero_rows = [f"{row['ticker']} {date}: Volume=0" for row in diagnostics
                     for date in row["zero_volume_dates"]]
        report.extend(["", "## Zero-volume observations", "",
                       *([f"- {row}" for row in zero_rows] or ["- None."])])
        with target.open("xb") as file:
            file.write(csv)
        with card.open("x", encoding="utf-8") as file:
            file.write("\n".join(report) + "\n")
        print(f"{target}: {prices.index[0]:%Y-%m-%d} through {prices.index[-1]:%Y-%m-%d}; "
              f"{len(frame):,} rows ({len(prices):,} per ETF); zero missing values and duplicates.")
        print(f"Data card: {card}")
        for row in zero_rows:
            print(f"Retained {row}")
        if any(row["unlinked_shifts"] for row in diagnostics):
            print("Review adjustment-factor flags in the data card before relying on the series.")
    except (OSError, RuntimeError, ValueError, KeyError) as exc:
        print(f"Download stopped: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
