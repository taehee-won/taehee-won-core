from typing import Any, List, Optional, Union
from importlib import import_module
from json5 import load as load_json

from .macro import ATTR, KWARGS_STR, LOOP
from .Trace import Trace
from .OS import OS
from ..data.OrderedDictList import OrderedDictList


class Files:
    def __init__(self, dirs: Optional[List[str]] = None, name: Optional[str] = None):
        self._name = name
        self._trace = ATTR(Files, "trace", lambda: Trace("core"))

        self._dirs = []
        self._files = OrderedDictList(
            "file",
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
            info(f"  dirs:")
            LOOP(info(f"    {dir}") for dir in self._dirs)

        if self._files:
            info(f"  files:")
            LOOP(info(f"    {file['file']}") for file in self._files)

    def register(self, dir: str) -> bool:
        if dir in self._dirs:
            return False

        self._dirs.append(dir)

        target = OS.get_abspath(dir)
        parent = OS.get_abspath(OS.get_pardir(dir))

        modules = OS.get_cwd() in parent

        for top, _, files in OS.get_tree(parent):
            for file in files:
                if top[: len(target)] == target and "__pycache__" not in top:
                    path = OS.get_path(top, file)

                    file = path.replace(parent, "")[1:]
                    if ex := OS.get_extension(file):
                        file = file.replace("." + ex, "")

                    file = OS.replace_sep(file, ".")

                    if self._files.get_element(file) is not None:
                        err = f"Already registered file: {file}"
                        self._trace.critical(err)
                        raise TypeError(err)

                    if modules and OS.get_extension(path) == "py":
                        name = OS.replace_sep(
                            path.replace(OS.get_cwd(), "")[1:][:-3],
                            ".",
                        )
                        module = import_module(name)

                    else:
                        module = None

                    self._files.append(
                        {
                            "file": file,
                            "path": path,
                            "module": module,
                            "dir": dir,
                        }
                    )

        return True

    def get_dirs(self) -> List[str]:
        return self._dirs

    def get_files(self) -> List[str]:
        return self._files.get_values()

    def execute(
        self,
        file: str,
        module: str,
        *args,
        **kwargs,
    ) -> Optional[Union[None, Any]]:
        if file_ := self._files.get_element(file):
            return getattr(file_["module"], module)(*args, **kwargs)

        err = f"Invalid file: {file}"
        self._trace.critical(err)
        raise TypeError(err)

    def load(self, file: str, encoding: str = "UTF-8-sig") -> Any:
        if file_ := self._files.get_element(file):
            with open(file_["path"], "r", encoding=encoding) as f:
                return load_json(f)

        err = f"Invalid file: {file}"
        self._trace.critical(err)
        raise TypeError(err)
