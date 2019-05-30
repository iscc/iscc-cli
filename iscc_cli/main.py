# -*- coding: utf-8 -*-
from os.path import basename
from tika import detector, parser, tika
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
                click.echo("Could not extract text from {}".format(basename(f)))
                continue
            cid = iscc.content_id_text(tika_result["content"])

        did = iscc.data_id(f)
        iid, _ = iscc.instance_id(f)
        click.echo(
            "ISCC:{mid}-{cid}-{did}-{iid},{fname},{title}".format(
                mid=mid, cid=cid, did=did, iid=iid, fname=basename(f), title=norm_title
            )
        )


@click.command()
def debug():
    click.echo("Tika TikaVersion: {}".format(tika.TikaVersion))
    click.echo("Tika TikaJarPath: {}".format(tika.TikaJarPath))
    click.echo("Tika TikaServerLogFilePath: {}".format(tika.TikaServerLogFilePath))
    click.echo("Tika TikaServerJar: {}".format(tika.TikaServerJar))
    click.echo("Tika ServerHost: {}".format(tika.ServerHost))
    click.echo("Tika Port: {}".format(tika.Port))
    click.echo("Tika ServerEndpoint: {}".format(tika.ServerEndpoint))
    click.echo("Tika Translator: {}".format(tika.Translator))
    click.echo("Tika TikaClientOnly: {}".format(tika.TikaClientOnly))
    click.echo("Tika TikaServerClasspath: {}".format(tika.TikaServerClasspath))
    click.echo("Tika TikaStartupSleep: {}".format(tika.TikaStartupSleep))
    click.echo("Tika TikaStartupMaxRetry: {}".format(tika.TikaStartupMaxRetry))
    click.echo("Tika TikaJava: {}".format(tika.TikaJava))


cli.add_command(debug)
cli.add_command(gen)


if __name__ == "__main__":
    cli()
