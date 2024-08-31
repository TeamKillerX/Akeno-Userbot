import asyncio
import os
import random
import time

from gpytranslate import SyncTranslator
from pyrogram import Client, filters
from pyrogram.types import Message

from Akeno.utils.handler import *
from config import *

trans = SyncTranslator()

@Akeno(
    ~filters.scheduled
    & filters.command(["tr"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def translate(update: Client, message: Message):
    global to_translate
    bot = update
    reply_msg = message.reply_to_message
    if not reply_msg:
        await message.reply_text("Reply to a message to translate it!")
        return
    if reply_msg.caption:
        to_translate = reply_msg.caption
    elif reply_msg.text:
        to_translate = reply_msg.text
    try:
        args = message.text.split()[1].lower()
        if "//" in args:
            source = args.split("//")[0]
            dest = args.split("//")[1]
        else:
            source = trans.detect(to_translate)
            dest = args
    except IndexError:
        source = trans.detect(to_translate)
        dest = "en"
    translation = trans(to_translate, sourcelang=source, targetlang=dest)
    reply = ""
    reply += f"<b>Translated from {source} to {dest}</b>:\n"
    reply += f"<code>{translation.text}</code>\n"
    try:
        await message.reply_text(reply)
    except Exception as e:
        await message.reply_text(f"Error : {e}")
