# -*- coding: utf-8 -*-
import click
import iscc
from tika import detector, parser
from iscc_cli import audio_id, fpcalc
from iscc_cli.const import SUPPORTED_MIME_TYPES, GMT
from iscc_cli.utils import get_title, mime_to_gmt, DefaultHelp


@click.command(cls=DefaultHelp)
@click.argument("file", type=click.File("rb"))
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
def gen(file, guess, title, extra, verbose):
    """Generate ISCC Code for FILE."""
    media_type = detector.from_file(file.name)
    if media_type not in SUPPORTED_MIME_TYPES:
        click.echo("Unsupported media type {}".format(media_type))
        return

    tika_result = parser.from_file(file.name)
    if not title:
        title = get_title(tika_result, guess=guess)

    if not extra:
        extra = ""

    mid, norm_title, _ = iscc.meta_id(title, extra)
    gmt = mime_to_gmt(media_type)
    if gmt == GMT.IMAGE:
        cid = iscc.content_id_image(file.name)
    elif gmt == GMT.TEXT:
        text = tika_result["content"]
        if not text:
            click.echo("Could not extract text from {}".format(file.name))
            return
        cid = iscc.content_id_text(tika_result["content"])
    elif gmt == GMT.AUDIO:
        if not fpcalc.is_installed():
            fpcalc.install()
        features = audio_id.get_chroma_vector(file.name)
        cid = audio_id.content_id_audio(features)

    did = iscc.data_id(file.name)
    iid, tophash = iscc.instance_id(file.name)

    if not norm_title:
        iscc_code = "-".join((cid, did, iid))
    else:
        iscc_code = "-".join((mid, cid, did, iid))

    click.echo("ISCC:{}".format(iscc_code))

    if verbose:
        if norm_title:
            click.echo("Norm Title: %s" % norm_title)
        click.echo("Tophash:    %s" % tophash)
        click.echo("Filepath:   %s" % file.name)
        click.echo("GMT:        %s" % gmt)

    return dict(iscc=iscc_code, norm_title=norm_title, tophash=tophash, gmt=gmt)
