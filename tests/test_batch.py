# -*- coding: utf-8 -*-
import os
from tests import ROOT_DIR
from iscc_cli.cli import cli
from click.testing import CliRunner


os.chdir(ROOT_DIR)
r = CliRunner()


def test_batch():
    result = r.invoke(cli, ["batch", "./tests"])
    assert result.exit_code == 0
    assert "ISCC:CCL9Aeao56G1R" in result.output


def test_batch_recursive():
    result = r.invoke(cli, ["batch", "-r", "./"])
    assert result.exit_code == 0
    assert "ISCC:CCL9Aeao56G1R" in result.output


if __name__ == "__main__":
    main()
