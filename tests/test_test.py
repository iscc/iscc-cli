# -*- coding: utf-8 -*-
import os
from tests import ROOT_DIR
from iscc_cli.cli import cli
from click.testing import CliRunner


os.chdir(ROOT_DIR)
r = CliRunner()


# def test_test_conformance():
#     result = r.invoke(cli, ["test"])
#     assert result.exit_code == 0
#     assert "PASSED" in result.output
#     assert "FAILED" not in result.output
