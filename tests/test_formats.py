import os
from tests import ROOT_DIR
from iscc_cli.cli import cli
from click.testing import CliRunner


os.chdir(ROOT_DIR)
r = CliRunner()


def test_xhtml():
    result = r.invoke(cli, ["gen", "tests/text/demo.xhtml"])
    assert result.exit_code == 0
