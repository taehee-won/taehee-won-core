from unittest import TestCase, skipIf
from os import environ
from datetime import datetime, timedelta

from core import Trace, KRX


@skipIf(
    environ.get("TEST_INTERNET") != "1" and environ.get("TEST_ALL") != "1",
    "KRX needs internet connection",
)
class TestKRX(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Trace.set_levels(Trace.Level.NOTSET)

    @classmethod
    def tearDownClass(cls) -> None:
        Trace.set_levels()

    def test_get_assets(self):
        assets = KRX.get_assets()

        self.assertIsInstance(assets, list)
        self.assertGreater(len(assets), 0)
        self.assertTrue(
            all(
                key in asset.keys()
                for asset in assets
                for key in ["market", "code", "name", "active"]
            )
        )

        for market in ["KOSPI", "KOSDAQ"]:
            for active in [True, False]:
                assets = KRX.get_assets(market, active)

                self.assertIsInstance(assets, list)
                self.assertGreater(len(assets), 0)
                self.assertTrue(
                    all(
                        key in asset.keys()
                        for asset in assets
                        for key in ["market", "code", "name", "active"]
                    )
                )
                self.assertTrue(all(asset["market"] == market for asset in assets))
                self.assertTrue(all(asset["active"] == active for asset in assets))

    def test_get_markets(self):
        markets = KRX.get_markets()

        self.assertIsInstance(markets, list)
        self.assertEqual(len(markets), 2)
        self.assertTrue(all(isinstance(market, str) for market in markets))

        for market in ["KOSPI", "KOSDAQ"]:
            self.assertIn(market, markets)

    def test_get_codes(self):
        codes = KRX.get_codes()

        self.assertIsInstance(codes, list)
        self.assertGreater(len(codes), 2000)
        self.assertTrue(all(isinstance(code, str) for code in codes))

        count = 0
        for market in ["KOSPI", "KOSDAQ"]:
            for active in [True, False]:
                count += len(KRX.get_codes(market, active))

        self.assertEqual(len(codes), count)

    def test_get_days(self):
        days = KRX.get_days()

        self.assertIsInstance(days, list)
        self.assertGreater(len(days), 2000)
        self.assertTrue(all(isinstance(day, datetime) for day in days))

    def test_get_assets_candles(self):
        candles = KRX.get_assets_candles()

        self.assertIsInstance(candles, list)
        self.assertGreater(len(candles), 2000)
        self.assertTrue(
            all(
                key in candle.keys()
                for candle in candles
                for key in [
                    "code",
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume",
                    "expense",
                    "capitalization",
                ]
            )
        )

        codes = []
        for candle in candles:
            self.assertNotIn(candle["code"], codes)
            codes.append(candle["code"])

        with self.assertRaises(ValueError):
            KRX.get_assets_candles(date=datetime(2024, 3, 1))

    def test_get_asset_candles(self):
        start = datetime(2000, 1, 1)
        end = datetime(2016, 12, 31)
        candles = KRX.get_asset_candles("005930", start=start, end=end)

        self.assertIsInstance(candles, list)
        self.assertGreater(len(candles), 2000)
        self.assertTrue(
            all(
                key in candle.keys()
                for candle in candles
                for key in [
                    "datetime",
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume",
                    "expense",
                    "capitalization",
                ]
            )
        )
        self.assertTrue(all(start <= candle["datetime"] <= end for candle in candles))

        date = start - timedelta(days=1)
        for candle in candles:
            self.assertGreater(candle["datetime"], date)
            date = candle["datetime"]

        with self.assertRaises(ValueError):
            KRX.get_asset_candles("000000")

        with self.assertRaises(ValueError):
            KRX.get_asset_candles("005930", end=datetime.now() + timedelta(days=2))
