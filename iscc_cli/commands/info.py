# -*- coding: utf-8 -*-
import click
import iscc
import iscc_cli
import requests
from iscc.bin import ffmpeg_version_info, ffprobe_version_info
from iscc.audio import fpcalc_version_info
from iscc.mediatype import SUPPORTED_EXTENSIONS


def tika_version():
    from tika import tika
    url = tika.ServerEndpoint + "/version"
    try:
        return requests.get(url).text
    except Exception:
        return 'WARNING: Not Installed - run "iscc init" to install!'


@click.command()
def info():
    """Show information about environment."""
    from tika import tika
    click.echo("ISCC Cli Version: %s" % iscc_cli.__version__)
    click.echo("ISCC Version: %s" % iscc.__version__)
    click.echo("FFMPEG Version: %s" % ffmpeg_version_info())
    click.echo("FFPROBE Version: %s" % ffprobe_version_info())
    click.echo("FPCALC Version: %s" % fpcalc_version_info())
    click.echo("Tika Version: %s" % tika_version())
    click.echo("Tika Jar Path: %s" % tika.TikaJarPath)
    click.echo("Supported File Types: %s" % ", ".join(sorted(SUPPORTED_EXTENSIONS)))


if __name__ == "__main__":
    info()
