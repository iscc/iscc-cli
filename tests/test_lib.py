# -*- coding: utf-8 -*-
import os
from tests import ROOT_DIR
from iscc_cli import lib


os.chdir(ROOT_DIR)


def test_iscc_from_file():
    res = lib.iscc_from_file("./tests/demo.jpg")
    assert isinstance(res, dict)
    assert res["iscc"] == "CCTcjug7rM3Da-CYDfTq7Qc7Fre-CDYkLqqmQJaQk-CRAPu5NwQgAhv"


def test_iscc_from_dir():
    res = lib.isccs_from_dir("./tests/subdir")
    assert isinstance(res, list)
    assert res[0]["iscc"] == "CYDfTq7Qc7Fre-CDij3vGU1BkCZ-CRNssh4Qc1x5B"


def test_iscc_from_url():
    url = "https://iscc.foundation/news/images/lib-arch-ottawa.jpg"
    res = lib.iscc_from_url(url)
    assert isinstance(res, dict)
    assert "CCbU23e7E8LAR" in res["iscc"]
