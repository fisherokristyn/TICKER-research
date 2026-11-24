"""Integration tests use synthetic inputs solely to exercise the replay."""
import importlib.util
import unittest

HAS_REPLAY = all(importlib.util.find_spec(package) for package in ("numpy", "pandas", "pandas_market_calendars"))


@unittest.skipUnless(HAS_REPLAY, "Install numerical and exchange-calendar dependencies.")
class ReplayTests(unittest.TestCase):
    def test_walk_forward_keeps_earlier_signal_and_applies_costs(self):
        import numpy as np
        import pandas as pd

        from backtest import walk_forward
        from data_loader import sessions
        from metrics import metrics
        from strategies import ACTIVE

        dates = sessions("2016-01-01", "2022-02-01")
        days = np.arange(len(dates))
        prices = pd.DataFrame(
            {"VT": 100 * np.exp(.0004 * days + .01 * np.sin(days / 20)),
             "BND": 100 * np.exp(.0002 * days + .002 * np.sin(days / 24)),
             "SHV": 100 * np.exp(.0001 * days)}, index=dates
        )
        volume = prices * 0 + 1e9
        nav, ledger, _ = walk_forward(prices, volume)
        first = ledger.loc[ledger["Strategy"] == ACTIVE].iloc[0]
        self.assertLess(first["Observation"], first["Cutoff"])
        self.assertLess(first["Cutoff"], first["Date"])
        self.assertEqual(first["Observation"].month, 11)
        self.assertTrue((ledger["Cost ($)"] >= 0).all())
        self.assertAlmostEqual(first["Cost ($)"], first["Traded ($)"] * .001, places=5)
        self.assertTrue(np.isfinite(metrics(nav, ledger).loc[ACTIVE, "Annualized volatility"]))
        changed = prices.copy()
        changed.loc[changed.index > first["Date"], "VT"] *= 1.5
        _, altered, _ = walk_forward(changed, volume)
        self.assertEqual(first["Target"], altered.loc[altered["Strategy"] == ACTIVE].iloc[0]["Target"])

    @unittest.skipUnless(importlib.util.find_spec("yfinance"), "Install yfinance.")
    def test_zero_bnd_volume_survives_download_and_csv_reload(self):
        from io import BytesIO
        from unittest.mock import patch

        import pandas as pd

        from data_loader import fetch_market, load_market, sessions

        dates = sessions("2024-01-02", "2024-02-02")[:20]
        histories = {
            ticker: pd.DataFrame({"Adj Close": 99., "Close": 100., "Volume": 1000},
                                 index=dates)
            for ticker in ("VT", "BND", "SHV")
        }
        # An in-memory fixture for the reported failure shape.
        bnd = histories["BND"]
        bnd.loc[dates[:11], "Volume"] = 0
        as_of = dates[-1].tz_localize("UTC") + pd.Timedelta(hours=23)
        with patch("yfinance.Ticker") as ticker:
            ticker.side_effect = lambda symbol: type("History", (), {
                "history": lambda self, **kwargs: histories[symbol].copy()
            })()
            frame, diagnostics = fetch_market(as_of)

        self.assertEqual(len(frame), 60)
        self.assertEqual(frame.loc[frame["ticker"].eq("BND"), "volume"].eq(0).sum(), 11)
        self.assertEqual(diagnostics[1]["zero_volume_dates"], dates[:11].strftime("%Y-%m-%d").tolist())
        prices, liquidity = load_market(BytesIO(frame.to_csv(index=False).encode()))
        self.assertTrue(prices.index.equals(dates))
        self.assertEqual(prices.iloc[0]["BND"], 99.)
        self.assertEqual(liquidity.iloc[-1]["BND"], 0.)

    def test_invalid_market_values_report_ticker_date_and_value(self):
        from io import StringIO

        from data_loader import load_market

        for field, raw, expected in (
            ("volume", "-1", r"BND 2024-01-02 volume=-1"),
            ("volume", "", r"BND 2024-01-02 volume=nan"),
            ("volume", "inf", r"BND 2024-01-02 volume=inf"),
            ("volume", "bad", r"BND 2024-01-02 volume='bad'"),
            ("adj_close", "0", r"BND 2024-01-02 adj_close=0"),
        ):
            with self.subTest(field=field, raw=raw):
                rows = ["date,ticker,adj_close,close,volume"]
                for date in ("2024-01-02", "2024-01-03"):
                    for ticker in ("VT", "BND", "SHV"):
                        fields = {"adj_close": "99", "close": "100", "volume": "1000"}
                        if (date, ticker) == ("2024-01-02", "BND"):
                            fields[field] = raw
                        rows.append(",".join((date, ticker, *fields.values())))
                with self.assertRaisesRegex(ValueError, expected):
                    load_market(StringIO("\n".join(rows)))

    @unittest.skipUnless(importlib.util.find_spec("streamlit"), "Install Streamlit.")
    def test_streamlit_local_csv_upload_displays_zero_volume_warning(self):
        from pathlib import Path
        from unittest.mock import patch

        from streamlit.testing.v1 import AppTest

        # Small in-memory CSV for the UI path, without financial replay results.
        rows = ["date,ticker,adj_close,close,volume"]
        for date in ("2024-01-02", "2024-01-03"):
            for ticker in ("VT", "BND", "SHV"):
                volume = 0 if (date, ticker) == ("2024-01-02", "BND") else 1000
                rows.append(f"{date},{ticker},99,100,{volume}")
        csv = "\n".join(rows).encode()
        app = Path(__file__).resolve().parents[1] / "app.py"
        def offline():
            raise AssertionError("Unexpected market request")

        with patch("data_loader.download_market", new=offline):
            dashboard = AppTest.from_file(str(app), default_timeout=30).run()
            dashboard.radio[0].set_value("Local CSV").run()
            uploader = dashboard.get("file_uploader")[0]
            if not hasattr(uploader, "upload"):
                self.skipTest("Streamlit version lacks upload support in AppTest.")
            uploader.upload("fixture.csv", csv, "text/csv").run()

        self.assertFalse(dashboard.exception)
        self.assertTrue(any("BND 2024-01-02" in item.value for item in dashboard.warning))
        self.assertFalse(any("Market data unavailable or invalid" in item.value for item in dashboard.error))

    def test_missing_market_session_rejected(self):
        import pandas as pd
        from io import StringIO

        from data_loader import load_market

        rows = [(date, ticker, 100, 100, 1234)
                for date in ("2024-01-02", "2024-01-04") for ticker in ("VT", "BND", "SHV")]
        csv = pd.DataFrame(rows, columns=["date", "ticker", "adj_close", "close", "volume"]).to_csv(index=False)
        with self.assertRaisesRegex(ValueError, "missing or unexpected"):
            load_market(StringIO(csv))


if __name__ == "__main__":
    unittest.main()
