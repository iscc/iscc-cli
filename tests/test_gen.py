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


def test_gen_single_guess():
    result = r.invoke(cli, ["gen", "tests/demo.txt"])
    assert result.exit_code == 0
    assert "ISCC:CTMjk4o5H96BV-CDcDwBFVJ54fe-CR7LRzaAJGwqX" in result.output
    result = r.invoke(cli, ["gen", "-g", "tests/demo.txt"])
    assert result.exit_code == 0
    assert (
        "ISCC:CCcdAr6GDoF3p-CTMjk4o5H96BV-CDcDwBFVJ54fe-CR7LRzaAJGwqX" in result.output
    )


def test_gen_python_call():
    from iscc_cli.gen import gen

    file = open("tests/demo.txt")
    result = gen.callback(file, True, "", "", True)
    assert result["iscc"] == "CCcdAr6GDoF3p-CTMjk4o5H96BV-CDcDwBFVJ54fe-CR7LRzaAJGwqX"
    assert result["norm_title"] == "iscc test document"
