from unittest import TestCase
from typing import List, Dict
from tempfile import NamedTemporaryFile
from os import remove
from logging import Handler, LogRecord
from string import ascii_letters, digits
from random import choice
from inspect import currentframe

from core import Trace


class TestTrace(TestCase):
    @classmethod
    def setUpClass(cls):
        Trace._get_attrs()["stream"] = _StreamHandler

        fd = NamedTemporaryFile(delete=False)
        cls.file = fd.name
        Trace.set_path(cls.file)
        fd.close()

    @classmethod
    def tearDownClass(cls) -> None:
        remove(cls.file)

    def setUp(self) -> None:
        Trace.set_levels()

    def tearDown(self) -> None:
        Trace.set_levels()

    @classmethod
    def _stream(cls) -> str:
        return _StreamHandler.stream()

    @classmethod
    def _file(cls) -> str:
        with open(cls.file, "r") as f:
            trace = f.read()

        return trace

    @staticmethod
    def _levels() -> List[str]:
        return ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]

    @staticmethod
    def _format(name: str, level: str, msg: str) -> str:
        return f"[{name:10s}][{level.upper():8s}] {msg}"

    @classmethod
    def _prepare(cls, test: str, stream: str, file: str):
        name = "".join(choice(ascii_letters + digits) for _ in range(10))
        levels = cls._levels()
        msgs = {level: f"{level} {test}" for level in levels}

        expected_stream_msgs, unexpected_stream_msgs = [], []
        expect = True if stream in levels else False
        for level in levels:
            if expect:
                expected_stream_msgs.append(msgs[level])
            else:
                unexpected_stream_msgs.append(msgs[level])

            if level == stream:
                expect = False

        expected_file_msgs, unexpected_file_msgs = [], []
        expect = True
        expect = True if file in levels else False
        for level in levels:
            if expect:
                expected_file_msgs.append(cls._format(name, level, msgs[level]))
            else:
                unexpected_file_msgs.append(cls._format(name, level, msgs[level]))

            if level == file:
                expect = False

        evaluations = [
            expected_stream_msgs,
            unexpected_stream_msgs,
            expected_file_msgs,
            unexpected_file_msgs,
        ]

        return name, msgs, evaluations

    @classmethod
    def _trace(cls, trace: Trace, msgs: Dict[str, str]) -> None:
        levels = cls._levels()
        for level in levels:
            getattr(trace, level.lower())(msgs[level])

    def _evaluate(self, evaluations: List[List[str]]) -> None:
        (
            expected_stream_msgs,
            unexpected_stream_msgs,
            expected_file_msgs,
            unexpected_file_msgs,
        ) = evaluations

        for msg in expected_stream_msgs:
            self.assertIn(msg, self._stream())

        for msg in unexpected_stream_msgs:
            self.assertNotIn(msg, self._stream())

        for msg in expected_file_msgs:
            self.assertIn(msg, self._file())

        for msg in unexpected_file_msgs:
            self.assertNotIn(msg, self._file())

    def test_primary(self):
        name, msgs, evaluations = self._prepare(
            frame.f_code.co_name if (frame := currentframe()) else "", "ERROR", "INFO"
        )

        Trace.set_levels(Trace.Level.ERROR, Trace.Level.INFO)
        Trace.set_levels(Trace.Level.INFO, Trace.Level.DEBUG, name)
        trace = Trace(name, Trace.Level.DEBUG, Trace.Level.DEBUG)

        self._trace(trace, msgs)
        self._evaluate(evaluations)

        name, msgs, evaluations = self._prepare(
            (frame.f_code.co_name if (frame := currentframe()) else "") + "+1",
            stream="NOTSET",
            file="DEBUG",
        )

        Trace.set_levels(Trace.Level.NOTSET, Trace.Level.DEBUG)
        Trace.set_levels(Trace.Level.INFO, Trace.Level.DEBUG, name)
        trace = Trace(name, Trace.Level.DEBUG, Trace.Level.DEBUG)

        self._trace(trace, msgs)
        self._evaluate(evaluations)

    def test_dedicated(self):
        name, msgs, evaluations = self._prepare(
            frame.f_code.co_name if (frame := currentframe()) else "",
            stream="INFO",
            file="DEBUG",
        )

        Trace.set_levels(Trace.Level.INFO, Trace.Level.DEBUG, name)
        trace = Trace(name, Trace.Level.ERROR, Trace.Level.WARNING)

        self._trace(trace, msgs)
        self._evaluate(evaluations)

        name, msgs, evaluations = self._prepare(
            (frame.f_code.co_name if (frame := currentframe()) else "") + "+1",
            stream="DEBUG",
            file="INFO",
        )

        Trace.set_levels(Trace.Level.DEBUG, Trace.Level.INFO, name)
        trace = Trace(name, Trace.Level.ERROR, Trace.Level.WARNING)

        self._trace(trace, msgs)
        self._evaluate(evaluations)

    def test_instance(self):
        name, msgs, evaluations = self._prepare(
            frame.f_code.co_name if (frame := currentframe()) else "",
            stream="ERROR",
            file="WARNING",
        )

        trace = Trace(name, Trace.Level.ERROR, Trace.Level.WARNING)

        self._trace(trace, msgs)
        self._evaluate(evaluations)

        name, msgs, evaluations = self._prepare(
            (frame.f_code.co_name if (frame := currentframe()) else "") + "+1",
            stream="DEBUG",
            file="NOTSET",
        )

        trace = Trace(name, stream=Trace.Level.DEBUG, file=Trace.Level.NOTSET)

        self._trace(trace, msgs)
        self._evaluate(evaluations)

    def test_default(self):
        name, msgs, evaluations = self._prepare(
            frame.f_code.co_name if (frame := currentframe()) else "",
            stream="INFO",
            file="NONE",
        )

        trace = Trace(name)

        self._trace(trace, msgs)
        self._evaluate(evaluations)

        name, msgs, evaluations = self._prepare(
            (frame.f_code.co_name if (frame := currentframe()) else "") + "+1",
            stream="INFO",
            file="NONE",
        )

        trace = Trace(name)

        self._trace(trace, msgs)
        self._evaluate(evaluations)

    def test_primary_str(self):
        name, msgs, evaluations = self._prepare(
            frame.f_code.co_name if (frame := currentframe()) else "",
            stream="ERROR",
            file="INFO",
        )

        Trace.set_levels("ERROR", "INFO")
        Trace.set_levels("INFO", "DEBUG", name)
        trace = Trace(name, stream="DEBUG", file="DEBUG")

        self._trace(trace, msgs)
        self._evaluate(evaluations)

        name, msgs, evaluations = self._prepare(
            (frame.f_code.co_name if (frame := currentframe()) else "") + "+1",
            stream="NOTSET",
            file="DEBUG",
        )

        Trace.set_levels("NOTSET", "DEBUG")
        Trace.set_levels("INFO", "DEBUG", name)
        trace = Trace(name, stream="DEBUG", file="DEBUG")

        self._trace(trace, msgs)
        self._evaluate(evaluations)

    def test_dedicated_str(self):
        name, msgs, evaluations = self._prepare(
            frame.f_code.co_name if (frame := currentframe()) else "",
            stream="INFO",
            file="DEBUG",
        )

        Trace.set_levels("INFO", "DEBUG", name)
        trace = Trace(name, stream="ERROR", file="WARNING")

        self._trace(trace, msgs)
        self._evaluate(evaluations)

        name, msgs, evaluations = self._prepare(
            (frame.f_code.co_name if (frame := currentframe()) else "") + "+1",
            stream="DEBUG",
            file="INFO",
        )

        Trace.set_levels("DEBUG", "INFO", name)
        trace = Trace(name, stream="ERROR", file="WARNING")

        self._trace(trace, msgs)
        self._evaluate(evaluations)

    def test_instance_str(self):
        name, msgs, evaluations = self._prepare(
            frame.f_code.co_name if (frame := currentframe()) else "",
            stream="ERROR",
            file="WARNING",
        )

        trace = Trace(name, stream="ERROR", file="WARNING")

        self._trace(trace, msgs)
        self._evaluate(evaluations)

        name, msgs, evaluations = self._prepare(
            (frame.f_code.co_name if (frame := currentframe()) else "") + "+1",
            stream="DEBUG",
            file="NOTSET",
        )

        trace = Trace(name, stream="DEBUG", file="NOTSET")

        self._trace(trace, msgs)
        self._evaluate(evaluations)

    def test_default_str(self):
        name, msgs, evaluations = self._prepare(
            frame.f_code.co_name if (frame := currentframe()) else "",
            stream="INFO",
            file="NONE",
        )

        trace = Trace(name)

        self._trace(trace, msgs)
        self._evaluate(evaluations)

        name, msgs, evaluations = self._prepare(
            (frame.f_code.co_name if (frame := currentframe()) else "") + "+1",
            stream="INFO",
            file="NONE",
        )

        trace = Trace(name)

        self._trace(trace, msgs)
        self._evaluate(evaluations)


class _StreamHandler(Handler):
    msgs = []

    def __init__(self, level: int = 0) -> None:
        super().__init__(level)

    def emit(self, record: LogRecord) -> None:
        self.msgs.append(record.getMessage())

    @classmethod
    def stream(cls) -> str:
        return "\n".join(_StreamHandler.msgs)
