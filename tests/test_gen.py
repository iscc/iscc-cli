import os
from tests import ROOT_DIR
from iscc_cli.cli import cli
from click.testing import CliRunner


os.chdir(ROOT_DIR)
r = CliRunner()


def test_gen_no_arg_shows_help():
    result = r.invoke(cli, ["gen"])
    assert result.exit_code == 0
    assert "-t, --title TEXT" in result.output


def test_gen_single_file():
    result = r.invoke(cli, ["gen", "tests/demo.jpg"])
    assert result.exit_code == 0
    assert "ISCC:CCTcjug7rM3Da" in result.output
