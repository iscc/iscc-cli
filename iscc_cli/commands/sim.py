# -*- coding: utf-8 -*-
import json
import click
import iscc
from iscc_cli.utils import DefaultHelp


@click.command(cls=DefaultHelp)
@click.argument("a", nargs=1)
@click.argument("b", nargs=1)
def sim(a, b):
    """Estimate Similarity of ISCC Codes A & B.

    Example:

        $ iscc sim AAA6P2X7C73P72Z4 AAAWTZWH76HZGAEF

    You may also compare fully qualified ISCC Codes with each other.
    """
    click.echo(json.dumps(iscc.metrics.compare(a, b), indent=2))
