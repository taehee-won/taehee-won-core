from typing import List
from sys import exc_info

from .macro import LOOP, RAISE
from .Trace import Trace
from .OS import OS


class Lib:
    @classmethod
    def clear_cache(
        cls,
        root: str = OS.get_cwd(),
        words: List[str] = [
            "__pycache__",  # python cache
            ".pyc",  # python cache
            ".pytest_cache",  # pytest cache
            "tempCodeRunnerFile.py",  # vscode code-runner cache
        ],
    ) -> None:
        cache_dirs = []
        cache_files = []
        for top, dirs, files in OS.get_tree(root):
            cache_dirs += [
                OS.get_path(top, dir)
                for dir in dirs
                if any(word in dir for word in words)
            ]
            cache_files += [
                OS.get_path(top, file)
                for file in files
                if any(word in file for word in words)
            ]

        debug = Trace(name="core.Lib").debug
        debug(f"clear caches from {len(words)} words")

        debug(f"{len(cache_dirs)} cache dirs:")
        LOOP(debug(f"    {dir}") for dir in cache_dirs)
        LOOP(OS.remove_dir(dir) for dir in cache_dirs)

        debug(f"{len(cache_files)} cache files:")
        LOOP(debug(f"    {file}") for file in cache_files)
        LOOP(OS.remove_file(file) for file in cache_files)

    @classmethod
    def trace_exception(cls) -> None:
        critical = Trace(name="core.Lib").critical

        exc_type, exc_value, exc_traceback = exc_info()

        if exc_type is None or exc_value is None:
            RAISE(ValueError, "Invalid exception")

        traces = []
        while exc_traceback is not None:
            traces.append(exc_traceback)
            exc_traceback = exc_traceback.tb_next

        traces = [
            [
                str(t.tb_frame.f_code.co_name),
                OS.get_file(t.tb_frame.f_code.co_filename),
                str(t.tb_lineno),
            ]
            for t in reversed(traces)
        ]
        widths = (
            max([len(traceback[0]) for traceback in traces]) + 2,
            max([len(traceback[1]) for traceback in traces]),
            max([len(traceback[2]) for traceback in traces]),
        )

        critical(f"exception {exc_type.__name__} raised for")
        critical(f"    {exc_value}")

        critical("call stack:")
        LOOP(
            critical(
                ("    --" if not index else "      "),
                (traceback[0] + "()").ljust(widths[0]),
                "from",
                traceback[1].ljust(widths[1]) + ",",
                traceback[2].ljust(widths[2]) + " line",
                ("--" if not index else ""),
            )
            for index, traceback in enumerate(traces)
        )
