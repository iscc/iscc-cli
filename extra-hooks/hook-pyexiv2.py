import os
import glob

from PyInstaller import compat
from PyInstaller.utils.hooks import get_package_paths

if compat.is_darwin:
    binaries = []
    datas = []
    package_root_base, package_root = get_package_paths('pyexiv2')

    # libs = glob.glob(os.path.join(package_root, 'lib', 'py3.*-darwin', '*.so'))
    # binaries += [(lib, '.') for lib in libs]

    libs = glob.glob(os.path.join(package_root, 'lib', '*.dylib'))
    binaries += [(lib, '.') for lib in libs]
