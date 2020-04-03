# -*- coding: utf-8 -*-
import os
import iscc
from tests import ROOT_DIR
from iscc_cli import lib


os.chdir(ROOT_DIR)


def test_iscc_from_file():
    res = lib.iscc_from_file("./tests/image/demo.jpg")
    assert isinstance(res, dict)
    assert res["iscc"] == "CC1GG3hSxtbWU-CYDfTq7Qc7Fre-CDYkLqqmQJaQk-CRAPu5NwQgAhv"


def test_iscc_from_dir():
    res = lib.isccs_from_dir("./tests/batch/subdir")
    assert isinstance(res, list)
    assert res[0]["iscc"] == "CCh7QKroUdKnH-CYDfTq7Qc7Fre-CDij3vGU1BkCZ-CRNssh4Qc1x5B"


def test_iscc_from_url():
    url = "https://iscc.foundation/news/images/lib-arch-ottawa.jpg"
    res = lib.iscc_from_url(url)
    assert isinstance(res, dict)
    assert "CCbUCUSqQpyJo-CYaHPGcucqwe3-CDt4nQptEGP6M-CRestDoG7xZFy" in res["iscc"]


def test_iscc_from_url_no_meta():
    url = "https://github.com/iscc/iscc-cli/raw/master/tests/image/demo.png"
    res = lib.iscc_from_url(url)
    assert isinstance(res, dict)
    assert "CYDfTq7Qc7Fre-CDij3vGU1BkCZ-CRNssh4Qc1x5B" in res["iscc"]
    meta_id, _, _ = iscc.meta_id("demo")
    assert meta_id in res["iscc"]
