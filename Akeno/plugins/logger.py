import asyncio
import datetime
import os
import random
import time

from pyrogram import *
from pyrogram import Client, filters
from pyrogram.types import *

from Akeno.utils.database import db
from Akeno.utils.handler import *
from Akeno.utils.logger import LOGS
from config import *


@Akeno(filters.incoming & filters.group & filters.mentioned & ~filters.service)
async def tag_logger(client: Client, message: Message):
    tag_gc = await db.get_env(ENV_TEMPLATE.tag_logger)
    if not tag_gc:
        return
    if message.from_user.is_bot:
        return
    if not message.mentioned:
        return
    msg = await message.forward(int(tag_gc), True)
    await client.send_message(
        int(tag_gc),
        f"{message.from_user.mention} **tagged** {client.me.mention} **in** {message.chat.title} (`{message.chat.id}`) Go to {message.link}",
        disable_web_page_preview=True,
        reply_to_message_id=msg.id
    )

@Akeno(filters.incoming & filters.private & ~filters.bot & ~filters.service)
async def pm_logger(client: Client, message: Message):
    if message.from_user.id == 777000:
        return
    logger = await db.get_env(ENV_TEMPLATE.pm_logger)
    try:
        if logger:
            if message.chat.id != client.me.id:
                await message.forward(int(logger), True)
    except Exception as e:
        LOGS.warning(f"PM Logger Err: {e}")
