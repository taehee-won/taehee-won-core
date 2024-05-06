from typing import Self
from os import getcwd, pardir
from os.path import basename, dirname, abspath, relpath, join, splitext, sep as sep_

from .macro import RAISE


class Path:
    def __init__(self, path: str) -> None:
        self._path = abspath(path)

    def __str__(self) -> str:
        return self._path

    def __eq__(self, value: object) -> bool:
        if isinstance(value, str):
            return self._path == value

        elif isinstance(value, Path):
            return self._path == value._path

        RAISE(TypeError, f"Invalid type: {type(value)}")

    def __len__(self) -> int:
        return len(self._path)

    @property
    def path(self) -> str:
        return self._path

    @property
    def relpath(self) -> str:
        return relpath(self._path)

    @property
    def file(self) -> str:
        return basename(self._path)

    @property
    def name(self) -> str:
        return splitext(basename(self._path))[0]

    @property
    def extension(self) -> str:
        return splitext(self._path)[1][1:]

    def get_dir(self) -> str:
        return dirname(self._path)

    @classmethod
    def from_cwd(cls) -> "Path":
        return cls(getcwd())

    @classmethod
    def from_tokens(cls, *tokens: str) -> "Path":
        return cls(join(*tokens))

    def get_pardir(self, upper: int = 1) -> str:
        path = self._path
        for _ in range(upper):
            path = join(path, pardir)

        return abspath(path)

    def set_dir(self) -> Self:
        self._path = dirname(self._path)
        return self

    def set_pardir(self, upper: int = 1) -> Self:
        for _ in range(upper):
            self._path = join(self._path, pardir)

        self._path = abspath(self._path)
        return self

    def replace_sep(self, sep: str) -> str:
        return self._path.replace(sep_, sep)
