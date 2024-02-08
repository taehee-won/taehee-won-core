from unittest import TestCase
from time import time, sleep
from tempfile import mktemp
from os import remove

from src.library.lib.LinkedInterval import LinkedInterval


class TestLinkedInterval(TestCase):
    def test_init(self):
        interval = LinkedInterval({0.3: 1, 0.5: 2})
        self.assertIsInstance(interval, LinkedInterval)

    def test_str(self):
        interval = LinkedInterval({0.3: 1, 0.5: 2, 3: 10})
        self.assertIsInstance(str(interval), str)
        self.assertIn("LinkedInterval", str(interval))
        self.assertIn("values:3", str(interval))
        self.assertNotIn("file:", str(interval))
        self.assertNotIn("name:", str(interval))

        interval = LinkedInterval({0.3: 1, 0.5: 2}, name="TestLinkedInterval")
        self.assertIsInstance(str(interval), str)
        self.assertIn("LinkedInterval", str(interval))
        self.assertIn("values:2", str(interval))
        self.assertNotIn("file:", str(interval))
        self.assertIn("name:TestLinkedInterval", str(interval))

        file = mktemp()
        interval = LinkedInterval(
            {0.3: 1, 0.5: 2, 3: 10, 5: 20},
            file=file,
            name="TestLinkedInterval",
        )
        self.assertIsInstance(str(interval), str)
        self.assertIn("LinkedInterval", str(interval))
        self.assertIn("values:4", str(interval))
        self.assertIn(f"file:{file}", str(interval))
        self.assertIn("name:TestLinkedInterval", str(interval))

    def test_wait(self):
        interval = LinkedInterval({0.05: 1, 0.15: 2})
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

        interval = LinkedInterval({0.05: 1}, file)
        start = time()
        wait = interval.wait()
        self.assertTrue(0 < time() - start < 0.02)
        self.assertEqual(wait, 0)

        interval = LinkedInterval({0.05: 1}, file)
        wait = interval.wait()
        self.assertTrue(0.05 < time() - start < 0.07)
        self.assertTrue(0.03 < wait < 0.05)

        remove(file)
