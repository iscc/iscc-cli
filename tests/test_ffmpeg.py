# -*- coding: utf-8 -*-
from iscc_cli import ffmpeg


def test_exe_path():
    assert "ffmpeg" in ffmpeg.exe_path()


def test_get_version_info():
    vi = ffmpeg.get_version_info()
    assert vi.startswith("4.2")
