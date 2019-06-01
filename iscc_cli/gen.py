# -*- coding: utf-8 -*-
import click
import iscc
from tika import detector, parser
from iscc_cli.const import SUPPORTED_MIME_TYPES, GMT
from iscc_cli.utils import get_title, mime_to_gmt


@click.command()
@click.argument("file", type=click.File("rb"))
@click.option("-t", "--title", type=click.STRING)
@click.option("-e", "--extra", type=click.STRING, default="")
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode")
def gen(file, title, extra, verbose):
    """Generate ISCC Code for a single media file."""
    media_type = detector.from_file(file.name)
    if media_type not in SUPPORTED_MIME_TYPES:
        click.echo("Unsupported media type {}".format(media_type))
        return

    tika_result = parser.from_file(file.name)
    if not title:
        title = get_title(tika_result)

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

    did = iscc.data_id(file.name)
    iid, tophash = iscc.instance_id(file.name)

    click.echo(
        "ISCC:{mid}-{cid}-{did}-{iid}".format(mid=mid, cid=cid, did=did, iid=iid)
    )

    if verbose:
        click.echo("Norm Title: %s" % norm_title)
        click.echo("Tophash:    %s" % tophash)
        click.echo("Filepath:   %s" % file.name)
        click.echo("GMT:        %s" % gmt)
