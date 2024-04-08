from unittest import TestCase
from copy import deepcopy

from core import Trace, HandledDictList, MA


class TestMA(TestCase):
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
                MA(
                    5,
                    "value1",
                    MA.Average.SIMPLE,
                    key="MA1",
                    target=MA.Param.ELEMENT,
                ).get_handle(),
                MA(
                    8,
                    "value2",
                    MA.Average.SIMPLE,
                    key="MA2",
                    target=MA.Param.ELEMENT,
                ).get_handle(),
            ],
            deepcopy(self.source),
        )
        self.assertListEqual(
            [e["MA1"] for e in data],
            [
                30,
                (30 + 31) / 2,
                (30 + 31 + 32) / 3,
                (30 + 31 + 32 + 33) / 4,
                (30 + 31 + 32 + 33 + 34) / 5,
                (31 + 32 + 33 + 34 + 35) / 5,
                (32 + 33 + 34 + 35 + 34) / 5,
                (33 + 34 + 35 + 34 + 33) / 5,
                (34 + 35 + 34 + 33 + 32) / 5,
                (35 + 34 + 33 + 32 + 31) / 5,
                (34 + 33 + 32 + 31 + 30) / 5,
            ],
        )
        self.assertListEqual(
            [e["MA2"] for e in data],
            [
                10,
                (10 + 20) / 2,
                (10 + 20 + 35) / 3,
                (10 + 20 + 35 + 56) / 4,
                (10 + 20 + 35 + 56 + 42) / 5,
                (10 + 20 + 35 + 56 + 42 + 21) / 6,
                (10 + 20 + 35 + 56 + 42 + 21 + 1) / 7,
                (10 + 20 + 35 + 56 + 42 + 21 + 1 + 0) / 8,
                (20 + 35 + 56 + 42 + 21 + 1 + 0 + 0) / 8,
                (35 + 56 + 42 + 21 + 1 + 0 + 0 + 10) / 8,
                (56 + 42 + 21 + 1 + 0 + 0 + 10 + 7) / 8,
            ],
        )

    def test_EXPONENTIAL(self):
        data = HandledDictList(
            [
                MA(
                    5,
                    "value1",
                    MA.Average.EXPONENTIAL,
                    key="MA1",
                    target=MA.Param.ELEMENT,
                ).get_handle(),
                MA(
                    8,
                    "value2",
                    MA.Average.EXPONENTIAL,
                    key="MA2",
                    target=MA.Param.ELEMENT,
                ).get_handle(),
            ],
            deepcopy(self.source),
        )
        self.assertListEqual(
            [e["MA1"] for e in data][:5],
            [
                30,
                (30 + 31) / 2,
                (30 + 31 + 32) / 3,
                (30 + 31 + 32 + 33) / 4,
                (30 + 31 + 32 + 33 + 34) / 5,
            ],
        )
        self.assertLess(data[4]["MA1"], data[5]["MA1"])
        self.assertLess(data[5]["MA1"], data[6]["MA1"])
        # self.assertLess(data[6]["MA1"], data[7]["MA1"])
        self.assertGreater(data[7]["MA1"], data[8]["MA1"])
        self.assertGreater(data[8]["MA1"], data[9]["MA1"])
        self.assertGreater(data[9]["MA1"], data[10]["MA1"])
        self.assertListEqual(
            [e["MA2"] for e in data][:8],
            [
                10,
                (10 + 20) / 2,
                (10 + 20 + 35) / 3,
                (10 + 20 + 35 + 56) / 4,
                (10 + 20 + 35 + 56 + 42) / 5,
                (10 + 20 + 35 + 56 + 42 + 21) / 6,
                (10 + 20 + 35 + 56 + 42 + 21 + 1) / 7,
                (10 + 20 + 35 + 56 + 42 + 21 + 1 + 0) / 8,
            ],
        )
        self.assertGreater(data[7]["MA2"], data[8]["MA2"])
        self.assertGreater(data[8]["MA2"], data[9]["MA2"])
        self.assertGreater(data[9]["MA2"], data[10]["MA2"])

    def test_SMOOTHED(self):
        data = HandledDictList(
            [
                MA(
                    5,
                    "value1",
                    MA.Average.SMOOTHED,
                    key="MA1",
                    target=MA.Param.ELEMENT,
                ).get_handle(),
                MA(
                    8,
                    "value2",
                    MA.Average.SMOOTHED,
                    key="MA2",
                    target=MA.Param.ELEMENT,
                ).get_handle(),
            ],
            deepcopy(self.source),
        )
        self.assertListEqual(
            [e["MA1"] for e in data][:5],
            [
                30,
                (30 + 31) / 2,
                (30 + 31 + 32) / 3,
                (30 + 31 + 32 + 33) / 4,
                (30 + 31 + 32 + 33 + 34) / 5,
            ],
        )
        self.assertLess(data[4]["MA1"], data[5]["MA1"])
        self.assertLess(data[5]["MA1"], data[6]["MA1"])
        self.assertLess(data[6]["MA1"], data[7]["MA1"])
        self.assertGreater(data[7]["MA1"], data[8]["MA1"])
        self.assertGreater(data[8]["MA1"], data[9]["MA1"])
        self.assertGreater(data[9]["MA1"], data[10]["MA1"])
        self.assertListEqual(
            [e["MA2"] for e in data][:8],
            [
                10,
                (10 + 20) / 2,
                (10 + 20 + 35) / 3,
                (10 + 20 + 35 + 56) / 4,
                (10 + 20 + 35 + 56 + 42) / 5,
                (10 + 20 + 35 + 56 + 42 + 21) / 6,
                (10 + 20 + 35 + 56 + 42 + 21 + 1) / 7,
                (10 + 20 + 35 + 56 + 42 + 21 + 1 + 0) / 8,
            ],
        )
        self.assertGreater(data[7]["MA2"], data[8]["MA2"])
        self.assertGreater(data[8]["MA2"], data[9]["MA2"])
        self.assertGreater(data[9]["MA2"], data[10]["MA2"])
