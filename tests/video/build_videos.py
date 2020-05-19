# -*- coding: utf-8 -*-
"""Build supported mediatype list based on ffmpeg & tika support.

See: https://en.wikipedia.org/wiki/Video_file_format
"""
import subprocess
from collections import defaultdict
from os.path import exists, abspath
from iscc_cli.tika import detector
from iscc_cli import ffmpeg
from iscc_cli import video_id
from utils import clean_mime

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
        media_type = clean_mime(detector.from_file(abspath(outf)))
        sigs = video_id.get_frame_vectors(abspath(outf))
        vid = video_id.content_id_video(sigs)
        print("{} -> {} -> {}".format(vid, outf, media_type))
        mt[media_type].append(fmt)
    for m, e in mt.items():
        if len(e) == 1:
            print(f'"{m}": {{"gmt": GMT.VIDEO, "ext": "{e[0]}"}},')
        else:
            print(f'"{m}": {{"gmt": GMT.VIDEO, "ext": {e}}},')


if __name__ == "__main__":
    build_media_types()
