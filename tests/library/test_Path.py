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

    def test_str(self):
        self.assertEqual(f"{Path('/path/to/file.txt')}", "/path/to/file.txt")

    def test_eq(self):
        self.assertEqual(Path("/path/to/file.txt"), "/path/to/file.txt")
        self.assertNotEqual(Path("/path/to/file.txt"), "/path/to/file.json")

        self.assertEqual(Path("/path/to/file.txt"), Path("/path/to/file.txt"))
        self.assertNotEqual(Path("/path/to/file.txt"), Path("/path/to/file.json"))

        with self.assertRaises(TypeError):
            eq = Path("/path/to/file.txt") == 3

    def test_len(self):
        self.assertEqual(len(Path("/path/to/file.txt")), 17)

    def test_path(self):
        self.assertEqual(Path("/path/to/file.txt").path, "/path/to/file.txt")

    def test_relpath(self):
        self.assertTrue(isabs("/path/to/dir"))
        self.assertFalse(isabs(Path("/path/to/dir").relpath))

    def test_file(self):
        self.assertEqual(Path("/path/to/file.txt").file, "file.txt")

    def test_name(self):
        self.assertEqual(Path("/path/to/file.txt").name, "file")
        self.assertEqual(Path("/path/to/dir").name, "dir")

    def test_extension(self):
        self.assertEqual(Path("/path/to/file.txt").extension, "txt")

    def test_from_cwd(self):
        self.assertEqual(Path.from_cwd().path, getcwd())

    def test_from_tokens(self):
        path1 = "/path/to/dir"
        path2 = "files"
        path3 = "file.txt"

        self.assertEqual(
            Path.from_tokens(path1, path2, path3).path,
            join(path1, path2, path3),
        )

    def test_get_dir(self):
        self.assertEqual(Path("/path/to/file.txt").get_dir(), "/path/to")

    def test_get_pardir(self):
        self.assertEqual(Path("/path/to/dir").get_pardir(), "/path/to")
        self.assertEqual(Path("/path/to/dir").get_pardir(2), "/path")

    def test_set_dir(self):
        self.assertEqual(Path("/path/to/file.txt").set_dir().path, "/path/to")

    def test_set_pardir(self):
        self.assertEqual(Path("/path/to/dir").set_pardir().path, "/path/to")
        self.assertEqual(Path("/path/to/dir").set_pardir(2).path, "/path")

    def test_replace_sep(self):
        self.assertEqual(Path("/path/to/dir").replace_sep("\\"), "\\path\\to\\dir")
        self.assertEqual(Path("/path/to/dir").replace_sep("."), ".path.to.dir")
