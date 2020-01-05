import json
import os
from tests import ROOT_DIR
from iscc_cli.cli import cli
from click.testing import CliRunner


os.chdir(ROOT_DIR)
r = CliRunner()


def test_dump_no_arg_shows_help():
    result = r.invoke(cli, ["dump"])
    assert result.exit_code == 0
    assert "dump [OPTIONS] FILE" in result.output


def test_dump_with_doc():
    result = r.invoke(cli, ["dump", "tests/text/demo.doc"])
    assert result.exit_code == 0
    assert '"status": 200' in result.output


def test_dump_strip():
    result = r.invoke(cli, ["dump", "-s", 50, "tests/text/demo.doc"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert len(data.get("content", "")) == 50


def test_dump_meta_only():
    result = r.invoke(cli, ["dump", "-m", "tests/text/demo.doc"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert "content" not in data


def test_dump_usage_error():
    result = r.invoke(cli, ["dump", "-m", "-c", "tests/text/demo.doc"])
    assert result.exit_code == 2
    assert "Use either" in result.output
