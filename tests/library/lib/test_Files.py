from unittest import TestCase
from os.path import join, dirname, abspath

from src.library.lib.Trace import Trace
from src.library.lib.Files import Files


D_FILES = join(dirname(abspath(__file__)), "Files")


class TestFiles(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Trace.set_levels(Trace.Level.NOTSET)

    @classmethod
    def tearDownClass(cls) -> None:
        Trace.set_levels()

    def setUp(self) -> None:
        self.files = Files([D_FILES])

    def test_init(self):
        self.assertIsInstance(self.files, Files)

    def test_len(self):
        self.assertEqual(len(self.files), 2)

    def test_str(self):
        self.assertIsInstance(str(self.files), str)
        self.assertIn("Files", str(self.files))
        self.assertIn(f"dirs:1", str(self.files))
        self.assertIn(f"files:2", str(self.files))
        self.assertNotIn("name:", str(self.files))

        files = Files(name="TestFiles")
        self.assertIsInstance(str(files), str)
        self.assertIn("Files", str(files))
        self.assertIn(f"dirs:0", str(files))
        self.assertIn(f"files:0", str(files))
        self.assertIn("name:TestFiles", str(files))

    def test_register(self):
        files = Files()
        self.assertTrue(files.register(D_FILES))

        self.assertEqual(len(files), 2)
        self.assertFalse(files.register(D_FILES))

    def test_get_dirs(self):
        dirs = self.files.get_dirs()
        self.assertEqual(len(dirs), 1)
        self.assertEqual(dirs[0], D_FILES)

    def test_get_files(self):
        files = self.files.get_files()
        self.assertEqual(len(files), 2)
        self.assertEqual(files[0], "Files.interface")
        self.assertEqual(files[1], "Files.json")

    def test_execute(self):
        self.assertEqual(self.files.execute("Files.interface", "add", 1, 2), 3)
        self.assertEqual(self.files.execute("Files.interface", "sub", 1, 2), -1)

        with self.assertRaises(AttributeError):
            self.files.execute("Files.json", "add")

    def test_load(self):
        with self.assertRaises(ValueError):
            self.files.load("Files.interface")

        self.assertListEqual(
            self.files.load("Files.json"),
            [
                {"name": "John", "age": 30},
                {"name": "Jane", "age": 25},
                {"name": "Doe", "age": 22},
            ],
        )

        with self.assertRaises(TypeError):
            self.files.load("Files.non_exist")
