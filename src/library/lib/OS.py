from typing import List, Iterable, Tuple

from os import getcwd, listdir, makedirs, walk, remove, pardir
from os.path import exists, basename, dirname, abspath, relpath
from os.path import isfile, isdir, islink, join, splitext, getsize
from os.path import sep as sep_
from shutil import rmtree, copy, move


class OS:
    @staticmethod
    def is_exist(path: str) -> bool:
        return exists(path)

    @staticmethod
    def is_file(path: str) -> bool:
        return isfile(path)

    @staticmethod
    def is_dir(path: str) -> bool:
        return isdir(path)

    @staticmethod
    def get_cwd() -> str:
        return getcwd()

    @staticmethod
    def get_path(*paths: str) -> str:
        return join(*paths)

    @staticmethod
    def get_file(path: str) -> str:
        return basename(path)

    @staticmethod
    def get_name(path: str) -> str:
        return splitext(basename(path))[0]

    @staticmethod
    def get_extension(path: str) -> str:
        return splitext(path)[1][1:]

    @staticmethod
    def get_dir(path: str) -> str:
        return dirname(abspath(path))

    @staticmethod
    def get_pardir(path: str) -> str:
        return join(path, pardir)

    @staticmethod
    def get_abspath(path: str) -> str:
        return abspath(path)

    @staticmethod
    def get_relpath(path: str) -> str:
        return relpath(path)

    @staticmethod
    def get_files(dir: str) -> List[str]:
        return [name for name in listdir(dir) if isfile(join(dir, name))]

    @staticmethod
    def get_dirs(dir: str) -> List[str]:
        return [name for name in listdir(dir) if isdir(join(dir, name))]

    @staticmethod
    def get_tree(root: str) -> Iterable[Tuple[str, List[str], List[str]]]:
        return walk(root)

    @staticmethod
    def get_file_size(path: str) -> int:
        return getsize(path) if isfile(path) else 0

    @staticmethod
    def get_dir_size(path: str) -> int:
        size = 0

        if isdir(path):
            for dir, dirs, files in walk(path):
                for file in files:
                    path_ = join(dir, file)
                    if not islink(path_):
                        size += getsize(path_)

        return size

    @staticmethod
    def get_size(path: str) -> int:
        return (
            OS.get_file_size(path)
            if isfile(path)
            else OS.get_dir_size(path) if isdir(path) else 0
        )

    @staticmethod
    def make_dir(dir: str) -> None:
        if not exists(dir):
            makedirs(dir)

    @staticmethod
    def remove_file(file: str) -> None:
        if isfile(file):
            remove(file)

    @staticmethod
    def remove_dir(dir: str) -> None:
        if isdir(dir):
            rmtree(dir)

    @staticmethod
    def remove(path: str) -> None:
        if isfile(path):
            OS.remove_file(path)

        elif isdir(path):
            OS.remove_dir(path)

    @staticmethod
    def copy(src: str, dst: str) -> None:
        copy(src, dst)

    @staticmethod
    def move(src: str, dst: str) -> None:
        move(src, dst)

    @staticmethod
    def replace_sep(path: str, sep: str) -> str:
        return path.replace(sep_, sep)
