# -*- coding: utf-8 -*-
import click
from iscc_cli import __version__, init, gen, batch, sim, info, web, dump, test
from click_default_group import DefaultGroup


@click.group(cls=DefaultGroup, default="gen", default_if_no_args=False)
@click.version_option(version=__version__, message="ISCC CLI - %(version)s")
def cli():
    pass


cli.add_command(init.init)
cli.add_command(gen.gen)
cli.add_command(batch.batch)
cli.add_command(web.web)
cli.add_command(sim.sim)
cli.add_command(info.info)
cli.add_command(dump.dump)
cli.add_command(test.test)


if __name__ == "__main__":
    cli()
