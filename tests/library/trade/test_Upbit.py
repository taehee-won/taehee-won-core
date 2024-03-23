from unittest import TestCase, skipIf
from os import environ

from src.library.lib.Trace import TraceLevel, Trace
from src.library.lib.Datetime import Period, Datetime
from src.library.trade.Upbit import Upbit


@skipIf(
    environ.get("TEST_INTERNET") != "1" and environ.get("TEST_ALL") != "1",
    "Upbit needs internet connection",
)
class TestUpbit(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Trace.set_levels(TraceLevel.NOTSET)

    @classmethod
    def tearDownClass(cls) -> None:
        Trace.set_levels()

    def test_get_codes(self):
        markets = Upbit.get_codes()

        self.assertIsInstance(markets, list)
        self.assertGreater(len(markets), 0)
        self.assertTrue(
            all(
                key in market.keys()
                for market in markets
                for key in ["code", "en", "ko"]
            )
        )

    def test_get_candles_month(self):
        basic = Datetime.from_values(2021, 1, 1, 9)
        candles = Upbit.get_candles(
            "KRW-BTC",
            Period.MONTH,
            start=basic.get_datetime(),
            end=basic.get_after(Period.MONTH, 11),
        )

        self.assertIsInstance(candles, list)
        self.assertEqual(len(candles), 12)

        for index in range(12):
            self.assertEqual(
                basic.get_after(Period.MONTH, index),
                candles[index]["datetime"],
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
            Period.WEEK,
            start=basic,
            end=basic.get_after(Period.WEEK, 51).get_datetime(),
        )

        self.assertIsInstance(candles, list)
        self.assertEqual(len(candles), 52)

        for index in range(52):
            self.assertEqual(
                basic.get_after(Period.WEEK, index),
                candles[index]["datetime"],
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
            Period.DAY,
            start=basic,
            end=basic.get_after(Period.DAY, 364),
        )

        self.assertIsInstance(candles, list)
        self.assertEqual(len(candles), 365)

        for index in range(365):
            self.assertEqual(
                basic.get_after(Period.DAY, index),
                candles[index]["datetime"],
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
            Period.MINUTE,
            start=basic,
            end=basic.get_after(Period.MINUTE, 199),
        )

        self.assertIsInstance(candles, list)
        self.assertEqual(len(candles), 200)

        for index in range(200):
            self.assertEqual(
                basic.get_after(Period.MINUTE, index),
                candles[index]["datetime"],
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
            Period.MINUTE,
            60,
            start=basic,
            end=basic.get_after(Period.MINUTE, 60 * 399),
        )

        self.assertIsInstance(candles, list)
        self.assertEqual(len(candles), 400)

        for index in range(400):
            self.assertEqual(
                basic.get_after(Period.MINUTE, 60 * index),
                candles[index]["datetime"],
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
            Upbit.get_candles("KRW-BTC", Period.YEAR)

        with self.assertRaises(TypeError):
            Upbit.get_candles("KRW-BTC", Period.MONTH, 2)

        with self.assertRaises(TypeError):
            Upbit.get_candles("KRW-BTC", Period.WEEK, 2)

        with self.assertRaises(TypeError):
            Upbit.get_candles("KRW-BTC", Period.DAY, 2)

        with self.assertRaises(TypeError):
            Upbit.get_candles("KRW-BTC", Period.HOUR)

        with self.assertRaises(TypeError):
            Upbit.get_candles("KRW-BTC", Period.MINUTE, 45)

        with self.assertRaises(TypeError):
            Upbit.get_candles("KRW-BTC", Period.MINUTE, 120)
