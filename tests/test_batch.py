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
    assert "CCKzUpp6U5hU7,CTMjk4o5H96BV,CDM6E14HcCZjQ,CR1LUvGDVrWye" in result.output


def test_batch_recursive():
    result = r.invoke(cli, ["batch", "-r", "./tests/batch"])
    assert result.exit_code == 0
    assert "CCKzUpp6U5hU7,CTMjk4o5H96BV,CDM6E14HcCZjQ,CR1LUvGDVrWye" in result.output


def test_batch_python_call():
    from iscc_cli.commands.batch import batch

    result = batch.callback("./tests/batch/subdir", False, False, False)
    assert isinstance(result, list)
    assert len(result) == 1
