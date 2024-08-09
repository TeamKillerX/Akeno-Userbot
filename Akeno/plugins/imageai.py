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
    if response.status_code != 200:
        LOGS.error(f"Error status {response.status_code}")
        return None
    return response.content

@Akeno(
    filters.command(["fluxai"], CMD_HANDLER)
    & filters.me
    & ~filters.forwarded
)
async def imgfluxai_(client: Client, message: Message):
    question = message.text.split(" ", 1)[1] if len(message.command) > 1 else None
    if not question:
        return await message.reply_text("Please provide a question for Flux.")
    try:
        if not HUGGING_TOKEN:
            return await message.reply_text("`HUGGING_TOKEN` is required to use this feature.")
        image_bytes = await schellwithflux(question)
        if image_bytes is None:
            return await message.reply_text("Failed to generate an image.")
        pro = await message.reply_text("Generating image, please wait...")
        with Image.open(io.BytesIO(image_bytes)) as img:
            img.save("testing.jpg", format="JPEG")
        ok = await pro.edit_text("Uploading image...")
        await message.reply_photo("testing.jpg")
        await ok.delete()
    except Exception as e:
        LOGS.error(str(e))
        await pro.edit_text(f"An error occurred: {str(e)}")
