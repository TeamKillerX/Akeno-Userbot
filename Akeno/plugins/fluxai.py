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

import io
import time

import requests
from akenoai import AkenoXToJs
from PIL import Image
from pyrogram import *
from pyrogram import Client, filters
from pyrogram.types import *

from Akeno.utils.handler import *
from Akeno.utils.logger import LOGS
from Akeno.utils.prefixprem import command
from Akeno.utils.scripts import progress
from config import *

js = AkenoXToJs().connect()

@Akeno(
    command(["fluxai"])
    & filters.me
    & ~filters.forwarded
)
async def imgfluxai_(client: Client, message: Message):
    question = message.text.split(" ", 1)[1] if len(message.command) > 1 else None
    if not question:
        return await message.reply_text("Please provide a question for Flux.")
    try:
        response = await js.image.create(
            "black-forest-labs/flux-1-schnell",
            api_key=AKENOX_API_KEY,
            image_read=True,
            query=question
        )
        pro = await message.reply_text("Generating image, please wait...")
        file_path = "randydev.jpg"
        with open(file_path, "wb") as f:
            f.write(response)
        ok = await pro.edit_text("Uploading image...")
        await message.reply_photo(
            file_path,
            progress=progress,
            progress_args=(ok, time.time(), "Uploading image...")
        )
        await ok.delete()
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        LOGS.error(str(e))
        await message.edit_text(str(e))

module = modules_help.add_module("fluxai", __file__)
module.add_command("fluxai", "to question flux image generator.")
