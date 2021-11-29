# -*- coding: utf-8 -*-
import PyInstaller.__main__

PyInstaller.__main__.run(
    [
        "iscc_cli/cli.py",
        "--clean",
        "--onefile",
        "--console",
        "--collect-all",
        "pyexiv2",
        "--name",
        "iscc",
    ]
)
