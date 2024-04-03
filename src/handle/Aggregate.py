from typing import List, Dict, Union, Optional, Callable
from enum import Enum


class Aggregate:
    class Method(Enum):
        ALL = "ALL"
        ANY = "ANY"

    class Param(Enum):
        ELEMENT = "element"
        PIPE = "pipe"

    def __init__(
        self,
        method: Union[Method, str],
        keys: List[str],
        source: Union[Param, str] = Param.ELEMENT,
        target: Union[Param, str] = Param.PIPE,
        key: Optional[str] = None,
    ):
        method = self.Method(method)
        if method == self.Method.ALL:
            self._aggregate = lambda values: all(values)

        else:  # method == self.Method.ANY
            self._aggregate = lambda values: any(values)

        self._keys = keys

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
        source = self._source(element, pipe)

        self._target(element, pipe).update(
            {self._key: self._aggregate(source[key] for key in self._keys)}
        )
