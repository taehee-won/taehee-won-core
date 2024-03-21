from typing import Any, Callable, Optional

from ..data.OrderedDictList import OrderedDictList
from .macro import ATTR, KWARGS_STR, LOOP
from .Trace import Trace


class Interface:
    def __init__(self, name: Optional[str] = None):
        self._name = name
        self._trace = ATTR(Interface, "trace", lambda: Trace("core"))

        attrs = KWARGS_STR(name=self._name)
        self._interfaces = OrderedDictList("command", name=f"Interface({attrs})")

    def __len__(self) -> int:
        return len(self._interfaces)

    def __str__(self) -> str:
        attrs = KWARGS_STR(
            len=len(self._interfaces),
            api=sum(1 for interface in self._interfaces if interface["api"]),
            name=self._name,
        )
        return f"{self.__class__.__name__}({attrs})"

    def print(self, api: Optional[bool] = None, description: bool = True) -> None:
        info = self._trace.info

        info(f"{self}")

        interfaces = [
            interface
            for interface in self._interfaces
            if api is None or interface["api"] == api
        ]
        if not interfaces:
            return

        length = max(len(interface["command"]) for interface in interfaces)
        LOOP(
            info(
                f"    {interface['command'].ljust(length)}",
                (
                    f"    - {interface['description']}"
                    if description and interface["description"]
                    else ""
                ),
            )
            for interface in interfaces
        )

    def register(
        self,
        command: str,
        func: Callable,
        api: bool = True,
        description: Optional[str] = None,
    ) -> bool:
        if self._interfaces.get_element(command):
            return False

        self._interfaces.append(
            {
                "command": command,
                "func": func,
                "api": api,
                "description": description,
            }
        )
        return True

    def remove(self, command: str) -> bool:
        if interface := self._interfaces.get_element(command):
            self._interfaces.remove(interface)
            return True

        return False

    def execute(self, command: str, *args, **kwargs) -> Any:
        if interface := self._interfaces.get_element(command):
            return interface["func"](*args, **kwargs)

        err = f"Invalid command: {command}"
        self._trace.critical(err)
        raise TypeError(err)
