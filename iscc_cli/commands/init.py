# -*- coding: utf-8 -*-
import click
from iscc.audio import fpcalc_install
from iscc.bin import ffmpeg_install, ffprobe_install


@click.command()
def init():
    """Inititalize and check environment."""
    ffmpeg_install()
    ffprobe_install()
    fpcalc_install()
    click.echo("Enviroment initialized")
