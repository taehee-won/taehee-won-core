from unittest import TestCase
from time import time, sleep

from src.library.lib.Interval import Interval


class TestInterval(TestCase):
    def test_str(self):
        interval = Interval(1.00)
        self.assertIsInstance(str(interval), str)
        self.assertIn("Interval", str(interval))
        self.assertNotIn("name:", str(interval))
        self.assertIn("interval:", str(interval))

        interval = Interval(1.00, name="")
        self.assertIsInstance(str(interval), str)
        self.assertIn("Interval", str(interval))
        self.assertIn("name:", str(interval))
        self.assertIn("interval:", str(interval))

    def test_wait(self):
        interval = Interval(0.5)
        start = time()
        wait = interval.wait()
        self.assertTrue(0 < time() - start < 0.02)
        self.assertEqual(wait, 0)

        wait = interval.wait()
        self.assertTrue(0.5 < time() - start < 0.52)
        self.assertTrue(0.4 < wait < 0.5)

        sleep(0.2)

        wait = interval.wait()
        self.assertTrue(1 < time() - start < 1.02)
        self.assertTrue(0.2 < wait < 0.3)
