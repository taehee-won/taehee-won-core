from typing import List, Optional, Union, Type
from enum import Enum
from threading import Thread
from queue import Queue

from ..library.lib.macro import KWARGS_STR, ARGS_STR, LOOP, RAISE
from ..library.lib.Trace import Trace
from ..library.lib.Interface import Interface
from ..library.lib.Lib import Lib
from .Component import Component
from .FrontEnd import FrontEnd as FrontEnd_


class FrontEnd(Enum):
    MAIN = "main"
    CLI = "cli"


def main(
    components: List[Type[Component]],
    frontend: FrontEnd = FrontEnd.MAIN,
):
    trace = Trace("main")
    interface = Interface(name="main")
    interface._trace = trace

    names = [component.__name__ for component in components]
    trace.debug(f"create components: {', '.join(names)}")
    instances = [component(interface) for component in components]

    trace.debug(f"initialize components")
    LOOP(instance.initialize() for instance in instances)

    if frontend == FrontEnd.MAIN:
        trace.debug(f"call main from components")
        LOOP(instance.main() for instance in instances)

    else:
        request = Queue()
        response = Queue()
        FrontEnd_.initialize(trace, interface, request, response)

        trace.debug(f"start {frontend}")
        Thread(
            target=(
                FrontEnd_.start_cli
                if frontend == FrontEnd.CLI
                else RAISE(TypeError, f"Invalid frontend: {frontend.value}")
            )
        ).start()

        while True:
            command, args, kwargs = request.get()
            try:
                if command == "exit":
                    break

                else:
                    trace.debug(
                        f"execute {command}",
                        f"{ARGS_STR(*args)}",
                        f"{KWARGS_STR(**kwargs)}",
                    )

                    response.put(interface.execute(command, *args, **kwargs))

            except Exception:
                Lib.trace_exception()
                response.put(None)

    trace.debug(f"finalize components")
    LOOP(instance.finalize() for instance in instances)
