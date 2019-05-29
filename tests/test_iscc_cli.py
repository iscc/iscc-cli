from iscc_cli import __version__
from iscc_cli.main import cli
import click
from click.testing import CliRunner


def test_version():
    assert __version__ == '0.1.0'


def test_iscc():
    runner = CliRunner()
    result = runner.invoke(cli)
    assert result.exit_code == 0
    assert result.output == 'Hello ISCC!\n'
