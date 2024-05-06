from typing import Any, List, Optional, Union
from enum import Enum
from importlib import import_module
from json5 import load as load_json

from ..data.OrderedDictList import OrderedDictList
from .macro import KWARGS_STR, LOOP, RAISE
from .Trace import Trace
from .Path import Path
from .FileSystem import FileSystem


class Files:
    class FileType(Enum):
        JSON = "json"
        PYTHON = "py"

    def __init__(self, dirs: Optional[List[str]] = None, name: Optional[str] = None):
        self._name = name
        self._trace = Trace(name=f"core.Files")

        self._dirs = []
        self._files = OrderedDictList(
            "name",
            name=f"{self.__class__.__name__}({KWARGS_STR(name=self._name)})",
        )

        if dirs:
            LOOP(self.register(dir) for dir in dirs)

    def __len__(self) -> int:
        return len(self._files)

    def __str__(self) -> str:
        attrs = KWARGS_STR(
            dirs=len(self._dirs),
            files=len(self._files),
            name=self._name,
        )
        return f"{self.__class__.__name__}({attrs})"

    def print(self) -> None:
        info = self._trace.info

        info(f"{self}")

        if self._dirs:
            info(f"    dirs:")
            LOOP(info(f"        {dir}") for dir in self._dirs)

        if self._files:
            info(f"    files:")
            LOOP(info(f"        {file['file']}") for file in self._files)

    def register(self, dir: str) -> bool:
        if dir in self._dirs:
            return False

        self._dirs.append(dir)

        target = Path(dir)
        parent = Path(dir).set_pardir()

        for top, _, files in FileSystem.get_tree(parent):
            if not top[: len(target)] == target or "__pycache__" in top:
                continue

            for file in files:
                path = Path.from_tokens(top, file)
                name = path.replace_sep(".")[len(parent) :][1:]

                if path.extension:
                    name = name[:-1][: -len(path.extension)]

                if self._files.get_element(name) is not None:
                    RAISE(TypeError, f"Already registered name: {name}")

                if "__init__" == name.split(".")[-1]:
                    name = name[:-9]

                self._files.append(
                    {
                        "name": name,
                        "path": path,
                        "dir": dir,
                    }
                )

        return True

    def get_dirs(self) -> List[str]:
        return self._dirs

    def get_files(self) -> List[str]:
        return self._files.get_values()

    def get_module(self, name: str) -> object:
        if file := self._files.get_element(name):
            if "module" not in file:
                path = file["path"]
                cwd = FileSystem.get_cwd()
                file_type = self.FileType(path.extension)

                if file_type != self.FileType.PYTHON:
                    RAISE(TypeError, f"Invalid type: {file_type}")

                if cwd not in path.path:
                    RAISE(ValueError, f"Invalid path: {path}")

                file["module"] = import_module(
                    path.replace_sep(".")[len(cwd) :][1:][:-1][: -len(file_type.value)]
                )

            return file["module"]

        RAISE(TypeError, f"Invalid name: {name}")

    def read(
        self,
        name: str,
        file_type: Optional[Union[FileType, str]] = None,
    ) -> Any:
        if file := self._files.get_element(name):
            if file_type is None:
                file_type = self.FileType(file["path"].extension)

            if file_type == self.FileType.JSON:
                with open(file["path"].path, "r", encoding="UTF-8-sig") as f:
                    return load_json(f)

            RAISE(TypeError, f"Invalid type: {file_type}")

        RAISE(TypeError, f"Invalid name: {name}")
