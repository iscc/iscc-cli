# -*- coding: utf-8 -*-
import click
import iscc
import iscc_cli
from iscc_cli import fpcalc, ffmpeg
from iscc_cli.const import SUPPORTED_EXTENSIONS
from tika import tika


@click.command()
def info():
    """Show information about environment."""
    click.echo("ISCC Cli Version: %s" % iscc_cli.__version__)
    click.echo("ISCC Version: %s" % iscc.__version__)
    click.echo("FFMPEG Version: %s" % ffmpeg.get_version_info())
    click.echo("FPCALC Version: %s" % fpcalc.get_version_info())
    click.echo("Tika Version: %s" % tika.TikaVersion)
    click.echo("Tika Jar Path: %s" % tika.TikaJarPath)
    click.echo("Supported File Types: %s" % ", ".join(sorted(SUPPORTED_EXTENSIONS)))


if __name__ == "__main__":
    info()
