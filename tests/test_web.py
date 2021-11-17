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
    assert "KEDYT2F222OCBGQRQBD7M4HPDLUZJZAA2JO4DE76UQWNVH76MP2AK2Q" in result.output


def test_iscc_web_video():
    result = r.invoke(cli, ["web", "https://craft.de/iscc-grinder.mp4"])
    assert result.exit_code == 0
    assert "KMDZPDVSLFQXGF54AWZFNUBT5AD43O2Z4IECXHVCCOBTQ4MXONZ5BOY" in result.output


def test_iscc_web_invalid_url():
    result = r.invoke(cli, ["web", "heise.de"])
    assert result.exit_code == 2
    assert "Error: Invalid URL" in result.output
