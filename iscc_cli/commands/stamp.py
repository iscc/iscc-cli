# -*- coding: utf-8 -*-
from pathlib import Path
import click
from iscc_cli.utils import DefaultHelp
import fitz


@click.command(cls=DefaultHelp)
@click.argument("file", type=click.File("rb"))
@click.option(
    "-q",
    "--quantity",
    type=click.IntRange(1, 9999),
    default=10,
    help="Number of individual copies to create.",
    show_default=True,
)
def stamp(file, quantity):
    """Create a series of "individual" copies of a PDF (via metadata)."""
    try:
        doc = fitz.open(file.name)
    except Exception:
        raise click.BadParameter("File format not supported: {}".format(file.name))
    fp = Path(file.name)
    meta = doc.metadata
    for idx in range(1, quantity + 1):
        serial_num = str(idx).zfill(4)
        insert = "_" + serial_num
        outpath = Path.joinpath(fp.parent.absolute(), fp.stem + insert + fp.suffix)
        meta["subject"] = "ISCC Copy No. {}".format(serial_num)
        doc.setMetadata(meta)
        doc.save(outpath)
        click.echo("Created: {}".format(outpath))
