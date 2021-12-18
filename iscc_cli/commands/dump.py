# -*- coding: utf-8 -*-
import shutil
from dataclasses import asdict

import click
import mobi
from PIL import Image
from click import UsageError
from iscc.mp7 import read_ffmpeg_signature
from iscc.schema import GMT

from iscc_cli.utils import DefaultHelp
import json
import iscc


@click.command(cls=DefaultHelp)
@click.argument("path", type=click.STRING)
@click.option(
    "-s", "--strip", type=click.INT, default=0, help="Strip content to first X elements."
)
@click.option("-m", "--meta", is_flag=True, default=False, help="Dump metadata only.")
@click.option("-c", "--content", is_flag=True, default=False, help="Dump content only.")
def dump(path, strip, meta, content):
    """Dump tika extraction results for PATH (file or url path)."""

    media_type = iscc.mediatype.mime_clean(iscc.mediatype.mime_guess(path))
    gmt = iscc.mediatype.mime_to_gmt(media_type)

    if media_type not in iscc.mediatype.SUPPORTED_MEDIATYPES:
        click.echo("Unsupported media type {}.".format(media_type))
        click.echo("Please request support at https://github.com/iscc/iscc-cli/issues")

    if media_type == "application/x-mobipocket-ebook":
        tempdir, epub_filepath = mobi.extract(path)
        extract = iscc.text.extract_text(epub_filepath)
        metadata = iscc.text.extract_text_metadata(epub_filepath, extract)
        shutil.rmtree(tempdir)
    else:
        if gmt == GMT.text:
            extract = iscc.text.extract_text(path)
            metadata = iscc.text.extract_text_metadata(path, extract)
        elif gmt == GMT.image:
            imo = Image.open(path)
            extract = list(iscc.image.normalize_image(imo))
            metadata = iscc.image.extract_image_metadata(path)
        elif gmt == GMT.audio:
            extract = iscc.audio.extract_audio_features(path)
            metadata = iscc.audio.extract_audio_metadata(path)
        elif gmt == GMT.video:
            extract = read_ffmpeg_signature(iscc.video.extract_video_signature(path))
            extract = [list(f.vector.tolist()) for f in extract]
            metadata = iscc.video.extract_video_metadata(path)
        else:
            click.echo("Unsupported media type {}.".format(media_type))
            raise click.Abort

    if all([meta, content]):
        raise UsageError("Use either --meta or --content for selective output.")

    if strip:
        extract = extract[:strip]

    if meta:
        click.echo(json.dumps(metadata, indent=2))
    elif content:
        click.echo(json.dumps(extract))
    else:
        click.echo(json.dumps(metadata, indent=2))
        click.echo(json.dumps(extract))
