from typing import Any, Dict, List, Optional, Union, Iterable, Iterator

from ..lib.macro import KWARGS, KWARGS_STR, RAISE
from .DictList import DictListFile, DictList


class OrderedDictList(DictList):
    def __init__(
        self,
        key: str,
        default: Optional[Union[str, List[Dict[str, Any]]]] = None,
        type: Optional[Union[DictListFile, str]] = None,
        encoding: Optional[str] = None,
        name: Optional[str] = None,
    ):
        self._key = key
        self._sorted = False

        super().__init__(
            **KWARGS(default=default, type=type, encoding=encoding, name=name)
        )

    def _sort(self) -> None:
        if not self._sorted:
            self._data.sort(key=lambda e: e[self._key])
            self._sorted = True

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        self._sort()
        for element in self._data:
            yield element

    def __getitem__(
        self,
        attr: Union[slice, int],
        /,
    ) -> Union["OrderedDictList", Dict[str, Any]]:
        self._sort()
        return (
            OrderedDictList(self._key, self._data[attr])
            if isinstance(attr, slice)
            else self._data[attr]
        )

    def __str__(self) -> str:
        attrs = KWARGS_STR(name=self._name, key=self._key, len=len(self._data))
        return f"{self.__class__.__name__}({attrs})"

    def print(self, shorten: Optional[bool] = None) -> None:
        self._sort()
        super().print(**KWARGS(shorten=shorten))

    def get(
        self,
        attr1: Union[Any, str, Dict[str, Any]],
        attr2: Optional[Any] = None,
        /,
    ) -> Union[Dict[str, Any], None]:
        if attr2 is None and not isinstance(attr1, dict):  # attr1: Any
            self._sort()

            l, r = 0, len(self._data) - 1
            while l <= r:
                if self._data[(i := (l + r) // 2)][self._key] > attr1:
                    r = i - 1

                elif self._data[i][self._key] < attr1:
                    l = i + 1

                else:
                    return self._data[i]

        else:
            return super().get(attr1, attr2)

    def items(
        self,
        attr1: Optional[Union[Any, str, Dict[str, Any]]] = None,
        attr2: Optional[Any] = None,
        /,
    ) -> "OrderedDictList":
        if attr2 is None and attr1 is not None and not isinstance(attr1, dict):
            return OrderedDictList(
                self._key, [e for e in self._data if e[self._key] == attr1]
            )

        else:
            return OrderedDictList(self._key, super().items(attr1, attr2)._data)

    def include(
        self,
        attr1: Union[str, Iterable],
        attr2: Optional[Iterable] = None,
    ) -> "OrderedDictList":  # type: ignore
        if attr2 is None:  # attr1: values
            return OrderedDictList(self._key, super().include(self._key, attr1)._data)

        elif isinstance(attr1, str):  # attr1: key, attr2: values
            return OrderedDictList(self._key, super().include(attr1, attr2)._data)

        RAISE(
            TypeError,
            f"Invalid OrderedDictList.include parameter({type(attr1)}, {type(attr2)})",
        )

    def exclude(
        self,
        attr1: Union[str, Iterable],
        attr2: Optional[Iterable] = None,
    ) -> "OrderedDictList":  # type: ignore
        if attr2 is None:  # attr1: values
            return OrderedDictList(self._key, super().exclude(self._key, attr1)._data)

        elif isinstance(attr1, str):  # attr1: key, attr2: values
            return OrderedDictList(self._key, super().exclude(attr1, attr2)._data)

        RAISE(
            TypeError,
            f"Invalid OrderedDictList.exclude parameter({type(attr1)}, {type(attr2)})",
        )

    def values(
        self,
        key: Optional[str] = None,
        overlap: Optional[bool] = None,
        sort: Optional[bool] = None,
    ) -> List:
        self._sort()
        return super().values(
            self._key if key is None else key,
            **KWARGS(overlap=overlap, sort=sort),
        )

    def append(self, element: Dict[str, Any]) -> None:
        super().append(element)
        self._sorted = False

    def extend(self, data: List[Dict[str, Any]]) -> None:
        super().extend(data)
        self._sorted = False

    def insert(self, element: Dict[str, Any], *, index: int = 0) -> None:
        RAISE(TypeError, "OrderedDictList does not support insert operation")

    def pop(self, index: Optional[int] = None) -> Dict[str, Any]:
        self._sort()
        return super().pop(**KWARGS(index=index))

    def read(
        self,
        file: str,
        type: Optional[Union[DictListFile, str]] = None,
        encoding: Optional[str] = None,
    ) -> None:
        super().read(file, **KWARGS(type=type, encoding=encoding))
        self._sorted = False

    def write(
        self,
        file: str,
        type: Optional[Union[DictListFile, str]] = None,
        encoding: Optional[str] = None,
    ) -> None:
        self._sort()
        super().write(file, **KWARGS(type=type, encoding=encoding))
