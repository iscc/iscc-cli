# -*- coding: utf-8 -*-
import os
from tests import ROOT_DIR
from iscc_cli.cli import cli
from click.testing import CliRunner


os.chdir(ROOT_DIR)
r = CliRunner()


def test_batch():
    result = r.invoke(cli, ["batch", "./tests/batch"])
    assert result.exit_code == 0
    assert "KADV5PDFXBL7HGBXFFU64KVNP6UGTUZC2CJTDBKMFYTTZPLQQVX22FI" in result.output


def test_batch_recursive():
    result = r.invoke(cli, ["batch", "-r", "./tests/batch"])
    assert result.exit_code == 0
    assert "KED6D6L5YDT5DNN4YNBTBHR4T2HGO6RDNMJX4P6UMT7LQXYXBH2R5PY" in result.output
