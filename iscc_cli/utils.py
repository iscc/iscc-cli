# -*- coding: utf-8 -*-
from tika import detector
from os import getcwd, listdir, walk
from os.path import isfile, splitext, isdir, join

from iscc_cli.const import SUPPORTED_EXTENSIONS, GMT


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


def get_gmt(fp):
    """Return Generic Media Type"""
    mime_type = detector.from_file(fp)
    if mime_type.startswith("image"):
        return GMT.IMAGE
    else:
        return GMT.TEXT


def get_title(tika_result: dict):
    title = ""

    meta = tika_result.get("metadata")
    if meta:
        title = meta.get("dc:title", "")
        if not title:
            title = meta.get("title", "")

    if not title:
        content = tika_result.get("content")
        if content:
            title = content.strip().splitlines()[0]

    if isinstance(title, list):
        title = title[0]

    return title
