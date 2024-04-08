from unittest import TestCase

from core import KWARGS, PARAMS, ATTR, LOOP, CALL, RAISE, ARGS_STR, KWARGS_STR


class TestMacro(TestCase):
    def test_KWARGS(self):
        self.assertEqual(KWARGS(a=1, b=None, c=3), {"a": 1, "c": 3})
        self.assertEqual(KWARGS(a=None, b=None), {})

    def test_PARAMS(self):
        self.assertEqual(PARAMS(a=1, b=None, c=3), {"a": 1, "c": 3})
        self.assertEqual(PARAMS(a=None, b=None), None)

    def test_ARGS_STR(self):
        self.assertEqual(ARGS_STR("apple", "banana", 123), "apple/banana/123")
        self.assertEqual(ARGS_STR("hello", "world"), "hello/world")

    def test_KWARGS_STR(self):
        self.assertEqual(KWARGS_STR(a=1, b=None, c=3), "a:1/c:3")
        self.assertEqual(KWARGS_STR(name="Alice", age=30), "name:Alice/age:30")
        self.assertEqual(KWARGS_STR(a=None, b=None), "")

    def test_ATTR(self):
        class Class:
            pass

        instance = Class()
        self.assertIsNone(getattr(instance, "attr", None))

        value = ATTR(instance, "attr", lambda: "default")
        self.assertEqual(value, "default")

        setattr(instance, "attr", "changed")
        value = ATTR(instance, "attr", lambda: "default")
        self.assertEqual(value, "changed")

    def test_LOOP(self):
        class Class:
            def func(self):
                self.attr = "default"

        instances = [Class() for i in range(3)]

        for instance in instances:
            self.assertIsNone(getattr(instance, "attr", None))

        LOOP(instance.func() for instance in instances)

        for instance in instances:
            self.assertEqual(getattr(instance, "attr"), "default")

    def test_CALL(self):
        def test_func(x, y):
            return x / y

        self.assertIsNone(CALL(test_func, 10, 0, ignore=ZeroDivisionError))
        self.assertEqual(CALL(lambda: 1 / 3, ignore=ZeroDivisionError), 1 / 3)

        with self.assertRaises(ZeroDivisionError):
            self.assertIsNone(CALL(lambda: 1 / 0, ignore=ValueError))

    def test_RAISE(self):
        with self.assertRaises(ValueError):
            RAISE(ValueError, "Invalid value provided")
