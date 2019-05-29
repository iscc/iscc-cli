# -*- coding: utf-8 -*-
import os
from iscc_cli import utils


TEST_DIR = os.path.dirname(os.path.realpath(__file__))


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
