from unittest import TestCase
from os.path import join, dirname, abspath

from core import Trace, Loader


D_LOADER = join(dirname(abspath(__file__)), "Loader")


class TestLoader(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Trace.set_levels(Trace.Level.NOTSET)

    @classmethod
    def tearDownClass(cls) -> None:
        Trace.set_levels()

    def setUp(self) -> None:
        self.loader = Loader([D_LOADER])

    def test_init(self):
        self.assertIsInstance(self.loader, Loader)

    def test_len(self):
        self.assertEqual(len(self.loader), 2)

    def test_str(self):
        self.assertIsInstance(str(self.loader), str)
        self.assertIn("Loader", str(self.loader))
        self.assertIn(f"dirs:1", str(self.loader))
        self.assertIn(f"resources:2", str(self.loader))
        self.assertNotIn("name:", str(self.loader))

        loader = Loader(name="TestLoader")
        self.assertIsInstance(str(loader), str)
        self.assertIn("Loader", str(loader))
        self.assertIn(f"dirs:0", str(loader))
        self.assertIn(f"resources:0", str(loader))
        self.assertIn("name:TestLoader", str(loader))

    def test_register(self):
        loader = Loader()
        self.assertTrue(loader.register(D_LOADER))

        self.assertEqual(len(loader), 2)
        self.assertFalse(loader.register(D_LOADER))

    def test_get_dirs(self):
        dirs = self.loader.get_dirs()
        self.assertEqual(len(dirs), 1)
        self.assertEqual(dirs[0], D_LOADER)

    def test_get_resources(self):
        resources = self.loader.get_resources()
        self.assertEqual(len(resources), 2)
        self.assertEqual(resources[0], "Loader.interface")
        self.assertEqual(resources[1], "Loader.json")

    def test_get_module(self):
        self.assertEqual(
            getattr(self.loader.get_module("Loader.interface"), "add")(1, 2),
            3,
        )
        self.assertEqual(
            getattr(self.loader.get_module("Loader.interface"), "sub")(1, 2),
            -1,
        )

        with self.assertRaises(TypeError):
            self.loader.get_module("Loader.json")

    def test_read(self):
        with self.assertRaises(TypeError):
            self.loader.read("Loader.interface")

        self.assertListEqual(
            self.loader.read("Loader.json"),
            [
                {"name": "John", "age": 30},
                {"name": "Jane", "age": 25},
                {"name": "Doe", "age": 22},
            ],
        )

        with self.assertRaises(TypeError):
            self.loader.read("Loader.non_exist.json")
