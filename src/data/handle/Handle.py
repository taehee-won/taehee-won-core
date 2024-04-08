from typing import Dict, Optional, Callable, Union
from enum import Enum
from abc import ABC, abstractmethod


class Handle(ABC):
    class Args(Enum):
        KEY_AND_KEY = "K&K"
        KEY_AND_VALUE = "K&V"
        VALUE_AND_KEY = "V&K"

    class Param(Enum):
        ELEMENT = "ELEMENT"
        PIPE = "PIPE"

    def __init__(
        self,
        key: str,
        source: Union[Param, str],
        target: Union[Param, str],
    ):
        self._key = key

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

    @abstractmethod
    def handle(self, element: Dict, pipe: Dict) -> Optional[Dict]:
        pass

    def get_handle(self) -> Callable[[Dict, Dict], Optional[Dict]]:
        return self.handle
