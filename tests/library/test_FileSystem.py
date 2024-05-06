from unittest import TestCase
from tempfile import mkdtemp, mktemp, NamedTemporaryFile
from os import remove, rmdir, getcwd, urandom
from os.path import exists, basename, isdir

from core import Trace, FileSystem


class TestFileSystem(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Trace.set_levels(Trace.Level.NOTSET)

    @classmethod
    def tearDownClass(cls) -> None:
        Trace.set_levels()

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
        self.assertTrue(FileSystem.is_exist(self.file))
        self.assertTrue(FileSystem.is_exist(self.dir))
        self.assertFalse(FileSystem.is_exist("non_existent_file.txt"))

    def test_is_file(self):
        self.assertTrue(FileSystem.is_file(self.file))
        self.assertFalse(FileSystem.is_file(self.dir))

        with self.assertRaises(ValueError):
            self.assertFalse(FileSystem.is_file("non_existent_file.txt"))

    def test_is_dir(self):
        self.assertFalse(FileSystem.is_dir(self.file))
        self.assertTrue(FileSystem.is_dir(self.dir))

        with self.assertRaises(ValueError):
            self.assertFalse(FileSystem.is_file("non_existent_file.txt"))

    # TODO: test_is_link

    def test_get_cwd(self):
        self.assertEqual(FileSystem.get_cwd(), getcwd())

    def test_get_files(self):
        fd1 = NamedTemporaryFile(dir=self.dir, delete=False)
        fd2 = NamedTemporaryFile(dir=self.dir, delete=False)
        file1 = fd1.name
        file2 = fd2.name
        fd1.close()
        fd2.close()

        files = FileSystem.get_files(self.dir)
        self.assertIn(basename(file1), files)
        self.assertIn(basename(file2), files)

        remove(file1)
        remove(file2)

        files = FileSystem.get_files(self.dir)
        self.assertNotIn(basename(file1), files)
        self.assertNotIn(basename(file2), files)

        with self.assertRaises(ValueError):
            self.assertFalse(FileSystem.get_files("non_existent_dir"))

    def test_get_dirs(self):
        dir1 = mkdtemp(dir=self.dir)
        dir2 = mkdtemp(dir=self.dir)

        dirs = FileSystem.get_dirs(self.dir)
        self.assertIn(basename(dir1), dirs)
        self.assertIn(basename(dir2), dirs)

        rmdir(dir1)
        rmdir(dir2)

        dirs = FileSystem.get_dirs(self.dir)
        self.assertNotIn(basename(dir1), dirs)
        self.assertNotIn(basename(dir2), dirs)

        with self.assertRaises(ValueError):
            self.assertFalse(FileSystem.get_dirs("non_existent_dir"))

    # TODO: test_get_links

    def test_get_tree(self):
        dir1 = mkdtemp(dir=self.dir)
        fd = NamedTemporaryFile(dir=dir1, delete=False)
        file = fd.name
        fd.close()

        for root, _, files in FileSystem.get_tree(self.dir):
            if root == dir1:
                self.assertIn(basename(file), files)

        remove(file)
        rmdir(dir1)

        with self.assertRaises(ValueError):
            self.assertFalse(FileSystem.get_tree("non_existent_dir"))

    def test_get_file_size(self):
        content = urandom(100)
        with open(self.file, "wb") as f:
            f.write(content)

        self.assertEqual(FileSystem.get_file_size(self.file), len(content))
        remove(self.file)

        with self.assertRaises(ValueError):
            FileSystem.get_file_size(self.file)

    def test_get_dir_size(self):
        fd = NamedTemporaryFile(dir=self.dir, delete=False)
        file = fd.name
        fd.close()

        content = urandom(100)
        with open(file, "wb") as f:
            f.write(content)

        self.assertEqual(FileSystem.get_dir_size(self.dir), len(content))
        remove(file)
        self.assertEqual(FileSystem.get_dir_size(self.dir), 0)

        with self.assertRaises(ValueError):
            FileSystem.get_file_size(file)

    def test_make_dir(self):
        dir = mktemp()
        FileSystem.make_dir(dir)
        self.assertTrue(exists(dir) and isdir(dir))

        with self.assertRaises(ValueError):
            FileSystem.make_dir(dir)

        rmdir(dir)

    def test_remove_file(self):
        FileSystem.remove_file(self.file)
        self.assertFalse(exists(self.file))

        with self.assertRaises(ValueError):
            FileSystem.remove_file(self.file)

    def test_remove_dir(self):
        FileSystem.remove_dir(self.dir)
        self.assertFalse(exists(self.dir))

        with self.assertRaises(ValueError):
            FileSystem.remove_dir(self.dir)

    def test_copy(self):
        content = urandom(100)
        with open(self.file, "wb") as f:
            f.write(content)

        dst = self.file + "_"
        dst_path = FileSystem.copy(self.file, dst)

        self.assertTrue(exists(dst))
        self.assertEqual(dst_path.path, dst)

        with open(dst, "rb") as f:
            content_ = f.read()

        self.assertEqual(content_, content)
        remove(dst)

    def test_move(self):
        content = urandom(100)
        with open(self.file, "wb") as f:
            f.write(content)

        dst = self.file + "_"
        dst_path = FileSystem.move(self.file, dst)

        self.assertTrue(exists(dst))
        self.assertFalse(exists(self.file))
        self.assertEqual(dst_path.path, dst)

        with open(dst, "rb") as f:
            content_ = f.read()

        self.assertEqual(content_, content)
        remove(dst)
