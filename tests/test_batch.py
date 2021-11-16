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
    assert "KADV5PDFXBL7HGBXFFW64" in result.output


def test_batch_recursive():
    result = r.invoke(cli, ["batch", "-r", "./tests/batch"])
    assert result.exit_code == 0
    assert "KADV5PDFXBL7HGBXFFW64" in result.output
