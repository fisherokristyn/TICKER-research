# Editable frozen case inputs: USD per share; FY2024 total GAAP diluted EPS.
TARGET = {"ticker": "ABG", "price": 243.03, "eps": 21.50}
PEERS = [
    {"ticker": "AN", "price": 169.84, "eps": 16.92},
    {"ticker": "GPI", "price": 421.48, "eps": 36.81},
]

from math import isfinite
from statistics import median


def positive(value):
    return (isinstance(value, (int, float)) and not isinstance(value, bool)
            and isfinite(value) and value > 0)


def multiple(company):
    price, eps = company.get("price"), company.get("eps")
    if not positive(price) or not positive(eps):
        return None
    return price / eps


def main():
    print("Retrospective training comparison: December 31, 2024 closing prices")
    print("paired with subsequently reported FY2024 total GAAP diluted EPS.")
    print("Equity P/E valuation; no cash/debt bridge. USD per share.\n")
    target_ticker = str(TARGET["ticker"]).strip().upper()
    target_pe = multiple(TARGET)
    print(f"Target {target_ticker} P/E: " + (
        f"{target_pe:.6f}x" if target_pe is not None else
        "not meaningful (missing, nonfinite or nonpositive price/EPS)"))

    seen = {target_ticker}
    peers = []
    for peer in PEERS:
        ticker = str(peer["ticker"]).strip().upper()
        if ticker in seen:
            print(f"Excluded {ticker}: target or duplicate (first entry retained).")
            continue
        seen.add(ticker)
        pe = multiple(peer)
        peers.append((ticker, pe))
        print(f"Peer {ticker} P/E: " + (
            f"{pe:.6f}x" if pe is not None else
            "not meaningful (missing, nonfinite or nonpositive price/EPS)"))

    valid = [pe for _, pe in peers if pe is not None]
    target_eps = TARGET.get("eps")
    eps_valid = positive(target_eps)
    full_price = None
    print()
    if not valid:
        print("No usable peers; no implied-price estimate.")
    else:
        middle = median(valid)
        print(f"Median peer P/E: {middle:.6f}x")
        if eps_valid:
            full_price = middle * target_eps
        if len(valid) == 1:
            print("One valid peer: reference estimate only; no range.")
            estimates = [("Reference", middle)]
        else:
            estimates = [("Minimum", min(valid)), ("Median", middle),
                         ("Maximum", max(valid))]
        for label, pe in estimates:
            result = (f"${pe * target_eps:.2f}" if eps_valid else
                      "not meaningful (missing, nonfinite or nonpositive target EPS)")
            print(f"{label} implied price: {result}")

    print("\nPeer-removal sensitivity (change from full-peer median estimate):")
    if not peers:
        print("No peers to remove.")
    for removed, _ in peers:
        remaining = [pe for ticker, pe in peers
                     if ticker != removed and pe is not None]
        if not remaining:
            print(f"Remove {removed}: no estimate (no usable peers remain).")
        elif not eps_valid:
            print(f"Remove {removed}: implied price and change not meaningful "
                  "(missing, nonfinite or nonpositive target EPS).")
        else:
            # Never round inputs or intermediate results; format only for display.
            estimate = median(remaining) * target_eps
            change = estimate - full_price
            print(f"Remove {removed}: remaining median-implied price "
                  f"${estimate:.2f}; dollar change {change:+.2f} USD.")


if __name__ == "__main__":
    main()
