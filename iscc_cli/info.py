# -*- coding: utf-8 -*-
import click
import iscc
import iscc_cli
from tika import tika


@click.command()
def info():
    """Show information about environment."""
    click.echo(("ISCC Version: %s" % iscc.__version__))
    click.echo("ISCC Cli Version: %s" % iscc_cli.__version__)
    click.echo("Tika Version: %s" % tika.TikaVersion)
    click.echo("Tika Jar Path: %s" % tika.TikaJarPath)


if __name__ == "__main__":
    info()
