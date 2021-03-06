import os
from tests import ROOT_DIR
from iscc_cli.cli import cli
from click.testing import CliRunner


os.chdir(ROOT_DIR)
r = CliRunner()


def test_unsupported():
    result = r.invoke(cli, ["gen", "tests/text/demo.sqlite"])
    assert result.exit_code == 0
    assert "Unsupported media type" in result.output


def test_xhtml():
    result = r.invoke(cli, ["gen", "tests/text/demo.xhtml"])
    assert result.exit_code == 0
    assert "CTMjk4o5H96BV" in result.output
