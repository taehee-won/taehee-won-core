from unittest import TestCase, skipIf
from os import environ

from core import Trace, Datetime, Upbit


@skipIf(
    environ.get("TEST_INTERNET") != "1" and environ.get("TEST_ALL") != "1",
    "Upbit needs internet connection",
)
class TestUpbit(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Trace.set_levels(Trace.Level.NOTSET)

    @classmethod
    def tearDownClass(cls) -> None:
        Trace.set_levels()

    def test_get_assets(self):
        assets = Upbit.get_assets()

        self.assertIsInstance(assets, list)
        self.assertGreater(len(assets), 0)
        self.assertTrue(
            all(key in asset.keys() for asset in assets for key in ["code", "en", "ko"])
        )

    def test_get_codes(self):
        codes = Upbit.get_codes()

        self.assertIsInstance(codes, list)
        self.assertGreater(len(codes), 0)
        self.assertTrue(all(isinstance(code, str) for code in codes))

    def test_get_candles_month(self):
        basic = Datetime.from_values(2021, 1, 1, 9)
        candles = Upbit.get_candles(
            "KRW-BTC",
            Upbit.Period.MONTH,
            start=basic.to_datetime(),
            end=basic.get_after(Datetime.Period.MONTH, 11),
        )

        self.assertIsInstance(candles, list)
        self.assertEqual(len(candles), 12)
        self.assertTrue(
            basic.get_after(Datetime.Period.MONTH, index) == candles[index]["datetime"]
            for index in range(12)
        )
        self.assertTrue(
            all(
                key in candle.keys()
                for candle in candles
                for key in ["datetime", "open", "high", "low", "close", "volume"]
            )
        )

    def test_get_candles_week(self):
        basic = Datetime.from_values(2021, 1, 4, 9)
        candles = Upbit.get_candles(
            "KRW-BTC",
            Upbit.Period.WEEK,
            start=basic,
            end=basic.get_after(Datetime.Period.WEEK, 51).to_datetime(),
        )

        self.assertIsInstance(candles, list)
        self.assertEqual(len(candles), 52)
        self.assertTrue(
            basic.get_after(Datetime.Period.WEEK, index) == candles[index]["datetime"]
            for index in range(52)
        )
        self.assertTrue(
            all(
                key in candle.keys()
                for candle in candles
                for key in ["datetime", "open", "high", "low", "close", "volume"]
            )
        )

    def test_get_candles_day(self):
        basic = Datetime.from_values(2021, 1, 1, 9)
        candles = Upbit.get_candles(
            "KRW-BTC",
            Upbit.Period.DAY,
            start=basic,
            end=basic.get_after(Datetime.Period.DAY, 364),
        )

        self.assertIsInstance(candles, list)
        self.assertEqual(len(candles), 365)
        self.assertTrue(
            basic.get_after(Datetime.Period.DAY, index) == candles[index]["datetime"]
            for index in range(365)
        )
        self.assertTrue(
            all(
                key in candle.keys()
                for candle in candles
                for key in ["datetime", "open", "high", "low", "close", "volume"]
            )
        )

    def test_get_candles_minute(self):
        basic = Datetime.from_values(2021, 1, 1, 9)
        candles = Upbit.get_candles(
            "KRW-BTC",
            Upbit.Period.MINUTE,
            start=basic,
            end=basic.get_after(Datetime.Period.MINUTE, 199),
        )

        self.assertIsInstance(candles, list)
        self.assertEqual(len(candles), 200)
        self.assertTrue(
            basic.get_after(Datetime.Period.MINUTE, index) == candles[index]["datetime"]
            for index in range(200)
        )
        self.assertTrue(
            all(
                key in candle.keys()
                for candle in candles
                for key in ["datetime", "open", "high", "low", "close", "volume"]
            )
        )

    def test_get_candles_minute_60(self):
        basic = Datetime.from_values(2021, 1, 1, 9)
        candles = Upbit.get_candles(
            "KRW-BTC",
            Upbit.Period.MINUTE,
            60,
            start=basic,
            end=basic.get_after(Datetime.Period.MINUTE, 60 * 399),
        )

        self.assertIsInstance(candles, list)
        self.assertEqual(len(candles), 400)
        self.assertTrue(
            basic.get_after(Datetime.Period.MINUTE, 60 * index)
            == candles[index]["datetime"]
            for index in range(400)
        )
        self.assertTrue(
            all(
                key in candle.keys()
                for candle in candles
                for key in ["datetime", "open", "high", "low", "close", "volume"]
            )
        )

    def test_get_candles_exception(self):
        with self.assertRaises(TypeError):
            Upbit.get_candles("KRW-BTC", Upbit.Period.MONTH, 2)

        with self.assertRaises(TypeError):
            Upbit.get_candles("KRW-BTC", Upbit.Period.WEEK, 2)

        with self.assertRaises(TypeError):
            Upbit.get_candles("KRW-BTC", Upbit.Period.DAY, 2)

        with self.assertRaises(TypeError):
            Upbit.get_candles("KRW-BTC", Upbit.Period.MINUTE, 45)

        with self.assertRaises(TypeError):
            Upbit.get_candles("KRW-BTC", Upbit.Period.MINUTE, 120)
