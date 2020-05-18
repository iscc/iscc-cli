# -*- coding: utf-8 -*-
import io
import click
import requests
from iscc_cli.tika import detector
from iscc_cli import fpcalc


@click.command()
def init():
    """Inititalize and check environment."""
    click.echo("Inititalizing Tika ...")
    detector.from_buffer(io.BytesIO(b"Wakeup Tika"))
    url = detector.ServerEndpoint + "/version"
    resp = requests.get(url)
    click.echo("Tika initialized: {}".format(resp.text))
    click.echo("Testing fpcalc ...")
    fpc_ok = fpcalc.is_installed()
    if not fpc_ok:
        fpcalc.install()
    fpc_version = fpcalc.get_version_info()
    click.echo("fpcalc installed: {}".format(fpc_version))
