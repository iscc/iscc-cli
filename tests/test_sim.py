# -*- coding: utf-8 -*-
import os
from tests import ROOT_DIR
from iscc_cli import sim
from iscc_cli.cli import cli
from click.testing import CliRunner
import iscc.const

os.chdir(ROOT_DIR)
r = CliRunner()


def test_sim_no_args():
    result = r.invoke(cli, ["sim"])
    assert result.exit_code == 0
    assert "$ iscc sim" in result.output
