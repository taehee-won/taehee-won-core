from unittest import TestCase
from copy import deepcopy

from core import Trace, HandledDictList, Cross


class TestCross(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Trace.set_levels(Trace.Level.NOTSET)

    @classmethod
    def tearDownClass(cls) -> None:
        Trace.set_levels()

    def setUp(self):
        self.source = [
            {"value1": 30, "value2": 30},
            {"value1": 44, "value2": 32},
            {"value1": 46, "value2": 46},
            {"value1": 48, "value2": 48},
            {"value1": 52, "value2": 48},
            {"value1": 48, "value2": 49},
            {"value1": 47, "value2": 47},
            {"value1": 48, "value2": 47},
            {"value1": 46, "value2": 46},
        ]

    def test_Cross_Golden_KEY_AND_KEY(self) -> None:
        key = "Golden"
        data = HandledDictList(
            [
                Cross(
                    Cross.Method.Golden,
                    Cross.Args.KEY_AND_KEY,
                    "value1",
                    "value2",
                    target=Cross.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        indexes = [7]
        self.assertTrue(
            all(
                (element[key] if index in indexes else not element[key])
                for index, element in enumerate(data)
            )
        )

    def test_Cross_Golden_KEY_AND_VALUE(self) -> None:
        key = "test"
        data = HandledDictList(
            [
                Cross(
                    Cross.Method.Golden,
                    Cross.Args.KEY_AND_VALUE,
                    "value1",
                    48,
                    key=key,
                    target=Cross.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        indexes = [4]
        self.assertTrue(
            all(
                (element[key] if index in indexes else not element[key])
                for index, element in enumerate(data)
            )
        )

    def test_Cross_Golden_VALUE_AND_KEY(self) -> None:
        key = "Golden"
        data = HandledDictList(
            [
                Cross(
                    Cross.Method.Golden,
                    Cross.Args.VALUE_AND_KEY,
                    48,
                    "value2",
                    target=Cross.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        indexes = [6]
        self.assertTrue(
            all(
                (element[key] if index in indexes else not element[key])
                for index, element in enumerate(data)
            )
        )

    def test_Cross_Dead_KEY_AND_KEY(self) -> None:
        key = "Dead"
        data = HandledDictList(
            [
                Cross(
                    Cross.Method.Dead,
                    Cross.Args.KEY_AND_KEY,
                    "value1",
                    "value2",
                    target=Cross.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        indexes = [5]
        self.assertTrue(
            all(
                (element[key] if index in indexes else not element[key])
                for index, element in enumerate(data)
            )
        )

    def test_Cross_Dead_KEY_AND_VALUE(self) -> None:
        key = "Dead"
        data = HandledDictList(
            [
                Cross(
                    Cross.Method.Dead,
                    Cross.Args.KEY_AND_VALUE,
                    "value1",
                    48,
                    target=Cross.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        indexes = [6]
        self.assertTrue(
            all(
                (element[key] if index in indexes else not element[key])
                for index, element in enumerate(data)
            )
        )

    def test_Cross_Dead_VALUE_AND_KEY(self) -> None:
        key = "test"
        data = HandledDictList(
            [
                Cross(
                    Cross.Method.Dead,
                    Cross.Args.VALUE_AND_KEY,
                    48,
                    "value2",
                    key=key,
                    target=Cross.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        indexes = [5]
        self.assertTrue(
            all(
                (element[key] if index in indexes else not element[key])
                for index, element in enumerate(data)
            )
        )
