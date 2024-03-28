from typing import Any, Dict, Union, Optional
from enum import Enum
from logging import CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
from logging import getLogger, StreamHandler, FileHandler, NullHandler, Formatter

from .Datetime import Datetime
from .macro import ATTR
from .OS import OS


class TraceLevel:
    CRITICAL = CRITICAL
    ERROR = ERROR
    WARNING = WARNING
    INFO = INFO
    DEBUG = DEBUG
    NOTSET = NOTSET


class Trace:
    @classmethod
    def _get_attrs(cls) -> Dict:
        return ATTR(
            cls,
            "attrs",
            lambda: {
                "traces": [],
                "configs": {
                    _ConfigLevel.PRIMARY: _Config(),
                    _ConfigLevel.DEDICATED: {},
                    _ConfigLevel.INSTANCE: {},
                    _ConfigLevel.DEFAULT: _Config(TraceLevel.INFO, TraceLevel.NOTSET),
                },
                "formatter": Formatter(
                    "[%(asctime)s][%(name)-10s][%(levelname)-8s] %(message)s"
                ),
                "stream": StreamHandler,
                "file": FileHandler,
                "path": OS.get_path(
                    "files",
                    "traces",
                    Datetime.from_now().to_str("%Y-%m-%d"),
                    Datetime.from_now().to_str("%H-%M-%S.trace"),
                ),
            },
        )

    @classmethod
    def set_levels(
        cls,
        stream: Union[int, str, None] = None,
        file: Union[int, str, None] = None,
        name: Optional[str] = None,
    ) -> None:
        configs = cls._get_attrs()["configs"]

        if name is None:
            configs[_ConfigLevel.PRIMARY] = _Config(stream, file)

        else:
            configs[_ConfigLevel.DEDICATED][name] = _Config(stream, file)

        cls._set_traces()

    @classmethod
    def set_path(cls, path: str) -> None:
        cls._get_attrs()["path"] = path

    def __new__(
        cls,
        name: str,
        stream: Union[int, str, None] = None,
        file: Union[int, str, None] = None,
    ):
        for trace in cls._get_attrs()["traces"]:
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
            self._name = name

            configs = self._get_attrs()["configs"]
            configs[_ConfigLevel.INSTANCE][self._name] = _Config(stream, file)

            self._logger = getLogger(name)
            self._logger.addHandler(NullHandler())
            self._logger.setLevel(TraceLevel.DEBUG)

            self._stream = None
            self._file = None

            self._get_attrs()["traces"].append(self)
            self._set_traces()

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

    @classmethod
    def _set_traces(cls) -> None:
        attrs = cls._get_attrs()

        configs = attrs["configs"]
        is_trace = lambda level: level != TraceLevel.NOTSET and level != "NOTSET"

        for trace in attrs["traces"]:
            stream = next(
                level
                for level in [
                    configs[_ConfigLevel.PRIMARY].stream,
                    configs[_ConfigLevel.DEDICATED].get(trace._name, _Config()).stream,
                    configs[_ConfigLevel.INSTANCE][trace._name].stream,
                    configs[_ConfigLevel.DEFAULT].stream,
                ]
                if level is not None
            )

            if is_trace(stream):
                if trace._stream is None:
                    trace._stream = attrs["stream"]()
                    trace._stream.setFormatter(attrs["formatter"])
                    trace._logger.addHandler(trace._stream)

                trace._stream.setLevel(stream)

            elif trace._stream is not None:
                trace._stream.close()
                trace._logger.removeHandler(trace._stream)
                trace._stream = None

            file = next(
                level
                for level in [
                    configs[_ConfigLevel.PRIMARY].file,
                    configs[_ConfigLevel.DEDICATED].get(trace._name, _Config()).file,
                    configs[_ConfigLevel.INSTANCE][trace._name].file,
                    configs[_ConfigLevel.DEFAULT].file,
                ]
                if level is not None
            )

            if is_trace(file):
                if trace._file is None:
                    OS.make_dir(OS.get_dir(attrs["path"]))
                    trace._file = attrs["file"](attrs["path"])
                    trace._file.setFormatter(attrs["formatter"])
                    trace._logger.addHandler(trace._file)

                trace._file.setLevel(file)

            elif trace._file is not None:
                trace._file.close()
                trace._logger.removeHandler(trace._file)
                trace._file = None


class _ConfigLevel(Enum):
    PRIMARY = "primary"
    DEDICATED = "dedicated"
    INSTANCE = "instance"
    DEFAULT = "default"


class _Config:
    def __init__(
        self,
        stream: Union[int, str, None] = None,
        file: Union[int, str, None] = None,
    ) -> None:
        self._stream = stream
        self._file = file

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(stream:{self._stream}/file:{self._file})"

    @property
    def stream(self) -> Union[int, str, None]:
        return self._stream

    @property
    def file(self) -> Union[int, str, None]:
        return self._file
