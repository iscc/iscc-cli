# -*- coding: utf-8 -*-
import click
import iscc
import iscc_cli
import requests
from iscc.bin import ffmpeg_version_info, ffprobe_version_info
from iscc.audio import fpcalc_version_info
from iscc.mediatype import SUPPORTED_EXTENSIONS
import importlib
import importlib.machinery
import inspect


EXTENSION_SUFFIXES = tuple(
    suffix.lstrip(".") for suffix in importlib.machinery.EXTENSION_SUFFIXES
)


suffix = lambda filename: "." in filename and filename.rpartition(".")[-1] or ""


def isnativemodule(module):
    """ isnativemodule(thing) → boolean predicate, True if `module`
        is a native-compiled (“extension”) module.

        Q.v. this fine StackOverflow answer on this subject:
            https://stackoverflow.com/a/39304199/298171
    """
    # Step one: modules only beyond this point:
    if not inspect.ismodule(module):
        return False

    # Step two: return truly when “__loader__” is set:
    if isinstance(
        getattr(module, "__loader__", None), importlib.machinery.ExtensionFileLoader
    ):
        return True

    # Step three: in leu of either of those indicators,
    # check the module path’s file suffix:
    try:
        ext = suffix(inspect.getfile(module))
    except TypeError as exc:
        return "is a built-in" in str(exc)

    return ext in EXTENSION_SUFFIXES


def tika_version():
    from tika import tika

    url = tika.ServerEndpoint + "/version"
    try:
        return requests.get(url).text
    except Exception:
        return 'WARNING: Not Installed - run "iscc init" to install!'


@click.command()
def info():
    """Show information about environment."""
    from tika import tika
    from iscc_core import minhash, simhash, cdc

    click.echo("ISCC Cli Version: %s" % iscc_cli.__version__)
    click.echo("ISCC Version: %s" % iscc.__version__)
    click.echo("FFMPEG Version: %s" % ffmpeg_version_info())
    click.echo("FFPROBE Version: %s" % ffprobe_version_info())
    click.echo("FPCALC Version: %s" % fpcalc_version_info())
    click.echo("Tika Version: %s" % tika_version())
    click.echo("Tika Jar Path: %s" % tika.TikaJarPath)
    click.echo("Simhash Native: %s" % isnativemodule(simhash))
    click.echo("Minhash Native: %s" % isnativemodule(minhash))
    click.echo("CDC Native: %s" % isnativemodule(cdc))
    click.echo("Supported File Types: %s" % ", ".join(sorted(SUPPORTED_EXTENSIONS)))


if __name__ == "__main__":
    info()
