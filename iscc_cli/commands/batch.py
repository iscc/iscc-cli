# -*- coding: utf-8 -*-
import json
import os
import click
import iscc
from iscc_cli.utils import get_files, DefaultHelp
from loguru import logger as log


@click.command(cls=DefaultHelp)
@click.argument("path", type=click.Path(exists=True))
@click.option("-r", "--recursive", is_flag=True, help="Recurse into subdirectories.")
@click.pass_context
def batch(ctx, path, recursive):
    """Create ISCC Codes for all files in PATH.

    Example:

      $ iscc batch ~/Documents

    """

    for f in get_files(path, recursive=recursive):
        filesize = os.path.getsize(f)
        if not filesize:
            msg = "Cannot proccess empty file: {}".format(f)
            log.warning(msg)
            continue
        try:
            result = iscc.code_iscc(
                f,
                all_granular=ctx.obj.granular,
                all_preview=ctx.obj.preview,
                text_store=ctx.obj.store_text,
            )

            if ctx.obj.store:
                ctx.obj.index.add(result)

            if ctx.obj.unpack:
                components = iscc.decompose(result["iscc"])
                decomposed = "-".join([c.code for c in components])
                result["iscc"] = decomposed

            click.echo(json.dumps(result, indent=2))
        except Exception as e:
            log.exception(e)
