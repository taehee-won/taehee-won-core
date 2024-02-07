from typing import List

from .macro import LOOP, ATTR
from .Trace import Trace
from .OS import OS


class Lib:
    @staticmethod
    def clear_cache(
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

        debug = ATTR(Lib, "trace", lambda: Trace("core")).debug
        debug(f"clear caches from {len(words)} words")

        debug(f"{len(cache_dirs)} cache dirs:")
        LOOP(debug(f"  {dir}") for dir in cache_dirs)
        LOOP(OS.remove_dir(dir) for dir in cache_dirs)

        debug(f"{len(cache_files)} cache files:")
        LOOP(debug(f"  {file}") for file in cache_files)
        LOOP(OS.remove_file(file) for file in cache_files)
