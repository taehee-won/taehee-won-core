from unittest import TestCase
from time import time, sleep
from tempfile import mktemp
from os import remove

from src.library.Interval import Interval


class TestInterval(TestCase):
    def test_init(self):
        interval = Interval({0.3: 1, 0.5: 2})
        self.assertIsInstance(interval, Interval)

    def test_str(self):
        interval = Interval({0.3: 1, 0.5: 2, 3: 10})
        self.assertIsInstance(str(interval), str)
        self.assertIn("Interval", str(interval))
        self.assertIn("values:3", str(interval))
        self.assertNotIn("file:", str(interval))
        self.assertNotIn("name:", str(interval))

        interval = Interval({0.3: 1, 0.5: 2}, name="TestInterval")
        self.assertIsInstance(str(interval), str)
        self.assertIn("Interval", str(interval))
        self.assertIn("values:2", str(interval))
        self.assertNotIn("file:", str(interval))
        self.assertIn("name:TestInterval", str(interval))

        file = mktemp()
        interval = Interval(
            {0.3: 1, 0.5: 2, 3: 10, 5: 20},
            file=file,
            name="TestInterval",
        )
        self.assertIsInstance(str(interval), str)
        self.assertIn("Interval", str(interval))
        self.assertIn("values:4", str(interval))
        self.assertIn(f"file:{file}", str(interval))
        self.assertIn("name:TestInterval", str(interval))

    def test_wait(self):
        interval = Interval({0.05: 1, 0.15: 2})
        start = time()
        wait = interval.wait()
        self.assertTrue(0 < time() - start < 0.02)
        self.assertEqual(wait, 0)

        wait = interval.wait()
        self.assertTrue(0.05 < time() - start < 0.07)
        self.assertTrue(0.03 < wait < 0.05)

        sleep(0.05)

        wait = interval.wait()
        self.assertTrue(0.15 < time() - start < 0.17)
        self.assertTrue(0.03 < wait < 0.05)

    def test_file(self):
        file = mktemp()

        interval = Interval({0.05: 1}, file)
        start = time()
        wait = interval.wait()
        self.assertTrue(0 < time() - start < 0.02)
        self.assertEqual(wait, 0)

        interval = Interval({0.05: 1}, file)
        wait = interval.wait()
        self.assertTrue(0.05 < time() - start < 0.07)
        self.assertTrue(0.03 < wait < 0.05)

        remove(file)

    def test_simplified_init(self):
        interval = Interval(1.00)
        self.assertIsInstance(interval, Interval)

    def test_simplified_str(self):
        interval = Interval(1)
        self.assertIsInstance(str(interval), str)
        self.assertIn("Interval", str(interval))
        self.assertNotIn("name:", str(interval))

        interval = Interval(1.00, name="TestInterval")
        self.assertIsInstance(str(interval), str)
        self.assertIn("Interval", str(interval))
        self.assertIn("name:TestInterval", str(interval))

    def test_simplified_wait(self):
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
