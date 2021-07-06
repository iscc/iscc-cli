# -*- coding: utf-8 -*-
from typing import Union, List
import hashlib
import io
import os
import re
import textwrap
from os import getcwd, listdir, walk
from os.path import isfile, splitext, isdir, join, basename
from urllib.parse import urlparse
import click
import iscc
import requests
from PIL import Image
import iscc_cli
from iscc_cli.const import (
    SUPPORTED_EXTENSIONS,
    SUPPORTED_MIME_TYPES,
    ISCC_COMPONENT_CODES,
    GMT,
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


def clean_mime(mime: Union[str, List]):
    """Returns first entry in mime and removes semicolon separated charset info"""
    if mime and isinstance(mime, List):
        mime = mime[0]
    if mime:
        mime = mime.split(";")[0]
    return mime.strip()


def mime_to_gmt(mime_type, file_path=None):
    mime_type = clean_mime(mime_type)
    if mime_type == "image/gif" and file_path:
        img = Image.open(file_path)
        if img.is_animated:
            return GMT.VIDEO
        else:
            return GMT.IMAGE
    entry = SUPPORTED_MIME_TYPES.get(mime_type)
    if entry:
        return entry["gmt"]
    gmt = mime_type.split("/")[0]
    if gmt in (GMT.TEXT, GMT.IMAGE, GMT.AUDIO, GMT.VIDEO):
        click.echo(
            "WARNING: Attempting to process unsupported media type %s" % mime_type
        )
        return gmt


def get_title(tika_result: dict, guess=False, uri=None):
    title = ""
    gmt = None
    meta = tika_result.get("metadata")

    if meta:
        mime_type = clean_mime(meta.get("Content-Type"))
        gmt = mime_to_gmt(mime_type)
        title = meta.get("dc:title", "")
        title = title[0].strip() if isinstance(title, list) else title.strip()
        if not title:
            title = meta.get("title", "")
            title = title[0].strip() if isinstance(title, list) else title.strip()

    # See if string would survive normalization
    norm_title = iscc.text_normalize(title, keep_ws=True)

    if not norm_title and guess and gmt == GMT.TEXT:
        content = tika_result.get("content", "")
        if content is not None:
            first_line = content.strip().splitlines()[0]
            title = iscc.text_trim(iscc.text_normalize(first_line, keep_ws=True))

    if not title and uri is not None:
        result = urlparse(uri)
        base = basename(result.path)
        title = splitext(base)[0]
        title = title.replace("-", " ")
        title = title.replace("_", " ")
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


def download_file(url, md5=None, sanitize=False):
    """Download file to app dir and return path."""
    url_obj = urlparse(url)
    file_name = os.path.basename(url_obj.path) or "temp.file"
    if sanitize:
        file_name = safe_filename(file_name)
    out_path = os.path.join(iscc_cli.APP_DIR, file_name)
    if os.path.exists(out_path):
        click.echo("Already downloaded: %s" % file_name)
        if md5:
            md5_calc = hashlib.md5(open(out_path, "rb").read()).hexdigest()
            assert md5 == md5_calc
        return out_path
    r = requests.get(url, stream=True)
    length = int(r.headers["content-length"])
    chunk_size = 512
    iter_size = 0
    with io.open(out_path, "wb") as fd:
        with click.progressbar(
            length=length, label="Downloading %s" % file_name
        ) as bar:
            for chunk in r.iter_content(chunk_size):
                fd.write(chunk)
                iter_size += chunk_size
                bar.update(chunk_size)
    if md5:
        md5_calc = hashlib.md5(open(out_path, "rb").read()).hexdigest()
        assert md5 == md5_calc
    return out_path


class cd:
    """Context manager for changing the current working directory"""

    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def safe_filename(s: str, max_len: int = 255) -> str:
    """Sanitize a string making it safe to use as a filename.
    See: https://en.wikipedia.org/wiki/Filename.
    """
    ntfs_chars = [chr(i) for i in range(0, 31)]
    chars = [
        r'"',
        r"\#",
        r"\$",
        r"\%",
        r"'",
        r"\*",
        r"\,",
        r"\.",
        r"\/",
        r"\:",
        r'"',
        r"\;",
        r"\<",
        r"\>",
        r"\?",
        r"\\",
        r"\^",
        r"\|",
        r"\~",
        r"\\\\",
    ]
    pattern = "|".join(ntfs_chars + chars)
    regex = re.compile(pattern, re.UNICODE)
    fname = regex.sub("", s)
    return fname[:max_len].rsplit(" ", 0)[0]
