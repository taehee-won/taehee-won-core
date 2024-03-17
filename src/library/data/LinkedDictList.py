from typing import Callable, Dict, Optional, List
from enum import IntEnum
from functools import reduce

from ..lib.macro import ATTR, KWARGS_STR, LOOP
from ..lib.Trace import Trace
from .DictList import DictList


class Node:
    def __init__(
        self,
        data: DictList,
        handles: List[Callable[[Dict, Dict], Dict]],
    ) -> None:
        self._data = data
        self._handles = handles

        self._handled = 0
        self._pipe = {}

    def __str__(self) -> str:
        attrs = KWARGS_STR(
            len=len(self._data),
            handles=len(self._handles),
            handled=self._handled,
        )
        return f"{self.__class__.__name__}({attrs})"

    @property
    def data(self):
        return self._data

    @property
    def handles(self):
        return self._handles

    @property
    def handled(self):
        return self._handled

    def update(self, count: int = 1):
        self._handled += count

    @property
    def pipe(self):
        return self._pipe

    @pipe.setter
    def pipe(self, pipe):
        self._pipe = pipe


class LinkedDictList:
    def __init__(
        self,
        key: str,
        nodes: List[Node],
        handles: Optional[List[Callable[[Dict, Dict], Dict]]] = None,
        name: Optional[str] = None,
    ):
        self._key = key
        self._nodes = nodes
        self._handles = handles
        self._name = name
        self._trace = ATTR(DictList, "trace", lambda: Trace("core"))

    def __len__(self) -> int:
        return len(self._nodes)

    def __getitem__(self, index: int) -> Node:
        return self._nodes[index]

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

        LOOP(info(f"  {node}") for node in self._nodes)

    def handle(self) -> None:
        for n, e, _ in sorted(
            [
                [n, node.handled + e, element[self._key]]
                for n, node in enumerate(self._nodes)
                for e, element in enumerate(node.data[node.handled :])
                if element[self._key] <= self._nodes[-1].data[-1][self._key]
            ],
            key=lambda target: (target[2], target[0]),
        ):
            self._nodes[n].pipe = reduce(
                lambda pipe, handle: handle(self._nodes[n].data[e], pipe),
                self._nodes[n].handles,
                self._nodes[n - 1].pipe if n else {},
            )
            self._nodes[n].update()

            if n == len(self._nodes) - 1 and self._handles:
                reduce(
                    lambda pipe, handle: handle(self._nodes[n].data[e], pipe),
                    self._handles,
                    self._nodes[n].pipe,
                )
