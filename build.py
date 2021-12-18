# -*- coding: utf-8 -*-
import PyInstaller.__main__
import platform

# fun hacks for pyexiv2 on macOS
# see https://github.com/pyinstaller/pyinstaller/discussions/6404
if platform.system() == "Darwin":
    import fileinput
    import pyexiv2
    import os
    import os.path

    pyexiv2_path = pyexiv2.__path__[0]
    libexiv2_dylib_original_path = os.path.join(pyexiv2_path, "lib", "libexiv2.dylib")
    libexiv2_dylib_path = os.path.join(pyexiv2_path, "lib", "libexiv2.27.dylib")

    if os.path.exists(libexiv2_dylib_original_path):
        os.rename(libexiv2_dylib_original_path, libexiv2_dylib_path)

    with fileinput.input(
        os.path.join(pyexiv2_path, "lib", "__init__.py"), inplace=True
    ) as f:
        for line in f:
            print(line.replace("libexiv2.dylib", "libexiv2.27.dylib"))

# fmt: off
cmd = [
        "iscc_cli/cli.py",
        "--clean",
        "--console",
        "--hidden-import", "dotenv",
        "--additional-hooks-dir", "extra-hooks/",
        "--collect-all", "pyexiv2",
        "--collect-data", "iscc_core",
        "--name", "iscc",
]

if platform.system() != "Darwin":
    cmd.append("--onefile")

# fmt: on

PyInstaller.__main__.run(cmd)
# fmt: on
