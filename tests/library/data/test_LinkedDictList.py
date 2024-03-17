from unittest import TestCase
from datetime import datetime

from src.library.lib.Trace import TraceLevel, Trace
from src.library.data.DictList import DictList
from src.library.data.LinkedDictList import Node, LinkedDictList


class TestLinkedDictList(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Trace.set_levels(TraceLevel.NOTSET)

    @classmethod
    def tearDownClass(cls) -> None:
        Trace.set_levels()

    def test_init(self):
        data = LinkedDictList("datetime", [])
        self.assertIsInstance(data, LinkedDictList)

    def test_len(self):
        data = LinkedDictList(
            "datetime",
            [
                Node(DictList(), []),
                Node(DictList(), []),
                Node(DictList(), []),
            ],
        )
        self.assertEqual(len(data), 3)

    def test_index(self):
        data = LinkedDictList(
            "datetime",
            [
                Node(DictList(name="first"), []),
                Node(DictList(name="second"), []),
                Node(DictList(name="third"), []),
            ],
        )
        self.assertIn("name:first", str(data[0].data))
        self.assertIn("name:second", str(data[1].data))
        self.assertIn("name:third", str(data[2].data))

    def test_str(self):
        data = LinkedDictList(
            "datetime",
            [
                Node(DictList(name="first"), []),
                Node(DictList(name="second"), []),
                Node(DictList(name="third"), []),
            ],
        )
        self.assertIsInstance(str(data), str)
        self.assertIn("LinkedDictList", str(data))
        self.assertIn("key:datetime", str(data))
        self.assertIn("nodes:3", str(data))
        self.assertNotIn("handles:", str(data))
        self.assertNotIn("name:", str(data))

        data = LinkedDictList(
            "datetime",
            [
                Node(DictList(name="first"), []),
                Node(DictList(name="second"), []),
            ],
            [lambda e, p: p],
            name="TestLinkedDictList",
        )
        self.assertIsInstance(str(data), str)
        self.assertIn("LinkedDictList", str(data))
        self.assertIn("key:datetime", str(data))
        self.assertIn("nodes:2", str(data))
        self.assertIn("handles:1", str(data))
        self.assertIn("name:TestLinkedDictList", str(data))

    count = 0

    @staticmethod
    def _count(element, pipe) -> None:
        element["count"] = TestLinkedDictList.count
        TestLinkedDictList.count += 1

    def test_handle_single(self):
        TestLinkedDictList.count = 0

        first = DictList(name="first")
        data = LinkedDictList("datetime", [Node(first, [TestLinkedDictList._count])])

        first.append({"datetime": datetime(2021, 1, 1)})
        first.append({"datetime": datetime(2021, 1, 2)})

        data.handle()

        self.assertEqual(first[0]["count"], 0)
        self.assertEqual(first[1]["count"], 1)

    def test_handle_linked(self):
        TestLinkedDictList.count = 0

        first = DictList(name="first")
        second = DictList(name="second")
        data = LinkedDictList(
            "datetime",
            [
                Node(first, [TestLinkedDictList._count]),
                Node(second, [TestLinkedDictList._count]),
            ],
        )

        first.append({"datetime": datetime(2021, 1, 1)})
        first.append({"datetime": datetime(2021, 2, 1)})
        second.append({"datetime": datetime(2021, 3, 1)})
        second.append({"datetime": datetime(2021, 4, 1)})

        data.handle()

        self.assertEqual(first[0]["count"], 0)
        self.assertEqual(first[1]["count"], 1)
        self.assertEqual(second[0]["count"], 2)
        self.assertEqual(second[1]["count"], 3)

    def test_handle_sequential(self):
        TestLinkedDictList.count = 0

        first = DictList(name="first")
        second = DictList(name="second")
        third = DictList(name="third")
        data = LinkedDictList(
            "datetime",
            [
                Node(first, [TestLinkedDictList._count]),
                Node(second, [TestLinkedDictList._count]),
                Node(third, [TestLinkedDictList._count]),
            ],
        )

        third.append({"datetime": datetime(2021, 1, 1)})
        second.append({"datetime": datetime(2021, 2, 1)})
        third.append({"datetime": datetime(2021, 3, 1)})
        second.append({"datetime": datetime(2021, 4, 1)})
        first.append({"datetime": datetime(2021, 5, 1)})
        first.append({"datetime": datetime(2021, 6, 1)})
        third.append({"datetime": datetime(2021, 7, 1)})
        second.append({"datetime": datetime(2021, 8, 1)})
        first.append({"datetime": datetime(2021, 9, 1)})

        data.handle()

        self.assertEqual(third[0]["count"], 0)
        self.assertEqual(second[0]["count"], 1)
        self.assertEqual(third[1]["count"], 2)
        self.assertEqual(second[1]["count"], 3)
        self.assertEqual(first[0]["count"], 4)
        self.assertEqual(first[1]["count"], 5)
        self.assertEqual(third[2]["count"], 6)

        with self.assertRaises(KeyError):
            self.assertEqual(second[2]["count"], 7)

        with self.assertRaises(KeyError):
            self.assertEqual(first[2]["count"], 8)

        third.append({"datetime": datetime(2021, 10, 1)})
        first.append({"datetime": datetime(2021, 11, 1)})
        second.append({"datetime": datetime(2021, 12, 1)})

        data.handle()

        self.assertEqual(third[0]["count"], 0)
        self.assertEqual(second[0]["count"], 1)
        self.assertEqual(third[1]["count"], 2)
        self.assertEqual(second[1]["count"], 3)
        self.assertEqual(first[0]["count"], 4)
        self.assertEqual(first[1]["count"], 5)
        self.assertEqual(third[2]["count"], 6)
        self.assertEqual(second[2]["count"], 7)
        self.assertEqual(first[2]["count"], 8)
        self.assertEqual(third[3]["count"], 9)

        with self.assertRaises(KeyError):
            self.assertEqual(first[3]["count"], 10)

        with self.assertRaises(KeyError):
            self.assertEqual(second[3]["count"], 11)
