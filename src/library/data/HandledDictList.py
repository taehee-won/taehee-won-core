from typing import Dict, List, Optional, Union, Any, Callable
from functools import reduce

from ..lib.macro import KWARGS, KWARGS_STR, LOOP
from .DictList import DictListFile, DictList


class HandledDictList(DictList):
    def __init__(
        self,
        handles: List[Callable[[Dict, Dict], Dict]],
        default: Optional[Union[str, List[Dict[str, Any]]]] = None,
        type: Optional[Union[DictListFile, str]] = None,
        encoding: Optional[str] = None,
        name: Optional[str] = None,
    ):
        self._handles = handles
        self._handled = 0

        super().__init__(
            **KWARGS(default=default, type=type, encoding=encoding, name=name),
        )
        self._handle()

    def _handle(self) -> None:
        LOOP(
            reduce(lambda pipe, handle: handle(self._data[i], pipe), self._handles, {})
            for i in range(self._handled, len(self._data))
        )
        self._handled = len(self._data)

    def __str__(self) -> str:
        attrs = KWARGS_STR(
            handles=len(self._handles), len=len(self._data), name=self._name
        )
        return f"{self.__class__.__name__}({attrs})"

    def append(self, element: Dict[str, Any]) -> None:
        super().append(element)
        self._handle()

    def extend(self, data: List[Dict[str, Any]]) -> None:
        super().extend(data)
        self._handle()

    def insert(self, element: Dict[str, Any], *, index: int = 0) -> None:
        err = "HandledDictList does not support insert operation"
        self._trace.critical(err)
        raise TypeError(err)

    def remove(self, element: Dict[str, Any]) -> None:
        err = "HandledDictList does not support remove operation"
        self._trace.critical(err)
        raise TypeError(err)

    def pop(self, index: int = 0) -> Dict[str, Any]:  # type: ignore
        err = "HandledDictList does not support pop operation"
        self._trace.critical(err)
        raise TypeError(err)

    def clear(self) -> None:
        err = "HandledDictList does not support clear operation"
        self._trace.critical(err)
        raise TypeError(err)

    def read(
        self,
        file: str,
        type: Optional[Union[DictListFile, str]] = None,
        encoding: Optional[str] = None,
    ) -> None:
        super().read(file, **KWARGS(type=type, encoding=encoding))
        self._handle()
