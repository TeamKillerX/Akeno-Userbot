#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2020-2024 (c) Randy W @xtdevs, @xtsea
#
# from : https://github.com/TeamKillerX
# Channel : @RendyProjects
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from pyrogram import *
from pyrogram import Client, filters
from pyrogram.types import *
from RyuzakiLib import FullStackDev, GeminiLatest, RendyDevChat

from Akeno.utils.chat import chat_message
from Akeno.utils.handler import Akeno
from Akeno.utils.logger import LOGS
from config import CMD_HANDLER, GOOGLE_API_KEY


@Akeno(
    ~filters.scheduled
    & filters.command(["askf"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def googlegm(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("Please reply to message photo")
        return
    user_message = message.reply_to_message
    caption = user_message.caption or "What's this?"
    if not user_message.photo:
        await message.reply_text("Not allowed text")
        return
    try:
        replys = await message.reply_text("Prossing.....")
        if user_message.photo:
            file_path = await user_message.download()
        if not GOOGLE_API_KEY:
            return await replys.edit_text("Required .env `GOOGLE_API_KEY`")
        x = GeminiLatest(api_keys=GOOGLE_API_KEY)
        response = x.get_response_image(caption, file_path)
        await replys.edit_text(response)
        return
    except Exception as e:
        LOGS.error(str(e))
        await replys.edit_text(str(e))
        return

@Akeno(
    ~filters.scheduled
    & filters.command(["askm"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def chatgpt_images(client: Client, message: Message):
    question = message.text.split(" ", 1)[1] if len(message.command) > 1 else None
    if not question:
        return await message.reply_text("Give ask from CHATGPT images")
    try:
        replys = await message.reply_text("Prossing.....")
        response = await RendyDevChat.image_generator(question)
        x = response["randydev"].get("url")
        for i, url in enumerate(x, start=1):
            await FullStackDev.fast(url, filename=f"original_{i}.png")
        await message.reply_media_group(
            [
                InputMediaPhoto(f"original_1.png"),
                InputMediaPhoto(f"original_2.png"),
                InputMediaPhoto(f"original_3.png"),
                InputMediaPhoto(f"original_4.png")
            ],
        )
        await replys.delete()
    except Exception as e:
        LOGS.error(str(e))
        return await message.reply_text(str(e))

@Akeno(
    ~filters.scheduled
    & filters.command(["ask"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def chatgpt(client: Client, message: Message):
    question = message.text.split(" ", 1)[1] if len(message.command) > 1 else None
    if not question:
        return await message.reply_text("Give ask from CHATGPT")
    try:
        messager = await chat_message(question)
        if len(messager) > 4096:
            with open("chat.txt", "w+", encoding="utf8") as out_file:
                out_file.write(messager)
            await message.reply_document(
                document="chat.txt",
                disable_notification=True
            )
            os.remove("chat.txt")
        else:
            await message.reply_text(messager)
    except Exception as e:
        LOGS.error(str(e))
        return await message.reply_text(str(e))
