# -*- coding: utf-8 -*-
import click
import json
import iscc
from iscc_cli.utils import DefaultHelp


@click.command(cls=DefaultHelp)
@click.argument("file", type=click.File("rb"))
@click.option("-t", "--title", type=click.STRING, help="Title for Meta-ID creation.")
@click.option(
    "-e", "--extra", type=click.STRING, help="Extra text for Meta-ID creation."
)
@click.option(
    "-g",
    "--granular",
    is_flag=True,
    default=False,
    help="Extract granular features (experimental)",
)
@click.option(
    "-p",
    "--preview",
    is_flag=True,
    default=False,
    help="Extract preview (experimental)",
)
def gen(file, title, extra, granular, preview):
    """Generate ISCC Code for FILE."""
    r = iscc.code_iscc(
        file, title=title, extra=extra, all_granular=granular, all_preview=preview
    )
    click.echo(json.dumps(r, indent=2))
