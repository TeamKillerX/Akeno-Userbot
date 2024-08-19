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

import requests
from pyrogram import *
from pyrogram import Client, filters
from pyrogram.types import *
from RyuzakiLib import FullStackDev, GeminiLatest, RendyDevChat
from RyuzakiLib import FaceAI
from Akeno.utils.chat import chat_message
from Akeno.utils.database import db
from Akeno.utils.handler import *
from Akeno.utils.logger import LOGS
from config import *


async def mistraai(messagestr):
    url = "https://randydev-ryuzaki-api.hf.space/api/v1/akeno/mistralai"
    payload = {"args": messagestr}
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        return None
    return response.json()

async def chatgptold(messagestr):
    url = "https://randydev-ryuzaki-api.hf.space/ryuzaki/chatgpt-old"
    payload = {"query": messagestr}
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        return None
    return response.json()

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
    & filters.command(["askface"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def faceai_(client: Client, message: Message):
    question = message.text.split(" ", 1)[1] if len(message.command) > 1 else None
    if not question:
        return await message.reply_text("Give ask from mistraai")
    try:
        clients_name, token = await db.get_env(ENV_TEMPLATE.face_clients_name), await db.get_env(ENV_TEMPLATE.face_token_key)
        if not clients_name and not token:
            return await message.reply_text("Required .setvar FACE_CLIENTS_NAME xxxx and .setvar FACE_TOKEN xxxx")
        send = FaceAI(clients_name=clients_name, token=token)
        response = await send.chat(question, no_db=True)
        if len(response) > 4096:
            with open("chat.txt", "w+", encoding="utf8") as out_file:
                out_file.write(response)
            await message.reply_document(
                document="chat.txt",
                disable_notification=True
            )
            os.remove("chat.txt")
        else:
            await message.reply_text(response)
    except Exception as e:
        LOGS.error(str(e))
        return await message.reply_text(str(e))

@Akeno(
    ~filters.scheduled
    & filters.command(["mistralai"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def mistralai_(client: Client, message: Message):
    question = message.text.split(" ", 1)[1] if len(message.command) > 1 else None
    if not question:
        return await message.reply_text("Give ask from mistraai")
    try:
        messager = await mistraai(question)
        if messager is None:
            return await message.reply_text("No response")
        output = messager["randydev"].get("message")
        if len(output) > 4096:
            with open("chat.txt", "w+", encoding="utf8") as out_file:
                out_file.write(output)
            await message.reply_document(
                document="chat.txt",
                disable_notification=True
            )
            os.remove("chat.txt")
        else:
            await message.reply_text(output)
    except Exception as e:
        LOGS.error(str(e))
        return await message.reply_text(str(e))

@Akeno(
    ~filters.scheduled
    & filters.command(["askold"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def chatgpt_old_(client: Client, message: Message):
    question = message.text.split(" ", 1)[1] if len(message.command) > 1 else None
    if not question:
        return await message.reply_text("Give ask from chatgpt-3")
    try:
        messager = await chatgptold(question)
        if messager is None:
            return await message.reply_text("No response")
        output = messager["randydev"].get("message")
        if len(output) > 4096:
            with open("chat.txt", "w+", encoding="utf8") as out_file:
                out_file.write(output)
            await message.reply_document(
                document="chat.txt",
                disable_notification=True
            )
            os.remove("chat.txt")
        else:
            await message.reply_text(output)
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

module = modules_help.add_module("chatgpt", __file__)
module.add_command("askf", "to read in the picture")
module.add_command("askm", "to give random image questions")
module.add_command("ask", "to question from chatgpt-4o")
module.add_command("askold", "to question from chatgpt-3")
module.add_command("askface", "to question from faceai")
module.add_command("mistralai", "to question from mistralai")
