from unittest import TestCase
from tempfile import mkdtemp
from os import makedirs
from os.path import exists, join
from shutil import rmtree
from string import ascii_letters, digits
from random import choice

from core import Trace, Lib


class TestLib(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Trace.set_levels(Trace.Level.NOTSET)

        cls.cache_dir_words = [
            "__pycache__",  # python cache
        ]
        cls.cache_file_words = [
            ".pyc",  # python cache
            ".pytest_cache",  # pytest cache
            "tempCodeRunnerFile.py",  # vscode code-runner cache
        ]

    @classmethod
    def tearDownClass(cls) -> None:
        Trace.set_levels()

    def setUp(self) -> None:
        self.dir = mkdtemp()

    def tearDown(self) -> None:
        rmtree(self.dir)

    def test_clear_cache(self):
        test_dir = join(self.dir, "test")
        makedirs(test_dir)

        cache_dirs = [join(test_dir, dir) for dir in TestLib.cache_dir_words]
        for dir in cache_dirs:
            makedirs(dir)

        cache_files = [join(test_dir, file) for file in TestLib.cache_file_words]
        for file in cache_files:
            with open(file, "w") as f:
                f.write("")

        Lib.clear_cache(test_dir)

        self.assertFalse(any(exists(dir) for dir in cache_dirs))
        self.assertFalse(any(exists(file) for file in cache_files))

    def test_clear_cache_word(self):
        test_dir = join(self.dir, "test")
        makedirs(test_dir)

        letters = lambda: "".join(choice(ascii_letters + digits) for _ in range(10))

        cache_dirs = [
            join(test_dir, letters() + dir + letters())
            for dir in TestLib.cache_dir_words
        ]
        for dir in cache_dirs:
            makedirs(dir)

        cache_files = [
            join(test_dir, letters() + file + letters())
            for file in TestLib.cache_file_words
        ]
        for file in cache_files:
            with open(file, "w") as f:
                f.write("")

        Lib.clear_cache(test_dir)

        self.assertFalse(any(exists(dir) for dir in cache_dirs))
        self.assertFalse(any(exists(file) for file in cache_files))

    def test_clear_cache_root(self):
        test_dir = join(self.dir, "test")
        makedirs(test_dir)

        cache_dirs = [join(test_dir, dir) for dir in TestLib.cache_dir_words]
        for dir in cache_dirs:
            makedirs(dir)

        cache_files = [join(test_dir, file) for file in TestLib.cache_file_words]
        for file in cache_files:
            with open(file, "w") as f:
                f.write("")

        out_dirs = [join(self.dir, dir) for dir in TestLib.cache_dir_words]
        for dir in out_dirs:
            makedirs(dir)

        out_files = [join(self.dir, file) for file in TestLib.cache_file_words]
        for file in out_files:
            with open(file, "w") as f:
                f.write("")

        Lib.clear_cache(test_dir)

        self.assertFalse(any(exists(dir) for dir in cache_dirs))
        self.assertFalse(any(exists(file) for file in cache_files))

        self.assertTrue(all(exists(dir) for dir in out_dirs))
        self.assertTrue(all(exists(file) for file in out_files))

    def test_clear_cache_custom(self):
        custom_dir_words = [
            "python_cache_dir",
            "python cache dir",
        ]
        custom_file_words = [
            "cache.py",
            "test.py",
            "temp.py",
        ]

        test_dir = join(self.dir, "test")
        makedirs(test_dir)

        custom_dirs = [join(test_dir, dir) for dir in custom_dir_words]
        for dir in custom_dirs:
            makedirs(dir)

        custom_files = [join(test_dir, file) for file in custom_file_words]
        for file in custom_files:
            with open(file, "w") as f:
                f.write("")

        Lib.clear_cache(test_dir, custom_dir_words + custom_file_words)

        self.assertFalse(any(exists(dir) for dir in custom_dirs))
        self.assertFalse(any(exists(file) for file in custom_files))

    def test_trace_exception(self):
        divide_zero = lambda: 1 / 0

        try:
            divide_zero()

        except Exception:
            Lib.trace_exception()

    def test_trace_exception_none(self):
        with self.assertRaises(ValueError):
            Lib.trace_exception()
