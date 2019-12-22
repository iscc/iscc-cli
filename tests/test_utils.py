# -*- coding: utf-8 -*-
import pytest

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
    assert len(list(result)) == 17
    result = utils.get_files(TEST_DIR, recursive=True)
    assert len(list(result)) == 19


def test_mime_to_gmt():
    result = utils.mime_to_gmt("image/jpeg")
    assert result == GMT.IMAGE


def test_iscc_clean():
    assert utils.iscc_clean("ISCC: SOME-CODE") == "SOMECODE"
    assert utils.iscc_clean(" SOMECODE ") == "SOMECODE"
    assert utils.iscc_clean("ISCC:") == ""


def test_iscc_verify():
    with pytest.raises(ValueError):
        utils.iscc_verify("I")


def test_iscc_split():
    i = "ISCC:CCcdAr6GDoF3p-CTMjk4o5H96BV-CD6XL9SFyWgsW-CR28vgw3inZGw"
    assert utils.iscc_split(i) == [
        "CCcdAr6GDoF3p",
        "CTMjk4o5H96BV",
        "CD6XL9SFyWgsW",
        "CR28vgw3inZGw",
    ]

    i = "ISCC:CCcdAr6GDoF3p"
    assert utils.iscc_split(i) == ["CCcdAr6GDoF3p"]

    i = "CCcdAr6GDoF3p"
    assert utils.iscc_split(i) == ["CCcdAr6GDoF3p"]
