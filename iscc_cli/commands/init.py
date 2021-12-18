# -*- coding: utf-8 -*-
import sys
import click
import iscc.bin


@click.command()
def init():
    """Inititalize and check environment."""
    from loguru import logger as log
    log.add(sys.stdout)
    iscc.bin.install()
    click.echo("Enviroment initialized")
