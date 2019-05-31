# -*- coding: utf-8 -*-
import io
from os.path import basename

import requests
import click
import iscc
from tika import detector, parser, tika
from iscc_cli import __version__
from iscc_cli.const import SUPPORTED_MIME_TYPES, GMT
from iscc_cli.utils import get_title, mime_to_gmt, get_files
from click_default_group import DefaultGroup


@click.group(cls=DefaultGroup, default="gen", default_if_no_args=False)
@click.version_option(version=__version__, message="ISCC CLI - %(version)s")
def cli():
    pass


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


@click.command()
def init():
    """Inititalize and check Tika server."""
    click.echo("Inititalizing Tika ...")
    detector.from_buffer(io.BytesIO(b"Wakeup Tika"))
    url = detector.ServerEndpoint + "/version"
    resp = requests.get(url)
    click.echo("Tika initialized: {}".format(resp.text))


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("-r", "--recursive", is_flag=True, help="Recurse into subdirectories.")
def batch(path, recursive):
    """Batch create ISCC Codes.

    Generates ISCC Codes for all media files in <PATH>.
    """
    for f in get_files(path, recursive=recursive):
        media_type = detector.from_file(f)
        if media_type not in SUPPORTED_MIME_TYPES:
            fname = basename(f)
            click.echo(
                "Unsupported file {} with mime type: {}".format(fname, media_type)
            )
            continue

        gmt = mime_to_gmt(media_type)
        tika_result = parser.from_file(f)
        title = get_title(tika_result)
        mid, norm_title, norm_extra = iscc.meta_id(title)

        if gmt == GMT.IMAGE:
            cid = iscc.content_id_image(f)
        elif gmt == GMT.TEXT:
            text = tika_result["content"]
            if not text:
                click.echo("Could not extract text from {}".format(basename(f)))
                continue
            cid = iscc.content_id_text(tika_result["content"])

        did = iscc.data_id(f)
        iid, _ = iscc.instance_id(f)
        click.echo(
            "ISCC:{mid}-{cid}-{did}-{iid},{fname},{title}".format(
                mid=mid, cid=cid, did=did, iid=iid, fname=basename(f), title=norm_title
            )
        )


cli.add_command(init)
cli.add_command(gen)
cli.add_command(batch)

if __name__ == "__main__":
    cli()
