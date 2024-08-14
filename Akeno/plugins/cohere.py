import asyncio
import os
from json import tool
from Akeno.utils.handler import *
from Akeno.utils.database import db

from pyrogram import Client, filters, enums
from pyrogram.types import Message
from config import cohere_key, CMD_HANDLER
import cohere

co = cohere.Client(api_key=cohere_key)

@Akeno(filters.command("cohere", CMD_HANDLER) & filters.me)
async def coheres_(c: Client, message: Message):
    try:
        user_id = message.from_user.id
        chat_history = await db._get_cohere_chat_from_db(user_id)
        if len(message.command) > 1:
            prompt = message.text.split(maxsplit=1)[1]
        elif message.reply_to_message:
            prompt = message.reply_to_message.text
        else:
            await message.edit_text(
                f"<b>Usage: </b><code>.cohere [prompt/reply to message]</code>"
            )
            return
        chat_history.append({"role": "USER", "message": prompt})
        pro = await message.edit_text("<code>Processing...</code>")
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
            await pro.delete()
            os.remove("chat.txt")
        else:
            await message.edit_text(output, disable_web_page_preview=True)
        chat_history.append({"role": "CHATBOT", "message": output})
        await db._update_cohere_chat_in_db(user_id, chat_history)
    except Exception as e:
        await message.edit_text(f"An error occurred: {e}")
