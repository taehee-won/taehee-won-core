from typing import Optional, Union, List, Dict, Any, Iterable, Iterator, overload
from enum import Enum
from collections import OrderedDict
from functools import reduce
from pickle import load as load_pickle, dump as dump_pickle
from json import load as load_json, dump as dump_json
from csv import reader as read_csv, DictWriter

from ..library.macro import KWARGS, KWARGS_STR, LOOP
from ..library.Trace import Trace
from ..library.OS import OS


class DictList:
    class FileType(Enum):
        DICTLIST = "DictList"
        CSV = "csv"
        JSON = "json"

    def __init__(
        self,
        default: Optional[Union[str, List[Dict[str, Any]]]] = None,
        file_type: Optional[Union[FileType, str]] = None,
        name: Optional[str] = None,
    ) -> None:
        self._name = name
        self._trace = Trace(name=f"core.DictList")

        if default is None:
            self._data = []

        elif isinstance(default, str):
            self._data = []
            self.read(default, **KWARGS(file_type=file_type))

        else:
            self._data = default

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[Dict[str, Any]]:
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
        return self._data[arg]

    def __str__(self) -> str:
        attrs = KWARGS_STR(len=len(self._data), name=self._name)
        return f"{self.__class__.__name__}({attrs})"

    def print(self, shorten: bool = True) -> None:
        info = self._trace.info

        info(f"{self}")

        if len(self._data) <= 6 or not shorten:
            LOOP(info(f"    {i}: {e}") for i, e in enumerate(self._data))

        else:
            LOOP(info(f"    {i}: {self._data[i]}") for i in (0, 1, 2))
            info("    ...")
            LOOP(
                info(f"    {len(self._data) + i}: {self._data[i]}")
                for i in (-3, -2, -1)
            )

    def get_element(
        self,
        arg1: Union[str, Dict[str, Any]],
        arg2: Optional[Any] = None,
        /,
    ) -> Union[Dict[str, Any], None]:
        if isinstance(arg1, str):  # arg1: key, arg2: value
            for e in self._data:
                if arg1 in e and e[arg1] == arg2:
                    return e

        else:  # arg1: queries: Dict[key, value]
            for e in self._data:
                if all(k in e and e[k] == v for k, v in arg1.items()):
                    return e

    def get_data(
        self,
        arg1: Optional[Union[str, Dict[str, Any]]] = None,
        arg2: Optional[Any] = None,
        /,
    ) -> List[Dict[str, Any]]:
        if isinstance(arg1, str):  # arg1: key, arg2: value
            return [e for e in self._data if arg1 in e and e[arg1] == arg2]

        elif isinstance(arg1, dict):  # arg1: queries: Dict[str, Any]
            return [
                e
                for e in self._data
                if all(k in e and e[k] == v for k, v in arg1.items())
            ]

        else:
            return self._data

    def get_filtered_data(
        self,
        key: str,
        *,
        start: Optional[Any] = None,
        end: Optional[Any] = None,
        include: Optional[Iterable] = None,
        exclude: Optional[Iterable] = None,
    ) -> List[Dict[str, Any]]:
        return [
            e
            for e in self._data
            if (
                (start is None or e[key] >= start)
                and (end is None or e[key] <= end)
                and (include is None or e[key] in include)
                and (exclude is None or e[key] not in exclude)
            )
        ]

    def get_values(
        self,
        key: str,
        overlap: bool = True,
        sort: bool = False,
    ) -> List[Any]:
        values = [e[key] for e in self._data if key in e]

        if not overlap:
            values = list(OrderedDict.fromkeys(values))

        if sort:
            values.sort()

        return values

    def append(self, element: Dict[str, Any]) -> None:
        self._data.append(element)

    def extend(self, data: List[Dict[str, Any]]) -> None:
        self._data.extend(data)

    def insert(self, element: Dict[str, Any], *, index: int = 0) -> None:
        self._data.insert(index, element)

    def remove(self, element: Dict[str, Any]) -> None:
        self._data.remove(element)

    def pop(self, index: int = 0) -> Dict[str, Any]:
        return self._data.pop(index)

    def clear(self) -> None:
        self._data.clear()

    def read(
        self,
        file: str,
        file_type: Optional[Union[FileType, str]] = None,
    ) -> None:
        if file_type is None:
            file_type = self.FileType(OS.get_extension(file))

        elif isinstance(file_type, str):
            file_type = self.FileType(file_type)

        if not OS.is_exist(file):
            return

        if file_type == self.FileType.DICTLIST:
            with open(file, "rb") as f:
                self.extend(load_pickle(f))

        elif file_type == self.FileType.CSV:
            with open(file, "r", encoding="UTF-8-sig") as f:
                if len((rows := [l for l in read_csv(f)])) >= 2:
                    keys = [key for key in rows[0]]
                    data = [
                        {k: l[i] for i, k in enumerate(keys) if l[i]} for l in rows[1:]
                    ]
                    self.extend(data)

        elif file_type == self.FileType.JSON:
            with open(file, "r", encoding="UTF-8-sig") as f:
                self.extend(load_json(f))

    def write(
        self,
        file: str,
        file_type: Optional[Union[FileType, str]] = None,
    ) -> None:
        if file_type is None:
            file_type = self.FileType(OS.get_extension(file))

        elif isinstance(file_type, str):
            file_type = self.FileType(file_type)

        if not len(self._data):
            return

        OS.make_dir(OS.get_dir(file))

        if file_type == self.FileType.DICTLIST:
            with open(file, "wb") as f:
                dump_pickle(self._data, f)

        elif file_type == self.FileType.CSV:
            with open(file, "w", encoding="UTF-8-sig", newline="\n") as f:
                keys = reduce(
                    lambda keys, element: list(
                        OrderedDict.fromkeys(keys + list(element.keys()))
                    ),
                    self._data,
                    [],
                )
                csv_writer = DictWriter(f, keys)
                csv_writer.writeheader()
                csv_writer.writerows(self._data)

        elif file_type == self.FileType.JSON:
            with open(file, "w", encoding="UTF-8-sig") as f:
                dump_json(self._data, f, ensure_ascii=False, indent="\t")
