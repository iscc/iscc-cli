# -*- coding: utf-8 -*-
import os
from iscc import bin


def test_exe_path():
    assert "ffmpeg" in bin.ffmpeg_bin()


def test_ffmpeg_exists():
    assert os.path.exists(bin.ffmpeg_bin())


def test_ffmpeg_executable():
    assert os.access(bin.ffmpeg_bin(), os.X_OK)


def test_get_version_info():
    vi = bin.ffmpeg_version_info()
    assert vi.startswith("4.2")
