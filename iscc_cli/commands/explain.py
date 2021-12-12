# -*- coding: utf-8 -*-
import json
import click
from iscc_core.codec import Code
from iscc.wrappers import decompose
from iscc_cli.utils import DefaultHelp


@click.command(cls=DefaultHelp)
@click.argument("iscc_code", nargs=1)
def explain(iscc_code):
    """Explain details of an ISCC code.

    Example:

        $ iscc explain KADQVKQBE5UKYT6VBPH4ZCPSZLTVQNYTWC6OZFO4DW37SLFETDMDAWQ

    """
    code_obj = Code(iscc_code)
    code_objs = decompose(code_obj)
    decomposed = "-".join(c.code for c in code_objs)
    components = {
        c.code: {
            "readable": c.explain,
            "hash_hex": c.hash_hex,
            "hash_uint": str(c.hash_uint),
            "hash_bits": c.hash_bits,
        }
        for c in code_objs
    }
    result = dict(
        iscc=code_obj.code,
        readable=code_obj.explain,
        decomposed=decomposed,
        components=components,
    )
    click.echo(json.dumps(result, indent=2))
