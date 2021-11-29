# -*- coding: utf-8 -*-
import pytest
import os
import sys
from iscc import bin


def is_linux():
    return sys.platform == "linux"


def is_py36():
    return sys.version.startswith("3.6")


def test_exe_path():
    assert "ffmpeg" in bin.ffmpeg_bin()


@pytest.mark.skipif(is_linux() and is_py36(), reason="custom ffmpeg")
def test_ffmpeg_exists():
    assert os.path.exists(bin.ffmpeg_bin())


@pytest.mark.skipif(is_linux() and is_py36(), reason="custom ffmpeg")
def test_ffmpeg_executable():
    assert os.access(bin.ffmpeg_bin(), os.X_OK)


@pytest.mark.skipif(is_linux() and is_py36(), reason="custom ffmpeg")
def test_get_version_info():
    vi = bin.ffmpeg_version_info()
    assert vi.startswith("4.2")
