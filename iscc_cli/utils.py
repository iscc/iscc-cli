# -*- coding: utf-8 -*-
from os import getcwd, listdir, walk
from os.path import isfile, splitext, isdir, join

from iscc_cli.const import SUPPORTED_EXTENSIONS


def iter_files(root, exts=None, recursive=False):
    """
    Iterate over file paths within root filtered by specified extensions.
    :param str root: Root folder to start collecting files
    :param iterable exts: Restrict results to given file extensions
    :param bool recursive: Wether to walk the complete directory tree
    :rtype collections.Iterable[str]: absolute file paths with given extensions
    """

    if exts is not None:
        exts = set((x.lower() for x in exts))

    def matches(e):
        return (exts is None) or (e in exts)

    if recursive is False:
        for entry in listdir(root):
            ext = splitext(entry)[-1].lstrip(".").lower()
            if not isdir(entry) and matches(ext):
                yield join(root, entry)
    else:
        for root, folders, files in walk(root):
            for f in files:
                ext = splitext(f)[-1].lstrip(".").lower()
                if matches(ext):
                    yield join(root, f)


def get_files(path, recursive=False):
    if path is None:
        path = getcwd()
    if isfile(path):
        return [path]
    return iter_files(path, exts=SUPPORTED_EXTENSIONS, recursive=recursive)
