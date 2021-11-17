# -*- coding: utf-8 -*-
import sys
from typing import Optional

import click
import iscc
from dataclasses import dataclass
from iscc_cli import __version__
from iscc_cli.commands import (
    init,
    gen,
    batch,
    sim,
    info,
    web,
    dump,
    test,
    explain,
    db,
    detect,
)
from click_default_group import DefaultGroup
from loguru import logger as log


@dataclass
class GlobalOptions:
    debug: bool
    granular: bool
    preview: bool
    store: bool
    unpack: bool
    store_text: bool
    index: Optional[iscc.Index] = None


@click.group(cls=DefaultGroup, default="gen", default_if_no_args=False)
@click.version_option(version=__version__, message="ISCC CLI - %(version)s")
@click.option("-d", "--debug", is_flag=True, default=False, help="Show debug output")
@click.option(
    "-g", "--granular", is_flag=True, default=False, help="Extract granular features"
)
@click.option(
    "-p", "--preview", is_flag=True, default=False, help="Extract asset preview",
)
@click.option(
    "-s", "--store", is_flag=True, default=False, help="Store ISCC in local index",
)
@click.option(
    "-u", "--unpack", is_flag=True, default=False, help="Unpack ISCC into components",
)
@click.option(
    "-st", "--store_text", is_flag=True, default=False, help="Store extracted text",
)
@click.pass_context
def cli(ctx, debug, granular, preview, store, unpack, store_text):
    ctx.obj = GlobalOptions(
        debug=debug,
        granular=granular,
        preview=preview,
        store=store,
        unpack=unpack,
        store_text=store_text,
    )

    ctx.obj.index = iscc.Index("cli-db", index_features=True, index_metadata=True)

    if debug:
        log.add(sys.stdout)
        log.info("Debug messages activated!")


cli.add_command(init.init)
cli.add_command(gen.gen)
cli.add_command(batch.batch)
cli.add_command(web.web)
cli.add_command(sim.sim)
cli.add_command(info.info)
cli.add_command(dump.dump)
cli.add_command(test.test)
cli.add_command(explain.explain)
cli.add_command(db.db)
cli.add_command(detect.detect)


if __name__ == "__main__":
    cli()
