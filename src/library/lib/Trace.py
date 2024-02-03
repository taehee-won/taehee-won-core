from typing import Final, Any, Dict, List, Union
from enum import IntEnum
from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
from logging import getLogger, StreamHandler, FileHandler, NullHandler, Formatter

from ..data.Datetime import Datetime
from .macro import LOOP
from .OS import OS


class TraceLevel:
    CRITICAL = CRITICAL
    ERROR = ERROR
    WARNING = WARNING
    INFO = INFO
    DEBUG = DEBUG
    NOTSET = NOTSET


class _Index(IntEnum):
    STREAM = 0
    FILE = 1


_FORMAT: Final[str] = "[%(asctime)s][%(name)-10s][%(levelname)-8s] %(message)s"
_DEFAULT_PATH: Final[str] = OS.get_path(
    "files",
    "traces",
    Datetime.from_now().get_str("%Y-%m-%d"),
    Datetime.from_now().get_str("%H-%M-%S.trace"),
)
_DEFAULT_CONFIG: Final[List[int]] = [TraceLevel.INFO, TraceLevel.NOTSET]
_DEFAULT_HANDLES: List = [StreamHandler, FileHandler]


class Trace:
    """
    Configuration Order:
        Primary  : Trace._config  : Trace.set(stream, file)
        Dedicated: Trace._configs : Trace.set_trace(name, stream, file)
        Instance : self._config_  : obj = Trace(stream, file)
        Default  : _DEFAULT_CONFIG

    File order:
        Primary: Trace._path  : Trace.set_path(path)
        Default: _DEFAULT_PATH
    """

    _config: List[Union[int, str, None]] = [None, None]
    _configs: Dict[str, List[Union[int, str, None]]] = {}
    _path: Union[str, None] = None
    _traces: List["Trace"] = []

    @classmethod
    def set(
        cls,
        stream: Union[int, str, None] = None,
        file: Union[int, str, None] = None,
    ) -> None:
        cls._config[_Index.STREAM] = stream
        cls._config[_Index.FILE] = file

        LOOP(trace._set_handler() for trace in Trace._traces)

    @classmethod
    def set_trace(
        cls,
        name: str,
        stream: Union[int, str, None] = None,
        file: Union[int, str, None] = None,
    ) -> None:
        cls._configs.setdefault(name, [None, None])

        cls._configs[name][_Index.STREAM] = stream
        cls._configs[name][_Index.FILE] = file

        LOOP(trace._set_handler() for trace in cls._traces if trace._name == name)

    @classmethod
    def set_file(cls, path: Union[str, None]) -> None:
        cls._path = path

    def __new__(
        cls,
        name: str,
        stream: Union[int, str, None] = None,
        file: Union[int, str, None] = None,
    ):
        for trace in Trace._traces:
            if trace._name == name:
                return trace

        return super().__new__(cls)

    def __init__(
        self,
        name: str,
        stream: Union[int, str, None] = None,
        file: Union[int, str, None] = None,
    ):
        if not hasattr(self, "_name"):
            self._name: str = name
            self._config_: List[Union[int, str, None]] = [stream, file]

            self._logger = getLogger(name)
            self._logger.addHandler(NullHandler())
            self._logger.setLevel(TraceLevel.DEBUG)

            self._handlers: List = [None, None]
            self._set_handler()

            Trace._traces.append(self)

    def _get_level(self, index: int) -> int:
        return next(
            (
                level
                for level in [
                    Trace._config[index],
                    Trace._configs.get(self._name, [None, None])[index],
                    self._config_[index],
                    _DEFAULT_CONFIG[index],
                ]
                if level is not None
            ),
            _DEFAULT_CONFIG[index],
        )

    def _get_path(self) -> str:
        return path if (path := Trace._path) is not None else _DEFAULT_PATH

    def _set_handler(self) -> None:
        for index in (_Index.STREAM, _Index.FILE):
            level = self._get_level(index)
            if level != TraceLevel.NOTSET and level != "NOTSET":
                if self._handlers[index] is None:
                    if index == _Index.STREAM:
                        self._handlers[index] = _DEFAULT_HANDLES[index]()
                    else:
                        path = self._get_path()
                        OS.make_dir(OS.get_dir(path))
                        self._handlers[index] = _DEFAULT_HANDLES[index](path)

                    self._handlers[index].setFormatter(Formatter(_FORMAT))
                    self._logger.addHandler(self._handlers[index])

                self._handlers[index].setLevel(level)

            elif self._handlers[index] is not None:
                self._handlers[index].close()
                self._logger.removeHandler(self._handlers[index])
                self._handlers[index] = None

    def critical(self, *msgs: Any, sep: str = " ") -> None:
        self._logger.critical(sep.join((str(msg) for msg in msgs)))

    def error(self, *msgs: Any, sep: str = " ") -> None:
        self._logger.error(sep.join((str(msg) for msg in msgs)))

    def warning(self, *msgs: Any, sep: str = " ") -> None:
        self._logger.warning(sep.join((str(msg) for msg in msgs)))

    def info(self, *msgs: Any, sep: str = " ") -> None:
        self._logger.info(sep.join((str(msg) for msg in msgs)))

    def debug(self, *msgs: Any, sep: str = " ") -> None:
        self._logger.debug(sep.join((str(msg) for msg in msgs)))
