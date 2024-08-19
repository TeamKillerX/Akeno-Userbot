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

import google.generativeai as genai
import requests
from pyrogram import *
from pyrogram import Client, filters
from pyrogram.types import *
from RyuzakiLib import FaceAI, FullStackDev, GeminiLatest, RendyDevChat

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
    & filters.command(["addchatbot"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def addchatbot_user(client: Client, message: Message):
    await db.add_chatbot(message.chat.id, client.me.id)
    await message.reply_text("Added chatbot user")

@Akeno(
    ~filters.scheduled
    & filters.command(["rmcdb"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def clearuserdb(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("why reply?")
    reply_message = message.reply_to_message
    if not reply_message.from_user:
        return await message.reply_text("Why reply to message user")
    user_id = reply_message.from_user.id
    response = await db._clear_chatbot_database(user_id)
    await message.reply_text(response)

@Akeno(
    ~filters.scheduled
    & filters.command(["rmchatbot"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def rmchatbot_user(client: Client, message: Message):
    await db.remove_chatbot(message.chat.id)
    await message.reply_text("removed chatbot user")

@Akeno(
    filters.incoming
    & filters.text
    & filters.reply
    & ~filters.bot
    & ~filters.via_bot
    & ~filters.forwarded,
    group=2,
)
async def chatbot_talk(client: Client, message: Message):
    if not message.reply_to_message:
        return
    if not message.reply_to_message.from_user:
        return
    if message.reply_to_message.from_user.id != client.me.id:
        return
    chat_user = await db.get_chatbot(message.chat.id)
    if chat_user:
        query = message.text.strip()
        try:
            system_prompt = await db.get_env(ENV_TEMPLATE.system_prompt)
            if not system_prompt:
                return await message.reply_text("Required `.setvar SYSTEM_PROMPT question`")
            genai.configure(api_key=GOOGLE_API_KEY)
            model_flash = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction=system_prompt,
                safety_settings={
                    genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_NONE,
                    genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                    genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                    genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                }
            )
            backup_chat = await db._get_chatbot_chat_from_db(message.from_user.id)
            backup_chat.append({"role": "user", "parts": [{"text": query}]})
            chat_session = model_flash.start_chat(history=backup_chat)
            response_data = chat_session.send_message(query)
            output = response_data.text
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
            backup_chat.append({"role": "model", "parts": [{"text": output}]})
            await db._update_chatbot_chat_in_db(message.from_user.id, backup_chat)
        except Exception as e:
            LOGS.error(str(e))
            return await message.reply_text(str(e))

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
    if len(message.command) > 1:
        prompt = message.text.split(maxsplit=1)[1]
    elif message.reply_to_message:
        prompt = message.reply_to_message.text
    else:
        return await message.reply_text("Give ask from CHATGPT images")
    try:
        replys = await message.reply_text("Prossing.....")
        response = await RendyDevChat.image_generator(prompt)
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
    if len(message.command) > 1:
        prompt = message.text.split(maxsplit=1)[1]
    elif message.reply_to_message:
        prompt = message.reply_to_message.text
    else:
        return await message.reply_text("Give ask from FaceAI")
    try:
        clients_name, token = await db.get_env(ENV_TEMPLATE.face_clients_name), await db.get_env(ENV_TEMPLATE.face_token_key)
        if not clients_name and not token:
            return await message.reply_text("Required .setvar FACE_CLIENTS_NAME xxxx and .setvar FACE_TOKEN xxxx")
        send = FaceAI(clients_name=clients_name, token=token)
        response = await send.chat(prompt, no_db=True)
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
    if len(message.command) > 1:
        prompt = message.text.split(maxsplit=1)[1]
    elif message.reply_to_message:
        prompt = message.reply_to_message.text
    else:
        return await message.reply_text("Give ask from mistralai")
    try:
        messager = await mistraai(prompt)
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
    if len(message.command) > 1:
        prompt = message.text.split(maxsplit=1)[1]
    elif message.reply_to_message:
        prompt = message.reply_to_message.text
    else:
        return await message.reply_text("Give ask from CHATGPT-3")
    try:
        messager = await chatgptold(prompt)
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
    if len(message.command) > 1:
        prompt = message.text.split(maxsplit=1)[1]
    elif message.reply_to_message:
        prompt = message.reply_to_message.text
    else:
        return await message.reply_text("Give ask from CHATGPT-4O")
    try:
        messager = await chat_message(prompt)
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
module.add_command("addchatbot", "to chatbot users")
module.add_command("rmchatbot", "to remove chatbot users")
module.add_command("rmcdb", "to chat history clearly from db")
