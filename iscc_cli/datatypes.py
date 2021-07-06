# -*- coding: utf-8 -*-
import mmap
from enum import Enum
from io import BytesIO, BufferedReader
from pathlib import Path
from typing import Union, BinaryIO

Data = Union[bytes, bytearray, memoryview]
Uri = Union[str, Path]
File = Union[BinaryIO, mmap.mmap, BytesIO, BufferedReader]
Readable = Union[Uri, Data, File]


class GMT(str, Enum):
    """Generic Metdia Type"""

    text = "text"
    image = "image"
    audio = "audio"
    video = "video"
    unknown = "unknown"
