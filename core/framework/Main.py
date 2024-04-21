from typing import Optional, Callable, Any, List, Union, Type
from enum import Enum
from threading import Thread
from queue import Queue
from cmd import Cmd

from ..library.macro import KWARGS, KWARGS_STR, ARGS_STR, LOOP, RAISE
from ..library.Trace import Trace
from ..library.Interface import Interface
from ..library.Lib import Lib


class Main:
    class Component:
        def __init__(self, interface: Interface):
            self._interface = interface

            trace = Trace(name=type(self).__name__)

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

    class FrontEnd(Enum):
        MAIN = "main"
        CLI = "cli"

    def __init__(self, components: List[Type[Component]]) -> None:
        self._components = components

        self._trace = Trace(name="core.Main")
        self._interface = Interface(name="core.Main")
        self._interface._trace = self._trace

    def start(self, frontend: Union[FrontEnd, str] = FrontEnd.MAIN) -> None:
        debug = self._trace.debug

        names = [component.__name__ for component in self._components]
        debug(f"create components: {', '.join(names)}")
        instances = [component(self._interface) for component in self._components]

        debug(f"initialize components")
        LOOP(instance.initialize() for instance in instances)

        frontend = self.FrontEnd(frontend)

        if frontend == self.FrontEnd.MAIN:
            debug(f"call main from components")
            LOOP(instance.main() for instance in instances)

        else:
            request = Queue()
            response = Queue()

            if frontend == self.FrontEnd.CLI:
                prompt = _Prompt()
                prompt.initialize(self._trace, self._interface, request, response)
                target = prompt.cmdloop

            else:
                RAISE(TypeError, f"Invalid frontend: {frontend}")

            debug(f"start {frontend}")
            Thread(target=target).start()

            while True:
                command, args, kwargs = request.get()
                try:
                    if command == "exit":
                        break

                    else:
                        debug(
                            f"execute {command}",
                            f"{ARGS_STR(*args)}",
                            f"{KWARGS_STR(**kwargs)}",
                        )

                        response.put(self._interface.execute(command, *args, **kwargs))

                except Exception:
                    Lib.trace_exception()
                    response.put(None)

        debug(f"finalize components")
        LOOP(instance.finalize() for instance in instances)


class _Prompt(Cmd):
    prompt = f"] ".rjust(48)

    def initialize(
        self,
        trace: Trace,
        interface: Interface,
        request: Queue,
        response: Queue,
    ) -> None:
        self._trace = trace
        self._interface = interface
        self._request = request
        self._response = response

    def preloop(self):
        self._interface.print(public=True)

    def precmd(self, args):
        tokens = args.split()

        if not len(tokens):
            return ""

        if tokens[0] == "exit":
            return "exit"

        elif tokens[0] == "help" and len(tokens) <= 3:  # help public description
            self._interface.print(
                **KWARGS(
                    public=(
                        None
                        if len(tokens) < 2 or tokens[1] == "?"
                        else tokens[1] == "o"
                    ),
                    description=(None if len(tokens) < 3 else tokens[2] == "o"),
                )
            )

            return ""

        elif tokens[0] not in self._interface.get_commands():
            self._trace.warning(f"invalid command: {tokens[0]}")
            return ""

        if (result := self._execute(*tokens)) is not None:
            self._trace.info(f"{' '.join(tokens)} = {result}")

        return ""

    def do_exit(self, _):
        self._request.put(("exit", [], {}))
        return True

    def _execute(self, command, *args, **kwargs) -> Any:
        self._request.put((command, args, kwargs))
        return self._response.get()
