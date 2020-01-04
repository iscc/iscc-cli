# -*- coding: utf-8 -*-
import os
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
    assert res[0]["iscc"] == "CTtW9UFoNJdXK-CDTp4cPJGiHfD-CRWoD5RiqBvNo"


def test_iscc_from_url():
    url = "https://iscc.foundation/news/images/lib-arch-ottawa.jpg"
    res = lib.iscc_from_url(url)
    assert isinstance(res, dict)
    assert "CCbUCUSqQpyJo-CYaHPGcucqwe3-CDt4nQptEGP6M-CRestDoG7xZFy" in res["iscc"]
