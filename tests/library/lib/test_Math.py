from unittest import TestCase
from math import sqrt

from src.library.lib.Math import Math


class TestMath(TestCase):
    def test_floor(self):
        self.assertEqual(Math.floor(3.7), 3)
        self.assertEqual(Math.floor(3.7, 0.5), 3.5)
        self.assertEqual(Math.floor(-3.7), -4)
        self.assertEqual(Math.floor(-3.2, 0.5), -3.5)

    def test_max(self):
        self.assertEqual(Math.max([1, 2, 3]), 3)
        self.assertEqual(Math.max([1, 2.5, 3]), 3)
        self.assertIsNone(Math.max([]))

    def test_min(self):
        self.assertEqual(Math.min([1, 2, 3]), 1)
        self.assertEqual(Math.min([1, 2.5, 3]), 1)
        self.assertIsNone(Math.min([]))

    def test_is_NaN(self):
        self.assertTrue(Math.is_NaN(float("NaN")))
        self.assertFalse(Math.is_NaN(float(0.03)))

    def test_ratio(self):
        self.assertEqual(Math.ratio(10, 2), 5)
        self.assertTrue(Math.is_NaN(Math.ratio(10, 0)))

    def test_percentage(self):
        self.assertEqual(Math.percentage(50, 100), 50)
        self.assertTrue(Math.is_NaN(Math.percentage(10, 0)))

    def test_change_percentage(self):
        self.assertEqual(Math.change_percentage(110, 100), 10)
        self.assertEqual(Math.change_percentage(-100, 100), -200)
        self.assertEqual(Math.change_percentage(100, -100), -200)
        self.assertTrue(Math.is_NaN(Math.change_percentage(100, 0)))

    def test_average(self):
        self.assertEqual(Math.average([10, 20, 30]), 20)
        self.assertEqual(Math.average([1, 2.5, 3]), 2.1666666666666665)
        self.assertEqual(Math.average([10]), 10)
        self.assertAlmostEqual(Math.average([1e9, -1e9]), 0)
        self.assertTrue(Math.is_NaN(Math.average([])))

    def test_variance(self):
        self.assertAlmostEqual(Math.variance([10, 20, 30]), 66.66666666666667)
        self.assertEqual(Math.variance([10]), 0)
        self.assertAlmostEqual(Math.variance([1e9, -1e9]), 1e18)
        self.assertTrue(Math.is_NaN(Math.variance([])))

    def test_standard_deviation(self):
        self.assertAlmostEqual(
            Math.standard_deviation([10, 20, 30]), sqrt(66.66666666666667)
        )
        self.assertEqual(Math.standard_deviation([10]), 0)
        self.assertAlmostEqual(Math.standard_deviation([1e9, -1e9]), 1e9)
        self.assertTrue(Math.is_NaN(Math.standard_deviation([])))

    def test_sum(self):
        self.assertEqual(Math.sum([1, 2, 3]), 6)
        self.assertEqual(Math.sum([]), 0)

    def test_range(self):
        self.assertEqual(Math.range([10, 20, 30]), 20)
        self.assertTrue(Math.is_NaN(Math.range([])))
