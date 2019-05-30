import os
from tests import ROOT_DIR
from iscc_cli import __version__
from iscc_cli.main import cli
from click.testing import CliRunner


os.chdir(ROOT_DIR)
r = CliRunner()


def test_iscc_no_args():
    result = r.invoke(cli)
    assert result.exit_code == 0
    assert result.output.startswith("Usage")


def test_version():
    result = r.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "ISCC" in result.output
    assert __version__ in result.output


def test_debug():
    result = r.invoke(cli, ["debug"])
    assert result.exit_code == 0
    assert result.output.startswith("Tika TikaVersion: 1.21")


def test_gen_single_file():
    result = r.invoke(cli, ["gen", "tests/demo.jpg"])
    assert result.exit_code == 0
    assert "ISCC:CCTcjug7rM3Da" in result.output


def test_gen_directory():
    result = r.invoke(cli, ["gen", "./tests"])
    assert result.exit_code == 0
    assert "ISCC:CCL9Aeao56G1R" in result.output


def test_gen_directory_recursive():
    result = r.invoke(cli, ["gen", "-r", "./"])
    assert result.exit_code == 0
    assert "ISCC:CCL9Aeao56G1R" in result.output
