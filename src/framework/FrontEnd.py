from typing import Any
from cmd import Cmd
from queue import Queue

from ..library.lib.macro import KWARGS
from ..library.lib.Trace import Trace
from ..library.lib.Interface import Interface


class FrontEnd:
    @classmethod
    def initialize(
        cls,
        trace: Trace,
        interface: Interface,
        request: Queue,
        response: Queue,
    ) -> None:
        cls._trace = trace
        cls._interface = interface
        cls._request = request
        cls._response = response

    @staticmethod
    def start_cli() -> None:
        _Prompt().cmdloop()


class _Prompt(Cmd):
    prompt = f"] ".rjust(48)

    def preloop(self):
        FrontEnd._interface.print(public=True)

    def precmd(self, args):
        tokens = args.split()

        if not len(tokens):
            return ""

        if tokens[0] == "exit":
            return "exit"

        elif tokens[0] == "help" and len(tokens) <= 3:  # help public description
            FrontEnd._interface.print(
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

        elif tokens[0] not in FrontEnd._interface.get_commands():
            FrontEnd._trace.warning(f"invalid command: {tokens[0]}")
            return ""

        if (result := self._execute(*tokens)) is not None:
            FrontEnd._trace.info(f"{' '.join(tokens)} = {result}")

        return ""

    def do_exit(self, _):
        FrontEnd._request.put(("exit", [], {}))
        return True

    def _execute(self, command, *args, **kwargs) -> Any:
        FrontEnd._request.put((command, args, kwargs))
        return FrontEnd._response.get()
