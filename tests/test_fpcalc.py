# -*- coding: utf-8 -*-
import os
import platform

from iscc_cli import fpcalc


def test_exe_path():
    assert "fpcalc" in fpcalc.exe_path()


def test_is_installed():
    assert isinstance(fpcalc.is_installed(), bool)


def test_download_url():
    url = fpcalc.download_url()
    assert platform.system().lower() in url
    assert fpcalc.FPCALC_VERSION in url


def test_download():
    out_path = fpcalc.download()
    assert os.path.exists(out_path)


def test_install():
    exe_path = fpcalc.install()
    assert os.path.exists(exe_path)
    assert fpcalc.is_installed()


def test_get_version_info():
    vi = fpcalc.get_version_info()
    assert vi.startswith("fpcalc version 1.4.3")
