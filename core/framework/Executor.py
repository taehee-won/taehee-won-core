from typing import Union, Any, Tuple, List, Dict, Optional
from enum import Enum
from functools import reduce

from ..library.macro import KWARGS, ATTR
from ..library.Datetime import Datetime
from ..library.Trace import Trace
from ..library.Files import Files


class Executor:
    def __init__(
        self,
        # Dict[key, [file, module, List[[type, value]], Dict[key, [type, value]]]]
        config: Dict[str, Tuple[str, str, List, Dict]],
    ) -> None:
        self._config = config

    def execute(self, files: Files, kwargs: Optional[Dict] = None) -> Any:
        return reduce(
            lambda pipe, item: {
                **pipe,
                item[0]: _Executor(item[1]).execute(
                    files,
                    pipe=pipe,
                    **KWARGS(kwargs=kwargs),
                ),
            },
            self._config.items(),
            {},
        )["="]


class _Executor:
    class Index:
        FILE = 0
        MODULE = 1
        ARG_CONFIGS = 2  # List[[type, value]]
        KWARG_CONFIGS = 3  # Dict[key, [type, value]]

    def __init__(
        self,
        # [file, module, List[[type, value]], Dict[key, [type, value]]]
        config: Tuple[str, str, List[Tuple[str, Any]], Dict[str, Tuple[str, Any]]],
    ) -> None:
        self._file = config[self.Index.FILE]
        self._module = config[self.Index.MODULE]
        self._arg_configs = config[self.Index.ARG_CONFIGS]
        self._kwarg_configs = config[self.Index.KWARG_CONFIGS]

    def execute(
        self,
        files: Files,
        kwargs: Optional[Dict] = None,
        pipe: Optional[Dict] = None,
    ) -> Any:
        return files.get_module(self._file, self._module)(
            *reduce(
                lambda a, arg_config: [
                    *a,
                    _Arg(arg_config).execute(
                        files=files,
                        **KWARGS(kwargs=kwargs, pipe=pipe),
                    ),
                ],
                self._arg_configs,
                [],
            ),
            **reduce(
                lambda k, item: {
                    **k,
                    item[0]: _Arg(item[1]).execute(
                        files=files,
                        **KWARGS(kwargs=kwargs, pipe=pipe),
                    ),
                },
                self._kwarg_configs.items(),
                {},
            ),
        )


class _Arg:
    class Index:
        TYPE = 0
        VALUE = 1

    class Type(Enum):
        BYPASS = "="
        KWARG = "K"
        PIPE = "P"
        STR = "S"
        INT = "I"
        FLOAT = "F"
        DATETIME = "D"
        EXECUTOR_CONFIGS = "E"

    def __init__(self, config: Tuple[str, Any]) -> None:  # [type, value]
        self._type = self.Type(config[self.Index.TYPE])
        self._value = config[self.Index.VALUE]

    def execute(
        self,
        files: Optional[Files] = None,
        kwargs: Optional[Dict] = None,
        pipe: Optional[Dict] = None,
    ) -> Any:
        if self._type == self.Type.BYPASS:
            return self._value

        if self._type == self.Type.KWARG:
            if not kwargs:
                err = f"Invalid kwargs: kwargs({kwargs})"
                ATTR(Executor, "trace", lambda: Trace("Executor")).critical(err)
                raise ValueError(err)

            elif self._value not in kwargs:
                err = f"Invalid key: key({self._value}), kwargs({kwargs.keys()})"
                ATTR(Executor, "trace", lambda: Trace("Executor")).critical(err)
                raise ValueError(err)

            return kwargs[self._value]

        elif self._type == self.Type.PIPE and pipe:
            if not pipe:
                err = f"Invalid pipe: pipe({pipe})"
                ATTR(Executor, "trace", lambda: Trace("Executor")).critical(err)
                raise ValueError(err)

            elif self._value not in pipe:
                err = f"Invalid key: key({self._value}), pipe({pipe.keys()})"
                ATTR(Executor, "trace", lambda: Trace("Executor")).critical(err)
                raise ValueError(err)

            return pipe[self._value]

        elif self._type == self.Type.STR:
            return str(self._value)

        elif self._type == self.Type.INT:
            return int(self._value)

        elif self._type == self.Type.FLOAT:
            return float(self._value)

        elif self._type == self.Type.DATETIME:
            return Datetime.from_values(
                **KWARGS(
                    year=int(self._value[:4]),
                    month=int(self._value[4:6]) if len(self._value) >= 6 else None,
                    day=int(self._value[6:8]) if len(self._value) >= 8 else None,
                    hour=int(self._value[8:10]) if len(self._value) >= 10 else None,
                    minute=int(self._value[10:12]) if len(self._value) >= 12 else None,
                    second=int(self._value[12:14]) if len(self._value) >= 14 else None,
                )
            ).to_datetime()

        else:  # self._type  == self.Type.EXECUTOR_CONFIGS
            if not files:
                err = f"Invalid files: files({files})"
                ATTR(Executor, "trace", lambda: Trace("Executor")).critical(err)
                raise ValueError(err)

            return Executor(self._value).execute(files, **KWARGS(kwargs=kwargs))
