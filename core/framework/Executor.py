from typing import Any, Tuple, List, Dict, Optional
from enum import Enum
from functools import reduce

from ..library.macro import KWARGS, RAISE
from ..library.Datetime import Datetime
from .Loader import Loader


class Executor:
    def __init__(
        self,
        # Dict[key, [resource, module, List[[type, value]], Dict[key, [type, value]]]]
        config: Dict[str, Tuple[str, str, List, Dict]],
    ) -> None:
        self._config = config

    def execute(self, loader: Loader, kwargs: Optional[Dict] = None) -> Any:
        return reduce(
            lambda pipe, item: {
                **pipe,
                item[0]: _Executor(item[1]).execute(
                    loader,
                    pipe=pipe,
                    **KWARGS(kwargs=kwargs),
                ),
            },
            self._config.items(),
            {},
        )["="]


class _Executor:
    class Index:
        RESOURCE = 0
        MODULE = 1
        ARG_CONFIGS = 2  # List[[type, value]]
        KWARG_CONFIGS = 3  # Dict[key, [type, value]]

    def __init__(
        self,
        # [resource, module, List[[type, value]], Dict[key, [type, value]]]
        config: Tuple[str, str, List[Tuple[str, Any]], Dict[str, Tuple[str, Any]]],
    ) -> None:
        self._resource = config[self.Index.RESOURCE]
        self._module = config[self.Index.MODULE]
        self._arg_configs = config[self.Index.ARG_CONFIGS]
        self._kwarg_configs = config[self.Index.KWARG_CONFIGS]

    def execute(
        self,
        loader: Loader,
        kwargs: Optional[Dict] = None,
        pipe: Optional[Dict] = None,
    ) -> Any:
        module = loader.get_module(self._resource)

        if not hasattr(module, self._module):
            RAISE(ValueError, f"Invalid module: {self._module}")

        return getattr(module, self._module)(
            *reduce(
                lambda a, arg_config: [
                    *a,
                    _Arg(arg_config).execute(
                        loader=loader,
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
                        loader=loader,
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
        loader: Optional[Loader] = None,
        kwargs: Optional[Dict] = None,
        pipe: Optional[Dict] = None,
    ) -> Any:
        if self._type == self.Type.BYPASS:
            return self._value

        if self._type == self.Type.KWARG:
            if not kwargs:
                RAISE(ValueError, f"Invalid kwargs: not exist")

            elif self._value not in kwargs:
                RAISE(
                    ValueError,
                    f"Invalid key: key({self._value}) not in kwargs({kwargs.keys()})",
                )

            return kwargs[self._value]

        elif self._type == self.Type.PIPE and pipe:
            if not pipe:
                RAISE(ValueError, "Invalid pipe: not exist")

            elif self._value not in pipe:
                RAISE(
                    ValueError,
                    f"Invalid key: key({self._value}) not in pipe({pipe.keys()})",
                )

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
            ).datetime

        else:  # self._type  == self.Type.EXECUTOR_CONFIGS
            if not loader:
                RAISE(ValueError, "Invalid loader: not exist")

            return Executor(self._value).execute(loader, **KWARGS(kwargs=kwargs))
