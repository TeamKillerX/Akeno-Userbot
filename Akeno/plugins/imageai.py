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
import io
from PIL import Image
from pyrogram import Client, filters
from pyrogram.types import *
from pyrogram import *

from Akeno.utils.logger import LOGS
from Akeno.utils.handler import Akeno
from config import HUGGING_TOKEN, CMD_HANDLER

async def schellwithflux(args):
    API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"
    headers = {"Authorization": f"Bearer {HUGGING_TOKEN}"}
    payload = {"inputs": args}
    response = requests.post(API_URL, headers=headers, json=payload)
    if not response.status_code != 200:
        LOGS.error(f"Error status {response.status_code}")
        return "Error Response"
    return response.content

@Akeno(
    ~filters.scheduled
    & filters.command(["fluxai"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def imgfluxai_(client: Client, message: Message):
    question = message.text.split(" ", 1)[1] if len(message.command) > 1 else None
    if not question:
        return await message.reply_text("Give ask from Flux")
    try:
        if not HUGGING_TOKEN:
            return await message.reply_text("Required `HUGGING_TOKEN`")
        image_bytes = await schellwithflux(question)
        pro = await message.reply_text("Image Generator wait...")
        with Image.open(io.BytesIO(image_bytes)) as img:
            img.save("testing.jpg", format="JPEG")
        ok = await pro.edit_text("Uploading......")
        await message.reply_photo("testing.jpg")
        await ok.delete()
    except Exception as e:
        LOGS.error(str(e))
        await pro.edit_text(str(e))
