import asyncio
import os
import random
import time

from lyricsgenius import Genius
from pyrogram import Client, filters
from pyrogram.types import Message

from Akeno.utils.database import db
from Akeno.utils.handler import *
from config import *


@Akeno(
    ~filters.scheduled
    & filters.command(["lyrics"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def lyrics_songs(_, message: Message):
    query = message.text.split(" ", 1)[1] if len(message.command) > 1 else None
    if not query:
        return await message.reply_text("Search For lyrics")
    token = await db.get_env(ENV_TEMPLATE.lyrics_api)
    if not token:
        return await message.reply_text("Required: `LYRICS_API`")
    genius = Genius(token)
    artist = genius.search_song(query)
    results = artist.lyrics
    if results is None:
        return await message.reply_text("no search in lyrics")
    if len(results) > 4096:
        with open("lyrics.txt", "w+", encoding="utf8") as out_file:
            out_file.write(results)
        await message.reply_document(
            document="lyrics.txt",
            disable_notification=True
        )
        os.remove("lyrics.txt")
    else:
        await message.reply_text(f"<b><blockquote>{results}</blockquote></b>")

module = modules_help.add_module("lyrics", __file__)
module.add_command("lyrics", "Get lyrics matched artist and song.")
