# -*- coding: utf-8 -*-
from os.path import join

from iscc_cli.const import GMT
from tests import TEST_DIR
from iscc_cli import utils


def test_iter_files_default():
    result = utils.iter_files(TEST_DIR)
    assert len(list(result)) >= 3


def test_iter_files_empty():
    result = utils.iter_files(TEST_DIR, exts=("nofile",))
    assert len(list(result)) == 0


def test_iter_files_filter():
    result = utils.iter_files(TEST_DIR, exts=("jpg",))
    assert list(result)[0].endswith("demo.jpg")


def test_iter_files_recursive():
    result = utils.iter_files(TEST_DIR, exts=("png",), recursive=False)
    assert len(list(result)) == 0
    result = utils.iter_files(TEST_DIR, exts=("png",), recursive=True)
    assert list(result)[0].endswith("demo.png")


def test_get_files():
    result = utils.get_files(TEST_DIR)
    assert len(list(result)) == 3
    result = utils.get_files(TEST_DIR, recursive=True)
    assert len(list(result)) == 4


def test_get_gmt():
    result = utils.get_gmt(join(TEST_DIR, "demo.jpg"))
    assert result == GMT.IMAGE
