# -*- coding: utf-8 -*-
"""A thin cross plattform installer and wrapper around chromaprint fpcalc."""
import io
import os
import platform
import shutil
import tarfile
import zipfile
import subprocess

import click
import requests
import iscc_cli


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
    file_name = FPCALC_OS_MAP[platform.system()]
    out_path = os.path.join(iscc_cli.APP_DIR, file_name)
    if os.path.exists(out_path):
        click.echo("Fpcalc already downloaded: {}".format(out_path))
        return out_path

    os.makedirs(iscc_cli.APP_DIR, exist_ok=True)
    url = download_url()

    r = requests.get(url, stream=True)
    length = int(r.headers["content-length"])
    chunk_size = 512
    iter_size = 0
    with io.open(out_path, "wb") as fd:
        with click.progressbar(length=length, label="Downloading fpcalc") as bar:
            for chunk in r.iter_content(chunk_size):
                fd.write(chunk)
                iter_size += chunk_size
                bar.update(chunk_size)
    return out_path


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
    assert is_installed()
    return exe_path()


def get_version_info() -> bytes:
    """Get fpcalc version"""
    r = subprocess.run([exe_path(), "-v"], stdout=subprocess.PIPE)
    return r.stdout
