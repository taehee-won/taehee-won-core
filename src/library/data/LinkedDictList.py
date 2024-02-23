from typing import Callable, Dict, Optional, List
from enum import IntEnum
from functools import reduce

from ..lib.macro import ATTR, KWARGS_STR, LOOP
from ..lib.Trace import Trace
from .DictList import DictList


class LinkedDictList:
    def __init__(
        self,
        key: str,
        nodes: Dict[DictList, List[Callable[[Dict, Dict], Dict]]],
        handles: Optional[List[Callable[[Dict, Dict], Dict]]] = None,
        name: Optional[str] = None,
    ):
        self._key = key
        self._nodes = [[node, handles, 0, {}] for node, handles in nodes.items()]
        self._handles = handles
        self._name = name
        self._trace: Trace = ATTR(DictList, "trace", lambda: Trace("core"))

    def __len__(self) -> int:
        return len(self._nodes)

    def __getitem__(self, index: int) -> DictList:
        return self._nodes[index][_I_Node.NODE]

    def __str__(self) -> str:
        attrs = KWARGS_STR(
            key=self._key,
            nodes=len(self._nodes),
            handles=len(self._handles) if self._handles else None,
            name=self._name,
        )
        return f"{self.__class__.__name__}({attrs})"

    def print(self) -> None:
        info = self._trace.info

        info(f"{self}")

        LOOP(
            info(
                f"  {i}: {node[_I_Node.NODE]}"
                + f"/handles:{len(node[_I_Node.HANDLES])}"
                + f"/handled:{node[_I_Node.HANDLED]}"
            )
            for i, node in enumerate(self._nodes)
        )

    def handle(self) -> None:
        for n, e, _ in sorted(
            [
                [n, node[_I_Node.HANDLED] + e, element[self._key]]
                for n, node in enumerate(self._nodes)
                for e, element in enumerate(node[_I_Node.NODE][node[_I_Node.HANDLED] :])
                if element[self._key] <= self._nodes[-1][_I_Node.NODE][-1][self._key]
            ],
            key=lambda target: (target[2], target[0]),
        ):
            self._nodes[n][_I_Node.PIPE] = reduce(
                lambda pipe, handle: handle(self._nodes[n][_I_Node.NODE][e], pipe),
                self._nodes[n][_I_Node.HANDLES],
                self._nodes[n - 1][_I_Node.PIPE] if n else {},
            )
            self._nodes[n][_I_Node.HANDLED] += 1

            if n == len(self._nodes) - 1 and self._handles:
                reduce(
                    lambda pipe, handle: handle(self._nodes[n][_I_Node.NODE][e], pipe),
                    self._handles,
                    self._nodes[n][_I_Node.PIPE],
                )


class _I_Node(IntEnum):
    NODE = 0
    HANDLES = 1
    HANDLED = 2
    PIPE = 3
