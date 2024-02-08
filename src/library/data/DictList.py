from typing import Optional, Union, List, Dict, Any, Iterable, Iterator
from enum import Enum
from collections import OrderedDict
from functools import reduce
from pickle import load as load_pickle, dump as dump_pickle
from json import load as load_json, dump as dump_json
from csv import reader as read_csv, DictWriter

from ..lib.macro import ATTR, KWARGS, KWARGS_STR, LOOP
from ..lib.Trace import Trace
from ..lib.OS import OS


class DictListFile(Enum):
    DICTLIST = "DictList"
    CSV = "csv"
    JSON = "json"


class DictList:
    def __init__(
        self,
        default: Optional[Union[str, List[Dict[str, Any]]]] = None,
        type: Optional[Union[DictListFile, str]] = None,
        encoding: Optional[str] = None,
        name: Optional[str] = None,
    ) -> None:
        self._name = name
        self._trace: Trace = ATTR(DictList, "trace", lambda: Trace("core"))
        self._data = []

        if default is not None:
            if isinstance(default, str):
                self.read(default, **KWARGS(type=type, encoding=encoding))

            else:
                self.extend(default)

    def __len__(self) -> int:
        return len(self._data)

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        for element in self._data:
            yield element

    def __getitem__(
        self,
        attr: Union[slice, int],
        /,
    ) -> Union["DictList", Dict[str, Any]]:
        return (
            DictList(self._data[attr]) if isinstance(attr, slice) else self._data[attr]
        )

    def __str__(self) -> str:
        attrs = KWARGS_STR(len=len(self._data), name=self._name)
        return f"{self.__class__.__name__}({attrs})"

    def print(self, shorten: bool = True) -> None:
        info = self._trace.info

        info(f"{self}")

        if len(self._data) <= 6 or not shorten:
            LOOP(info(f"  {i}: {e}") for i, e in enumerate(self._data))

        else:
            LOOP(info(f"  {i}: {self._data[i]}") for i in (0, 1, 2))
            info("  ...")
            LOOP(
                info(f"  {len(self._data) + i}: {self._data[i]}") for i in (-3, -2, -1)
            )

    def get(
        self,
        attr1: Union[str, Dict[str, Any]],
        attr2: Optional[Any] = None,
        /,
    ) -> Union[Dict[str, Any], None]:
        if isinstance(attr1, str):  # attr1: key, attr2: value
            for e in self._data:
                if attr1 in e and e[attr1] == attr2:
                    return e

        else:  # attr1: queries: Dict[key, value]
            for e in self._data:
                if all(k in e and e[k] == v for k, v in attr1.items()):
                    return e

    def items(
        self,
        attr1: Optional[Union[str, Dict[str, Any]]] = None,
        attr2: Optional[Any] = None,
        /,
    ) -> "DictList":
        if isinstance(attr1, str):  # attr1: key, attr2: value
            return DictList([e for e in self._data if attr1 in e and e[attr1] == attr2])

        elif isinstance(attr1, dict):  # attr1: queries: Dict[str, Any]
            return DictList(
                [
                    e
                    for e in self._data
                    if all(k in e and e[k] == v for k, v in attr1.items())
                ]
            )

        else:
            return DictList(self._data)

    def include(self, key: str, values: Iterable) -> "DictList":
        return DictList([e for e in self._data if e[key] in values])

    def exclude(self, key: str, values: Iterable) -> "DictList":
        return DictList([e for e in self._data if e[key] not in values])

    def values(
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
        type: Optional[Union[DictListFile, str]] = None,
        encoding: str = "UTF-8-sig",
    ) -> None:
        if type is None:
            type = DictListFile(OS.get_extension(file))

        elif isinstance(type, str):
            type = DictListFile(type)

        if not OS.is_exist(file):
            return

        if type == DictListFile.DICTLIST:
            with open(file, "rb") as f:
                self.extend(load_pickle(f))

        elif type == DictListFile.CSV:
            with open(file, "r", encoding=encoding) as f:
                if len((rows := [l for l in read_csv(f)])) >= 2:
                    keys = [key for key in rows[0]]
                    data = [
                        {k: l[i] for i, k in enumerate(keys) if l[i]} for l in rows[1:]
                    ]
                    self.extend(data)

        elif type == DictListFile.JSON:
            with open(file, "r", encoding=encoding) as f:
                self.extend(load_json(f))

    def write(
        self,
        file: str,
        type: Optional[Union[DictListFile, str]] = None,
        encoding: str = "UTF-8-sig",
    ) -> None:
        if type is None:
            type = DictListFile(OS.get_extension(file))

        elif isinstance(type, str):
            type = DictListFile(type)

        if not len(self._data):
            return

        OS.make_dir(OS.get_dir(file))

        if type == DictListFile.DICTLIST:
            with open(file, "wb") as f:
                dump_pickle(self._data, f)

        elif type == DictListFile.CSV:
            with open(file, "w", encoding=encoding, newline="\n") as f:
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

        elif type == DictListFile.JSON:
            with open(file, "w", encoding=encoding) as f:
                dump_json(self._data, f, ensure_ascii=False, indent="\t")
