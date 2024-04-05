from typing import List, Dict, Union, Optional
from enum import Enum

from .Handle import Handle


class Aggregate(Handle):
    class Method(Enum):
        ALL = "ALL"
        ANY = "ANY"

    def __init__(
        self,
        method: Union[Method, str],
        keys: List[str],
        key: Optional[str] = None,
        source: Union[Handle.Param, str] = Handle.Param.ELEMENT,
        target: Union[Handle.Param, str] = Handle.Param.PIPE,
    ):
        method = self.Method(method)
        if method == self.Method.ALL:
            self._aggregate = lambda values: all(values)

        else:  # method == self.Method.ANY
            self._aggregate = lambda values: any(values)

        self._keys = keys

        super().__init__(key if key is not None else method.value, source, target)

    def handle(self, element: Dict, pipe: Dict) -> Optional[Dict]:
        source = self._source(element, pipe)
        self._target(element, pipe).update(
            {self._key: self._aggregate(source[key] for key in self._keys)}
        )
