# -*- coding: utf-8 -*-
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
    result = r.invoke(cli, ["sim", "CCKzPWegaT3hS", "CCcdAr6GDoF3p"])
    assert result.exit_code == 0
    assert "Estimated Similarity of Meta-ID" in result.output


def test_sim_incompatible_components():
    result = r.invoke(cli, ["sim", "CCKzPWegaT3hS", "CDM6E14HcCZjQ"])
    assert result.exit_code == 0
    assert "Incompatible component types" in result.output


def test_sim_full_iscc():
    result = r.invoke(
        cli,
        [
            "sim",
            "ISCC:CCKzPWegaT3hS-CTMjk4o5H96BV-CDM6E14HcCZjQ-CR1LUvGDVrWye",
            "CCcdAr6GDoF3p-CTMjk4o5H96BV-CD6XL9SFyWgsW-CR28vgw3inZGw",
        ],
    )
    assert result.exit_code == 0
    assert "Estimated Total Similarity" in result.output
