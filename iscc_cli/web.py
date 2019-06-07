# -*- coding: utf-8 -*-
from io import BytesIO
import click
import iscc
import requests
from tika import parser

import iscc_cli
from iscc_cli import fpcalc, audio_id
from iscc_cli.const import SUPPORTED_MIME_TYPES, GMT
from iscc_cli.utils import get_title, mime_to_gmt, DefaultHelp


HEADERS = {"User-Agent": "ISCC {}".format(iscc_cli.__version__)}


@click.command(cls=DefaultHelp)
@click.argument("url")
@click.option(
    "-g",
    "--guess",
    is_flag=True,
    default=False,
    help="Guess title (first line of text).",
)
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
def web(url, guess, verbose):

    resp = requests.get(url, headers=HEADERS, stream=True)
    media_type = resp.headers.get("Content-Type", "").split(";")[0]
    if media_type not in SUPPORTED_MIME_TYPES:
        click.echo("Unsupported media type {}".format(media_type))
        return

    data = BytesIO(resp.content)
    tika_result = parser.from_buffer(data)
    title = get_title(tika_result, guess=guess)
    mid, norm_title, _ = iscc.meta_id(title)
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
    data.seek(0)
    did = iscc.data_id(data)
    data.seek(0)
    iid, tophash = iscc.instance_id(data)

    if not norm_title:
        click.echo("ISCC:{cid}-{did}-{iid}".format(cid=cid, did=did, iid=iid))
    else:
        click.echo(
            "ISCC:{mid}-{cid}-{did}-{iid}".format(mid=mid, cid=cid, did=did, iid=iid)
        )

    if verbose:
        if norm_title:
            click.echo("Norm Title: %s" % norm_title)
        click.echo("Tophash:    %s" % tophash)
        click.echo("Filepath:   %s" % url)
        click.echo("GMT:        %s" % gmt)
