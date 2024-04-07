from unittest import TestCase
from copy import deepcopy

from src.library.lib.Trace import Trace
from src.library.data.HandledDictList import HandledDictList
from src.handle.indicator.RSI import RSI


class TestRSI(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Trace.set_levels(Trace.Level.NOTSET)

    @classmethod
    def tearDownClass(cls) -> None:
        Trace.set_levels()

    def setUp(self):
        self.source = [
            {"value1": 30, "value2": 10},
            {"value1": 31, "value2": 20},
            {"value1": 32, "value2": 35},
            {"value1": 33, "value2": 56},
            {"value1": 34, "value2": 42},
            {"value1": 35, "value2": 21},
            {"value1": 34, "value2": 1},
            {"value1": 33, "value2": 0},
            {"value1": 32, "value2": 0},
            {"value1": 31, "value2": 10},
            {"value1": 30, "value2": 7},
        ]

    def test_SIMPLE(self):
        data = HandledDictList(
            [
                RSI(
                    5,
                    "value1",
                    RSI.Average.SIMPLE,
                    target=RSI.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        for actual, expected in zip(
            [e["RSI"] for e in data],
            [50, 100, 100, 100, 100, 100, 80, 60, 40, 20, 0],
        ):
            self.assertAlmostEqual(actual, expected)
