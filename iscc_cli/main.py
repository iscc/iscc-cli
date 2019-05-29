# -*- coding: utf-8 -*-
import iscc
import iscc_cli
import click
from iscc_cli.utils import get_files


@click.group()
@click.version_option(
    version=iscc_cli.__version__, message="ISCC - Command Line Tool - %(version)s"
)
def cli():
    pass


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("-r", "--recursive", is_flag=True)
def gen(path, recursive):
    for f in get_files(path, recursive=recursive):
        cid = iscc.content_id_image(f)
        did = iscc.data_id(f)
        iid, _ = iscc.instance_id(f)
        click.echo("ISCC:{cid}-{did}-{iid}".format(cid=cid, did=did, iid=iid))


cli.add_command(gen)


if __name__ == "__main__":
    cli()
