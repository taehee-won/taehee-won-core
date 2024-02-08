from typing import Final, Optional, Union
from time import time, sleep

from .macro import ATTR, KWARGS_STR
from .Trace import Trace


_SECONDS_PER_DAY: Final[int] = 86400


class Interval:
    def __init__(
        self,
        value: Union[int, float],
        name: Optional[str] = None,
    ):
        self._value: Union[int, float] = value
        self._name: Union[str, None] = name
        self._trace: Trace = ATTR(Interval, "trace", lambda: Trace("core"))
        self._record = time() - _SECONDS_PER_DAY

    def _moment(self) -> Union[int, float]:
        return self._value - (time() - self._record)

    def __str__(self) -> str:
        attrs = KWARGS_STR(value=f"{self._value}s", name=self._name)
        return f"{self.__class__.__name__}({attrs})"

    def print(self) -> None:
        info = self._trace.info

        if (moment := self._moment()) > 0:
            info(f"{self}: interval {moment:.5f} seconds")

        else:
            info(f"{self}: no interval")

    def wait(self) -> Union[int, float]:
        moment = self._moment()
        if moment > 0:
            self._trace.debug(f"wait {moment:.5f} seconds by {self}")
            sleep(moment)

        self._record = time()

        return max(moment, 0)
