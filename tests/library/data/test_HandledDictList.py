from unittest import TestCase
from typing import Dict
from copy import deepcopy
from random import randint
from os import remove
from os.path import join, abspath, dirname
from tempfile import mktemp

from src.library.lib.Trace import TraceLevel, Trace
from src.library.data.HandledDictList import HandledDictList
from .test_DictList import (
    F_DICTLIST_DICTLIST,
    F_JSON_JSON,
    F_DICTLIST_CSV,
    F_DICTLIST,
)


D_TEST_FILE_DIR = join(dirname(abspath(__file__)), "HandledDictList")

# data file type, extension
F_DICTLIST_DICTLIST_HANDLED = join(D_TEST_FILE_DIR, "DictList_handled.DictList")
F_CSV_CSV_HANDLED = join(D_TEST_FILE_DIR, "csv_handled.csv")
F_JSON_JSON_HANDLED = join(D_TEST_FILE_DIR, "json_handled.json")


class TestHandledDictList(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Trace.set_levels(TraceLevel.NOTSET)

    @classmethod
    def tearDownClass(cls) -> None:
        Trace.set_levels()

    def setUp(self):
        self.source = [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 25},
            {"name": "Doe", "age": 22},
        ]
        self.source_handled = [
            {"name": "John_handled", "age": 31},
            {"name": "Jane_handled", "age": 26},
            {"name": "Doe_handled", "age": 23},
        ]
        self.data = HandledDictList(
            [_name_handle, _age_handle],
            deepcopy(self.source),
        )

    # def test_prepare_TestHandledDictList(self):
    #     self.data.write(F_DICTLIST_DICTLIST_HANDLED, HandledDictList.FileType.DICTLIST)
    #     self.data.write(F_CSV_CSV_HANDLED, HandledDictList.FileType.CSV)
    #     self.data.write(F_JSON_JSON_HANDLED, HandledDictList.FileType.JSON)

    def test_init(self):
        self.assertIsInstance(self.data, HandledDictList)

    def test_init_read(self):
        data = HandledDictList([_name_handle, _age_handle], F_DICTLIST_DICTLIST)
        for index, element in enumerate(data):
            self.assertEqual(element, self.source_handled[index])

        data = HandledDictList(
            [_name_handle, _age_handle],
            F_DICTLIST_CSV,
            HandledDictList.FileType.DICTLIST,
        )
        for index, element in enumerate(data):
            self.assertEqual(element, self.source_handled[index])

    def test_len(self):
        self.assertEqual(len(self.data), len(self.source_handled))

    def test_iter(self):
        for index, element in enumerate(self.data):
            self.assertEqual(element, self.source_handled[index])

    def test_iter_overlap(self):
        data = []
        for index, element in enumerate(self.data):
            if index == 1:
                self.assertEqual([e for e in self.data], self.source_handled)

            data.append(element)

        self.assertEqual(data, self.source_handled)

    def test_index(self):
        index = randint(0, len(self.source_handled) - 1)
        element = self.data[index]
        self.assertIsInstance(element, dict)
        self.assertEqual(element, self.source_handled[index])

    def test_slice(self):
        index1 = randint(0, len(self.source_handled) - 1)
        index2 = randint(0, len(self.source_handled) - 1)

        data = self.data[min(index1, index2) : max(index1, index2)]
        self.assertIsInstance(data, list)
        self.assertListEqual(
            data,
            self.source_handled[min(index1, index2) : max(index1, index2)],
        )

    def test_str(self):
        self.assertIsInstance(str(self.data), str)
        self.assertIn("HandledDictList", str(self.data))
        self.assertIn("handles:2", str(self.data))
        self.assertIn(f"len:{len(self.source)}", str(self.data))
        self.assertNotIn("name:", str(self.data))

        data = HandledDictList([], name="TestHandledDictList")
        self.assertIsInstance(str(data), str)
        self.assertIn("HandledDictList", str(data))
        self.assertIn("handles:0", str(data))
        self.assertIn(f"len:0", str(data))
        self.assertIn("name:TestHandledDictList", str(data))

    def test_get_element_key_value(self):
        index = randint(0, len(self.source_handled) - 1)
        self.assertEqual(
            self.data.get_element("name", self.source_handled[index]["name"]),
            self.source_handled[index],
        )

        index = randint(0, len(self.source_handled) - 1)
        self.assertEqual(
            self.data.get_element("age", self.source_handled[index]["age"]),
            self.source_handled[index],
        )

        self.assertIsNone(self.data.get_element("name", "Theodore"))

    def test_get_element_query(self):
        index = randint(0, len(self.source_handled) - 1)
        self.assertEqual(
            self.data.get_element({"name": self.source_handled[index]["name"]}),
            self.source_handled[index],
        )

        index = randint(0, len(self.source_handled) - 1)
        self.assertEqual(
            self.data.get_element({"age": self.source_handled[index]["age"]}),
            self.source_handled[index],
        )

        self.assertIsNone(self.data.get_element({"name": "Theodore"}))
        self.assertIsNone(self.data.get_element({"name": "Jane", "age": 10}))

    def test_get_data_key_value(self):
        data = self.data.get_data("name", "John_handled")
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_get_data_query(self):
        data = self.data.get_data({"name": "John_handled"})
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_get_data(self):
        data = self.data.get_data()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3)

    def test_get_filtered_data_start(self):
        data = self.data.get_filtered_data("age", start=26)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

        data = self.data.get_filtered_data("age", start=27)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_get_filtered_data_end(self):
        data = self.data.get_filtered_data("age", end=26)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

        data = self.data.get_filtered_data("age", end=27)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    def test_get_filtered_data_include(self):
        data = self.data.get_filtered_data("age", include=[23, 26, 36])
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    def test_get_filtered_data_exclude(self):
        data = self.data.get_filtered_data(
            "name", exclude=["John_handled", "Theodore_handled"]
        )
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    def test_get_filtered_data(self):
        data = self.data.get_filtered_data("age", start=23, end=27)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

        data = self.data.get_filtered_data("age", start=28, exclude=[31])
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

    def test_get_values(self):
        names = self.data.get_values("name")
        self.assertIn("John_handled", names)
        self.assertEqual(len(names), 3)

    def test_append(self):
        element = {"name": "Smith", "age": 40}
        element_handled = {"name": "Smith_handled", "age": 41}
        self.data.append(element)
        self.assertIn(element_handled, self.data._data)

    def test_extend(self):
        data = [{"name": "Alice", "age": 26}, {"name": "Bob", "age": 24}]
        data_handled = [
            {"name": "Alice_handled", "age": 27},
            {"name": "Bob_handled", "age": 25},
        ]
        self.data.extend(data)
        for element in data_handled:
            self.assertIn(element, self.data._data)

        self.assertEqual(len(self.data._data), 5)

    def test_insert(self):
        element = {"name": "Charlie", "age": 20}
        with self.assertRaises(TypeError):
            self.data.insert(element, index=1)

    def test_remove(self):
        element = {"name": "John", "age": 30}
        with self.assertRaises(TypeError):
            self.data.remove(element)

    def test_pop(self):
        with self.assertRaises(TypeError):
            element = self.data.pop(1)

    def test_clear(self):
        with self.assertRaises(TypeError):
            self.data.clear()

    def test_read(self):
        data = HandledDictList([_name_handle, _age_handle])
        data.read(F_DICTLIST_DICTLIST)
        for index, element in enumerate(data):
            self.assertEqual(element, self.source_handled[index])

        data = HandledDictList([_name_handle, _age_handle])
        data.read(F_JSON_JSON)
        for index, element in enumerate(data):
            self.assertEqual(element, self.source_handled[index])

        data = HandledDictList([_name_handle, _age_handle])
        data.read(F_DICTLIST_CSV, HandledDictList.FileType.DICTLIST)
        for index, element in enumerate(data):
            self.assertEqual(element, self.source_handled[index])

        data = HandledDictList([_name_handle, _age_handle])
        data.read(F_DICTLIST, HandledDictList.FileType.DICTLIST)
        for index, element in enumerate(data):
            self.assertEqual(element, self.source_handled[index])

    def test_read_str(self):
        data = HandledDictList([_name_handle, _age_handle])
        data.read(F_DICTLIST_CSV, "DictList")
        for index, element in enumerate(data):
            self.assertEqual(element, self.source_handled[index])

        data = HandledDictList([_name_handle, _age_handle])
        data.read(F_DICTLIST, "DictList")
        for index, element in enumerate(data):
            self.assertEqual(element, self.source_handled[index])

    def test_write(self):
        file = mktemp()
        self.data.write(file, HandledDictList.FileType.DICTLIST)
        self.assertTrue(_compare(file, F_DICTLIST_DICTLIST_HANDLED))
        remove(file)

        file = mktemp()
        self.data.write(file, HandledDictList.FileType.CSV)
        self.assertTrue(_compare(file, F_CSV_CSV_HANDLED))
        remove(file)

        file = mktemp()
        self.data.write(file, HandledDictList.FileType.JSON)
        self.assertTrue(_compare(file, F_JSON_JSON_HANDLED))
        remove(file)

    def test_pipe(self):
        def _handle_1(element, pipe) -> Dict:
            # pipe["age"] = 4
            return {"age": 4}

        def _handle_2(element, pipe) -> None:
            element["age"] += pipe["age"]

        data = HandledDictList([_handle_1, _handle_2], deepcopy(self.source))
        source_handled = [
            {"name": "John", "age": 34},
            {"name": "Jane", "age": 29},
            {"name": "Doe", "age": 26},
        ]
        for index, element in enumerate(data):
            self.assertEqual(element, source_handled[index])


def _compare(file1, file2):
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        return f1.read() == f2.read()


def _name_handle(element: Dict, pipe: Dict) -> None:
    element["name"] += "_handled"


def _age_handle(element: Dict, pipe: Dict) -> None:
    element["age"] += 1
