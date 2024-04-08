from typing import Dict, Union, Optional

from ...data.handle.Handle import Handle
from .Indicator import Indicator
from .MA import MA


class RSI(Handle, Indicator):  # Relative Strength Index
    def __init__(
        self,
        period: int = 15,
        source_key: str = "close",
        average: Union[Indicator.Average, str] = Indicator.Average.SMOOTHED,
        key: Optional[str] = None,
        source: Union[Handle.Param, str] = Handle.Param.ELEMENT,
        target: Union[Handle.Param, str] = Handle.Param.PIPE,
    ):
        self._source_key = source_key

        self._U_MA = MA(period, average=average)
        self._D_MA = MA(period, average=average)

        self._prev = 0
        self._get = self._intro

        super().__init__(
            key if key is not None else self.__class__.__name__,
            source,
            target,
        )

    def get(self, value: Union[int, float]) -> float:
        return self._get(value)

    def handle(self, element: Dict, pipe: Dict) -> Dict:
        self._target(element, pipe).update(
            {self._key: self.get(self._source(element, pipe)[self._source_key])}
        )
        return pipe

    def _intro(self, value: Union[int, float]) -> float:
        self._prev = value
        self._get = self._main

        return self._main(value)

    def _main(self, value: Union[int, float]) -> float:
        if self._prev <= value:
            U = self._U_MA.get(value - self._prev)
            D = self._D_MA.get(0)

        else:
            U = self._U_MA.get(0)
            D = self._D_MA.get(self._prev - value)

        self._prev = value

        return 50 if not U and not D else 100 if not D else (100 * (1 - (D / (U + D))))
