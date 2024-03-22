from typing import Optional, Callable, Any

from ..library.lib.macro import KWARGS
from ..library.lib.Trace import Trace
from ..library.lib.Interface import Interface


class Component:
    def __init__(self, interface: Interface):
        self._interface = interface

        trace = Trace(type(self).__name__)

        self.critical = trace.critical
        self.error = trace.error
        self.warning = trace.warning
        self.info = trace.info
        self.debug = trace.debug

    def register(
        self,
        command: str,
        func: Callable,
        public: Optional[bool] = None,
        description: Optional[str] = None,
    ) -> None:
        self._interface.register(
            command,
            func,
            **KWARGS(public=public, description=description),
        )

    def execute(self, command: str, *args, **kwargs) -> Any:
        return self._interface.execute(command, *args, **kwargs)

    def initialize(self) -> None:
        pass

    def main(self) -> None:
        pass

    def finalize(self) -> None:
        pass
