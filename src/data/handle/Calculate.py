from typing import Dict, Any, Union, Optional, Callable
from enum import Enum

from .Handle import Handle


class Calculate(Handle):
    class Method(Enum):
        ADD = "ADD"
        SUB = "SUB"
        MUL = "MUL"
        DIV = "DIV"

    def __init__(
        self,
        method: Union[Method, str],
        args: Union[Handle.Args, str],
        arg1: Any,
        arg2: Any,
        key: Optional[str] = None,
        source: Union[Handle.Param, str] = Handle.Param.ELEMENT,
        target: Union[Handle.Param, str] = Handle.Param.PIPE,
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

        self._arg1 = arg1
        self._arg2 = arg2

        args = self.Args(args)
        if args == self.Args.KEY_AND_KEY:
            self._calculate = lambda v: self._state(v[self._arg1], v[self._arg2])

        elif args == self.Args.KEY_AND_VALUE:
            self._calculate = lambda v: self._state(v[self._arg1], self._arg2)

        else:  # args == self.Args.VALUE_AND_KEY
            self._calculate = lambda v: self._state(self._arg1, v[self._arg2])

        super().__init__(key if key is not None else method.value, source, target)

    def get_handle(self) -> Callable[[Dict, Dict], Optional[Dict]]:
        return self.handle

    def handle(self, element: Dict, pipe: Dict) -> Optional[Dict]:
        self._target(element, pipe).update(
            {self._key: self._calculate(self._source(element, pipe))}
        )
