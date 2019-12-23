# -*- coding: utf-8 -*-
import os
from iscc_cli import ffmpeg
import pytest


def test_exe_path():
    assert "ffmpeg" in ffmpeg.exe_path()


def test_is_installed():
    assert isinstance(ffmpeg.is_installed(), bool)


@pytest.mark.dependency()
def test_download():
    out_path = ffmpeg.download()
    assert os.path.exists(out_path)


@pytest.mark.dependency(depends=['test_download'])
def test_install():
    exe_path = ffmpeg.install()
    assert os.path.exists(exe_path)
    assert ffmpeg.is_installed()


@pytest.mark.dependency(depends=['test_install'])
def test_get_version_info():
    vi = ffmpeg.get_version_info()
    assert vi.startswith("ffmpeg version 4.2.1")
