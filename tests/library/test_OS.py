from unittest import TestCase
from tempfile import mkdtemp, mktemp, NamedTemporaryFile
from os import remove, rmdir, getcwd, urandom
from os.path import exists, join, isabs, basename, isdir

from core import OS


class TestOS(TestCase):
    def setUp(self) -> None:
        fd = NamedTemporaryFile(delete=False)
        self.file = fd.name
        fd.close()

        self.dir = mkdtemp()

    def tearDown(self) -> None:
        if exists(self.file):
            remove(self.file)

        if exists(self.dir):
            rmdir(self.dir)

    def test_is_exist(self):
        self.assertTrue(OS.is_exist(self.file))
        self.assertTrue(OS.is_exist(self.dir))
        self.assertFalse(OS.is_exist("non_existent_file.txt"))

    def test_is_file(self):
        self.assertTrue(OS.is_file(self.file))
        self.assertFalse(OS.is_file(self.dir))

    def test_is_dir(self):
        self.assertFalse(OS.is_dir(self.file))
        self.assertTrue(OS.is_dir(self.dir))

    def test_get_cwd(self):
        self.assertEqual(OS.get_cwd(), getcwd())

    def test_get_path(self):
        path1 = "/path/to/dir"
        path2 = "files"
        path3 = "file.txt"

        self.assertEqual(OS.get_path(path1, path2, path3), join(path1, path2, path3))

    def test_get_file(self):
        self.assertEqual(OS.get_file("/path/to/file.txt"), "file.txt")

    def test_get_name(self):
        self.assertEqual(OS.get_name("/path/to/file.txt"), "file")

    def test_get_extension(self):
        self.assertEqual(OS.get_extension("/path/to/file.txt"), "txt")

    def test_get_dir(self):
        self.assertEqual(OS.get_dir("/path/to/file.txt"), "/path/to")

    def test_get_pardir(self):
        self.assertEqual(OS.get_pardir("/path/to/dir"), "/path/to/dir/..")

    def test_get_abspath(self):
        self.assertTrue(isabs(OS.get_abspath("some/relative/path")))

    def test_get_relpath(self):
        self.assertTrue(isabs("/path/to/dir"))
        self.assertFalse(isabs(OS.get_relpath("/path/to/dir")))

    def test_get_files(self):
        fd1 = NamedTemporaryFile(dir=self.dir, delete=False)
        fd2 = NamedTemporaryFile(dir=self.dir, delete=False)
        file1 = fd1.name
        file2 = fd2.name
        fd1.close()
        fd2.close()

        files = OS.get_files(self.dir)
        self.assertIn(basename(file1), files)
        self.assertIn(basename(file2), files)

        remove(file1)
        remove(file2)

        files = OS.get_files(self.dir)
        self.assertNotIn(basename(file1), files)
        self.assertNotIn(basename(file2), files)

    def test_get_dirs(self):
        dir1 = mkdtemp(dir=self.dir)
        dir2 = mkdtemp(dir=self.dir)

        dirs = OS.get_dirs(self.dir)
        self.assertIn(basename(dir1), dirs)
        self.assertIn(basename(dir2), dirs)

        rmdir(dir1)
        rmdir(dir2)

        dirs = OS.get_dirs(self.dir)
        self.assertNotIn(basename(dir1), dirs)
        self.assertNotIn(basename(dir2), dirs)

    def test_get_tree(self):
        dir1 = mkdtemp(dir=self.dir)
        fd = NamedTemporaryFile(dir=dir1, delete=False)
        file = fd.name
        fd.close()

        for root, _, files in OS.get_tree(self.dir):
            if root == dir1:
                self.assertIn(basename(file), files)

        remove(file)
        rmdir(dir1)

    def test_get_file_size(self):
        content = urandom(100)
        with open(self.file, "wb") as f:
            f.write(content)

        self.assertEqual(OS.get_file_size(self.file), len(content))
        remove(self.file)
        self.assertEqual(OS.get_file_size(self.file), 0)

    def test_get_dir_size(self):
        fd = NamedTemporaryFile(dir=self.dir, delete=False)
        file = fd.name
        fd.close()

        content = urandom(100)
        with open(file, "wb") as f:
            f.write(content)

        self.assertEqual(OS.get_dir_size(self.dir), len(content))
        remove(file)
        self.assertEqual(OS.get_dir_size(self.dir), 0)

    def test_get_size(self):
        content = urandom(100)
        with open(self.file, "wb") as f:
            f.write(content)

        self.assertEqual(OS.get_size(self.file), len(content))
        remove(self.file)
        self.assertEqual(OS.get_size(self.file), 0)

        fd = NamedTemporaryFile(dir=self.dir, delete=False)
        file = fd.name
        fd.close()

        with open(file, "wb") as f:
            f.write(content)

        self.assertEqual(OS.get_size(self.dir), len(content))

        remove(file)
        rmdir(self.dir)
        self.assertEqual(OS.get_size(self.dir), 0)

    def test_make_dir(self):
        dir = mktemp()
        OS.make_dir(dir)
        self.assertTrue(exists(dir) and isdir(dir))
        OS.make_dir(dir)
        rmdir(dir)

    def test_remove_file(self):
        OS.remove_file(self.file)
        self.assertFalse(exists(self.file))
        OS.remove_file(self.file)

    def test_remove_dir(self):
        OS.remove_dir(self.dir)
        self.assertFalse(exists(self.dir))
        OS.remove_dir(self.dir)

    def test_remove(self):
        OS.remove(self.file)
        self.assertFalse(exists(self.file))
        OS.remove(self.file)

        OS.remove(self.dir)
        self.assertFalse(exists(self.dir))
        OS.remove(self.dir)

    def test_copy(self):
        content = urandom(100)
        with open(self.file, "wb") as f:
            f.write(content)

        dst = self.file + "_"
        OS.copy(self.file, dst)

        self.assertTrue(exists(dst))

        with open(dst, "rb") as f:
            content_ = f.read()

        self.assertEqual(content_, content)
        remove(dst)

    def test_move(self):
        content = urandom(100)
        with open(self.file, "wb") as f:
            f.write(content)

        dst = self.file + "_"
        OS.move(self.file, dst)

        self.assertTrue(exists(dst))
        self.assertFalse(exists(self.file))

        with open(dst, "rb") as f:
            content_ = f.read()

        self.assertEqual(content_, content)
        remove(dst)

    def test_replace_sep(self):
        self.assertEqual(OS.replace_sep("/path/to/dir", "\\"), "\\path\\to\\dir")
