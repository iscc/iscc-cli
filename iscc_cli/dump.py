# -*- coding: utf-8 -*-
import click
from click import UsageError
from tika import parser
from iscc_cli.utils import DefaultHelp
import json


@click.command(cls=DefaultHelp)
@click.argument("file", type=click.File("rb"))
@click.option(
    "-s", "--strip", type=click.INT, default=0, help="Strip content to first X chars."
)
@click.option("-m", "--meta", is_flag=True, default=False, help="Dump metadata only.")
@click.option("-c", "--content", is_flag=True, default=False, help="Dump content only.")
def dump(file, strip, meta, content):
    """Dump Tika extraction results for FILE."""
    tika_result = parser.from_file(file.name)
    if all([meta, content]):
        raise UsageError("Use either --meta or --content for selecitve output.")

    if strip:
        tika_result["content"] = tika_result.get("content", "")[:strip]

    if meta:
        click.echo(json.dumps(tika_result.get("metadata", ""), indent=2))
    elif content:
        click.echo(json.dumps(tika_result.get("content", ""), indent=2))
    else:
        click.echo(json.dumps(tika_result, indent=2))
