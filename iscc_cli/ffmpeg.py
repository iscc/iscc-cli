# -*- coding: utf-8 -*-
"""A thin cross plattform installer and wrapper around ffmpeg."""
import imageio_ffmpeg


def exe_path():
    """Returns path to ffmpeg executable."""
    return imageio_ffmpeg.get_ffmpeg_exe()


def get_version_info():
    """Get ffmpeg version info."""
    return imageio_ffmpeg.get_ffmpeg_version()


if __name__ == "__main__":
    print(exe_path())
    print(get_version_info())
