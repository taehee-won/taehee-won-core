from typing import Any, Dict, List, Optional, Union, Iterable, Iterator, overload

from ..lib.macro import KWARGS, KWARGS_STR
from .DictList import DictList


class OrderedDictList(DictList):
    def __init__(
        self,
        key: str,
        default: Optional[Union[str, List[Dict[str, Any]]]] = None,
        file_type: Optional[Union[DictList.FileType, str]] = None,
        name: Optional[str] = None,
    ):
        self._key: str = key
        self._sorted = False

        super().__init__(**KWARGS(default=default, file_type=file_type, name=name))

    def _sort(self) -> None:
        if not self._sorted:
            self._data.sort(key=lambda e: e[self._key])
            self._sorted = True

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        self._sort()
        for element in self._data:
            yield element

    @overload
    def __getitem__(self, arg: slice, /) -> List[Dict[str, Any]]: ...

    @overload
    def __getitem__(self, arg: int, /) -> Dict[str, Any]: ...

    def __getitem__(
        self,
        arg: Union[slice, int],
        /,
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        self._sort()
        return super().__getitem__(arg)

    def __str__(self) -> str:
        attrs = KWARGS_STR(key=self._key, len=len(self._data), name=self._name)
        return f"{self.__class__.__name__}({attrs})"

    def print(self, shorten: Optional[bool] = None) -> None:
        self._sort()
        super().print(**KWARGS(shorten=shorten))

    def get_element(
        self,
        arg1: Union[Any, str, Dict[str, Any]],
        arg2: Optional[Any] = None,
        /,
    ) -> Union[Dict[str, Any], None]:
        if arg2 is None and not isinstance(arg1, dict):  # arg1: Any
            self._sort()

            l, r = 0, len(self._data) - 1
            while l <= r:
                if self._data[(i := (l + r) // 2)][self._key] > arg1:
                    r = i - 1

                elif self._data[i][self._key] < arg1:
                    l = i + 1

                else:
                    return self._data[i]

        else:
            return super().get_element(arg1, arg2)

    def get_data(
        self,
        arg1: Optional[Union[Any, str, Dict[str, Any]]] = None,
        arg2: Optional[Any] = None,
        /,
    ) -> List[Dict[str, Any]]:
        if arg2 is None and arg1 is not None and not isinstance(arg1, dict):
            arg2 = arg1
            arg1 = self._key

        return super().get_data(arg1, arg2)

    def get_filtered_data(
        self,
        key: Optional[str] = None,
        *,
        start: Optional[Any] = None,
        end: Optional[Any] = None,
        include: Optional[Iterable] = None,
        exclude: Optional[Iterable] = None,
    ) -> List[Dict[str, Any]]:
        return super().get_filtered_data(
            self._key if key is None else key,
            **KWARGS(start=start, end=end, include=include, exclude=exclude),
        )

    def get_values(
        self,
        key: Optional[str] = None,
        overlap: Optional[bool] = None,
        sort: Optional[bool] = None,
    ) -> List:
        self._sort()
        return super().get_values(
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
        err = "OrderedDictList does not support insert operation"
        self._trace.critical(err)
        raise TypeError(err)

    def pop(self, index: Optional[int] = None) -> Dict[str, Any]:
        self._sort()
        return super().pop(**KWARGS(index=index))

    def read(
        self,
        file: str,
        file_type: Optional[Union[DictList.FileType, str]] = None,
    ) -> None:
        super().read(file, **KWARGS(file_type=file_type))
        self._sorted = False

    def write(
        self,
        file: str,
        file_type: Optional[Union[DictList.FileType, str]] = None,
    ) -> None:
        self._sort()
        super().write(file, **KWARGS(file_type=file_type))
