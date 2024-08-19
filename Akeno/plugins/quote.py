import asyncio
import base64
import datetime
import os
import random
import time
from typing import Dict, List, Tuple

import requests
from pyrogram import *
from pyrogram import Client, filters
from pyrogram.types import *

from Akeno.utils.database import db
from Akeno.utils.handler import *
from Akeno.utils.logger import LOGS
from config import *


def generate_quote(messages: List[Dict]) -> Tuple[bool, str]:
    json = {
        "type": "quote",
        "format": "webp",
        "backgroundColor": "#260746/#6100c2",
        "width": 512,
        "height": 768,
        "scale": 2,
        "messages": messages,
    }
    try:
        response = requests.post("https://bot.lyo.su/quote/generate", json=json).json()
        image = base64.b64decode(str(response["result"]["image"]).encode("utf-8"))
        file_name = f"Quote_{int(time.time())}.webp"
        with open(file_name, "wb") as f:
            f.write(image)
        return True, file_name
    except Exception as e:
        return False, str(e)

def get_entities(message: Message) -> List[Dict]:
    entities = []
    if message.entities:
        for entity in message.entities:
            entities.append(
                {
                    "type": entity.type.name.lower(),
                    "offset": entity.offset,
                    "length": entity.length,
                }
            )
    return entities

@Akeno(
    ~filters.scheduled
    & filters.command(["q"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def quotely(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a message to quote it.")
    if message.reply_to_message.media:
        if message.reply_to_message.caption:
            message.reply_to_message.text = message.reply_to_message.caption
        else:
            return await message.reply_text("Reply to a text message to quote it.")
    cmd = None
    if len(message.command) > 1:
        cmd = message.command[1].lower()
    pro = await message.reply_text("__Generating quote...__")
    msg_data = []
    if cmd and cmd == "r":
        await pro.edit_text("__Generating quote with reply...__")
        reply_msg_id = message.reply_to_message.reply_to_message_id
        if reply_msg_id:
            reply_msg = await client.get_messages(message.chat.id, reply_msg_id)
            if reply_msg and reply_msg.text:
                replied_name = reply_msg.from_user.first_name
                if reply_msg.from_user.last_name:
                    replied_name += f" {reply_msg.from_user.last_name}"
                reply_message = {
                    "chatId": reply_msg.from_user.id,
                    "entities": get_entities(reply_msg),
                    "name": replied_name,
                    "text": reply_msg.text,
                }
            else:
                reply_message = {}
        else:
            reply_message = {}
    else:
        reply_message = {}
    name = message.reply_to_message.from_user.first_name
    if message.reply_to_message.from_user.last_name:
        name += f" {message.reply_to_message.from_user.last_name}"
    emoji_status = None
    if message.reply_to_message.from_user.emoji_status:
        emoji_status = str(message.reply_to_message.from_user.emoji_status.custom_emoji_id)
    msg_data.append(
        {
            "entities": get_entities(message.reply_to_message),
            "avatar": True,
            "from": {
                "id": message.reply_to_message.from_user.id,
                "name": name,
                "emoji_status": emoji_status,
            },
            "text": message.reply_to_message.text,
            "replyMessage": reply_message,
        }
    )
    status, path = generate_quote(msg_data)
    if not status:
        return await message.reply_text(f"`{path}`")
    await message.reply_sticker(path)
    await pro.delete()
    os.remove(path)

module = modules_help.add_module("quote", __file__)
module.add_command("q", "Generate a quote sticker of the replied message.")
module.add_command("q r", "Generate a quote sticker of the replied message with it's reply message.")
