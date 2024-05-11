from typing import Union, List, Iterable, Tuple
from os import getcwd, listdir, makedirs, walk, remove
from os.path import exists, isfile, isdir, islink, join, getsize
from shutil import rmtree, copy, move

from .macro import RAISE
from .Path import Path


class FileSystem:
    @staticmethod
    def is_exist(path: Union[Path, str]) -> bool:
        if isinstance(path, Path):
            path = path.path

        return exists(path)

    @classmethod
    def is_file(cls, path: Union[Path, str]) -> bool:
        if isinstance(path, Path):
            path = path.path

        if not cls.is_exist(path):
            RAISE(ValueError, f"Invalid path: {path} is not exist")

        return isfile(path) if not islink(path) else False

    @classmethod
    def is_dir(cls, path: Union[Path, str]) -> bool:
        if isinstance(path, Path):
            path = path.path

        if not cls.is_exist(path):
            RAISE(ValueError, f"Invalid path: {path} is not exist")

        return isdir(path) if not islink(path) else False

    @classmethod
    def is_link(cls, path: Union[Path, str]) -> bool:
        if isinstance(path, Path):
            path = path.path

        if not cls.is_exist(path):
            RAISE(ValueError, f"Invalid path: {path} is not exist")

        return islink(path)

    @staticmethod
    def get_cwd() -> Path:
        return Path(getcwd())

    @classmethod
    def get_files(cls, path: Union[Path, str]) -> List[Path]:
        if isinstance(path, Path):
            path = path.path

        if not cls.is_dir(path):
            RAISE(ValueError, f"Invalid path: {path} is not dir")

        return [Path(p) for name in listdir(path) if cls.is_file(p := join(path, name))]

    @classmethod
    def get_dirs(cls, path: Union[Path, str]) -> List[Path]:
        if isinstance(path, Path):
            path = path.path

        if not cls.is_dir(path):
            RAISE(ValueError, f"Invalid path: {path} is not dir")

        return [Path(p) for name in listdir(path) if cls.is_dir(p := join(path, name))]

    @classmethod
    def get_links(cls, path: Union[Path, str]) -> List[Path]:
        if isinstance(path, Path):
            path = path.path

        if not cls.is_dir(path):
            RAISE(ValueError, f"Invalid path: {path} is not dir")

        return [Path(p) for name in listdir(path) if cls.is_link(p := join(path, name))]

    @classmethod
    def get_file_size(cls, path: Union[Path, str]) -> int:
        if isinstance(path, Path):
            path = path.path

        if not cls.is_file(path):
            RAISE(ValueError, f"Invalid path: {path} is not file")

        return getsize(path)

    @classmethod
    def get_dir_size(cls, path: Union[Path, str]) -> int:
        return sum(
            getsize(p)
            for top, _, files in cls.walk(path)
            for file in files
            if cls.is_file(p := join(top, file))
        )

    @classmethod
    def make_dir(cls, path: Union[Path, str]) -> Path:
        if isinstance(path, Path):
            path = path.path

        if cls.is_exist(path):
            RAISE(ValueError, f"Invalid path: {path} is exist")

        makedirs(path)

        return Path(path)

    @classmethod
    def remove_file(cls, path: Union[Path, str]) -> None:
        if isinstance(path, Path):
            path = path.path

        if not cls.is_file(path):
            RAISE(ValueError, f"Invalid path: {path} is not file")

        remove(path)

    @classmethod
    def remove_dir(cls, path: Union[Path, str]) -> None:
        if isinstance(path, Path):
            path = path.path

        if not cls.is_dir(path):
            RAISE(ValueError, f"Invalid path: {path} is not dir")

        rmtree(path)

    @classmethod
    def remove_link(cls, path: Union[Path, str]) -> None:
        if isinstance(path, Path):
            path = path.path

        if not cls.is_link(path):
            RAISE(ValueError, f"Invalid path: {path} is not link")

        remove(path)

    @classmethod
    def copy(cls, src: Union[Path, str], dst: Union[Path, str]) -> Path:
        if isinstance(src, Path):
            src = src.path

        if isinstance(dst, Path):
            dst = dst.path

        if not cls.is_exist(src):
            RAISE(ValueError, f"Invalid src: {src} is not exist")

        if cls.is_exist(dst):
            RAISE(ValueError, f"Invalid dst: {dst} is exist")

        copy(src, dst)

        return Path(dst)

    @classmethod
    def move(cls, src: Union[Path, str], dst: Union[Path, str]) -> Path:
        if isinstance(src, Path):
            src = src.path

        if isinstance(dst, Path):
            dst = dst.path

        if not cls.is_exist(src):
            RAISE(ValueError, f"Invalid src: {src} is not exist")

        if cls.is_exist(dst):
            RAISE(ValueError, f"Invalid dst: {dst} is exist")

        move(src, dst)

        return Path(dst)

    @classmethod
    def walk(
        cls,
        path: Union[Path, str],
    ) -> Iterable[Tuple[str, List[str], List[str]]]:
        if isinstance(path, Path):
            path = path.path

        if not cls.is_dir(path):
            RAISE(ValueError, f"Invalid path: {path} is not dir")

        return walk(path)
