# -*- coding: utf-8 -*-
from os.path import basename
import click
from tika import detector, parser
import iscc
from iscc_cli.const import SUPPORTED_MIME_TYPES, GMT
from iscc_cli.utils import get_files, mime_to_gmt, get_title


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("-r", "--recursive", is_flag=True, help="Recurse into subdirectories.")
def batch(path, recursive):
    """Batch create ISCC Codes.

    Generates ISCC Codes for all media files in <PATH>.
    """
    for f in get_files(path, recursive=recursive):
        media_type = detector.from_file(f)
        if media_type not in SUPPORTED_MIME_TYPES:
            fname = basename(f)
            click.echo(
                "Unsupported file {} with mime type: {}".format(fname, media_type)
            )
            continue

        gmt = mime_to_gmt(media_type)
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
