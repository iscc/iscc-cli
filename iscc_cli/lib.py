# -*- coding: utf-8 -*-
"""Expose cli commands with standard python api."""
from typing import List, Dict
from iscc_cli.gen import gen
from iscc_cli.batch import batch
from iscc_cli.web import web
import click


def iscc_from_file(file, guess=False, title="", extra="") -> Dict:
    if isinstance(file, str):
        file = open(file)
    return gen.callback(file, guess, title, extra, False)


def isccs_from_dir(path, recursive=False, guess=False) -> List[Dict]:
    return batch.callback(path, recursive, guess)


def iscc_from_url(url, guess=False, title="", extra="") -> Dict:
    return web.callback(url, guess, title, extra, False)
