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
    assert "KAD5YBQODD5TOV365LNE5MM5OM245IFU4H2JIVUSWE24XQFCJCLPUWY" in result.output


def test_batch_recursive():
    result = r.invoke(cli, ["batch", "-r", "./tests/batch"])
    assert result.exit_code == 0
    assert "KED6P2X7C73P72Z4YNBTBHR4T2HGO6RDNMJX4P6UMT7LQXYXBH2R5PY" in result.output
