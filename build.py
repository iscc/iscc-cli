# -*- coding: utf-8 -*-
import PyInstaller.__main__

# fmt: off
cmd = [
        "iscc_cli/cli.py",
        "--clean",
        "--console",
        "--hidden-import", "dotenv",
        "--collect-binaries", "exiv2",
        "--collect-data", "iscc_core",
        "--onefile",
        "--name", "iscc",
]
# fmt: on

PyInstaller.__main__.run(cmd)
