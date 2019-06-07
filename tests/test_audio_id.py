# -*- coding: utf-8 -*-
import os
from tests import ROOT_DIR
from iscc_cli import audio_id
from iscc_cli import fpcalc

os.chdir(ROOT_DIR)


def test_content_id_audio():
    assert audio_id.content_id_audio([1, 2, 3]) == "CAFcywC1ZGJy9"


def test_get_chroma_vector_file_path():
    if not fpcalc.is_installed():
        fpcalc.install()
    r = audio_id.get_chroma_vector("tests/demo.mp3")
    assert isinstance(r, list)
    assert r[0] == 684003877


def test_get_chroma_vector_file_stream():
    if not fpcalc.is_installed():
        fpcalc.install()
    with open("tests/demo.mp3", 'rb') as file_obj:
        r = audio_id.get_chroma_vector(file_obj)
    assert isinstance(r, list)
    assert r[0] == 684003877

