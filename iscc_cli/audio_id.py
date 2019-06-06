# -*- coding: utf-8 -*-
"""Experimetal support for Audio-ID."""
import json
import subprocess
import iscc
from iscc_cli import fpcalc


def content_id_audio(features, partial=False):
    minhash = iscc.minimum_hash(features, n=64)
    lsb = "".join([str(x & 1) for x in minhash])
    digest = int(lsb, 2).to_bytes(8, "big", signed=False)
    if partial:
        content_id_audio_digest = iscc.HEAD_CID_A_PCF + digest
    else:
        content_id_audio_digest = iscc.HEAD_CID_A + digest
    return iscc.encode(content_id_audio_digest)


def get_chroma_vector(filepath):
    """Returns 32-bit (4 byte) integers as features"""
    cmd = [fpcalc.exe_path(), filepath, "-raw", "-json", "-algorithm", "5"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE)
    vec = json.loads(res.stdout.decode("utf-8"))["fingerprint"]
    return vec
