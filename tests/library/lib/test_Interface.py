from unittest import TestCase

from src.library.lib.Trace import TraceLevel, Trace
from src.library.lib.Interface import Interface


class TestInterface(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Trace.set_levels(TraceLevel.NOTSET)

    @classmethod
    def tearDownClass(cls) -> None:
        Trace.set_levels()

    def setUp(self) -> None:
        self.interface = Interface(name="TestInterface")

        self.assertTrue(self.interface.register("add", self._add, description="a + b"))
        self.assertTrue(self.interface.register("sub", self._sub, api=False))

        self.assertTrue(self.interface.register("set", self._set))
        self.assertTrue(self.interface.register("get", self._get))

    @staticmethod
    def _add(a, b):
        return a + b

    @staticmethod
    def _sub(a, b):
        return a - b

    def _set(self, value):
        self.value = value

    def _get(self):
        return self.value

    def test_init(self):
        interface = Interface()
        self.assertIsInstance(interface, Interface)

    def test_len(self):
        self.assertEqual(len(self.interface), 4)

    def test_str(self):
        self.assertIsInstance(str(self.interface), str)
        self.assertIn("Interface", str(self.interface))
        self.assertIn("len:4", str(self.interface))
        self.assertIn("name:TestInterface", str(self.interface))

        interface = Interface()
        self.assertIsInstance(str(interface), str)
        self.assertIn("Interface", str(interface))
        self.assertIn("len:0", str(interface))
        self.assertNotIn("name:", str(interface))

        interface.register("test", TestInterface.test_str)
        self.assertIn("len:1", str(interface))

    def test_register(self):
        interface = Interface()

        self.assertTrue(interface.register("add", self._add))
        self.assertTrue(interface.register("sub", self._sub))

        self.assertFalse(interface.register("add", self._add))
        self.assertFalse(interface.register("sub", self._sub))

    def test_remove(self):
        interface = Interface()

        self.assertTrue(interface.register("add", self._add))
        self.assertTrue(interface.register("sub", self._sub))

        self.assertFalse(interface.register("add", self._add))
        self.assertFalse(interface.register("sub", self._sub))

        self.assertTrue(interface.remove("add"))
        self.assertTrue(interface.remove("sub"))

        self.assertFalse(interface.remove("add"))
        self.assertFalse(interface.remove("sub"))

    def test_execute(self):
        self.assertEqual(self.interface.execute("add", 1, 2), 3)
        self.assertEqual(self.interface.execute("sub", 1, 2), -1)

        with self.assertRaises(TypeError):
            self.assertEqual(self.interface.execute("none", 1, 2), 3)

        with self.assertRaises(AttributeError):
            self.assertEqual(self.interface.execute("get"), 3)

        self.interface.execute("set", 3)
        self.assertEqual(self.interface.execute("get"), 3)

    def test_get_commands(self):
        self.assertEqual(len(self.interface.get_commands()), 4)
        self.assertEqual(len(self.interface.get_commands(api=True)), 3)
        self.assertEqual(len(self.interface.get_commands(api=False)), 1)
