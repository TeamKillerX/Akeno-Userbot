import asyncio
import logging
import os
import random
import re
import string
import time
from datetime import datetime as dt
from inspect import getfullargspec
from os import path
from platform import python_version
from random import choice

import aiohttp
import pyrogram
from pyrogram import Client
from pyrogram import __version__ as pyrogram_version
from pyrogram import filters
from pyrogram.handlers import MessageHandler
from pyrogram.raw.all import layer
from pyrogram.types import *

from Akeno.utils.logger import LOGS
from config import API_HASH, API_ID, SESSION

logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

StartTime = time.time()
START_TIME = dt.now()
CMD_HELP = {}
clients = []
ids = []
act = []
db = {}

SUDOERS = filters.user()

__version__ = {
    "pyrogram": pyrogram_version,
    "python": python_version(),
}

client = Client(
    "one",
    app_version="latest",
    device_model="Akeno",
    system_version="Linux",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION,
    plugins=dict(root="Akeno.plugins"),
)
clients.append(client)
