from unittest import TestCase
from os.path import join, dirname, abspath

from core import Trace, Executor, Loader


D_LOADER = join(dirname(abspath(__file__)), "Executor")


class TestExecutor(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Trace.set_levels(Trace.Level.NOTSET)

    @classmethod
    def tearDownClass(cls) -> None:
        Trace.set_levels()

    def setUp(self) -> None:
        self.loader = Loader([D_LOADER])

    def test_execute(self):
        self.assertEqual(
            Executor(
                {"=": ("Executor", "add", [["I", 3], ["I", 4]], {})},
            ).execute(self.loader),
            7,
        )
        self.assertEqual(
            Executor(
                {
                    "=": ("Executor", "add", [["I", 3], ["I", 4]], {}),
                    "a": ("Executor", "add", [["I", 11], ["I", 12]], {}),
                }
            ).execute(self.loader),
            7,
        )

        with self.assertRaises(ValueError):
            Executor(
                {"=": ("Executor", "add_", [["I", 3], ["I", 4]], {})},
            ).execute(self.loader)

    def test_kwargs(self):
        executor = Executor({"=": ("Executor", "add", [["K", "a"], ["K", "b"]], {})})

        self.assertEqual(executor.execute(self.loader, {"a": 10, "b": 30}), 40)
        self.assertEqual(executor.execute(self.loader, {"a": 20, "b": 5}), 25)

    def test_pipe(self):
        self.assertEqual(
            Executor(
                {
                    "a": ("Executor", "add", [["I", 3], ["I", 4]], {}),
                    "b": ("Executor", "add", [["I", 11], ["I", 12]], {}),
                    "=": ("Executor", "sub", [["P", "a"], ["P", "b"]], {}),
                }
            ).execute(self.loader),
            (3 + 4) - (11 + 12),
        )

    def test_executor(self):
        self.assertEqual(
            Executor(
                {
                    "=": (
                        "Executor",
                        "add",
                        [
                            ["E", {"=": ("Executor", "add", [["I", 3], ["I", 4]], {})}],
                            ["E", {"=": ("Executor", "add", [["I", 2], ["I", 1]], {})}],
                        ],
                        {},
                    )
                }
            ).execute(self.loader),
            10,
        )
