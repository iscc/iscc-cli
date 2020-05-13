# -*- coding: utf-8 -*-
"""Experimetal support for Audio-ID."""
import json
import subprocess
import iscc
from iscc_cli import fpcalc


def content_id_audio(features, partial=False):
    digests = []
    for a, b in iscc.sliding_window(features, 2):
        digest = a.to_bytes(4, 'big', signed=True) + b.to_bytes(4, 'big', signed=True)
        digests.append(digest)
    shash_digest = iscc.similarity_hash(digests)
    if partial:
        content_id_audio_digest = iscc.HEAD_CID_A_PCF + shash_digest
    else:
        content_id_audio_digest = iscc.HEAD_CID_A + shash_digest
    return iscc.encode(content_id_audio_digest)


def get_chroma_vector(file):
    """Returns 32-bit (4 byte) integers as features"""

    if hasattr(file, "read"):
        file.seek(0)
        cmd = [fpcalc.exe_path(), "-raw", "-json", "-signed", "-"]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, input=file.read())
    else:
        cmd = [fpcalc.exe_path(), "-raw", "-json", "-signed", file]
        res = subprocess.run(cmd, stdout=subprocess.PIPE)

    vec = json.loads(res.stdout.decode("utf-8"))["fingerprint"]
    return vec
