# -*- coding: utf-8 -*-
"""Tests that should pass before external tools and dependencies are installed."""
import os
from tests import ROOT_DIR
from iscc_cli.cli import cli
from click.testing import CliRunner

os.chdir(ROOT_DIR)
r = CliRunner()


def test_info():
    result = r.invoke(cli, ["info"])
    assert result.exit_code == 0
    assert "Supported File Types" in result.output
