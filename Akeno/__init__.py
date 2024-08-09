import asyncio
import logging
import time
import pyrogram
import string
import random
from inspect import getfullargspec
from os import path
from random import choice
import aiohttp
import re
import os

from datetime import datetime as dt
from pyrogram import Client
from pyrogram.types import *
from pyrogram import filters
from pyrogram.raw.all import layer
from pyrogram.handlers import MessageHandler
from config import API_HASH, API_ID, SESSION
from pytgcalls import GroupCallFactory
from aiohttp import ClientSession
from Akeno.utils.logger import LOGS
from platform import python_version
from pyrogram import __version__ as pyrogram_version

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
    
aiohttpsession = ClientSession()

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
if not hasattr(client, "group_call"):
    setattr(client, "group_call", GroupCallFactory(client).get_group_call())

clients.append(client)
