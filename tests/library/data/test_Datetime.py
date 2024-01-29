from unittest import TestCase
from datetime import datetime, timedelta

from src.library.data.Datetime import Period, Datetime


class TestDatetime(TestCase):
    def test_from_values(self):
        self.assertEqual(
            Datetime.from_values(2020, 1, 1).get_datetime(),
            datetime(2020, 1, 1),
        )
        self.assertEqual(
            Datetime.from_values(2020, 1, 1, 12, 30).get_datetime(),
            datetime(2020, 1, 1, 12, 30),
        )

    def test_from_now(self):
        self.assertAlmostEqual(
            Datetime.from_now().get_datetime(),
            datetime.now(),
            delta=timedelta(seconds=1),
        )

    def test_from_str(self):
        self.assertEqual(
            Datetime.from_str("2023-12-11", "%Y-%m-%d").get_datetime(),
            datetime(2023, 12, 11),
        )

    def test_get_datetime(self):
        dt = datetime(2008, 8, 16)
        self.assertEqual(
            Datetime(dt).get_datetime(),
            dt,
        )

    def test_get_str(self):
        self.assertEqual(
            Datetime.from_str("2023-12-11", "%Y-%m-%d").get_str("%Y%m%d"),
            "20231211",
        )

    def test_get_before(self):
        self.assertEqual(
            Datetime.from_values(2011, 3, 4).get_before(Period.DAY, 17).get_datetime(),
            datetime(2011, 2, 15),
        )
        self.assertEqual(
            Datetime.from_values(2001, 4, 7).get_before(Period.MONTH, 9).get_datetime(),
            datetime(2000, 7, 7),
        )

    def test_get_after(self):
        self.assertEqual(
            Datetime.from_values(2011, 3, 4).get_after(Period.DAY, 17).get_datetime(),
            datetime(2011, 3, 21),
        )
        self.assertEqual(
            Datetime.from_values(2001, 4, 7).get_after(Period.MONTH, 9).get_datetime(),
            datetime(2002, 1, 7),
        )

    def test_get_quarter_start(self):
        self.assertEqual(
            Datetime.from_values(2020, 4, 15).get_quarter_start().get_datetime(),
            datetime(2020, 4, 1),
        )
        self.assertEqual(
            Datetime.from_values(2023, 2, 15).get_quarter_start(3).get_datetime(),
            datetime(2023, 10, 1),
        )
        self.assertEqual(
            Datetime.from_values(2012, 3, 7).get_quarter_start(-3).get_datetime(),
            datetime(2011, 4, 1),
        )

    def test_get_quarter_end(self):
        self.assertEqual(
            Datetime.from_values(2020, 4, 15).get_quarter_end().get_datetime(),
            datetime(2020, 6, 30),
        )
        self.assertEqual(
            Datetime.from_values(2023, 2, 15).get_quarter_end(3).get_datetime(),
            datetime(2023, 12, 31),
        )
        self.assertEqual(
            Datetime.from_values(2012, 3, 7).get_quarter_end(-3).get_datetime(),
            datetime(2011, 6, 30),
        )

    def test_before(self):
        dt = Datetime.from_values(2020, 1, 15)
        dt.before(Period.DAY, 10)
        self.assertEqual(dt.get_datetime(), datetime(2020, 1, 5))

        dt = Datetime.from_values(2020, 1, 15)
        dt.before(Period.MONTH, 1)
        self.assertEqual(dt.get_datetime(), datetime(2019, 12, 15))

    def test_after(self):
        dt = Datetime.from_values(2020, 1, 15)
        dt.after(Period.DAY, 10)
        self.assertEqual(dt.get_datetime(), datetime(2020, 1, 25))

        dt = Datetime.from_values(2020, 1, 15)
        dt.after(Period.MONTH, 1)
        self.assertEqual(dt.get_datetime(), datetime(2020, 2, 15))

    def test_quarter_start(self):
        dt = Datetime.from_values(2020, 5, 15)
        dt.quarter_start()
        self.assertEqual(dt.get_datetime(), datetime(2020, 4, 1))

    def test_quarter_end(self):
        dt = Datetime.from_values(2020, 5, 15)
        dt.quarter_end()
        self.assertEqual(dt.get_datetime(), datetime(2020, 6, 30))

    def test_extract(self):
        dt = Datetime.from_values(2020, 1, 15, 12, 30)
        dt.extract("%Y-%m-%d")
        self.assertEqual(dt.get_datetime(), datetime(2020, 1, 15))
