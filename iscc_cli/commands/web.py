# -*- coding: utf-8 -*-
import json
import os
from io import BytesIO
import click
import iscc
import requests
from iscc.mediatype import SUPPORTED_MEDIATYPES
from iscc.utils import download_file

import iscc_cli
from iscc_cli.utils import DefaultHelp

HEADERS = {"User-Agent": "ISCC {}".format(iscc_cli.__version__)}


@click.command(cls=DefaultHelp)
@click.argument("url", type=click.STRING)
@click.option("-t", "--title", type=click.STRING, help="Title for Meta-ID creation.")
@click.option(
    "-e", "--extra", type=click.STRING, help="Extra text for Meta-ID creation."
)
@click.pass_context
def web(ctx, url, title, extra):
    """Generate ISCC Code from URL."""

    try:
        resp = requests.get(url, headers=HEADERS, stream=True)
    except Exception as e:
        raise click.BadArgumentUsage(e)

    data = BytesIO(resp.content)
    media_type = iscc.mime_clean(iscc.mime_guess(data))
    if media_type not in SUPPORTED_MEDIATYPES:
        click.echo("Unsupported media type {}".format(media_type))
        click.echo("Please request support at https://github.com/iscc/iscc-cli/issues")
        return

    local_path = download_file(url, iscc_cli.APP_DIR, sanitize=True)
    try:
        result = iscc.code_iscc(
            local_path,
            title=title,
            extra=extra,
            all_granular=ctx.obj.granular,
            all_preview=ctx.obj.preview,
            text_store=ctx.obj.store_text,
        )
    except ValueError as e:
        raise click.ClickException(e)

    if ctx.obj.store:
        ctx.obj.index.add(result)

    if ctx.obj.unpack:
        components = iscc.decompose(result["iscc"])
        decomposed = "-".join([c.code for c in components])
        result["iscc"] = decomposed

    click.echo(json.dumps(result, indent=2))
