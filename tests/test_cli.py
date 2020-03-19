import os
from tests import ROOT_DIR
from iscc_cli import __version__
from iscc_cli.cli import cli
from click.testing import CliRunner


os.chdir(ROOT_DIR)
r = CliRunner()


def test_iscc_no_args():
    result = r.invoke(cli)
    assert result.exit_code == 0
    assert result.output.startswith("Usage")


def test_iscc_no_ars_but_opt():
    result = r.invoke(cli, ["-v"])
    assert result.exit_code == 2
    assert 'Error: Missing argument' in result.output


def test_version():
    result = r.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "ISCC" in result.output
    assert __version__ in result.output


def test_no_command_with_valid_file():
    result = r.invoke(cli, ["tests/image/demo.jpg"])
    assert result.exit_code == 0
    assert "CC1GG3hSxtbWU-CYDfTq7Qc7Fre-CDYkLqqmQJaQk-CRAPu5NwQgAhv" in result.output
    assert "7a8d0c513142c45f" not in result.output


def test_no_command_with_valid_file_verbose():
    result = r.invoke(cli, ["-v", "tests/image/demo.jpg"])
    assert result.exit_code == 0
    assert "7a8d0c513142c45f" in result.output
