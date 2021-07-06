# -*- coding: utf-8 -*-
import io
from typing import Union
from iscc_cli.datatypes import Readable, Uri, File, Data
from typing import BinaryIO
from iscc_cli.utils import download_file


def open_data(data):
    # type: (Readable) -> Union[BinaryIO]
    """Open filepath, rawdata or file-like object."""
    if isinstance(data, Uri.__args__):
        if isinstance(data, str) and (
            data.startswith("http://") or data.startswith("https://")
        ):
            data = download_file(data, sanitize=True)
        return open(str(data), "rb")
    elif isinstance(data, Data.__args__):
        return io.BytesIO(data)
    elif isinstance(data, File.__args__):
        data.seek(0)
        return data
    else:
        raise ValueError(f"unsupported data type {type(data)}")
