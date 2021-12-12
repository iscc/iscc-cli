# -*- coding: utf-8 -*-
"""Build supported mediatype list based on ffmpeg & tika support.

See: https://en.wikipedia.org/wiki/Video_file_format
"""
import subprocess
from collections import defaultdict
from os.path import exists, abspath
import iscc
from utils import clean_mime
from tika import detector

FORMATS = (
    "rm",
    "drc",
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
                    iscc.bin.ffmpeg_bin(),
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
                cmd = [
                    iscc.bin.ffmpeg_bin(),
                    "-i",
                    "master.3gp",
                    "-loglevel",
                    "2",
                    outf,
                ]
            subprocess.run(cmd)
        media_type = iscc.mediatype.mime_clean(iscc.mediatype.mime_guess(abspath(outf)))
        try:
            vid = iscc.code_video(abspath(outf))["iscc"]
            print("{} -> {} -> {}".format(vid, outf, media_type))
        except Exception as e:
            print(f"Error with {outf}: {e}")
        mt[media_type].append(fmt)
    for m, e in mt.items():
        if len(e) == 1:
            print(f'"{m}": {{"gmt": GMT.VIDEO, "ext": "{e[0]}"}},')
        else:
            print(f'"{m}": {{"gmt": GMT.VIDEO, "ext": {e}}},')


if __name__ == "__main__":
    build_media_types()
