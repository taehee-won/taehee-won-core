from typing import Final, Callable, Optional, Union
from time import time, sleep

from .macro import ATTR, KWARGS_STR
from .Trace import Trace


_SECONDS_PER_DAY: Final[int] = 86400


class Interval:
    def __init__(
        self,
        interval: Union[int, float],
        name: Optional[str] = None,
    ):
        self._interval: Union[int, float] = interval
        self._name: Union[str, None] = name
        self._trace: Trace = ATTR(Interval, "trace", lambda: Trace("core"))
        self._record = time() - _SECONDS_PER_DAY

    def __str__(self) -> str:
        attrs = KWARGS_STR(name=self._name, interval=f"{self._interval}s")
        return f"{self.__class__.__name__}({attrs})"

    def wait(self) -> Union[int, float]:
        if (moment := self._interval - (time() - self._record)) > 0:
            self._trace.debug(f"delay {moment:.5f} seconds by {self}")
            sleep(moment)

        self._record = time()

        return max(moment, 0)
