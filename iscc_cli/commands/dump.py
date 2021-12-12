# -*- coding: utf-8 -*-
import shutil
import click
import mobi
from click import UsageError
from iscc_cli.utils import DefaultHelp
import json
import iscc


@click.command(cls=DefaultHelp)
@click.argument("path", type=click.STRING)
@click.option(
    "-s", "--strip", type=click.INT, default=0, help="Strip content to first X chars."
)
@click.option("-m", "--meta", is_flag=True, default=False, help="Dump metadata only.")
@click.option("-c", "--content", is_flag=True, default=False, help="Dump content only.")
def dump(path, strip, meta, content):
    """Dump Tika extraction results for PATH (file or url path)."""
    from tika import parser

    media_type = iscc.mediatype.mime_clean(iscc.mediatype.mime_guess(path))

    if media_type not in iscc.mediatype.SUPPORTED_MEDIATYPES:
        click.echo("Unsupported media type {}.".format(media_type))
        click.echo("Please request support at https://github.com/iscc/iscc-cli/issues")

    if media_type == "application/x-mobipocket-ebook":
        tempdir, epub_filepath = mobi.extract(path)
        tika_result = parser.from_file(epub_filepath)
        shutil.rmtree(tempdir)
    else:
        tika_result = parser.from_file(path)

    if all([meta, content]):
        raise UsageError("Use either --meta or --content for selective output.")

    if strip:
        tika_result["content"] = tika_result.get("content", "")[:strip]

    if meta:
        click.echo(json.dumps(tika_result.get("metadata", ""), indent=2))
    elif content:
        click.echo(json.dumps(tika_result.get("content", ""), indent=2))
    else:
        click.echo(json.dumps(tika_result, indent=2))
