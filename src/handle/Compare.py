from typing import Dict, Any, Union, Optional, Callable
from enum import Enum


class Compare:
    class Method(Enum):
        GT = "GT"
        GTE = "GTE"
        LT = "LT"
        LTE = "LTE"

    class Args(Enum):
        KEY_COMPARE_KEY = "KvK"
        KEY_COMPARE_VALUE = "KvV"
        VALUE_COMPARE_KEY = "VvK"

    class Param(Enum):
        ELEMENT = "element"
        PIPE = "pipe"

    def __init__(
        self,
        method: Union[Method, str],
        args: Union[Args, str],
        arg1: Any,
        arg2: Any,
        source: Union[Param, str] = Param.ELEMENT,
        target: Union[Param, str] = Param.PIPE,
        key: Optional[str] = None,
    ):
        method = self.Method(method)
        if method == self.Method.GT:
            self._state = lambda value1, value2: value1 > value2

        elif method == self.Method.GTE:
            self._state = lambda value1, value2: value1 >= value2

        elif method == self.Method.LT:
            self._state = lambda value1, value2: value1 < value2

        else:  # method == self.Method.LTE
            self._state = lambda value1, value2: value1 <= value2

        args = self.Args(args)
        if args == self.Args.KEY_COMPARE_KEY:
            self._compare = lambda v: self._state(v[self._arg1], v[self._arg2])

        elif args == self.Args.KEY_COMPARE_VALUE:
            self._compare = lambda v: self._state(v[self._arg1], self._arg2)

        else:  # args == self.Args.VALUE_COMPARE_KEY
            self._compare = lambda v: self._state(self._arg1, v[self._arg2])

        self._arg1 = arg1
        self._arg2 = arg2

        source = self.Param(source)
        if source == self.Param.ELEMENT:
            self._source = lambda element, pipe: element

        else:
            self._source = lambda element, pipe: pipe

        target = self.Param(target)
        if target == self.Param.ELEMENT:
            self._target = lambda element, pipe: element

        else:
            self._target = lambda element, pipe: pipe

        self._key = key if key is not None else method.value

    def get_handle(self) -> Callable[[Dict, Dict], Optional[Dict]]:
        return self._handle

    def _handle(self, element: Dict, pipe: Dict) -> Optional[Dict]:
        self._target(element, pipe).update(
            {self._key: self._compare(self._source(element, pipe))}
        )
