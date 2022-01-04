# -*- coding: utf-8 -*-
import click
from iscc_cli.utils import DefaultHelp
import iscc_core


@click.command(cls=DefaultHelp, name="sum")
@click.argument("file", type=click.File("rb"))
@click.pass_context
def sum_(ctx, file):
    """Generate ISCC SUM for FILE."""
    ih = iscc_core.code_instance.InstanceHasherV0()
    dh = iscc_core.code_data.DataHasherV0()
    bs = iscc_core.core_opts.io_read_size
    data = file.read(bs)
    while data:
        ih.push(data)
        dh.push(data)
        data = file.read(bs)
    result = iscc_core.gen_iscc_code([dh.code(bits=128), ih.code(128)])
    click.echo(result.iscc)
