# -*- coding: utf-8 -*-
import os
from os.path import abspath

from tests import ROOT_DIR
from iscc_cli import video_id
import pytest


os.chdir(ROOT_DIR)


def test_wta_hash():
    vec = tuple([0] * 379) + (1,)
    assert video_id.wta_hash(vec) == b"\xff\xff\xff\xff\xff\xff\xff\xff"
    vec = (1,) + tuple([0] * 379)
    assert video_id.wta_hash(vec) == b"\xff\xff\xff\xff\xff\xff\xff\xff"
    vec = (1,) + tuple([0] * 378) + (1,)
    assert video_id.wta_hash(vec) == b"\xff\xff\xff\xff\xff\xff\xff\xff"
    vec = (0,) + tuple([2] * 378) + (0,)
    assert video_id.wta_hash(vec) == b"\x00\x00\x00\x00\x00\x00\x00\x00"


def test_crop():
    assert video_id.get_crop("./tests/video/master.3gp") == "crop=176:96:0:24"


def test_get_frame_vectors():
    fv = video_id.get_frame_vectors(abspath("./tests/video/master.3gp"))
    assert isinstance(fv, tuple)
    assert isinstance(fv[0][0], int)
    assert len(fv[0]) == 380


def test_content_id_video():
    assert video_id.content_id_video([tuple(range(380))]) == "CVEowL1rB7Z8P"


def test_content_id_video_0_fetures():
    with pytest.raises(AssertionError):
        video_id.content_id_video([tuple([0] * 380)])
