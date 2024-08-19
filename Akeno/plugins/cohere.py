import asyncio
import os
from json import tool

import cohere
from pyrogram import Client, enums, filters
from pyrogram.types import Message

from Akeno.utils.database import db
from Akeno.utils.handler import *
from config import *


@Akeno(filters.command("cohere", CMD_HANDLER) & filters.me)
async def coheres_(c: Client, message: Message):
    status_key = await db.get_env(ENV_TEMPLATE.cohere_api_key)
    if not status_key:
        return await message.reply_text("Required `.setvar COHERE_API_KEY xxxx`")
    co = cohere.Client(api_key=status_key)
    try:
        user_id = message.from_user.id
        chat_history = await db._get_cohere_chat_from_db(user_id)
        if len(message.command) > 1:
            prompt = message.text.split(maxsplit=1)[1]
        elif message.reply_to_message:
            prompt = message.reply_to_message.text
        else:
            await message.reply_text(
                "<b>Usage: </b><code>.cohere [prompt/reply to message]</code>"
            )
            return
        chat_history.append({"role": "USER", "message": prompt})
        response = co.chat(
            chat_history=chat_history,
            model="command-r-plus",
            message=prompt
        )
        output = response.text
        if len(output) > 4096:
            with open("chat.txt", "w+", encoding="utf8") as out_file:
                out_file.write(output)
            await message.reply_document(
                document="chat.txt",
                disable_notification=True
            )
            os.remove("chat.txt")
        else:
            await message.reply_text(output, disable_web_page_preview=True)
        chat_history.append({"role": "CHATBOT", "message": output})
        await db._update_cohere_chat_in_db(user_id, chat_history)
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

module = modules_help.add_module("cohere", __file__)
module.add_command("cohere", "to question from cohere ai.")
