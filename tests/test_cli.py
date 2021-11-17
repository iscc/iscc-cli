import json
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
    result = r.invoke(cli, ["-p"])
    assert result.exit_code == 2
    assert "Error: Missing" in result.output


def test_version():
    result = r.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "ISCC" in result.output
    assert __version__ in result.output


def test_no_command_with_valid_file():
    result = r.invoke(cli, ["tests/image/demo.jpg"])
    assert result.exit_code == 0
    assert "KED6D635YTR5XNF6YNBTBHR4T2HGP3HKVFO7TYUP2BKVFG724W63HVI" in result.output
    assert "7a8d0c513142c45f" not in result.output


def test_no_command_with_valid_file_granular():
    result = r.invoke(cli, ["--granular", "tests/image/demo.jpg"])
    assert result.exit_code == 0
    assert "features" in json.loads(result.output)


def test_no_command_with_valid_file_preview():
    result = r.invoke(cli, ["--preview", "tests/image/demo.jpg"])
    assert result.exit_code == 0
    assert "preview" in json.loads(result.output)
