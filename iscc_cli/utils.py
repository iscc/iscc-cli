# -*- coding: utf-8 -*-
import textwrap
from os import getcwd, listdir, walk
from os.path import isfile, splitext, isdir, join
import click
import iscc

from iscc_cli.const import (
    SUPPORTED_EXTENSIONS,
    SUPPORTED_MIME_TYPES,
    ISCC_COMPONENT_CODES,
)


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


def mime_to_gmt(mime_type):
    entry = SUPPORTED_MIME_TYPES.get(mime_type)
    if entry:
        return entry["gmt"]


def get_title(tika_result: dict, guess=False):
    title = ""

    meta = tika_result.get("metadata")
    if meta:
        title = meta.get("dc:title", "")
        title = title[0].strip() if isinstance(title, list) else title.strip()
        if not title:
            title = meta.get("title", "").strip()

    # See if string would survive normalization
    norm_title = iscc.text_normalize(title, keep_ws=True)

    if not norm_title and guess:
        first_line = tika_result.get("content", "").strip().splitlines()[0]
        if first_line:
            title = iscc.text_trim(iscc.text_normalize(first_line, keep_ws=True))

    return title


class DefaultHelp(click.Command):
    def __init__(self, *args, **kwargs):
        context_settings = kwargs.setdefault("context_settings", {})
        if "help_option_names" not in context_settings:
            context_settings["help_option_names"] = ["-h", "--help"]
        self.help_flag = context_settings["help_option_names"][0]
        super(DefaultHelp, self).__init__(*args, **kwargs)

    def parse_args(self, ctx, args):
        if not args:
            args = [self.help_flag]
        return super(DefaultHelp, self).parse_args(ctx, args)


def iscc_clean(i):
    """Remove leading scheme and dashes"""
    return i.split(":")[-1].strip().replace("-", "")


def iscc_verify(i):
    i = iscc_clean(i)
    for c in i:
        if c not in iscc.SYMBOLS:
            raise ValueError('Illegal character "{}" in ISCC Code'.format(c))
    for component_code in iscc_split(i):
        iscc_verify_component(component_code)


def iscc_verify_component(component_code):

    if not len(component_code) == 13:
        raise ValueError(
            "Illegal component length {} for {}".format(
                len(component_code), component_code
            )
        )

    header_code = component_code[:2]
    if header_code not in ISCC_COMPONENT_CODES.keys():
        raise ValueError("Illegal component header {}".format(header_code))


def iscc_split(i):
    return textwrap.wrap(iscc_clean(i), 13)
