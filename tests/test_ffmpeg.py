# -*- coding: utf-8 -*-
import pytest
import os
import sys
from iscc_cli import ffmpeg


def is_linux():
    return sys.platform == "linux"


def is_py36():
    return sys.version.major == 3 and sys.version.minor == 6


def test_exe_path():
    assert "ffmpeg" in ffmpeg.exe_path()


def test_ffmpeg_exists():
    assert os.path.exists(ffmpeg.exe_path())


def test_ffmpeg_executable():
    assert os.access(ffmpeg.exe_path(), os.X_OK)


@pytest.mark.skipif(is_linux() and is_py36(), reason="custom ffmpeg")
def test_get_version_info():
    vi = ffmpeg.get_version_info()
    assert vi.startswith("4.2")
