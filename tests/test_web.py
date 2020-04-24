# -*- coding: utf-8 -*-
import os
from tests import ROOT_DIR
from iscc_cli.cli import cli
from click.testing import CliRunner


os.chdir(ROOT_DIR)
r = CliRunner()


def test_iscc_web_no_args():
    result = r.invoke(cli)
    assert result.exit_code == 0
    assert result.output.startswith("Usage")


def test_iscc_web_image():
    result = r.invoke(
        cli, ["web", "https://iscc.foundation/news/images/lib-arch-ottawa.jpg"]
    )
    assert result.exit_code == 0
    assert "CCbUCUSqQpyJo-CYaHPGcucqwe3-CDt4nQptEGP6M-CRestDoG7xZFy" in result.output


def test_iscc_web_video():
    result = r.invoke(cli, ["web", "https://craft.de/iscc-grinder.mp4"])
    assert result.exit_code == 0
    assert "CV2TgqeKWE7K8-CDKaC252w9QKN-CRYKUhn2RpzF4" in result.output


def test_iscc_web_invalid_url():
    result = r.invoke(cli, ["web", "heise.de"])
    assert result.exit_code == 2
    assert "Error: Invalid URL" in result.output


def test_iscc_web_python_call():
    from iscc_cli.commands.web import web

    url = "https://iscc.foundation/news/images/lib-arch-ottawa.jpg"
    result = web.callback(url=url, guess=False, title="", extra="", verbose=False)
    assert "CCbUCUSqQpyJo-CYaHPGcucqwe3-CDt4nQptEGP6M-CRestDoG7xZFy" in result["iscc"]
    assert result["norm_title"] == "library and archives canada ottawa"
