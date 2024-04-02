from typing import Dict, Any, Union, Optional, Callable
from enum import Enum


class Cross:
    class Method(Enum):
        Golden = "Golden"
        Dead = "Dead"

    class Args(Enum):
        KEY_CROSS_KEY = "K]K"
        KEY_CROSS_VALUE = "K]V"
        VALUE_CROSS_KEY = "V]K"

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
        if method == self.Method.Golden:
            self._cross_state = lambda value1, value2: value1 > value2
            self._release_state = lambda value1, value2: value1 < value2

        else:  # method == self.Method.Dead
            self._cross_state = lambda value1, value2: value1 < value2
            self._release_state = lambda value1, value2: value1 > value2

        args = self.Args(args)
        if args == self.Args.KEY_CROSS_KEY:
            self._cross = lambda v: self._cross_state(v[self._arg1], v[self._arg2])
            self._release = lambda v: self._release_state(v[self._arg1], v[self._arg2])

        elif args == self.Args.KEY_CROSS_VALUE:
            self._cross = lambda v: self._cross_state(v[self._arg1], self._arg2)
            self._release = lambda v: self._release_state(v[self._arg1], self._arg2)

        else:  # args == self.Args.VALUE_CROSS_KEY
            self._cross = lambda v: self._cross_state(self._arg1, v[self._arg2])
            self._release = lambda v: self._release_state(self._arg1, v[self._arg2])

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

        self._crossed = True

    def get_handle(self) -> Callable[[Dict, Dict], Optional[Dict]]:
        return self._handle

    def _handle(self, element: Dict, pipe: Dict) -> Optional[Dict]:
        source = self._source(element, pipe)

        cross = self._cross(source)
        release = self._release(source)

        v = not self._crossed and cross

        if not self._crossed:
            self._crossed = cross

        elif self._crossed and release:
            self._crossed = False

        self._target(element, pipe).update({self._key: v})
