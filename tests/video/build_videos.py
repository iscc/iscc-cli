# -*- coding: utf-8 -*-
"""Build supported mediatype list based on ffmpeg & tika support"""
import os
import subprocess
from collections import defaultdict
from os.path import exists, abspath
from tika import detector
from iscc_cli import ffmpeg
from video_id import content_id_video

FORMATS = (
    "3gp",
    "3g2",
    "asf",
    "avi",
    "webm",
    "mpeg",
    "mpg",
    "mp4",
    "m4v",
    "mkv",
    "m1v",
    "ogg",
    "mov",
    "flv",
    "swf",
    "f4v",
    "h264",
    "ogv",
    "vob",
    "wmv",
)


def build_media_types():
    mt = defaultdict(list)
    for fmt in FORMATS:
        outf = "demo.{}".format(fmt)
        print("Processing {}:".format(outf), end=" ")
        if not exists(outf):
            if fmt in ("3gp", "3g2"):
                cmd = [
                    ffmpeg.exe_path(),
                    "-i",
                    "master.3gp",
                    "-f",
                    fmt,
                    "-vcodec",
                    "h263",
                    "-vf",
                    "scale=352x288",
                    "-acodec",
                    "amr_nb",
                    "-ar",
                    "8000",
                    "-ac",
                    "1",
                    outf,
                ]
            else:
                cmd = [ffmpeg.exe_path(), "-i", "master.3gp", "-loglevel", "2", outf]
            subprocess.run(cmd)
        media_type = detector.from_file(abspath(outf))
        vid = content_id_video(abspath(outf))
        os.remove(outf)
        print("{} -> {} -> {}".format(vid, outf, media_type))
        mt[media_type].append(fmt)
    for m, e in mt.items():
        if len(e) == 1:
            print(f'"{m}": {{"gmt": GMT.VIDEO, "ext": "{e[0]}"}},')
        else:
            print(f'"{m}": {{"gmt": GMT.VIDEO, "ext": {e}}},')


if __name__ == "__main__":
    build_media_types()