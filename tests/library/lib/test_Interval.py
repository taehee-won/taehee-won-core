from unittest import TestCase
from time import time, sleep

from src.library.lib.Interval import Interval


class TestInterval(TestCase):
    def test_init(self):
        interval = Interval(1.00)
        self.assertIsInstance(interval, Interval)

    def test_str(self):
        interval = Interval(1)
        self.assertIsInstance(str(interval), str)
        self.assertIn("Interval", str(interval))
        self.assertIn("value:1", str(interval))
        self.assertNotIn("name:", str(interval))

        interval = Interval(1.00, name="TestInterval")
        self.assertIsInstance(str(interval), str)
        self.assertIn("Interval", str(interval))
        self.assertIn("value:1", str(interval))
        self.assertIn("name:TestInterval", str(interval))

    def test_wait(self):
        interval = Interval(0.1)
        start = time()
        wait = interval.wait()
        self.assertTrue(0 < time() - start < 0.02)
        self.assertEqual(wait, 0)

        wait = interval.wait()
        self.assertTrue(0.1 < time() - start < 0.12)
        self.assertTrue(0.08 < wait < 0.1)

        sleep(0.05)

        wait = interval.wait()
        self.assertTrue(0.2 < time() - start < 0.22)
        self.assertTrue(0.03 < wait < 0.05)
