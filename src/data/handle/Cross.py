from typing import Dict, Any, Union, Optional
from enum import Enum

from .Handle import Handle


class Cross(Handle):
    class Method(Enum):
        Golden = "Golden"
        Dead = "Dead"

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
        if method == self.Method.Golden:
            self._cross_state = lambda value1, value2: value1 > value2
            self._release_state = lambda value1, value2: value1 < value2

        else:  # method == self.Method.Dead
            self._cross_state = lambda value1, value2: value1 < value2
            self._release_state = lambda value1, value2: value1 > value2

        self._arg1 = arg1
        self._arg2 = arg2

        args = self.Args(args)
        if args == self.Args.KEY_AND_KEY:
            self._cross = lambda v: self._cross_state(v[self._arg1], v[self._arg2])
            self._release = lambda v: self._release_state(v[self._arg1], v[self._arg2])

        elif args == self.Args.KEY_AND_VALUE:
            self._cross = lambda v: self._cross_state(v[self._arg1], self._arg2)
            self._release = lambda v: self._release_state(v[self._arg1], self._arg2)

        else:  # args == self.Args.VALUE_AND_KEY
            self._cross = lambda v: self._cross_state(self._arg1, v[self._arg2])
            self._release = lambda v: self._release_state(self._arg1, v[self._arg2])

        self._crossed = True

        super().__init__(key if key is not None else method.value, source, target)

    def handle(self, element: Dict, pipe: Dict) -> Optional[Dict]:
        source = self._source(element, pipe)

        cross = self._cross(source)
        release = self._release(source)

        v = not self._crossed and cross

        if not self._crossed:
            self._crossed = cross

        elif self._crossed and release:
            self._crossed = False

        self._target(element, pipe).update({self._key: v})
