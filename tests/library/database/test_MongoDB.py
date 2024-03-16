from unittest import TestCase, skipIf
from os import environ
from pymongo import MongoClient, ASCENDING
from pymongo.errors import DuplicateKeyError

from src.library.lib.Trace import TraceLevel, Trace
from src.library.database.MongoDB import SortOrder, MongoDB


TEST_DATABASE = "TEST-DATABASE"
TEST_COLLECTION = "TEST-COLLECTION"


@skipIf(environ.get("TEST_MONGODB") != "1", "MongoDB connects local DB server")
class TestMongoDB(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Trace.set_levels(TraceLevel.NOTSET)

    @classmethod
    def tearDownClass(cls) -> None:
        Trace.set_levels()

    def setUp(self):
        self.client = MongoClient(serverSelectionTimeoutMS=1000)
        self.client[TEST_DATABASE][TEST_COLLECTION].insert_many(
            [
                {"name": "John", "age": 30},
                {"name": "Jane", "age": 25},
                {"name": "Doe", "age": 22},
            ]
        )
        self.client[TEST_DATABASE][TEST_COLLECTION].create_index(
            [("name", ASCENDING)],
            unique=True,
        )

        self.db = MongoDB()

    def tearDown(self):
        self.client.drop_database(TEST_DATABASE)
        self.client.close()

        del self.db

    def test_init(self):
        db = MongoDB()
        self.assertIsInstance(db, MongoDB)

    def test_init_with(self):
        with MongoDB() as db:
            self.assertIsInstance(db, MongoDB)

    def test_get_databases(self):
        self.assertIn(TEST_DATABASE, self.db.get_databases())

    def test_get_collections(self):
        self.assertIn(TEST_COLLECTION, self.db.get_collections(TEST_DATABASE))

    def test_drop_database(self):
        self.assertTrue(self.db.drop_database(TEST_DATABASE))
        self.assertFalse(self.db.drop_database(TEST_DATABASE))

        self.assertNotIn(TEST_DATABASE, self.client.list_database_names())

    def test_drop_collection(self):
        self.assertTrue(self.db.drop_collection(TEST_DATABASE, TEST_COLLECTION))
        self.assertFalse(self.db.drop_collection(TEST_DATABASE, TEST_COLLECTION))

        self.assertNotIn(TEST_DATABASE, self.client.list_database_names())
        self.assertNotIn(
            TEST_COLLECTION,
            self.client[TEST_DATABASE].list_collection_names(),
        )

    def test_get_indexes(self):
        self.assertIn("name", self.db.get_indexes(TEST_DATABASE, TEST_COLLECTION))

    def test_set_index(self):
        self.db.set_index(TEST_DATABASE, TEST_COLLECTION, "age", SortOrder.DESCENDING)

        names = [
            index["name"]
            for index in self.client[TEST_DATABASE][TEST_COLLECTION].list_indexes()
        ]
        self.assertIn("name_1", names)
        self.assertIn("age_-1", names)

        with self.assertRaises(DuplicateKeyError):
            self.client[TEST_DATABASE][TEST_COLLECTION].insert_one({"age": 30})

    def test_drop_index(self):
        with self.assertRaises(DuplicateKeyError):
            self.client[TEST_DATABASE][TEST_COLLECTION].insert_one({"name": "John"})

        self.assertTrue(self.db.drop_index(TEST_DATABASE, TEST_COLLECTION, "name"))
        self.assertFalse(self.db.drop_index(TEST_DATABASE, TEST_COLLECTION, "name"))

        names = [
            index["name"]
            for index in self.client[TEST_DATABASE][TEST_COLLECTION].list_indexes()
        ]
        self.assertNotIn("name_1", names)

        self.client[TEST_DATABASE][TEST_COLLECTION].insert_one({"name": "John"})

    def test_insert(self):
        self.assertFalse(self.db.insert(TEST_DATABASE, TEST_COLLECTION, []))
        self.assertTrue(
            self.db.insert(
                TEST_DATABASE,
                TEST_COLLECTION,
                [{"name": "Alice", "age": 26}, {"name": "Bob", "age": 24}],
            )
        )

        data = list(
            self.client[TEST_DATABASE][TEST_COLLECTION].find(projection={"_id": False})
        )
        self.assertIn({"name": "Alice", "age": 26}, data)
        self.assertIn({"name": "Bob", "age": 24}, data)

    def test_select(self):
        data = self.db.select(TEST_DATABASE, TEST_COLLECTION)
        self.assertIsInstance(data, list)
        self.assertEqual(data[0], {"name": "Doe", "age": 22})
        self.assertEqual(data[1], {"name": "Jane", "age": 25})
        self.assertEqual(data[2], {"name": "John", "age": 30})

        data = self.db.select(TEST_DATABASE, TEST_COLLECTION, key="age", value=30)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], {"name": "John", "age": 30})

        data = self.db.select(TEST_DATABASE, TEST_COLLECTION, key="age", start=24)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0], {"name": "Jane", "age": 25})
        self.assertEqual(data[1], {"name": "John", "age": 30})

        data = self.db.select(
            TEST_DATABASE,
            TEST_COLLECTION,
            key="age",
            start=24,
            end=29,
        )
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0], {"name": "Jane", "age": 25})

    def test_update(self):
        self.assertFalse(
            self.db.update(
                TEST_DATABASE,
                TEST_COLLECTION,
                "name",
                "John+",
                {"name": "Theodore"},
            )
        )
        self.assertTrue(
            self.db.update(
                TEST_DATABASE,
                TEST_COLLECTION,
                "name",
                "John",
                {"name": "Theodore"},
            )
        )
        self.assertFalse(
            self.db.update(
                TEST_DATABASE,
                TEST_COLLECTION,
                "name",
                "John",
                {"name": "Theodore"},
            )
        )

        data = list(
            self.client[TEST_DATABASE][TEST_COLLECTION].find(projection={"_id": False})
        )
        self.assertIn({"name": "Doe", "age": 22}, data)
        self.assertIn({"name": "Jane", "age": 25}, data)
        self.assertNotIn({"name": "John", "age": 30}, data)
        self.assertIn({"name": "Theodore", "age": 30}, data)
