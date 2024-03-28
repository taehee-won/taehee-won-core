from unittest import TestCase
from datetime import datetime, timedelta

from src.library.lib.Datetime import Period, Datetime


class TestDatetime(TestCase):
    def test_eq(self):
        dt = Datetime.from_values(2020, 1, 15)

        self.assertTrue(dt == datetime(2020, 1, 15))
        self.assertFalse(dt == datetime(2020, 1, 16))

        self.assertTrue(dt == Datetime.from_values(2020, 1, 15))
        self.assertFalse(dt == Datetime.from_values(2020, 1, 16))

        with self.assertRaises(TypeError):
            eq = dt == 1

    def test_ne(self):
        dt = Datetime.from_values(2020, 1, 15)

        self.assertFalse(dt != datetime(2020, 1, 15))
        self.assertTrue(dt != datetime(2020, 1, 16))

        self.assertFalse(dt != Datetime.from_values(2020, 1, 15))
        self.assertTrue(dt != Datetime.from_values(2020, 1, 16))

        with self.assertRaises(TypeError):
            ne = dt != 1

    def test_lt(self):
        dt = Datetime.from_values(2020, 1, 15)

        self.assertFalse(dt < datetime(2020, 1, 14))
        self.assertFalse(dt < datetime(2020, 1, 15))
        self.assertTrue(dt < datetime(2020, 1, 16))

        self.assertFalse(dt < Datetime.from_values(2020, 1, 14))
        self.assertFalse(dt < Datetime.from_values(2020, 1, 15))
        self.assertTrue(dt < Datetime.from_values(2020, 1, 16))

        with self.assertRaises(TypeError):
            lt = dt < 1

    def test_le(self):
        dt = Datetime.from_values(2020, 1, 15)

        self.assertFalse(dt <= datetime(2020, 1, 14))
        self.assertTrue(dt <= datetime(2020, 1, 15))
        self.assertTrue(dt <= datetime(2020, 1, 16))

        self.assertFalse(dt <= Datetime.from_values(2020, 1, 14))
        self.assertTrue(dt <= Datetime.from_values(2020, 1, 15))
        self.assertTrue(dt <= Datetime.from_values(2020, 1, 16))

        with self.assertRaises(TypeError):
            le = dt <= 1

    def test_gt(self):
        dt = Datetime.from_values(2020, 1, 15)

        self.assertTrue(dt > datetime(2020, 1, 14))
        self.assertFalse(dt > datetime(2020, 1, 15))
        self.assertFalse(dt > datetime(2020, 1, 16))

        self.assertTrue(dt > Datetime.from_values(2020, 1, 14))
        self.assertFalse(dt > Datetime.from_values(2020, 1, 15))
        self.assertFalse(dt > Datetime.from_values(2020, 1, 16))

        with self.assertRaises(TypeError):
            gt = dt > 1

    def test_ge(self):
        dt = Datetime.from_values(2020, 1, 15)

        self.assertTrue(dt >= datetime(2020, 1, 14))
        self.assertTrue(dt >= datetime(2020, 1, 15))
        self.assertFalse(dt >= datetime(2020, 1, 16))

        self.assertTrue(dt >= Datetime.from_values(2020, 1, 14))
        self.assertTrue(dt >= Datetime.from_values(2020, 1, 15))
        self.assertFalse(dt >= Datetime.from_values(2020, 1, 16))

        with self.assertRaises(TypeError):
            ge = dt >= 1

    def test_from_values(self):
        self.assertEqual(
            Datetime.from_values(2020, 1, 1).to_datetime(),
            datetime(2020, 1, 1),
        )
        self.assertEqual(
            Datetime.from_values(2020, 1, 1, 12, 30).to_datetime(),
            datetime(2020, 1, 1, 12, 30),
        )

    def test_from_now(self):
        self.assertAlmostEqual(
            Datetime.from_now().to_datetime(),
            datetime.now(),
            delta=timedelta(seconds=1),
        )

    def test_from_str(self):
        self.assertEqual(
            Datetime.from_str("2023-12-11", "%Y-%m-%d").to_datetime(),
            datetime(2023, 12, 11),
        )

    def test_from_timestamp(self):
        timestamp = datetime.now().timestamp()
        self.assertEqual(
            Datetime.from_timestamp(timestamp).to_datetime().timestamp(),
            timestamp,
        )

    def test_get_datetime(self):
        dt = datetime(2008, 8, 16)
        self.assertEqual(
            Datetime(dt).to_datetime(),
            dt,
        )

    def test_to_str(self):
        self.assertEqual(
            Datetime.from_str("2023-12-11", "%Y-%m-%d").to_str("%Y%m%d"),
            "20231211",
        )

    def test_get_before(self):
        self.assertEqual(
            Datetime.from_values(2011, 3, 4).get_before(Period.DAY, 17).to_datetime(),
            datetime(2011, 2, 15),
        )
        self.assertEqual(
            Datetime.from_values(2001, 4, 7).get_before(Period.MONTH, 9).to_datetime(),
            datetime(2000, 7, 7),
        )

    def test_get_after(self):
        self.assertEqual(
            Datetime.from_values(2011, 3, 4).get_after(Period.DAY, 17).to_datetime(),
            datetime(2011, 3, 21),
        )
        self.assertEqual(
            Datetime.from_values(2001, 4, 7).get_after(Period.MONTH, 9).to_datetime(),
            datetime(2002, 1, 7),
        )

    def test_get_quarter_start(self):
        self.assertEqual(
            Datetime.from_values(2020, 4, 15).get_quarter_start().to_datetime(),
            datetime(2020, 4, 1),
        )
        self.assertEqual(
            Datetime.from_values(2023, 2, 15).get_quarter_start(3).to_datetime(),
            datetime(2023, 10, 1),
        )
        self.assertEqual(
            Datetime.from_values(2012, 3, 7).get_quarter_start(-3).to_datetime(),
            datetime(2011, 4, 1),
        )

    def test_get_quarter_end(self):
        self.assertEqual(
            Datetime.from_values(2020, 4, 15).get_quarter_end().to_datetime(),
            datetime(2020, 6, 30, 23, 59),
        )
        self.assertEqual(
            Datetime.from_values(2023, 2, 15).get_quarter_end(3).to_datetime(),
            datetime(2023, 12, 31, 23, 59),
        )
        self.assertEqual(
            Datetime.from_values(2012, 3, 7).get_quarter_end(-3).to_datetime(),
            datetime(2011, 6, 30, 23, 59),
        )

    def test_get_slice(self):
        dt = Datetime.from_values(2020, 3, 15, 12, 30, 44)

        self.assertEqual(dt.get_slice(Period.YEAR), datetime(2020, 1, 1))
        self.assertEqual(dt.get_slice(Period.MONTH), datetime(2020, 3, 1))
        self.assertEqual(dt.get_slice(Period.DAY), datetime(2020, 3, 15))
        self.assertEqual(dt.get_slice(Period.HOUR), datetime(2020, 3, 15, 12))
        self.assertEqual(dt.get_slice(Period.MINUTE), datetime(2020, 3, 15, 12, 30))

        with self.assertRaises(TypeError):
            self.assertEqual(
                dt.get_slice(Period.WEEK),
                datetime(2020, 3, 15, 12, 30, 44),
            )

    def test_set_before(self):
        dt = Datetime.from_values(2020, 1, 15)
        dt.set_before(Period.DAY, 10)
        self.assertEqual(dt.to_datetime(), datetime(2020, 1, 5))

        dt = Datetime.from_values(2020, 1, 15)
        dt.set_before(Period.MONTH, 1)
        self.assertEqual(dt.to_datetime(), datetime(2019, 12, 15))

    def test_set_after(self):
        dt = Datetime.from_values(2020, 1, 15)
        dt.set_after(Period.DAY, 10)
        self.assertEqual(dt.to_datetime(), datetime(2020, 1, 25))

        dt = Datetime.from_values(2020, 1, 15)
        dt.set_after(Period.MONTH, 1)
        self.assertEqual(dt.to_datetime(), datetime(2020, 2, 15))

    def test_set_quarter_start(self):
        dt = Datetime.from_values(2020, 5, 15)
        dt.set_quarter_start()
        self.assertEqual(dt.to_datetime(), datetime(2020, 4, 1))

    def test_set_quarter_end(self):
        dt = Datetime.from_values(2020, 5, 15)
        dt.set_quarter_end()
        self.assertEqual(dt.to_datetime(), datetime(2020, 6, 30, 23, 59))

    def test_set_slice(self):
        dt = Datetime.from_values(2020, 3, 15, 12, 30, 44)
        dt.set_slice(Period.YEAR)
        self.assertEqual(dt.to_datetime(), datetime(2020, 1, 1))

        dt = Datetime.from_values(2020, 3, 15, 12, 30, 44)
        dt.set_slice(Period.MONTH)
        self.assertEqual(dt.to_datetime(), datetime(2020, 3, 1))

        with self.assertRaises(TypeError):
            dt = Datetime.from_values(2020, 3, 15, 12, 30, 44)
            dt.set_slice(Period.WEEK)

        dt = Datetime.from_values(2020, 3, 15, 12, 30, 44)
        dt.set_slice(Period.DAY)
        self.assertEqual(dt.to_datetime(), datetime(2020, 3, 15))

        dt = Datetime.from_values(2020, 3, 15, 12, 30, 44)
        dt.set_slice(Period.HOUR)
        self.assertEqual(dt.to_datetime(), datetime(2020, 3, 15, 12))

        dt = Datetime.from_values(2020, 3, 15, 12, 30, 44)
        dt.set_slice(Period.MINUTE)
        self.assertEqual(dt.to_datetime(), datetime(2020, 3, 15, 12, 30))
