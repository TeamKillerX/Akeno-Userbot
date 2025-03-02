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

import asyncio
import json
import time

import requests
from akenoai import AkenoXToJs
from pyrogram import *
from pyrogram import Client, filters
from pyrogram.types import *

from Akeno.utils.chat import *
from Akeno.utils.database import db
from Akeno.utils.handler import *
from Akeno.utils.logger import LOGS
from Akeno.utils.prefixprem import command
from Akeno.utils.tools import *
from config import *

js = AkenoXToJs().connect()

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
        response = await js.chat.create(
            "cohere/command-plus",
            api_key=AKENOX_API_KEY_PREMIUM,
            query=prompt,
            is_obj=True,
        )
        if not hasattr(response, "results") or not isinstance(response.results, str):
            await message.reply_text("Unexpected response format from chat API.")
            return
        if len(response.results) > 4096:
            with open("chat.txt", "w+", encoding="utf8") as out_file:
                out_file.write(response.results)
            await message.reply_document(
                document="chat.txt",
                disable_notification=True
            )
            os.remove("chat.txt")
        else:
            await message.reply_text(response.results, reply_to_message_id=ReplyCheck(message))
    except Exception as e:
        LOGS.error(str(e))
        return await message.reply_text(str(e))

module = modules_help.add_module("chatgpt", __file__)
module.add_command("ask", "to question from chatgpt")
