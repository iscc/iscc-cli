# -*- coding: utf-8 -*-
import sys
import click
import iscc

from iscc_cli.const import ISCC_COMPONENT_CODES
from iscc_cli.utils import DefaultHelp, iscc_verify, iscc_split, iscc_clean


@click.command(cls=DefaultHelp)
@click.argument("a", nargs=1)
@click.argument("b", nargs=1)
def sim(a, b):
    """Estimate Similarity of ISCC Codes A & B.

    Example:

        $ iscc sim CCUcKwdQc1jUM CCjMmrCsKWu1D

    You may also compare fully qualified ISCC Codes with each other.
    """
    try:
        iscc_verify(a)
        iscc_verify(b)
    except ValueError as e:
        click.echo(str(e))
        sys.exit(1)

    # Fully Qualified ISCC Code Similarity
    if len(iscc_clean(a)) == 52 and len(iscc_clean(b)) == 52:
        digest_a = b"".join(iscc.decode(code)[1:] for code in iscc_split(a))
        digest_b = b"".join(iscc.decode(code)[1:] for code in iscc_split(b))
        int_a = int.from_bytes(digest_a, "big", signed=False)
        int_b = int.from_bytes(digest_b, "big", signed=False)
        dist = bin(int_a ^ int_b).count("1")
        similarity = ((192 - dist) / 192) * 100
        click.echo("Estimated Total Similarity: {:.2f} %".format(similarity))

    # Per Component Similarity
    a = iscc_split(a)
    b = iscc_split(b)

    for ca in a:
        for cb in b:
            type_a = ISCC_COMPONENT_CODES.get(ca[:2])["name"]
            type_b = ISCC_COMPONENT_CODES.get(cb[:2])["name"]
            if type_a == type_b and type_a != "Instance-ID":
                dist = iscc.distance(ca, cb)
                similarity = ((64 - dist) / 64) * 100
                click.echo(
                    "Estimated Similarity of {}: {:.2f} %".format(type_a, similarity)
                )
            if type_a == "Instance-ID" and type_b == "Instance-ID":
                if ca == cb:
                    click.echo("Identical Instance-ID")
