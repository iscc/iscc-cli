# -*- coding: utf-8 -*-
import json
import os
from tests import ROOT_DIR
from iscc_cli.cli import cli
from click.testing import CliRunner

os.chdir(ROOT_DIR)
r = CliRunner()


def test_sim_no_args():
    result = r.invoke(cli, ["sim"])
    assert result.exit_code == 0
    assert "$ iscc sim" in result.output


def test_sim_components():
    result = r.invoke(cli, ["sim", "EEA4GQZQTY6J5DTH", "EEA4GZZQTY6J5DTH"])
    assert result.exit_code == 0
    assert json.loads(result.output) == {"cdist": 2}


def test_sim_incompatible_components():
    result = r.invoke(cli, ["sim", "AAA6D635YTR5XNF6", "EEA4GQZQTY6J5DTH"])
    assert result.exit_code == 0
    assert json.loads(result.output) == {}


def test_sim_full_iscc():
    result = r.invoke(
        cli,
        [
            "sim",
            "ISCC:KED6D635YTR5XNF6YNBTBHR4T2HGOLRHH2UOB2NTWEPWQTLPT75L7MI",
            "KED6D635YTR5XNF6YNBTBHR4T2HGP7CIREBNRDTS2PM4AJ6IQHO3L4A",
        ],
    )
    assert result.exit_code == 0
    assert json.loads(result.output) == {
        "cdist": 0,
        "ddist": 34,
        "imatch": False,
        "mdist": 0,
    }
