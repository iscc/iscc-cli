# -*- coding: utf-8 -*-
import os
import subprocess
import sys
from os.path import basename, dirname
from statistics import mode
import iscc
from lxml import etree

from iscc_cli import ffmpeg
from iscc_cli.const import WTA_PERMUTATIONS
from iscc_cli.utils import cd

NSMAP = {
    "a": "urn:mpeg:mpeg7:schema:2001",
    "b": "http://www.w3.org/2001/XMLSchema-instance",
}


def content_id_video(features, partial=False):
    sigs = set(features)
    hashsum = [sum(col) for col in zip(*sigs)]
    sh = wta_hash(hashsum, 64)
    if partial:
        content_id_video_digest = iscc.HEAD_CID_V_PCF + sh[:8]
    else:
        content_id_video_digest = iscc.HEAD_CID_V + sh[:8]
    return iscc.encode(content_id_video_digest)


def get_frame_vectors(file):
    crop = get_crop(file)
    sigfile = basename(file) + ".xml"
    folder = dirname(file)
    if crop:
        vf = "{},signature=format=xml:filename={}".format(crop, sigfile)
    else:
        vf = "signature=format=xml:filename={}".format(sigfile)
    with cd(folder):
        cmd = [ffmpeg.exe_path(), "-i", file, "-vf", vf, "-f", "null", "-"]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        tree = etree.parse(sigfile)
        root = tree.getroot()
        os.remove(sigfile)
    frames = []
    frame_els = root.xpath("//a:FrameSignature", namespaces=NSMAP)
    for frame_el in frame_els:
        frames.append(tuple(int(t) for t in frame_el.text.split()))
    return tuple(frames)


def get_crop(file) -> str:
    """Detect crop value for video."""
    cmd = [ffmpeg.exe_path(), "-i", file, "-vf", "cropdetect", "-f", "null", "-"]
    res = subprocess.run(cmd, stderr=subprocess.PIPE)
    text = res.stderr.decode(encoding=sys.stdout.encoding)
    crops = [
        line.split()[-1]
        for line in text.splitlines()
        if line.startswith("[Parsed_cropdetect")
    ]
    return mode(crops)


def wta_hash(vec, hl=64) -> bytes:
    """Calculate WTA Hash from vector with 380 features."""
    vl = len(vec)
    perms = WTA_PERMUTATIONS
    h = []
    assert len(set(vec)) > 1, "Vector for wta_hash needs at least 2 different values."

    def get_neq_vals(idxs):
        vals = vec[idxs[0]], vec[idxs[1]]
        while vals[0] == vals[1]:
            idxs = idxs[0], (idxs[1] + 1) % vl
            vals = vec[idxs[0]], vec[idxs[1]]
        return vals

    for n, perm in enumerate(perms):
        vals = get_neq_vals(perm)
        h.append(vals.index(max(vals)))
        if len(h) == hl:
            break
    h = bytes([int("".join(map(str, h[i : i + 8])), 2) for i in range(0, len(h), 8)])
    return h
