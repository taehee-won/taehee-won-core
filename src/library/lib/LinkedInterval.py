from typing import Optional, Union, Dict
from time import time, sleep

from .macro import ATTR, KWARGS_STR, RAISE, LOOP
from .Trace import Trace

from ..data.DictList import DictListFile, DictList


class LinkedInterval:
    def __init__(
        self,
        values: Dict[Union[int, float], int],
        file: Optional[str] = None,
        name: Optional[str] = None,
    ):
        self._file: Union[str, None] = file
        self._name: Union[str, None] = name
        self._trace: Trace = ATTR(LinkedInterval, "trace", lambda: Trace("core"))

        attrs = KWARGS_STR(file=self._file, name=self._name)
        self._values: DictList = DictList(name=f"{self.__class__.__name__}({attrs})")

        if self._file is not None:
            self._values.read(self._file, DictListFile.DICTLIST)

        if not self._values:
            self._values.extend(
                [{"value": v, "count": c, "records": []} for v, c in values.items()]
            )

    def _moment(self) -> Union[int, float]:
        now = time()
        moments = [0] + [
            moment
            for v in self._values
            if v["count"] == len(v["records"])
            and (moment := v["value"] - (now - v["records"][0])) > 0
        ]
        return max(moments)

    def __str__(self) -> str:
        attrs = KWARGS_STR(
            values=len(self._values),
            file=self._file,
            name=self._name,
        )
        return f"{self.__class__.__name__}({attrs})"

    def print(self) -> None:
        info = self._trace.info

        if (moment := self._moment()) > 0:
            info(f"{self}: interval {moment:.5f} seconds")

        else:
            info(f"{self}: no interval")

    def wait(self) -> Union[int, float]:
        now = time()
        for v in self._values:
            v["records"] = [r for r in v["records"] if v["value"] - (now - r) > 0]

        moments = [0] + [
            v["value"] - (now - v["records"].pop(0))
            for v in self._values
            if v["count"] == len(v["records"])
        ]

        moment = max(moments)
        if moment > 0:
            self._trace.debug(f"wait {moment:.5f} seconds by {self}")
            sleep(moment)

        now = time()
        LOOP(v["records"].append(now) for v in self._values)

        if self._file is not None:
            self._values.write(self._file, DictListFile.DICTLIST)

        return max(moment, 0)
