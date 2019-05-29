# -*- coding: utf-8 -*-
from os.path import basename
from tika import detector, parser
import click
import iscc
import iscc_cli
from iscc_cli.const import SUPPORTED_MIME_TYPES, GMT
from iscc_cli.utils import get_files, get_gmt, get_title


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
        mime_type = detector.from_file(f)
        if mime_type not in SUPPORTED_MIME_TYPES:
            fname = basename(f)
            click.echo(
                "Unsupported file {} with mime type: {}".format(fname, mime_type)
            )
            continue

        gmt = get_gmt(f)

        tika_result = parser.from_file(f)
        title = get_title(tika_result)
        mid, norm_title, norm_extra = iscc.meta_id(title)

        if gmt == GMT.IMAGE:
            cid = iscc.content_id_image(f)
        elif gmt == GMT.TEXT:
            text = tika_result["content"]
            if not text:
                click.echo('Coult not extract text from {}'.format(basename(f)))
                continue
            cid = iscc.content_id_text(tika_result["content"])

        did = iscc.data_id(f)
        iid, _ = iscc.instance_id(f)
        click.echo(
            "ISCC:{mid}-{cid}-{did}-{iid},{fname},{title}".format(
                mid=mid, cid=cid, did=did, iid=iid, fname=basename(f), title=norm_title
            )
        )


cli.add_command(gen)


if __name__ == "__main__":
    cli()
