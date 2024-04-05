from unittest import TestCase
from copy import deepcopy

from src.library.lib.Trace import Trace
from src.library.data.HandledDictList import HandledDictList
from src.handle.Compare import Compare


class TestCompare(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Trace.set_levels(Trace.Level.NOTSET)

    @classmethod
    def tearDownClass(cls) -> None:
        Trace.set_levels()

    def setUp(self):
        self.source = [
            {"value1": 30, "value2": 30},
            {"value1": 31, "value2": 40},
            {"value1": 32, "value2": 20},
        ]

    def test_Compare_GT_KEY_AND_KEY(self) -> None:
        key = "GT"
        data = HandledDictList(
            [
                Compare(
                    Compare.Method.GT,
                    Compare.Args.KEY_AND_KEY,
                    "value1",
                    "value2",
                    target=Compare.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertFalse(data[0][key])
        self.assertFalse(data[1][key])
        self.assertTrue(data[2][key])

    def test_Compare_GT_KEY_AND_VALUE(self) -> None:
        key = "test"
        data = HandledDictList(
            [
                Compare(
                    Compare.Method.GT,
                    Compare.Args.KEY_AND_VALUE,
                    "value1",
                    31,
                    key=key,
                    target=Compare.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertFalse(data[0][key])
        self.assertFalse(data[1][key])
        self.assertTrue(data[2][key])

    def test_Compare_GT_VALUE_AND_KEY(self) -> None:
        key = "GT"
        data = HandledDictList(
            [
                Compare(
                    Compare.Method.GT,
                    Compare.Args.VALUE_AND_KEY,
                    30,
                    "value2",
                    target=Compare.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertFalse(data[0][key])
        self.assertFalse(data[1][key])
        self.assertTrue(data[2][key])

    def test_Compare_GTE_KEY_AND_KEY(self) -> None:
        key = "GTE"
        data = HandledDictList(
            [
                Compare(
                    Compare.Method.GTE,
                    Compare.Args.KEY_AND_KEY,
                    "value1",
                    "value2",
                    target=Compare.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertTrue(data[0][key])
        self.assertFalse(data[1][key])
        self.assertTrue(data[2][key])

    def test_Compare_GTE_KEY_AND_VALUE(self) -> None:
        key = "GTE"
        data = HandledDictList(
            [
                Compare(
                    Compare.Method.GTE,
                    Compare.Args.KEY_AND_VALUE,
                    "value1",
                    31,
                    target=Compare.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertFalse(data[0][key])
        self.assertTrue(data[1][key])
        self.assertTrue(data[2][key])

    def test_Compare_GTE_VALUE_AND_KEY(self) -> None:
        key = "t"
        data = HandledDictList(
            [
                Compare(
                    Compare.Method.GTE,
                    Compare.Args.VALUE_AND_KEY,
                    30,
                    "value2",
                    key=key,
                    target=Compare.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertTrue(data[0][key])
        self.assertFalse(data[1][key])
        self.assertTrue(data[2][key])

    def test_Compare_LT_KEY_AND_KEY(self) -> None:
        key = "test"
        data = HandledDictList(
            [
                Compare(
                    Compare.Method.LT,
                    Compare.Args.KEY_AND_KEY,
                    "value1",
                    "value2",
                    key=key,
                    target=Compare.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertFalse(data[0][key])
        self.assertTrue(data[1][key])
        self.assertFalse(data[2][key])

    def test_Compare_LT_KEY_AND_VALUE(self) -> None:
        key = "LT"
        data = HandledDictList(
            [
                Compare(
                    Compare.Method.LT,
                    Compare.Args.KEY_AND_VALUE,
                    "value1",
                    31,
                    target=Compare.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertTrue(data[0][key])
        self.assertFalse(data[1][key])
        self.assertFalse(data[2][key])

    def test_Compare_LT_VALUE_AND_KEY(self) -> None:
        key = "LT"
        data = HandledDictList(
            [
                Compare(
                    Compare.Method.LT,
                    Compare.Args.VALUE_AND_KEY,
                    30,
                    "value2",
                    target=Compare.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertFalse(data[0][key])
        self.assertTrue(data[1][key])
        self.assertFalse(data[2][key])

    def test_Compare_LTE_KEY_AND_KEY(self) -> None:
        key = "LTE"
        data = HandledDictList(
            [
                Compare(
                    Compare.Method.LTE,
                    Compare.Args.KEY_AND_KEY,
                    "value1",
                    "value2",
                    target=Compare.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertTrue(data[0][key])
        self.assertTrue(data[1][key])
        self.assertFalse(data[2][key])

    def test_Compare_LTE_KEY_AND_VALUE(self) -> None:
        key = "t"
        data = HandledDictList(
            [
                Compare(
                    Compare.Method.LTE,
                    Compare.Args.KEY_AND_VALUE,
                    "value1",
                    31,
                    key=key,
                    target=Compare.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertTrue(data[0][key])
        self.assertTrue(data[1][key])
        self.assertFalse(data[2][key])

    def test_Compare_LTE_VALUE_AND_KEY(self) -> None:
        key = "LTE"
        data = HandledDictList(
            [
                Compare(
                    Compare.Method.LTE,
                    Compare.Args.VALUE_AND_KEY,
                    30,
                    "value2",
                    target=Compare.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertTrue(data[0][key])
        self.assertTrue(data[1][key])
        self.assertFalse(data[2][key])
