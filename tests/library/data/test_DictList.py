from unittest import TestCase
from copy import deepcopy
from random import randint
from os import remove
from os.path import join, abspath, dirname
from tempfile import mktemp

from src.library.data.DictList import DictList


D_TEST_FILE_DIR = join(dirname(abspath(__file__)), "DictList")

# data file type, extension
F_DICTLIST_DICTLIST = join(D_TEST_FILE_DIR, "DictList.DictList")
F_CSV_CSV = join(D_TEST_FILE_DIR, "csv.csv")
F_JSON_JSON = join(D_TEST_FILE_DIR, "json.json")
F_DICTLIST_CSV = join(D_TEST_FILE_DIR, "DictList.csv")
F_DICTLIST = join(D_TEST_FILE_DIR, "DictList")


class TestDictList(TestCase):
    def setUp(self):
        self.source = [
            {"name": "John", "age": 30},
            {"name": "Jane", "age": 25},
            {"name": "Doe", "age": 22},
        ]
        self.data = DictList(deepcopy(self.source))

    # def test_prepare_TestDictList(self):
    #     self.data.write(F_DICTLIST_DICTLIST, DictList.FileType.DICTLIST)
    #     self.data.write(F_CSV_CSV, DictList.FileType.CSV)
    #     self.data.write(F_JSON_JSON, DictList.FileType.JSON)
    #     self.data.write(F_DICTLIST_CSV, DictList.FileType.DICTLIST)
    #     self.data.write(F_DICTLIST, DictList.FileType.DICTLIST)

    def test_init(self):
        self.assertIsInstance(self.data, DictList)

    def test_init_read(self):
        data = DictList(F_DICTLIST_DICTLIST)
        for index, element in enumerate(data):
            self.assertEqual(element, self.source[index])

        data = DictList(F_DICTLIST_CSV, DictList.FileType.DICTLIST)
        for index, element in enumerate(data):
            self.assertEqual(element, self.source[index])

    def test_len(self):
        self.assertEqual(len(self.data), len(self.source))

    def test_iter(self):
        for index, element in enumerate(self.data):
            self.assertEqual(element, self.source[index])

    def test_iter_overlap(self):
        data = []
        for index, element in enumerate(self.data):
            if index == 1:
                self.assertEqual([e for e in self.data], self.source)

            data.append(element)

        self.assertEqual(data, self.source)

    def test_index(self):
        index = randint(0, len(self.source) - 1)
        element = self.data[index]
        self.assertIsInstance(element, dict)
        self.assertEqual(element, self.source[index])

    def test_slice(self):
        index1 = randint(0, len(self.source) - 1)
        index2 = randint(0, len(self.source) - 1)

        data = self.data[min(index1, index2) : max(index1, index2)]
        self.assertIsInstance(data, list)
        self.assertListEqual(
            data,
            self.source[min(index1, index2) : max(index1, index2)],
        )

    def test_str(self):
        self.assertIsInstance(str(self.data), str)
        self.assertIn("DictList", str(self.data))
        self.assertIn(f"len:{len(self.source)}", str(self.data))
        self.assertNotIn("name:", str(self.data))

        data = DictList(name="TestDictList")
        self.assertIsInstance(str(data), str)
        self.assertIn("DictList", str(data))
        self.assertIn(f"len:0", str(data))
        self.assertIn("name:TestDictList", str(data))

    def test_get_element_key_value(self):
        index = randint(0, len(self.source) - 1)
        self.assertEqual(
            self.data.get_element("name", self.source[index]["name"]),
            self.source[index],
        )

        index = randint(0, len(self.source) - 1)
        self.assertEqual(
            self.data.get_element("age", self.source[index]["age"]),
            self.source[index],
        )

        self.assertIsNone(self.data.get_element("name", "Theodore"))

    def test_get_element_query(self):
        index = randint(0, len(self.source) - 1)
        self.assertEqual(
            self.data.get_element({"name": self.source[index]["name"]}),
            self.source[index],
        )

        index = randint(0, len(self.source) - 1)
        self.assertEqual(
            self.data.get_element({"age": self.source[index]["age"]}),
            self.source[index],
        )

        self.assertIsNone(self.data.get_element({"name": "Theodore"}))
        self.assertIsNone(self.data.get_element({"name": "Jane", "age": 10}))

    def test_get_data_key_value(self):
        data = self.data.get_data("name", "John")
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_get_data_query(self):
        data = self.data.get_data({"name": "John"})
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_get_data(self):
        data = self.data.get_data()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3)

    def test_get_filtered_data_start(self):
        data = self.data.get_filtered_data("age", start=25)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

        data = self.data.get_filtered_data("age", start=26)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_get_filtered_data_end(self):
        data = self.data.get_filtered_data("age", end=25)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

        data = self.data.get_filtered_data("age", end=26)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    def test_get_filtered_data_include(self):
        data = self.data.get_filtered_data("age", include=[22, 25, 35])
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    def test_get_filtered_data_exclude(self):
        data = self.data.get_filtered_data("name", exclude=["John", "Theodore"])
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

    def test_get_filtered_data(self):
        data = self.data.get_filtered_data("age", start=22, end=26)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)

        data = self.data.get_filtered_data("age", start=27, exclude=[30])
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

    def test_get_values(self):
        names = self.data.get_values("name")
        self.assertIn("John", names)
        self.assertEqual(len(names), 3)

    def test_append(self):
        element = {"name": "Smith", "age": 40}
        self.data.append(element)
        self.assertIn(element, self.data._data)

    def test_extend(self):
        data = [{"name": "Alice", "age": 26}, {"name": "Bob", "age": 24}]
        self.data.extend(data)
        self.assertEqual(len(self.data._data), 5)

    def test_insert(self):
        element = {"name": "Charlie", "age": 20}
        self.data.insert(element, index=1)
        self.assertEqual(self.data._data[1], element)

    def test_remove(self):
        element = {"name": "John", "age": 30}
        self.data.remove(element)
        self.assertNotIn(element, self.data._data)

    def test_pop(self):
        element = self.data.pop(1)
        self.assertEqual(element, {"name": "Jane", "age": 25})
        self.assertEqual(len(self.data._data), 2)

    def test_clear(self):
        self.data.clear()
        self.assertEqual(len(self.data._data), 0)

    def test_read(self):
        data = DictList()
        data.read(F_DICTLIST_DICTLIST)
        for index, element in enumerate(data):
            self.assertEqual(element, self.source[index])

        data = DictList()
        data.read(F_CSV_CSV)
        for element in data:
            element["age"] = int(element["age"])

        for index, element in enumerate(data):
            self.assertEqual(element, self.source[index])

        data = DictList()
        data.read(F_JSON_JSON)
        for index, element in enumerate(data):
            self.assertEqual(element, self.source[index])

        data = DictList()
        data.read(F_DICTLIST_CSV, DictList.FileType.DICTLIST)
        for index, element in enumerate(data):
            self.assertEqual(element, self.source[index])

        data = DictList()
        data.read(F_DICTLIST, DictList.FileType.DICTLIST)
        for index, element in enumerate(data):
            self.assertEqual(element, self.source[index])

    def test_read_str(self):
        data = DictList()
        data.read(F_DICTLIST_CSV, "DictList")
        for index, element in enumerate(data):
            self.assertEqual(element, self.source[index])

        data = DictList()
        data.read(F_DICTLIST, "DictList")
        for index, element in enumerate(data):
            self.assertEqual(element, self.source[index])

    def test_write(self):
        file = mktemp()
        self.data.write(file, DictList.FileType.DICTLIST)
        self.assertTrue(_compare(file, F_DICTLIST_DICTLIST))
        remove(file)

        file = mktemp()
        self.data.write(file, DictList.FileType.CSV)
        self.assertTrue(_compare(file, F_CSV_CSV))
        remove(file)

        file = mktemp()
        self.data.write(file, DictList.FileType.JSON)
        self.assertTrue(_compare(file, F_JSON_JSON))
        remove(file)


def _compare(file1, file2):
    with open(file1, "rb") as f1, open(file2, "rb") as f2:
        return f1.read() == f2.read()
