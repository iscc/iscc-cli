# -*- coding: utf-8 -*-
import os
import shutil
from io import BytesIO
import click
import iscc
import mobi
import requests
from iscc_cli.tika import parser
import iscc_cli
from iscc_cli import fpcalc, audio_id, video_id
from iscc_cli.const import SUPPORTED_MIME_TYPES, GMT
from iscc_cli.utils import (
    get_title,
    mime_to_gmt,
    DefaultHelp,
    download_file,
)
from iscc_cli.mediatype import mime_guess, mime_clean

HEADERS = {"User-Agent": "ISCC {}".format(iscc_cli.__version__)}


@click.command(cls=DefaultHelp)
@click.argument("url", type=click.STRING)
@click.option(
    "-g",
    "--guess",
    is_flag=True,
    default=False,
    help="Guess title (first line of text).",
)
@click.option("-t", "--title", type=click.STRING, help="Title for Meta-ID creation.")
@click.option(
    "-e", "--extra", type=click.STRING, help="Extra text for Meta-ID creation."
)
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
def web(url, guess, title, extra, verbose):
    """Generate ISCC Code from URL."""

    extra = extra or ""

    try:
        resp = requests.get(url, headers=HEADERS, stream=True)
    except Exception as e:
        raise click.BadArgumentUsage(e)

    data = BytesIO(resp.content)
    media_type = mime_clean(mime_guess(data))
    if media_type not in SUPPORTED_MIME_TYPES:
        click.echo("Unsupported media type {}".format(media_type))
        click.echo("Please request support at https://github.com/iscc/iscc-cli/issues")
        return

    if media_type == "application/x-mobipocket-ebook":
        data.seek(0)
        tempdir, filepath = mobi.extract(data)
        tika_result = parser.from_file(filepath)
        shutil.rmtree(tempdir)
    else:
        data.seek(0)
        tika_result = parser.from_buffer(data)

    if not title:
        title = get_title(tika_result, guess=guess, uri=url)

    mid, norm_title, _ = iscc.meta_id(title, extra)
    gmt = mime_to_gmt(media_type)
    if gmt == GMT.IMAGE:
        data.seek(0)
        cid = iscc.content_id_image(data)
    elif gmt == GMT.TEXT:
        text = tika_result["content"]
        if not text:
            click.echo("Could not extract text")
            return
        cid = iscc.content_id_text(tika_result["content"])
    elif gmt == GMT.AUDIO:
        if not fpcalc.is_installed():
            fpcalc.install()
        data.seek(0)
        features = audio_id.get_chroma_vector(data)
        cid = audio_id.content_id_audio(features)
    elif gmt == GMT.VIDEO:
        local_path = download_file(url, sanitize=True)
        features = video_id.get_frame_vectors(local_path)
        cid = video_id.content_id_video(features)
        os.remove(local_path)

    data.seek(0)
    did = iscc.data_id(data)
    data.seek(0)
    iid, tophash = iscc.instance_id(data)

    if not norm_title:
        iscc_code = "-".join((cid, did, iid))
    else:
        iscc_code = "-".join((mid, cid, did, iid))

    click.echo("ISCC:{}".format(iscc_code))

    if verbose:
        if norm_title:
            click.echo("Norm Title: %s" % norm_title)
        click.echo("Tophash:    %s" % tophash)
        click.echo("Filepath:   %s" % url)
        click.echo("GMT:        %s" % gmt)

    return dict(iscc=iscc_code, norm_title=norm_title, tophash=tophash, gmt=gmt)
