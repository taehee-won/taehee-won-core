from unittest import TestCase
from tempfile import mkdtemp, mktemp, NamedTemporaryFile
from os import remove, rmdir, getcwd, urandom, symlink
from os.path import exists, basename, join, islink, isfile, isdir

from core import Trace, FileSystem, Path


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

        self.link = join(self.dir, "link")
        symlink(self.file, self.link)

    def tearDown(self) -> None:
        if islink(self.link):
            remove(self.link)

        if isfile(self.file):
            remove(self.file)

        if isdir(self.dir):
            rmdir(self.dir)

    def test_is_exist(self):
        is_exist = FileSystem.is_exist(self.file)
        self.assertIsInstance(is_exist, bool)
        self.assertTrue(is_exist)

        is_exist = FileSystem.is_exist(self.dir)
        self.assertIsInstance(is_exist, bool)
        self.assertTrue(is_exist)

        is_exist = FileSystem.is_exist(self.link)
        self.assertIsInstance(is_exist, bool)
        self.assertTrue(is_exist)

        is_exist = FileSystem.is_exist("non_existent_file.txt")
        self.assertIsInstance(is_exist, bool)
        self.assertFalse(is_exist)

    def test_is_file(self):
        is_file = FileSystem.is_file(self.file)
        self.assertIsInstance(is_file, bool)
        self.assertTrue(is_file)

        is_file = FileSystem.is_file(self.dir)
        self.assertIsInstance(is_file, bool)
        self.assertFalse(is_file)

        is_file = FileSystem.is_file(self.link)
        self.assertIsInstance(is_file, bool)
        self.assertFalse(is_file)

        with self.assertRaises(ValueError):
            is_file = FileSystem.is_file("non_existent")

    def test_is_dir(self):
        is_dir = FileSystem.is_dir(self.file)
        self.assertIsInstance(is_dir, bool)
        self.assertFalse(is_dir)

        is_dir = FileSystem.is_dir(self.dir)
        self.assertIsInstance(is_dir, bool)
        self.assertTrue(is_dir)

        is_dir = FileSystem.is_dir(self.link)
        self.assertIsInstance(is_dir, bool)
        self.assertFalse(is_dir)

        self.assertFalse(FileSystem.is_dir(self.file))
        self.assertTrue(FileSystem.is_dir(self.dir))

        with self.assertRaises(ValueError):
            is_dir = FileSystem.is_file("non_existent")

    def test_is_link(self):
        is_link = FileSystem.is_link(self.file)
        self.assertIsInstance(is_link, bool)
        self.assertFalse(is_link)

        is_link = FileSystem.is_link(self.dir)
        self.assertIsInstance(is_link, bool)
        self.assertFalse(is_link)

        is_link = FileSystem.is_link(self.link)
        self.assertIsInstance(is_link, bool)
        self.assertTrue(is_link)

        with self.assertRaises(ValueError):
            is_link = FileSystem.is_link("")

    def test_get_cwd(self):
        cwd = FileSystem.get_cwd()

        self.assertIsInstance(cwd, Path)
        self.assertEqual(cwd, getcwd())

    def test_get_files(self):
        fd1 = NamedTemporaryFile(dir=self.dir, delete=False)
        fd2 = NamedTemporaryFile(dir=self.dir, delete=False)
        file1 = fd1.name
        file2 = fd2.name
        fd1.close()
        fd2.close()

        files = FileSystem.get_files(self.dir)
        self.assertIsInstance(files, list)
        self.assertIn(file1, files)
        self.assertIn(file2, files)

        remove(file1)
        remove(file2)

        files = FileSystem.get_files(self.dir)
        self.assertIsInstance(files, list)
        self.assertNotIn(file1, files)
        self.assertNotIn(file2, files)

        with self.assertRaises(ValueError):
            files = FileSystem.get_files("non_existent")

    def test_get_dirs(self):
        dir1 = mkdtemp(dir=self.dir)
        dir2 = mkdtemp(dir=self.dir)

        dirs = FileSystem.get_dirs(self.dir)
        self.assertIsInstance(dirs, list)
        self.assertIn(dir1, dirs)
        self.assertIn(dir2, dirs)

        rmdir(dir1)
        rmdir(dir2)

        dirs = FileSystem.get_dirs(self.dir)
        self.assertIsInstance(dirs, list)
        self.assertNotIn(dir1, dirs)
        self.assertNotIn(dir2, dirs)

        with self.assertRaises(ValueError):
            dirs = FileSystem.get_dirs("non_existent")

    def test_get_links(self):
        links = FileSystem.get_links(self.dir)
        self.assertIsInstance(links, list)
        self.assertIn(self.link, links)

        remove(self.link)

        links = FileSystem.get_links(self.dir)
        self.assertIsInstance(links, list)
        self.assertNotIn(self.link, links)

        with self.assertRaises(ValueError):
            links = FileSystem.get_links("non_existent")

    def test_get_file_size(self):
        content = urandom(100)
        with open(self.file, "wb") as f:
            f.write(content)

        size = FileSystem.get_file_size(self.file)
        self.assertIsInstance(size, int)
        self.assertEqual(size, len(content))
        remove(self.file)

        with self.assertRaises(ValueError):
            size = FileSystem.get_file_size(self.file)

    def test_get_dir_size(self):
        fd = NamedTemporaryFile(dir=self.dir, delete=False)
        file = fd.name
        fd.close()

        content = urandom(100)
        with open(file, "wb") as f:
            f.write(content)

        size = FileSystem.get_dir_size(self.dir)
        self.assertIsInstance(size, int)
        self.assertEqual(size, len(content))

        remove(file)

        size = FileSystem.get_dir_size(self.dir)
        self.assertIsInstance(size, int)
        self.assertEqual(size, 0)

        with self.assertRaises(ValueError):
            FileSystem.get_file_size(file)

    def test_make_dir(self):
        dir = mktemp()
        make_dir = FileSystem.make_dir(dir)
        self.assertIsInstance(make_dir, Path)
        self.assertEqual(make_dir, dir)
        self.assertTrue(exists(dir))
        self.assertTrue(isdir(dir))

        with self.assertRaises(ValueError):
            FileSystem.make_dir(dir)

        rmdir(dir)

    def test_remove_file(self):
        remove_file = FileSystem.remove_file(self.file)
        self.assertIsNone(remove_file)
        self.assertFalse(exists(self.file))

        with self.assertRaises(ValueError):
            FileSystem.remove_file(self.file)

        with self.assertRaises(ValueError):
            FileSystem.remove_file(self.dir)

        with self.assertRaises(ValueError):
            FileSystem.remove_file(self.link)

    def test_remove_dir(self):
        remove_dir = FileSystem.remove_dir(self.dir)
        self.assertIsNone(remove_dir)
        self.assertFalse(exists(self.dir))

        with self.assertRaises(ValueError):
            FileSystem.remove_dir(self.dir)

        with self.assertRaises(ValueError):
            FileSystem.remove_dir(self.file)

        with self.assertRaises(ValueError):
            FileSystem.remove_dir(self.link)

    def test_remove_link(self):
        remove_link = FileSystem.remove_link(self.link)
        self.assertIsNone(remove_link)
        self.assertFalse(exists(self.link))

        with self.assertRaises(ValueError):
            FileSystem.remove_link(self.link)

        with self.assertRaises(ValueError):
            FileSystem.remove_link(self.file)

        with self.assertRaises(ValueError):
            FileSystem.remove_link(self.dir)

    def test_copy(self):
        content = urandom(100)
        with open(self.file, "wb") as f:
            f.write(content)

        dst = self.file + "_"
        dst_path = FileSystem.copy(self.file, dst)
        self.assertIsInstance(dst_path, Path)
        self.assertTrue(exists(dst))
        self.assertTrue(exists(self.file))
        self.assertEqual(dst_path, dst)

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
        self.assertIsInstance(dst_path, Path)
        self.assertTrue(exists(dst))
        self.assertFalse(exists(self.file))
        self.assertEqual(dst_path, dst)

        with open(dst, "rb") as f:
            content_ = f.read()

        self.assertEqual(content_, content)
        remove(dst)

    def test_get_walk(self):
        dir = mkdtemp(dir=self.dir)
        fd = NamedTemporaryFile(dir=dir, delete=False)
        file = fd.name
        fd.close()

        walk = FileSystem.walk(self.dir)
        for top, dirs, files in walk:
            if top == dir:
                self.assertIn(basename(file), files)

            if top == self.dir:
                self.assertIn(basename(dir), dirs)

        remove(file)

        walk = FileSystem.walk(self.dir)
        for top, dirs, files in walk:
            if top == dir:
                self.assertNotIn(basename(file), files)

            if top == self.dir:
                self.assertIn(basename(dir), dirs)

        rmdir(dir)

        walk = FileSystem.walk(self.dir)
        for top, dirs, files in walk:
            if top == self.dir:
                self.assertNotIn(basename(dir), dirs)

        with self.assertRaises(ValueError):
            walk = FileSystem.walk("non_existent_dir")
