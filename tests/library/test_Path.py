from unittest import TestCase
from os import getcwd
from os.path import join, isabs

from core import Trace, Path


class TestPath(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Trace.set_levels(Trace.Level.NOTSET)

    @classmethod
    def tearDownClass(cls) -> None:
        Trace.set_levels()

    def test_init(self):
        obj = Path("/path/to/file.txt")
        self.assertIsInstance(obj, Path)
        self.assertIsNot(obj, Path(obj))
        self.assertEqual(obj, Path(obj))

    def test_str(self):
        obj = Path("/path/to/file.txt")
        self.assertIsInstance(str(obj), str)
        self.assertEqual(str(obj), "/path/to/file.txt")

    def test_eq(self):
        path = "/path/to/file.txt"
        obj = Path(path)
        self.assertEqual(obj, path)
        self.assertNotEqual(obj, "/path/to/file.json")
        self.assertEqual(obj, Path(path))
        self.assertNotEqual(obj, Path("/path/to/file.json"))

        with self.assertRaises(TypeError):
            eq = obj == 3

    def test_len(self):
        obj = Path("/path/to/file.txt")
        self.assertIsInstance(len(obj), int)
        self.assertEqual(len(obj), 17)

    def test_path(self):
        obj = Path("/path/to/file.txt")
        self.assertIsInstance(obj.path, str)
        self.assertEqual(obj.path, "/path/to/file.txt")

    def test_relpath(self):
        path = "/path/to/dir"
        obj = Path(path)
        self.assertTrue(isabs(path))
        self.assertIsInstance(obj.relpath, str)
        self.assertFalse(isabs(obj.relpath))

    def test_file(self):
        obj = Path("/path/to/file.txt")
        self.assertIsInstance(obj.file, str)
        self.assertEqual(obj.file, "file.txt")

    def test_name(self):
        obj = Path("/path/to/file.txt")
        self.assertIsInstance(obj.name, str)
        self.assertEqual(obj.name, "file")

        obj = Path("/path/to/dir")
        self.assertIsInstance(obj.name, str)
        self.assertEqual(obj.name, "dir")

    def test_extension(self):
        obj = Path("/path/to/file.txt")
        self.assertIsInstance(obj.extension, str)
        self.assertEqual(obj.extension, "txt")

    def test_from_cwd(self):
        obj = Path.from_cwd()
        self.assertIsInstance(obj, Path)
        self.assertEqual(obj, getcwd())

    def test_from_tokens(self):
        token1 = "/path/to/dir"
        token2 = "files"
        token3 = "file.txt"
        obj = Path.from_tokens(token1, token2, token3)
        self.assertIsInstance(obj.path, str)
        self.assertEqual(obj, join(token1, token2, token3))

    def test_is_pardir(self):
        obj = Path("/path/to/dir1/dir2/dir3")
        for dir, expect in [
            ["/", True],
            ["/path", True],
            ["/path/to", True],
            ["/path/to/dir1", True],
            ["/path/to/dir1/dir2", True],
            ["/path/to/dir1/dir2/dir3", False],
            ["/path/to/dir1/dir2/dir3/dir4", False],
            ["/invalid", False],
            ["/invalid/to", False],
        ]:
            is_pardir = obj.is_pardir(dir)
            self.assertIsInstance(is_pardir, bool)
            self.assertTrue(is_pardir) if expect else self.assertFalse(is_pardir)

            is_pardir = obj.is_pardir(Path(dir))
            self.assertIsInstance(is_pardir, bool)
            self.assertTrue(is_pardir) if expect else self.assertFalse(is_pardir)

    def test_get_dir(self):
        obj = Path("/path/to/file.txt")
        dir = obj.get_dir()
        self.assertIsInstance(dir, Path)
        self.assertEqual(dir, "/path/to")

    def test_get_pardir(self):
        obj = Path("/path/to/dir")
        pardir1 = obj.get_pardir()
        pardir2 = obj.get_pardir(2)
        self.assertIsInstance(pardir1, Path)
        self.assertIsInstance(pardir2, Path)
        self.assertEqual(pardir1, "/path/to")
        self.assertEqual(pardir2, "/path")

    def test_set_dir(self):
        obj = Path("/path/to/file.txt")
        dir = obj.set_dir()
        self.assertIs(dir, obj)
        self.assertEqual(obj, "/path/to")

    def test_set_pardir(self):
        obj = Path("/path/to/dir")
        pardir = obj.set_pardir()
        self.assertIs(pardir, obj)
        self.assertEqual(obj, "/path/to")

        obj = Path("/path/to/dir")
        pardir = obj.set_pardir(2)
        self.assertIs(pardir, obj)
        self.assertEqual(obj, "/path")

    def test_replace_sep(self):
        obj = Path("/path/to/dir")

        path = obj.replace_sep("\\")
        self.assertIsInstance(path, str)
        self.assertEqual(path, "\\path\\to\\dir")

        path = obj.replace_sep(".")
        self.assertIsInstance(path, str)
        self.assertEqual(path, ".path.to.dir")
