# -*- coding: utf-8 -*-
import io
import click
from tika import detector
import requests


@click.command()
def init():
    """Inititalize and check Tika server."""
    click.echo("Inititalizing Tika ...")
    detector.from_buffer(io.BytesIO(b"Wakeup Tika"))
    url = detector.ServerEndpoint + "/version"
    resp = requests.get(url)
    click.echo("Tika initialized: {}".format(resp.text))
