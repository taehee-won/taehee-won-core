from typing import List, Union, Optional
from sys import exc_info

from .macro import LOOP, RAISE
from .Trace import Trace
from .Path import Path
from .FileSystem import FileSystem


class Lib:
    @classmethod
    def clear_cache(
        cls,
        root: Optional[Union[Path, str]] = None,
        words: List[str] = [
            "__pycache__",  # python cache
            ".pyc",  # python cache
            ".pytest_cache",  # pytest cache
            "tempCodeRunnerFile.py",  # vscode code-runner cache
        ],
    ) -> None:
        if root is None:
            root = Path.from_cwd()

        if isinstance(root, str):
            root = Path(root)

        cache_dirs = []
        cache_files = []
        for top, dirs, files in FileSystem.walk(root):
            cache_dirs += [
                Path.from_tokens(top, dir)
                for dir in dirs
                if any(word in dir for word in words)
            ]
            cache_files += [
                Path.from_tokens(top, file)
                for file in files
                if any(word in file for word in words)
            ]

        debug = Trace(name="core.Lib").debug
        debug(f"clear caches from {len(words)} words")

        debug(f"{len(cache_dirs)} cache dirs:")
        LOOP(debug(f"    {dir}") for dir in cache_dirs)
        LOOP(
            FileSystem.remove_dir(dir) for dir in cache_dirs if FileSystem.is_exist(dir)
        )

        debug(f"{len(cache_files)} cache files:")
        LOOP(debug(f"    {file}") for file in cache_files)
        LOOP(
            FileSystem.remove_file(file)
            for file in cache_files
            if FileSystem.is_exist(file)
        )

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
                Path(t.tb_frame.f_code.co_filename).file,
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
