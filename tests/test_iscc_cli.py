from iscc_cli import __version__
from iscc_cli.main import cli
from click.testing import CliRunner


r = CliRunner()


def test_iscc_no_args():
    result = r.invoke(cli)
    assert result.exit_code == 0
    assert result.output.startswith("Usage")


def test_version():
    result = r.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert result.output.startswith("ISCC")
    assert __version__ in result.output


def test_gen_image():
    result = r.invoke(cli, ["gen", "-r", "."])
    assert result.output.startswith("ISCC:CYDfTq7Qc7Fre-CDC7Lg4oHA8DC-CRLdd9g4BSUyY")
