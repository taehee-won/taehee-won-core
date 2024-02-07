from unittest import TestCase
from random import randint
from os import remove
from os.path import join, abspath, dirname
from tempfile import mktemp

from src.library.data.OrderedDictList import DictListFile, OrderedDictList
from .test_DictList import (
    _DICTLIST_DICTLIST,
    _CSV_CSV,
    _JSON_JSON,
    _DICTLIST_CSV,
    _DICTLIST,
)


_TEST_FILE_DIR = join(dirname(abspath(__file__)), "OrderedDictList")

# data file type, extension
_DICTLIST_DICTLIST_NAME_SORTED = join(_TEST_FILE_DIR, "DictList_name_sorted.DictList")
_CSV_CSV_NAME_SORTED = join(_TEST_FILE_DIR, "csv_name_sorted.csv")
_JSON_JSON_NAME_SORTED = join(_TEST_FILE_DIR, "json_name_sorted.json")


class TestOrderedDictList(TestCase):
    def setUp(self):
        self.source = [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 25},
            {"name": "Doe", "age": 22},
        ]
        self.source_name_sorted = [
            {"name": "Doe", "age": 22},
            {"name": "Jane", "age": 25},
            {"name": "John", "age": 30},
        ]
        self.source_age_sorted = [
            {"name": "Doe", "age": 22},
            {"name": "Jane", "age": 25},
            {"name": "John", "age": 30},
        ]
        self.data_name_sorted = OrderedDictList("name", self.source)
        self.data_age_sorted = OrderedDictList("age", self.source)

    # def test_prepare_TestOrderedDictList(self):
    #     self.data_name_sorted.write(
    #         _DICTLIST_DICTLIST_NAME_SORTED, DictListFile.DICTLIST
    #     )
    #     self.data_name_sorted.write(_CSV_CSV_NAME_SORTED, DictListFile.CSV)
    #     self.data_name_sorted.write(_JSON_JSON_NAME_SORTED, DictListFile.JSON)

    def test_init_read(self):
        data = OrderedDictList("name", _DICTLIST_DICTLIST)
        for index, element in enumerate(data):
            self.assertEqual(element, self.source_name_sorted[index])

        data = OrderedDictList("age", _DICTLIST_CSV, type=DictListFile.DICTLIST)
        for index, element in enumerate(data):
            self.assertEqual(element, self.source_age_sorted[index])

    def test_len(self):
        self.assertEqual(len(self.data_name_sorted), len(self.source))
        self.assertEqual(len(self.data_age_sorted), len(self.source))

    def test_iter(self):
        for index, element in enumerate(self.data_name_sorted):
            self.assertEqual(element, self.source_name_sorted[index])

        for index, element in enumerate(self.data_age_sorted):
            self.assertEqual(element, self.source_age_sorted[index])

    def test_iter_overlap(self):
        data = []
        for index, element in enumerate(self.data_name_sorted):
            if index == 1:
                self.assertEqual(
                    [e for e in self.data_name_sorted],
                    self.source_name_sorted,
                )

            data.append(element)

        self.assertEqual(data, self.source_name_sorted)

    def test_index(self):
        index = randint(0, len(self.source) - 1)
        element = self.data_name_sorted[index]
        self.assertIsInstance(element, dict)
        self.assertEqual(element, self.source_name_sorted[index])

        index = randint(0, len(self.source) - 1)
        element = self.data_age_sorted[index]
        self.assertIsInstance(element, dict)
        self.assertEqual(element, self.source_age_sorted[index])

    def test_slice(self):
        index1 = randint(0, len(self.source) - 1)
        index2 = randint(0, len(self.source) - 1)

        data = self.data_name_sorted[min(index1, index2) : max(index1, index2)]
        self.assertIsInstance(data, OrderedDictList)
        self.assertListEqual(
            data._data,  # type: ignore
            self.source_name_sorted[min(index1, index2) : max(index1, index2)],
        )

    def test_get_value(self):
        index = randint(0, len(self.source) - 1)
        self.assertEqual(
            self.data_name_sorted.get(self.source[index]["name"]),
            self.source[index],
        )

        index = randint(0, len(self.source) - 1)
        self.assertEqual(
            self.data_age_sorted.get(self.source[index]["age"]),
            self.source[index],
        )

        self.assertIsNone(self.data_name_sorted.get("name", "Theodore"))

    def test_get_key_value(self):
        index = randint(0, len(self.source) - 1)
        self.assertEqual(
            self.data_name_sorted.get("name", self.source[index]["name"]),
            self.source[index],
        )

        index = randint(0, len(self.source) - 1)
        self.assertEqual(
            self.data_name_sorted.get("age", self.source[index]["age"]),
            self.source[index],
        )

        self.assertIsNone(self.data_name_sorted.get("name", "Theodore"))

    def test_get_query(self):
        index = randint(0, len(self.source) - 1)
        self.assertEqual(
            self.data_name_sorted.get({"name": self.source[index]["name"]}),
            self.source[index],
        )

        index = randint(0, len(self.source) - 1)
        self.assertEqual(
            self.data_name_sorted.get({"age": self.source[index]["age"]}),
            self.source[index],
        )

        self.assertIsNone(self.data_name_sorted.get({"name": "Theodore"}))
        self.assertIsNone(self.data_name_sorted.get({"name": "Jane", "age": 10}))

    def test_items_value(self):
        data = self.data_name_sorted.items("John")
        self.assertIsInstance(data, OrderedDictList)
        self.assertEqual(len(data), 1)

        data = self.data_age_sorted.items(40)
        self.assertIsInstance(data, OrderedDictList)
        self.assertEqual(len(data), 0)

    def test_items_key_value(self):
        data = self.data_name_sorted.items("name", "John")
        self.assertIsInstance(data, OrderedDictList)
        self.assertEqual(len(data), 1)

    def test_items_query(self):
        data = self.data_name_sorted.items({"name": "John"})
        self.assertIsInstance(data, OrderedDictList)
        self.assertEqual(len(data), 1)

    def test_items(self):
        data = self.data_name_sorted.items()
        self.assertIsInstance(data, OrderedDictList)
        self.assertEqual(len(data), 3)

    def test_values(self):
        names = self.data_name_sorted.values()
        self.assertIn("John", names)
        self.assertEqual(len(names), 3)

    def test_values_key(self):
        names = self.data_name_sorted.values("name")
        self.assertIn("John", names)
        self.assertEqual(len(names), 3)

    def test_append(self):
        element = {"name": "Atom", "age": 40}
        self.data_name_sorted.append(element)
        self.assertIn(element, self.data_name_sorted._data)
        self.assertEqual(element, self.data_name_sorted[0])

    def test_extend(self):
        data = [{"name": "Alice", "age": 26}, {"name": "Bob", "age": 24}]
        self.data_name_sorted.extend(data)
        self.assertEqual(len(self.data_name_sorted._data), 5)
        self.assertEqual(data[0], self.data_name_sorted[0])
        self.assertEqual(data[1], self.data_name_sorted[1])

    def test_insert(self):
        element = {"name": "Charlie", "age": 20}
        with self.assertRaises(TypeError):
            self.data_name_sorted.insert(element, index=1)

    def test_remove(self):
        element = {"name": "John", "age": 30}
        self.data_name_sorted.remove(element)
        self.assertNotIn(element, self.data_name_sorted._data)

    def test_pop(self):
        element = self.data_name_sorted.pop(0)
        self.assertEqual(element, self.source_name_sorted[0])
        self.assertEqual(len(self.data_name_sorted._data), 2)

    def test_clear(self):
        self.data_name_sorted.clear()
        self.assertEqual(len(self.data_name_sorted._data), 0)

    def test_include(self):
        data = self.data_age_sorted.include([22, 25, 35])
        self.assertIsInstance(data, OrderedDictList)
        self.assertEqual(len(data._data), 2)

    def test_include_key(self):
        data = self.data_name_sorted.include("age", [22, 25, 35])
        self.assertIsInstance(data, OrderedDictList)
        self.assertEqual(len(data._data), 2)

    def test_exclude(self):
        data = self.data_name_sorted.exclude(["John", "Theodore"])
        self.assertIsInstance(data, OrderedDictList)
        self.assertEqual(len(data._data), 2)

    def test_exclude_key(self):
        data = self.data_name_sorted.exclude("name", ["John", "Theodore"])
        self.assertIsInstance(data, OrderedDictList)
        self.assertEqual(len(data._data), 2)

    def test_read(self):
        data = OrderedDictList("name")
        data.read(_DICTLIST_DICTLIST)
        for index, element in enumerate(data):
            self.assertEqual(element, self.source_name_sorted[index])

        data = OrderedDictList("age")
        data.read(_CSV_CSV)
        for element in data:
            element["age"] = int(element["age"])

        for index, element in enumerate(data):
            self.assertEqual(element, self.source_age_sorted[index])

        data = OrderedDictList("name")
        data.read(_JSON_JSON)
        for index, element in enumerate(data):
            self.assertEqual(element, self.source_name_sorted[index])

        data = OrderedDictList("name")
        data.read(_DICTLIST_CSV, DictListFile.DICTLIST)
        for index, element in enumerate(data):
            self.assertEqual(element, self.source_name_sorted[index])

        data = OrderedDictList("age")
        data.read(_DICTLIST, DictListFile.DICTLIST)
        for index, element in enumerate(data):
            self.assertEqual(element, self.source_age_sorted[index])

    def test_read_str(self):
        data = OrderedDictList("name")
        data.read(_DICTLIST_CSV, "DictList")
        for index, element in enumerate(data):
            self.assertEqual(element, self.source_name_sorted[index])

        data = OrderedDictList("age")
        data.read(_DICTLIST, "DictList")
        for index, element in enumerate(data):
            self.assertEqual(element, self.source_age_sorted[index])

    @staticmethod
    def compare(file1, file2):
        with open(file1, "rb") as f1, open(file2, "rb") as f2:
            return f1.read() == f2.read()

    def test_write(self):
        file = mktemp()
        self.data_name_sorted.write(file, DictListFile.DICTLIST)
        self.assertTrue(
            TestOrderedDictList.compare(file, _DICTLIST_DICTLIST_NAME_SORTED)
        )
        remove(file)

        file = mktemp()
        self.data_name_sorted.write(file, DictListFile.CSV)
        self.assertTrue(TestOrderedDictList.compare(file, _CSV_CSV_NAME_SORTED))
        remove(file)

        file = mktemp()
        self.data_name_sorted.write(file, DictListFile.JSON)
        self.assertTrue(TestOrderedDictList.compare(file, _JSON_JSON_NAME_SORTED))
        remove(file)
