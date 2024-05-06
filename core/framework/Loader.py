from typing import Any, List, Optional, Union
from enum import Enum
from importlib import import_module
from json5 import load as load_json

from ..data.OrderedDictList import OrderedDictList
from ..library.macro import KWARGS_STR, LOOP, RAISE
from ..library.Trace import Trace
from ..library.Path import Path
from ..library.FileSystem import FileSystem


class Loader:
    class FileType(Enum):
        JSON = "json"
        PYTHON = "py"

    def __init__(self, dirs: Optional[List[str]] = None, name: Optional[str] = None):
        self._name = name
        self._trace = Trace(name=f"core.Loader")

        self._dirs = []
        self._resources = OrderedDictList(
            "resource",
            name=f"{self.__class__.__name__}({KWARGS_STR(name=self._name)})",
        )

        if dirs:
            LOOP(self.register(dir) for dir in dirs)

    def __len__(self) -> int:
        return len(self._resources)

    def __str__(self) -> str:
        attrs = KWARGS_STR(
            dirs=len(self._dirs),
            resources=len(self._resources),
            name=self._name,
        )
        return f"{self.__class__.__name__}({attrs})"

    def print(self) -> None:
        info = self._trace.info

        info(f"{self}")

        if self._dirs:
            info(f"    dirs:")
            LOOP(info(f"        {dir}") for dir in self._dirs)

        if self._resources:
            info(f"    resources:")
            LOOP(
                info(f"        {resource['resource']}") for resource in self._resources
            )

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
                resource = path.replace_sep(".")[len(parent) :][1:]

                if path.extension:
                    resource = resource[:-1][: -len(path.extension)]

                if self._resources.get_element(resource) is not None:
                    RAISE(TypeError, f"Already registered resource: {resource}")

                if "__init__" == resource.split(".")[-1]:
                    resource = resource[:-9]

                self._resources.append(
                    {
                        "resource": resource,
                        "path": path,
                        "dir": dir,
                    }
                )

        return True

    def get_dirs(self) -> List[str]:
        return self._dirs

    def get_resources(self) -> List[str]:
        return self._resources.get_values()

    def get_module(self, resource: str) -> object:
        if r := self._resources.get_element(resource):
            if "module" not in r:
                path = r["path"]
                cwd = FileSystem.get_cwd()
                file_type = self.FileType(path.extension)

                if file_type != self.FileType.PYTHON:
                    RAISE(TypeError, f"Invalid type: {file_type}")

                if cwd not in path.path:
                    RAISE(ValueError, f"Invalid path: {path}")

                r["module"] = import_module(
                    path.replace_sep(".")[len(cwd) :][1:][:-1][: -len(file_type.value)]
                )

            return r["module"]

        RAISE(TypeError, f"Invalid resource: {resource}")

    def read(
        self,
        resource: str,
        file_type: Optional[Union[FileType, str]] = None,
    ) -> Any:
        if r := self._resources.get_element(resource):
            if file_type is None:
                file_type = self.FileType(r["path"].extension)

            if file_type == self.FileType.JSON:
                with open(r["path"].path, "r", encoding="UTF-8-sig") as f:
                    return load_json(f)

            RAISE(TypeError, f"Invalid type: {file_type}")

        RAISE(TypeError, f"Invalid resource: {resource}")
