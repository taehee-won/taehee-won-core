from unittest import TestCase
from copy import deepcopy

from src.library.lib.Trace import Trace
from src.library.data.HandledDictList import HandledDictList
from src.handle.Aggregate import Aggregate


class TestAggregate(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Trace.set_levels(Trace.Level.NOTSET)

    @classmethod
    def tearDownClass(cls) -> None:
        Trace.set_levels()

    def setUp(self):
        self.source = [
            {"value1": True, "value2": True, "value3": True},
            {"value1": False, "value2": True, "value3": True},
            {"value1": True, "value2": False, "value3": True},
            {"value1": True, "value2": True, "value3": False},
            {"value1": False, "value2": False, "value3": True},
            {"value1": False, "value2": True, "value3": False},
            {"value1": True, "value2": False, "value3": False},
            {"value1": False, "value2": False, "value3": False},
        ]

    def test_Aggregate_ALL(self) -> None:
        key = "ALL"
        data = HandledDictList(
            [
                Aggregate(
                    Aggregate.Method.ALL,
                    ["value1", "value2", "value3"],
                    target=Aggregate.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        indexes = [0]
        self.assertTrue(
            all(
                (element[key] if index in indexes else not element[key])
                for index, element in enumerate(data)
            )
        )

    def test_Aggregate_ALL_key(self) -> None:
        key = "test"
        data = HandledDictList(
            [
                Aggregate(
                    Aggregate.Method.ALL,
                    ["value1", "value2", "value3"],
                    key=key,
                    target=Aggregate.Param.ELEMENT,
                ).get_handle(),
            ],
            deepcopy(self.source),
        )
        indexes = [0]
        self.assertTrue(
            all(
                (element[key] if index in indexes else not element[key])
                for index, element in enumerate(data)
            )
        )

    def test_Aggregate_ANY(self) -> None:
        key = "ANY"
        data = HandledDictList(
            [
                Aggregate(
                    Aggregate.Method.ANY,
                    ["value1", "value2", "value3"],
                    target=Aggregate.Param.ELEMENT,
                ).get_handle()
            ],
            deepcopy(self.source),
        )
        indexes = [0, 1, 2, 3, 4, 5, 6]
        self.assertTrue(
            all(
                (element[key] if index in indexes else not element[key])
                for index, element in enumerate(data)
            )
        )

    def test_Aggregate_ANY_key(self) -> None:
        key = "test"
        data = HandledDictList(
            [
                Aggregate(
                    Aggregate.Method.ANY,
                    ["value1", "value2", "value3"],
                    key=key,
                    target=Aggregate.Param.ELEMENT,
                ).get_handle(),
            ],
            deepcopy(self.source),
        )
        indexes = [0, 1, 2, 3, 4, 5, 6]
        self.assertTrue(
            all(
                (element[key] if index in indexes else not element[key])
                for index, element in enumerate(data)
            )
        )
