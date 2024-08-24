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

import os
import time

import requests
import wget
from pyrogram import *
from pyrogram import Client, filters
from pyrogram.types import *
from RyuzakiLib import PornoHub

from Akeno.utils.handler import *
from Akeno.utils.logger import LOGS
from Akeno.utils.scripts import progress
from config import *


async def pornosearch(query):
    url = "https://randydev-ryuzaki-api.hf.space/akeno/xnxxsearch"
    headers = {"Content-Type": "application/json"}
    data = {"query": query}
    response = requests.get(url, params=data)
    response_json = response.json()["randydev"]["results"]
    return response_json

@Akeno(
    filters.command(["hubsearch"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def porno_search(client: Client, message: Message):
    question = message.text.split(" ", 1)[1] if len(message.command) > 1 else None
    if not question:
        return await message.reply_text("Search for pornohub.")
    try:
        response = await pornosearch(question)
        data_dict = {}
        for data in response:
            data_dict[data["title"]] = data["link"]
        res = ""
        for x in data_dict.items():
            res += f"• Title: [{x[0]}]({x[1]})\n\n"
        if len(res) > 4096:
            with open("log.txt", "w+", encoding="utf8") as out_file:
                out_file.write(res)
            await message.reply_document(
                document="log.txt",
                disable_notification=True
            )
            os.remove("log.txt")
        else:
            await message.reply_text(res, disable_web_page_preview=True)
    except Exception as e:
        LOGS.error(str(e))
        await message.edit_text(str(e))

@Akeno(
    filters.command(["hubdl"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def porno_download(client: Client, message: Message):
    api = PornoHub()
    link = message.text.split(" ", 1)[1] if len(message.command) > 1 else None
    if not link:
        return await message.reply_text("Please link for pornohub.")
    if not link.startswith("https://www.xnxx.com/"):
        return await message.reply_text("invalid link.")
    try:
        pro = await message.reply_text("Processing.....")
        file_path, thumb, _ = await api.x_download(url=link, is_stream=True)
        upload_text = f"**⬆️ 𝖴𝗉𝗅𝗈𝖺𝖽𝗂𝗇𝗀 video ...**"
        await pro.edit_text(upload_text)
        await message.reply_video(
            file_path,
            caption=f"• Powered by {client.me.mention}",
            thumb=thumb,
            has_spoiler=True,
            progress=progress,
            progress_args=(
                pro,
                time.time(),
                upload_text
            )
        )
        await pro.delete()
        os.remove(thumb)
        os.remove(file_path)
    except Exception as e:
        LOGS.error(str(e))
        await pro.edit_text(str(e))
