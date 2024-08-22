import asyncio
import math
import os
import re
import sys
import time
from os import getenv
from traceback import format_exc
from urllib.parse import unquote
from urllib.request import urlretrieve

from telegraph import Telegraph, exceptions, upload_file


def QuoteApi(user_id, first_name, link, text):
    json = {
        "type": "quote",
        "format": "webp",
        "backgroundColor": "#1b1429",
        "width": 512,
        "height": 768,
        "scale": 2,
        "messages": [
            {
                "entities": [],
                "avatar": True,
                "from": {
                    "id": user_id,
                    "name": first_name,
                    "photo": {
                        "url": link
                    }
                },
                "text": text,
                "replyMessage": {}
            }
        ]
    }
    return json

def get_telegraph_link(media):
    try:
        response = upload_file(media)
    except exceptions.TelegraphException as exc:
        return
    return response

def humanbytes(size):
    if not size:
        return "0 B"
    for unit in ["", "K", "M", "G", "T"]:
        if size < 1024:
            break
        size /= 1024
    if isinstance(size, int):
        size = f"{size}{unit}B"
    elif isinstance(size, float):
        size = f"{size:.2f}{unit}B"
    return size

def _fix_logging(handler):
    handler._builtin_open = open

    def _new_open(self):
        open_func = self._builtin_open
        return open_func(self.baseFilename, self.mode)

    setattr(handler, "_open", _new_open)

def _ask_input():
    def new_input(*args, **kwargs):
        raise EOFError("args=" + str(args) + ", kwargs=" + str(kwargs))

    __builtins__["input"] = new_input

def where_hosted():
    if os.getenv("DYNO"):
        return "heroku"
    if os.getenv("RAILWAY_STATIC_URL"):
        return "railway"
    if os.getenv("OKTETO_TOKEN"):
        return "okteto"
    if os.getenv("KUBERNETES_PORT"):
        return "qovery | kubernetes"
    if os.getenv("RUNNER_USER") or os.getenv("HOSTNAME"):
        return "github actions"
    if os.getenv("ANDROID_ROOT"):
        return "termux"
    if os.getenv("FLY_APP_NAME"):
        return "fly.io"
    return "local"

    if int(v) < 10:
        _fix_logging(FileHandler)

    if where_hosted() == "local":
        _ask_input()
