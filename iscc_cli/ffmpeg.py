# -*- coding: utf-8 -*-
"""A thin cross plattform installer and wrapper around ffmpeg."""
import os
import platform
import shutil
import subprocess
import tarfile
import zipfile
import stat
import click
import iscc_cli
from iscc_cli.utils import download_file


FFMPEG_OS_MAP = {
    "Linux": "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz",
    "Darwin": "https://evermeet.cx/ffmpeg/ffmpeg-4.2.1.zip",
    "Windows": "https://ffmpeg.zeranoe.com/builds/win64/static/ffmpeg-4.2.1-win64-static.zip",
}


def exe_path():
    """Returns path to ffmpeg executable."""
    if platform.system() == "Windows":
        return os.path.join(iscc_cli.APP_DIR, "ffmpeg.exe")
    return os.path.join(iscc_cli.APP_DIR, "ffmpeg")


def is_installed():
    """Check if ffmpeg is installed."""
    fp = exe_path()
    return os.path.isfile(fp) and os.access(fp, os.X_OK)


def download_url():
    """Return system specific download url"""
    return FFMPEG_OS_MAP[platform.system()]


def download():
    """Download ffmpeg and return path to archive file"""
    return download_file(download_url())


def extract(archive):
    exe_file = os.path.basename(exe_path())
    if archive.endswith(".zip"):
        with zipfile.ZipFile(archive, "r") as zip_file:
            for member in zip_file.namelist():
                filename = os.path.basename(member)
                if filename == exe_file:
                    print(member)
                    source = zip_file.open(member)
                    target = open(exe_path(), "wb")
                    with source, target:
                        shutil.copyfileobj(source, target)
    elif archive.endswith("tar.xz"):
        with tarfile.open(archive, "r:xz") as tar_file:
            for member in tar_file.getmembers():
                if member.isfile() and member.name.endswith(exe_file):
                    source = tar_file.extractfile(member)
                    target = open(exe_path(), "wb")
                    with source, target:
                        shutil.copyfileobj(source, target)


def install():
    """Install fpcalc command line tool and retur path to executable."""
    if is_installed():
        click.echo("FFMPEG is already installed.")
        return exe_path()
    archive_path = download()
    extract(archive_path)
    st = os.stat(exe_path())
    os.chmod(exe_path(), st.st_mode | stat.S_IEXEC)
    assert is_installed()
    return exe_path()


def get_version_info():
    """Get ffmpeg version info."""
    try:
        r = subprocess.run([exe_path(), "-version"], stdout=subprocess.PIPE)
        return r.stdout.decode("utf-8").splitlines()[0].strip()
    except Exception:
        return ""


if __name__ == "__main__":
    print(install())
    print(get_version_info())
