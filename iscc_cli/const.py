# -*- coding: utf-8 -*-


class GMT:
    """Generic Media Type"""

    IMAGE = "image"
    TEXT = "text"


SUPPORTED_MIME_TYPES = {
    "application/rtf": {"gmt": GMT.TEXT, "ext": "rtf"},
    "application/msword": {"gmt": GMT.TEXT, "ext": "doc"},
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": {
        "gmt": GMT.TEXT,
        "ext": "docx",
    },
    "image/jpeg": {"gmt": GMT.IMAGE, "ext": "jpg"},
    "image/png": {"gmt": GMT.IMAGE, "ext": "png"},
    "application/pdf": {"gmt": GMT.TEXT, "ext": "pdf"},
    "application/epub+zip": {"gmt": GMT.TEXT, "ext": "epub"},
}


SUPPORTED_EXTENSIONS = [value["ext"] for _, value in SUPPORTED_MIME_TYPES.items()]
