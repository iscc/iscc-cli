import os
from tests import ROOT_DIR
from iscc_cli.cli import cli
from click.testing import CliRunner


os.chdir(ROOT_DIR)
r = CliRunner()


def test_init():
    result = r.invoke(cli, ["init"])
    assert result.exit_code == 0
    assert "Apache Tika 1.22" in result.output
