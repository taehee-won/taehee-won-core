from typing import Dict, Any, Union, Optional, Callable
from enum import Enum


class Calculate:
    class Method(Enum):
        ADD = "ADD"
        SUB = "SUB"
        MUL = "MUL"
        DIV = "DIV"

    class Args(Enum):
        KEY_CALCULATE_KEY = "K#K"
        KEY_CALCULATE_VALUE = "K#V"
        VALUE_CALCULATE_KEY = "V#K"

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
        if method == self.Method.ADD:
            self._state = lambda value1, value2: value1 + value2

        elif method == self.Method.SUB:
            self._state = lambda value1, value2: value1 - value2

        elif method == self.Method.MUL:
            self._state = lambda value1, value2: value1 * value2

        else:  # method == self.Method.DIV
            self._state = lambda value1, value2: value1 / value2

        args = self.Args(args)
        if args == self.Args.KEY_CALCULATE_KEY:
            self._calculate = lambda v: self._state(v[self._arg1], v[self._arg2])

        elif args == self.Args.KEY_CALCULATE_VALUE:
            self._calculate = lambda v: self._state(v[self._arg1], self._arg2)

        else:  # args == self.Args.VALUE_CALCULATE_KEY
            self._calculate = lambda v: self._state(self._arg1, v[self._arg2])

        self._arg1 = arg1
        self._arg2 = arg2

        source = self.Param(source)
        if source == self.Param.ELEMENT:
            self._source = lambda element, pipe: element

        else:  # source == self.Param.PIPE
            self._source = lambda element, pipe: pipe

        target = self.Param(target)
        if target == self.Param.ELEMENT:
            self._target = lambda element, pipe: element

        else:  # target == self.Param.PIPE
            self._target = lambda element, pipe: pipe

        self._key = key if key is not None else method.value

    def get_handle(self) -> Callable[[Dict, Dict], Optional[Dict]]:
        return self.handle

    def handle(self, element: Dict, pipe: Dict) -> Optional[Dict]:
        self._target(element, pipe).update(
            {self._key: self._calculate(self._source(element, pipe))}
        )
