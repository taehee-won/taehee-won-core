from unittest import TestCase
from multiprocessing import cpu_count
from random import randint

from src.library.lib.Trace import TraceLevel, Trace
from src.library.lib.Process import Bundle, Process


class TestProcess(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Trace.set_levels(TraceLevel.NOTSET)

    @classmethod
    def tearDownClass(cls) -> None:
        Trace.set_levels()

    def setUp(self) -> None:
        self.process = Process(name="TestProcess")

    def tearDown(self) -> None:
        del self.process

    def test_init(self):
        process = Process()
        self.assertIsInstance(process, Process)

    def test_del(self):
        process = Process()
        self.assertIsInstance(process, Process)

        del process

    def test_len(self):
        self.assertEqual(len(self.process), cpu_count())

        process = Process(count=5)
        self.assertEqual(len(process), 5)

    def test_str(self):
        self.assertIsInstance(str(self.process), str)
        self.assertIn("Process", str(self.process))
        self.assertIn(f"len:{cpu_count()}", str(self.process))
        self.assertIn("name:TestProcess", str(self.process))

        process = Process(count=5)
        self.assertIsInstance(str(process), str)
        self.assertIn("Process", str(process))
        self.assertIn("len:5", str(process))
        self.assertNotIn("name:", str(process))

    @staticmethod
    def _add(a: int, b: int, c: int, d: int) -> int:
        return a + b + c + d

    def test_execute(self):
        bundles = [
            Bundle(
                randint(0, 100),
                randint(0, 100),
                c=randint(0, 100),
                d=randint(0, 100),
            )
            for _ in range(10000)
        ]
        outputs = [self._add(*bundle.args, **bundle.kwargs) for bundle in bundles]

        results = self.process.execute(self._add, bundles, silent=True)
        for result in results:
            outputs.remove(result)

        self.assertListEqual(outputs, [])
