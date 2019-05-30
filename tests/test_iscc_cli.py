import os
from tests import ROOT_DIR
from iscc_cli import __version__
from iscc_cli.cli import cli
from click.testing import CliRunner


os.chdir(ROOT_DIR)
r = CliRunner()


def test_init():
    result = r.invoke(cli, ["init"])
    assert result.exit_code == 0
    assert "Apache Tika 1.21" in result.output


def test_iscc_no_args():
    result = r.invoke(cli)
    assert result.exit_code == 0
    assert result.output.startswith("Usage")


def test_version():
    result = r.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "ISCC" in result.output
    assert __version__ in result.output


def test_no_command_with_valid_file():
    result = r.invoke(cli, ["tests/demo.jpg"])
    assert result.exit_code == 0
    assert "ISCC:CCTcjug7rM3Da" in result.output
    assert "7a8d0c513142c45f" not in result.output


def test_no_command_with_valid_file_verbose():
    result = r.invoke(cli, ["-v", "tests/demo.jpg"])
    assert result.exit_code == 0
    assert "7a8d0c513142c45f" in result.output


def test_gen_single_file():
    result = r.invoke(cli, ["gen", "tests/demo.jpg"])
    assert result.exit_code == 0
    assert "ISCC:CCTcjug7rM3Da" in result.output


def test_batch():
    result = r.invoke(cli, ["batch", "./tests"])
    assert result.exit_code == 0
    assert "ISCC:CCL9Aeao56G1R" in result.output


def test_batch_recursive():
    result = r.invoke(cli, ["batch", "-r", "./"])
    assert result.exit_code == 0
    assert "ISCC:CCL9Aeao56G1R" in result.output
