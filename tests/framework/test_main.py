from unittest import TestCase, skipIf
from os import environ

from src.library.lib.Trace import Trace
from src.framework.Component import Component
from src.framework.main import main, FrontEnd


class TestMain(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        Trace.set_levels(Trace.Level.NOTSET)

    @classmethod
    def tearDownClass(cls) -> None:
        Trace.set_levels()

    def setUp(self) -> None:
        global cli, value

        cli = False
        value = 0

    def test_main(self):
        global value, set_value, add_values

        set_value = 30
        add_values = [20, 30, 40]

        main([A, B])

        self.assertEqual(value, 120)

    @skipIf(
        environ.get("TEST_CLI") != "1" and environ.get("TEST_ALL") != "1",
        "CLI needs user input",
    )
    def test_cli(self):
        global cli, value, set_value, add_values

        cli = True
        set_value = 20
        add_values = [10, 20, 30]

        main([A, B], FrontEnd.CLI)

        self.assertEqual(value, 80)


cli = False
value = 0
set_value = 0
add_values = []


class A(Component):
    def initialize(self) -> None:
        global cli
        self.register("test", self.test)

        if cli:
            print(f"] ".rjust(48) + "enter 'test' and 'exit'")

    def main(self) -> None:
        self.test()

    def test(self) -> None:
        global value, set_value, add_values

        self.execute("set", set_value)
        for value in add_values:
            self.execute("add", value)

        value = self.execute("get")


class B(Component):
    def initialize(self) -> None:
        self._value = 0

        self.register("set", self.set, public=False)
        self.register("add", self.add, public=False)
        self.register("get", self.get, public=False)

    def get(self) -> int:
        return self._value

    def set(self, value: int) -> None:
        self._value = value

    def add(self, value: int) -> None:
        self._value += value
