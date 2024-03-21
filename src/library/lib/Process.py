from typing import Optional, Callable, List
from enum import Enum
from multiprocessing import cpu_count, Queue
from multiprocessing import Process as Process_
from queue import Empty
from tqdm import tqdm

from .macro import ATTR, LOOP, KWARGS_STR
from .Trace import Trace


class Bundle:
    def __init__(self, *args, **kwargs) -> None:
        self._args = args
        self._kwargs = kwargs

    @property
    def args(self):
        return self._args

    @property
    def kwargs(self):
        return self._kwargs


class Process:
    def __init__(self, count: int = cpu_count(), name: Optional[str] = None):
        self._name = name
        self._trace = ATTR(Process, "trace", lambda: Trace("core"))

        self._processes = [_Process() for _ in range(count)]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close()

    def __del__(self):
        self._close()

    def _close(self):
        if not (
            all(process.close() for process in self._processes)
            and all(process.join() for process in self._processes)
        ):
            err = "Destruct failed"
            self._trace.critical(err)
            self.print(critical=True)
            raise ValueError(err)

    def __len__(self) -> int:
        return len(self._processes)

    def __str__(self) -> str:
        attrs = KWARGS_STR(len=len(self._processes), name=self._name)
        return f"{self.__class__.__name__}({attrs})"

    def print(self, critical: bool = False) -> None:
        trace = self._trace.critical if critical else self._trace.info

        trace(f"{self}")

        LOOP(trace(f"    {process}") for process in self._processes)

    def execute(
        self,
        target: Callable,
        bundles: List[Bundle],
        unit: int = 100,
        silent: bool = False,
    ) -> List:
        portions = [
            bundles[i * unit : (i + 1) * unit]
            for i in range((len(bundles) + unit - 1) // unit)
        ]

        self._trace.debug(
            f"execute {len(portions)} portions"
            + f" for {len(bundles)} bundles"
            + f" in by {len(self)} processes"
        )

        results = []
        with tqdm(
            total=len(bundles),
            leave=False,
            dynamic_ncols=True,
            disable=silent,
        ) as progress:
            while len(results) != len(bundles):
                for process, portion in zip(
                    [process for process in self._processes if process.idle()],
                    portions,
                ):
                    if not process.execute(target, portion):
                        err = "Execute failed"
                        self._trace.critical(err)
                        self.print(critical=True)
                        raise ValueError(err)

                    portions.remove(portion)

                for process in [
                    process for process in self._processes if not process.idle()
                ]:
                    data = process.get()
                    if data is None:
                        err = "Execute failed"
                        self._trace.critical(err)
                        self.print(critical=True)
                        raise ValueError(err)

                    if data:
                        results.extend(data)
                        progress.update(len(data))

        return results


class _Process:
    def __init__(self) -> None:
        self._request = Queue()
        self._response = Queue()

        self._process = Process_(target=_process, args=(self._request, self._response))
        self._process.start()
        self._state = _State.IDLE

        self._bundles = 0
        self._results = []

    def __str__(self) -> str:
        return (
            f"process(state:{self._state.value}"
            + f"/alive:{self._process.is_alive()}"
            + f"/bundles:{self._bundles})"
        )

    def close(self) -> bool:
        if self._state != _State.IDLE:
            return False

        self._request.put(_Command.CLOSE)
        self._state = _State.UNKNOWN

        return True

    def join(self) -> bool:
        if self._state != _State.UNKNOWN:
            return False

        message = self._response.get()
        if not (isinstance(message, _State) and message == _State.CLOSED):
            return False

        self._state = _State.CLOSED
        return True

    def idle(self) -> bool:
        return self._state == _State.IDLE

    def execute(self, target: Callable, bundles: List) -> bool:
        if self._state != _State.IDLE:
            return False

        self._request.put(_Request(target, bundles))
        self._state = _State.BUSY

        self._bundles = len(bundles)

        return True

    def get(self) -> Optional[List]:
        if self._state == _State.IDLE:
            return None

        results = []

        try:
            while self._bundles and (message := self._response.get(block=False)):
                if isinstance(message, _Result):
                    results.append(message.result)
                    self._bundles -= 1

                else:
                    return None

        except Empty:
            pass

        if not self._bundles:
            self._state = _State.IDLE

        return results


def _process(request: Queue, response: Queue) -> None:
    while message := request.get():
        if isinstance(message, _Request):
            try:
                for bundle in message.bundles:
                    response.put(_Result(message.target(*bundle.args, **bundle.kwargs)))

            except Exception as e:
                response.put(_State.EXCEPTION)
                return

        elif isinstance(message, _Command) and message == _Command.CLOSE:
            response.put(_State.CLOSED)
            break

        else:
            response.put(_State.UNKNOWN)
            return


class _Command(Enum):
    CLOSE = "close"


class _State(Enum):
    IDLE = "idle"
    BUSY = "busy"
    CLOSED = "closed"
    UNKNOWN = "unknown"
    EXCEPTION = "exception"


class _Request:
    def __init__(self, target, bundles) -> None:
        self._target = target
        self._bundles = bundles

    @property
    def target(self):
        return self._target

    @property
    def bundles(self):
        return self._bundles


class _Result:
    def __init__(self, result) -> None:
        self._result = result

    @property
    def result(self):
        return self._result
