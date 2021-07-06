# -*- coding: utf-8 -*-
import os
import shutil
import sys
from os.path import basename, abspath
import click
import mobi
from iscc_cli.tika import parser
import iscc
from iscc_cli import video_id
from iscc_cli.const import SUPPORTED_MIME_TYPES, GMT
from iscc_cli.utils import get_files, mime_to_gmt, get_title, DefaultHelp
from iscc_cli import audio_id, fpcalc
from loguru import logger as log
from iscc_cli.mediatype import mime_guess, mime_clean


@click.command(cls=DefaultHelp)
@click.argument("path", type=click.Path(exists=True))
@click.option("-r", "--recursive", is_flag=True, help="Recurse into subdirectories.")
@click.option(
    "-g",
    "--guess",
    is_flag=True,
    default=False,
    help="Guess title (first line of text).",
    show_default=True,
)
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    default=False,
    help="Show debug output",
    show_default=True,
)
def batch(path, recursive, guess, debug):
    """Create ISCC Codes for all files in PATH.

    Example:

      $ iscc batch ~/Documents

    """
    if debug:
        log.add(sys.stdout)

    results = []
    for f in get_files(path, recursive=recursive):
        filesize = os.path.getsize(f)
        if not filesize:
            msg = "Cannot proccess empty file: {}".format(f)
            log.warning(msg)
            continue

        media_type = mime_clean(mime_guess(f))
        if media_type not in SUPPORTED_MIME_TYPES:
            fname = basename(f)
            msg = "Unsupported file {} with mime type: {},,,,".format(fname, media_type)
            log.warning(msg)
            continue

        if media_type == "application/x-mobipocket-ebook":
            try:
                tempdir, epub_filepath = mobi.extract(f)
                tika_result = parser.from_file(epub_filepath)
                shutil.rmtree(tempdir)
            except Exception as e:
                msg = "Error with mobi extraction %s"
                log.error(msg)
                continue
        else:
            tika_result = parser.from_file(f)

        title = get_title(tika_result, guess=guess, uri=f)

        mid, norm_title, _ = iscc.meta_id(title)
        gmt = mime_to_gmt(media_type, file_path=f)
        if gmt == GMT.IMAGE:
            try:
                cid = iscc.content_id_image(f)
            except Exception as e:
                msg = "Clould not proccess image: {} ({})".format(f, e)
                log.error(msg)
                continue

        elif gmt == GMT.TEXT:
            text = tika_result["content"]
            if not text:
                msg = "Could not extract text from {}".format(basename(f))
                log.warning(msg)
                continue
            cid = iscc.content_id_text(tika_result["content"])
        elif gmt == GMT.AUDIO:
            if not fpcalc.is_installed():
                fpcalc.install()
            features = audio_id.get_chroma_vector(f)
            cid = audio_id.content_id_audio(features)
        elif gmt == GMT.VIDEO:
            features = video_id.get_frame_vectors(abspath(f))
            cid = video_id.content_id_video(features)
        else:
            log.error("Could not generate ISCC")
            continue

        did = iscc.data_id(f)
        iid, tophash = iscc.instance_id(f)

        iscc_code_cs = ",".join((mid, cid, did, iid))

        click.echo(
            "{iscc_code},{tophash},{fname},{gmt},{title}".format(
                iscc_code=iscc_code_cs,
                tophash=tophash,
                fname=basename(f),
                gmt=gmt,
                title=norm_title,
            )
        )
        iscc_code = "-".join((mid, cid, did, iid))
        results.append(
            dict(
                iscc=iscc_code,
                norm_title=norm_title,
                tophash=tophash,
                gmt=gmt,
                file_name=basename(f),
            )
        )

    return results
