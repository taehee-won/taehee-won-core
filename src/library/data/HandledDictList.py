from typing import Dict, List, Optional, Union, Any, Callable

from ..lib.macro import KWARGS, KWARGS_STR
from .DictList import DictList


class HandledDictList(DictList):
    def __init__(
        self,
        handles: List[Callable[[Dict, Dict], Optional[Dict]]],
        default: Optional[Union[str, List[Dict[str, Any]]]] = None,
        file_type: Optional[Union["HandledDictList.FileType", str]] = None,
        name: Optional[str] = None,
    ):
        self._handles = handles
        self._handled = 0

        super().__init__(
            **KWARGS(default=default, file_type=file_type, name=name),
        )
        self._handle()

    def _handle(self) -> None:
        for element in self._data[self._handled :]:
            pipe = {}
            for handle in self._handles:
                if result := handle(element, pipe):
                    pipe.update(result)

        self._handled = len(self._data)

    def __str__(self) -> str:
        attrs = KWARGS_STR(
            handles=len(self._handles),
            len=len(self._data),
            name=self._name,
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

    def pop(self, index: int = 0) -> Dict[str, Any]:
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
        file_type: Optional[Union["HandledDictList.FileType", str]] = None,
    ) -> None:
        super().read(file, **KWARGS(file_type=file_type))
        self._handle()
