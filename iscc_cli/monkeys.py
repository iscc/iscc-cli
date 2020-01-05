# -*- coding: utf-8 -*-
"""Monkey patches to external libraries"""
import json
from urllib.parse import parse_qsl, unquote
import pytube.mixins


def apply_descrambler_monkey(stream_data, key):
    if key == "url_encoded_fmt_stream_map" and not stream_data.get(
        "url_encoded_fmt_stream_map"
    ):
        formats = json.loads(stream_data["player_response"])["streamingData"]["formats"]
        formats.extend(
            json.loads(stream_data["player_response"])["streamingData"][
                "adaptiveFormats"
            ]
        )
        try:
            stream_data[key] = [
                {
                    u"url": format_item[u"url"],
                    u"type": format_item[u"mimeType"],
                    u"quality": format_item[u"quality"],
                    u"itag": format_item[u"itag"],
                }
                for format_item in formats
            ]
        except KeyError:
            cipher_url = [
                parse_qsl(formats[i]["cipher"]) for i, data in enumerate(formats)
            ]
            stream_data[key] = []
            for i, format_item in enumerate(formats):
                stream_data[key].append(
                    {
                        u"type": format_item[u"mimeType"],
                        u"quality": format_item[u"quality"],
                        u"itag": format_item[u"itag"],
                    }
                )
                for c in cipher_url[i]:
                    if c[0] in "url":
                        stream_data[key][i].update({"url": c[1]})
                    elif c[0] in "s":
                        stream_data[key][i].update({"s": c[1]})
                    elif c[0] in "sp":
                        stream_data[key][i].update({"sp": c[1]})
    else:
        stream_data[key] = [
            {k: unquote(v) for k, v in parse_qsl(i)}
            for i in stream_data[key].split(",")
        ]


pytube.mixins.apply_descrambler = apply_descrambler_monkey
