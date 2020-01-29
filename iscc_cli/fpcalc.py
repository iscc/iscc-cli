# -*- coding: utf-8 -*-
"""A thin cross plattform installer and wrapper around chromaprint fpcalc."""
import os
import platform
import shutil
import tarfile
import zipfile
import subprocess
import stat
import click
import iscc_cli
from iscc_cli.utils import download_file


FPCALC_VERSION = "1.4.3"
FPCALC_URL_BASE = "https://github.com/acoustid/chromaprint/releases/download/v{}/".format(
    FPCALC_VERSION
)
FPCALC_OS_MAP = {
    "Linux": "chromaprint-fpcalc-{}-linux-x86_64.tar.gz".format(FPCALC_VERSION),
    "Darwin": "chromaprint-fpcalc-{}-macos-x86_64.tar.gz".format(FPCALC_VERSION),
    "Windows": "chromaprint-fpcalc-{}-windows-x86_64.zip".format(FPCALC_VERSION),
}


def exe_path():
    """Returns patth to fpcalc executable."""
    if platform.system() == "Windows":
        return os.path.join(iscc_cli.APP_DIR, "fpcalc.exe")
    return os.path.join(iscc_cli.APP_DIR, "fpcalc")


def is_installed():
    """"Check if fpcalc is installed."""
    fp = exe_path()
    return os.path.isfile(fp) and os.access(fp, os.X_OK)


def download_url():
    """Return system and version dependant download url"""
    return os.path.join(FPCALC_URL_BASE, FPCALC_OS_MAP[platform.system()])


def download():
    """Download fpcalc and return path to archive file."""
    return download_file(download_url())


def extract(archive):
    if archive.endswith(".zip"):
        with zipfile.ZipFile(archive, "r") as zip_file:
            for member in zip_file.namelist():
                filename = os.path.basename(member)
                if filename == "fpcalc.exe":
                    source = zip_file.open(member)
                    target = open(exe_path(), "wb")
                    with source, target:
                        shutil.copyfileobj(source, target)
    elif archive.endswith("tar.gz"):
        with tarfile.open(archive, "r:gz") as tar_file:
            for member in tar_file.getmembers():
                if member.isfile() and member.name.endswith("fpcalc"):
                    source = tar_file.extractfile(member)
                    target = open(exe_path(), "wb")
                    with source, target:
                        shutil.copyfileobj(source, target)


def install():
    """Install fpcalc command line tool and retur path to executable."""
    if is_installed():
        click.echo("Fpcalc is already installed.")
        return exe_path()
    archive_path = download()
    extract(archive_path)
    st = os.stat(exe_path())
    os.chmod(exe_path(), st.st_mode | stat.S_IEXEC)
    assert is_installed()
    return exe_path()


def get_version_info():
    """Get fpcalc version"""
    try:
        r = subprocess.run([exe_path(), "-v"], stdout=subprocess.PIPE)
        return r.stdout.decode("utf-8").strip().split()[-1]
    except FileNotFoundError:
        return 'WARNING: Not Installed - run "iscc init" to install!'
