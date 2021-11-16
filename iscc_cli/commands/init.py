# -*- coding: utf-8 -*-
import click
import iscc


@click.command()
def init():
    """Inititalize and check environment."""
    iscc.bin.ffmpeg_install()
    iscc.bin.ffprobe_install()
    iscc.audio.fpcalc_install()
