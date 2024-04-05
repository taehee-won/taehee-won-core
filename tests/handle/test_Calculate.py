from unittest import TestCase
from copy import deepcopy

from src.library.lib.Trace import Trace
from src.library.data.HandledDictList import HandledDictList
from src.handle.Calculate import Calculate


class TestCalculate(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Trace.set_levels(Trace.Level.NOTSET)

    @classmethod
    def tearDownClass(cls) -> None:
        Trace.set_levels()

    def setUp(self):
        self.source = [
            {"value1": 2, "value2": 5},
            {"value1": 7, "value2": 4},
            {"value1": 9, "value2": -8},
            {"value1": 4, "value2": -2},
        ]

    def test_Calculate_ADD_KEY_AND_KEY(self) -> None:
        key = "ADD"
        data = HandledDictList(
            [
                Calculate(
                    Calculate.Method.ADD,
                    Calculate.Args.KEY_AND_KEY,
                    "value1",
                    "value2",
                    target=Calculate.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertEqual(data[0][key], 7)
        self.assertEqual(data[1][key], 11)
        self.assertEqual(data[2][key], 1)
        self.assertEqual(data[3][key], 2)

    def test_Calculate_ADD_KEY_AND_VALUE(self) -> None:
        key = "test"
        data = HandledDictList(
            [
                Calculate(
                    Calculate.Method.ADD,
                    Calculate.Args.KEY_AND_VALUE,
                    "value1",
                    10,
                    key=key,
                    target=Calculate.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertEqual(data[0][key], 12)
        self.assertEqual(data[1][key], 17)
        self.assertEqual(data[2][key], 19)
        self.assertEqual(data[3][key], 14)

    def test_Calculate_ADD_VALUE_AND_KEY(self) -> None:
        key = "ADD"
        data = HandledDictList(
            [
                Calculate(
                    Calculate.Method.ADD,
                    Calculate.Args.VALUE_AND_KEY,
                    10,
                    "value2",
                    target=Calculate.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertEqual(data[0][key], 15)
        self.assertEqual(data[1][key], 14)
        self.assertEqual(data[2][key], 2)
        self.assertEqual(data[3][key], 8)

    def test_Calculate_SUB_KEY_AND_KEY(self) -> None:
        key = "t"
        data = HandledDictList(
            [
                Calculate(
                    Calculate.Method.SUB,
                    Calculate.Args.KEY_AND_KEY,
                    "value1",
                    "value2",
                    key=key,
                    target=Calculate.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertEqual(data[0][key], -3)
        self.assertEqual(data[1][key], 3)
        self.assertEqual(data[2][key], 17)
        self.assertEqual(data[3][key], 6)

    def test_Calculate_SUB_KEY_AND_VALUE(self) -> None:
        key = "SUB"
        data = HandledDictList(
            [
                Calculate(
                    Calculate.Method.SUB,
                    Calculate.Args.KEY_AND_VALUE,
                    "value1",
                    10,
                    target=Calculate.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertEqual(data[0][key], -8)
        self.assertEqual(data[1][key], -3)
        self.assertEqual(data[2][key], -1)
        self.assertEqual(data[3][key], -6)

    def test_Calculate_SUB_VALUE_AND_KEY(self) -> None:
        key = "SUB"
        data = HandledDictList(
            [
                Calculate(
                    Calculate.Method.SUB,
                    Calculate.Args.VALUE_AND_KEY,
                    10,
                    "value2",
                    target=Calculate.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertEqual(data[0][key], 5)
        self.assertEqual(data[1][key], 6)
        self.assertEqual(data[2][key], 18)
        self.assertEqual(data[3][key], 12)

    def test_Calculate_MUL_KEY_AND_KEY(self) -> None:
        key = "MUL"
        data = HandledDictList(
            [
                Calculate(
                    Calculate.Method.MUL,
                    Calculate.Args.KEY_AND_KEY,
                    "value1",
                    "value2",
                    target=Calculate.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertEqual(data[0][key], 10)
        self.assertEqual(data[1][key], 28)
        self.assertEqual(data[2][key], -72)
        self.assertEqual(data[3][key], -8)

    def test_Calculate_MUL_KEY_AND_VALUE(self) -> None:
        key = "MUL"
        data = HandledDictList(
            [
                Calculate(
                    Calculate.Method.MUL,
                    Calculate.Args.KEY_AND_VALUE,
                    "value1",
                    10,
                    target=Calculate.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertEqual(data[0][key], 20)
        self.assertEqual(data[1][key], 70)
        self.assertEqual(data[2][key], 90)
        self.assertEqual(data[3][key], 40)

    def test_Calculate_MUL_VALUE_AND_KEY(self) -> None:
        key = "test"
        data = HandledDictList(
            [
                Calculate(
                    Calculate.Method.MUL,
                    Calculate.Args.VALUE_AND_KEY,
                    10,
                    "value2",
                    key=key,
                    target=Calculate.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertEqual(data[0][key], 50)
        self.assertEqual(data[1][key], 40)
        self.assertEqual(data[2][key], -80)
        self.assertEqual(data[3][key], -20)

    def test_Calculate_DIV_KEY_AND_KEY(self) -> None:
        key = "DIV"
        data = HandledDictList(
            [
                Calculate(
                    Calculate.Method.DIV,
                    Calculate.Args.KEY_AND_KEY,
                    "value1",
                    "value2",
                    target=Calculate.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertEqual(data[0][key], 2 / 5)
        self.assertEqual(data[1][key], 7 / 4)
        self.assertEqual(data[2][key], 9 / -8)
        self.assertEqual(data[3][key], 4 / -2)

    def test_Calculate_DIV_KEY_AND_VALUE(self) -> None:
        key = "t"
        data = HandledDictList(
            [
                Calculate(
                    Calculate.Method.DIV,
                    Calculate.Args.KEY_AND_VALUE,
                    "value1",
                    10,
                    key=key,
                    target=Calculate.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertEqual(data[0][key], 2 / 10)
        self.assertEqual(data[1][key], 7 / 10)
        self.assertEqual(data[2][key], 9 / 10)
        self.assertEqual(data[3][key], 4 / 10)

    def test_Calculate_DIV_VALUE_AND_KEY(self) -> None:
        key = "DIV"
        data = HandledDictList(
            [
                Calculate(
                    Calculate.Method.DIV,
                    Calculate.Args.VALUE_AND_KEY,
                    10,
                    "value2",
                    target=Calculate.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        self.assertEqual(data[0][key], 10 / 5)
        self.assertEqual(data[1][key], 10 / 4)
        self.assertEqual(data[2][key], 10 / -8)
        self.assertEqual(data[3][key], 10 / -2)
