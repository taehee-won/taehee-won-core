from typing import Dict, Union, Optional

from ...data.handle.Handle import Handle
from .Indicator import Indicator


class MA(Handle, Indicator):  # Moving Average
    def __init__(
        self,
        period: int = 20,
        source_key: str = "close",
        average: Union[Indicator.Average, str] = Indicator.Average.EXPONENTIAL,
        key: Optional[str] = None,
        source: Union[Handle.Param, str] = Handle.Param.ELEMENT,
        target: Union[Handle.Param, str] = Handle.Param.PIPE,
    ):
        self._period = period
        self._source_key = source_key
        self._average = self.Average(average)

        self._values = []
        self._get = self._intro

        super().__init__(
            key if key is not None else self.__class__.__name__,
            source,
            target,
        )

    def get(self, value: Union[int, float]) -> float:
        return self._get(value)

    def handle(self, element: Dict, pipe: Dict) -> Optional[Dict]:
        self._target(element, pipe).update(
            {self._key: self.get(self._source(element, pipe)[self._source_key])}
        )

    def _intro(self, value: Union[int, float]) -> float:
        self._values.append(value)
        n = len(self._values)
        v = sum(self._values) / n

        if n == self._period:
            if self._average == self.Average.SIMPLE:
                self._get = self._simple

            elif self._average == self.Average.EXPONENTIAL:
                self._prev = v
                self._coefficient = 2 / (self._period + 1)
                self._get = self._exponential

            else:  # self._average == AverageType.SMOOTHED
                self._prev = v
                self._get = self._smoothed

        return v

    def _simple(self, value: Union[int, float]) -> float:
        self._values.pop(0)
        self._values.append(value)

        return sum(self._values) / len(self._values)

    def _exponential(self, value: Union[int, float]) -> float:
        v = (self._coefficient * value) + ((1 - self._coefficient) * self._prev)
        self._prev = v

        return v

    def _smoothed(self, value: Union[int, float]) -> float:
        self._prev = v = (self._prev * (self._period - 1) + value) / self._period

        return v
