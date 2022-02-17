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
    result = r.invoke(cli, ["gen", "tests/image/demo.jpg"])
    assert result.exit_code == 0
    assert "KED6D635YTR5XNF6YNBTBHR4T2HGP3HKVFO7TYUP2BKVFG724W63HVI" in result.output


def test_gen_empty_file():
    result = r.invoke(cli, ["gen", "tests/batch/empty.txt"])
    assert result.exit_code == 2
    assert "empty file" in result.output


def test_gen_single_demo():
    result = r.invoke(cli, ["gen", "tests/text/demo.doc"])
    assert result.exit_code == 0
    assert "KADV5PDFXBL7HGBXFFU64KVNP6UGTUZC2CJTDBKMFYTTZPLQQVX22FI" in result.output


def test_gen_image_bmp():
    result = r.invoke(cli, ["gen", "tests/image/demo.bmp"])
    assert result.exit_code == 0


def test_gen_image_png():
    result = r.invoke(cli, ["gen", "tests/image/demo.png"])
    assert "KED6P2X7C73P72Z4YNBTBHR4T2HGO6RDNMJX4P6UMT7LQXYXBH2R5PY" in result.output
