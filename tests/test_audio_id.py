# -*- coding: utf-8 -*-
import os
from tests import ROOT_DIR
from iscc_cli import audio_id
from iscc_cli import fpcalc

os.chdir(ROOT_DIR)


def test_content_id_audio():
    assert audio_id.content_id_audio([1, 2, 3]) == "CAFcywC1ZGJy9"


def test_get_chroma_vector():
    if not fpcalc.is_installed():
        fpcalc.install()
    r = audio_id.get_chroma_vector("tests/demo.mp3")
    assert isinstance(r, list)
    assert r[0] == 684003877
