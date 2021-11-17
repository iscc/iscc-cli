import os
from tests import ROOT_DIR
from iscc_cli.cli import cli
from click.testing import CliRunner


os.chdir(ROOT_DIR)
r = CliRunner()


def test_unsupported():
    result = r.invoke(cli, ["gen", "tests/text/demo.sqlite"])
    assert result.exit_code == 1
    assert "Error: Unsupported mediatype: application/x-sqlite" in result.output


def test_xhtml():
    result = r.invoke(cli, ["gen", "tests/text/demo.xhtml"])
    assert result.exit_code == 0
    assert "KAD6P2X7C73P72Z4FFU64KVNP6UGSFNUYYO6XQJ75GYBJ7FJUMEKTMY" in result.output
